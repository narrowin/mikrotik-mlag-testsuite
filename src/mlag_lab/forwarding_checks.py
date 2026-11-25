"""Where frames went: delivery outside the conversation, reflected copies, bridge host table and sync warnings.

Each check takes evidence the evaluators already parsed and returns plain measurements for result["forwarding"].
grade turns those measurements into fail checks tagged with their phase.
"""

from datetime import datetime
import re

from .evidence import load_jsonl
from .legacy import NS
from .measure import seconds, within
from .root_state import router_members

CLIENT1, CLIENT2, MOBILE = "02:00:00:11:00:11", "02:00:00:11:00:12", "02:00:00:11:00:50"
PEER_PORT = "ether2"

# Capture points that face a host which is neither the source nor the destination of the stream.
SMALL_OUTSIDE = {
    101: ("c2-bond0",), 201: ("c2-bond0",),
    102: ("c1-eth1", "c1-eth2"), 202: ("c1-eth1", "c1-eth2"),
    302: ("p1-tap4", "p2-tap4", "mobile-bond0"),
}
DIRECT_OUTSIDE = dict.fromkeys((101, 201), ("mobile-eth1", "mobile-eth2", "p1-tap4", "p2-tap4"))
MEDIUM_OUTSIDE = "not applicable: the Medium lab has no host outside the conversation"
TWO_PAIR_OUTSIDE = "not applicable: the two-pair lab has no host outside the conversation"

# Expected on-interface per MLAG peer and traffic host MAC: the MLAG bond and its local bond member.
SMALL_HOSTS = dict.fromkeys(("p1", "p2"), {CLIENT1: ("client1", "ether3"), CLIENT2: ("client2", "ether4")})
MEDIUM_HOSTS = dict.fromkeys(("p1", "p2"), {CLIENT1: ("access-uplink", "ether3"), CLIENT2: ("client2", "ether4")})
TWO_PAIR_HOSTS = {
    **dict.fromkeys(("p1", "p2"), {CLIENT1: ("interpair", "ether3"), CLIENT2: ("client2", "ether4")}),
    **dict.fromkeys(("q1", "q2"), {CLIENT1: ("client1", "ether4"), CLIENT2: ("interpair", "ether3")}),
}
HOST_ENTRY = re.compile(r"mac-address=([0-9A-Fa-f:]+)\s+vid=\d+\s+interface=\S+\s+bridge=\S+\s+on-interface=(\S+)")
SYNC_WARNINGS = ("failed to sync", "attempting to resync", "heartbeat timeout")
# MLAG bonds whose LACP partner is a RouterOS bridge: the partner's member ports that face one MLAG pair.
MEDIUM_PARTNER_BONDS = {"access-uplink, seen by the access switch": (("witness", "ether2"), ("witness", "ether3"))}
TWO_PAIR_PARTNER_BONDS = {"pair A inter-pair bond, seen by pair B": (("q1", "ether3"), ("q2", "ether3")),
                          "pair B inter-pair bond, seen by pair A": (("p1", "ether3"), ("p2", "ether3"))}
LINUX_PARTNER = re.compile(r"Slave Interface: (\S+)[\s\S]*?details partner lacp pdu:\s*\n\s*system priority: (\d+)"
                           r"\s*\n\s*system mac address: (\S+)")
# Check E: the access switch's bridge MAC and the captures on the Medium traffic host's MLAG bond (client2 on
# ether4 of each MLAG peer, captured at both CHR TAPs and at the host's members and bond).
ACCESS_BRIDGE_MAC = "02:00:00:21:00:13"
HOST_BOND_CAPTURES = ("c2-eth1", "c2-eth2", "c2-bond0", "p1-tap3", "p2-tap3")
ROUTEROS_PARTNER = re.compile(r"port=(ether\d+) [^\n]*?partner-sys-id=(\S+)\s+partner-sys-priority=(\d+)")


def phase_of(stamp, phases):
    return next((label for label, low, high in phases if within(stamp, low, high)), None)


def outside_delivery(icmp, points, phases, start):
    """Check A: frames of each stream seen at a point facing an unrelated host, per point and phase."""
    if isinstance(points, str):
        return {"status": points}
    found = {}
    for ident, captures in points.items():
        for point in captures:
            for (i, _, _), stamps in icmp.get(point, {}).items():
                if i != ident:
                    continue
                for stamp in stamps:
                    if phase := phase_of(stamp, phases):
                        found.setdefault((ident, point, phase), []).append(stamp)
    findings = [{"stream": ident, "point": point, "phase": phase, "frames": len(stamps),
                 "first_s": seconds(min(stamps) - start), "span_s": seconds(max(stamps) - min(stamps))}
                for (ident, point, phase), stamps in sorted(found.items())]
    return {"points": {str(ident): list(captures) for ident, captures in points.items()}, "findings": findings}


def members(icmp, point):
    """Both bond member captures of a traffic host, where the run saved them."""
    if not point.endswith("-bond0"):
        return ()
    legs = tuple(point.replace("-bond0", f"-eth{n}") for n in (1, 2))
    if point == "mobile-bond0" and not all(leg in icmp for leg in legs):
        # Small link-fault runs saved no mobile-eth captures. The active-backup bond drops frames on its backup
        # leg before bond0 sees them, so count the wire captures facing both legs instead.
        legs = ("p1-tap4", "p2-tap4")
    return legs if all(leg in icmp for leg in legs) else ()


def reflected_copies(icmp, definitions, phases, start):
    """Check B: a request seen again at its source, a reply seen again at its destination."""
    found = {}
    for ident, (source, dest, _, _) in definitions.items():
        for kind, point, label in ((8, source, "request at source"), (0, dest, "reply at destination")):
            legs = members(icmp, point)
            for (i, k, seq), stamps in icmp.get(point, {}).items():
                if i != ident or k != kind:
                    continue
                # While a bond has no active member, its bond0 capture shows the same request every 100 ms
                # but no bond member sends it, so only the member captures show what crossed the wire.
                seen = [t for leg in legs for t in icmp[leg].get((i, k, seq), [])] if legs else stamps
                phase = phase_of(min(seen), phases) if seen else None
                if len(seen) > 1 and phase:
                    entry = found.setdefault((ident, label, phase), {"copies": 0, "seqs": []})
                    entry["copies"] += 1
                    entry["seqs"].append(seq)
    findings = [{"stream": ident, "kind": label, "phase": phase, "sequences": entry["copies"],
                 "first_seqs": sorted(entry["seqs"])[:10]}
                for (ident, label, phase), entry in sorted(found.items())]
    counted = {str(ident): [p for p in (source, dest) if members(icmp, p)]
               for ident, (source, dest, _, _) in definitions.items()}
    return {"member_points": {ident: points for ident, points in counted.items() if points}, "findings": findings}


def host_table(samples, expected, window, start):
    """Check C: on-interface of each traffic host MAC in the last complete sample of each MLAG peer."""
    if isinstance(window, str):
        return {"status": window}
    low, high = window
    tables, chosen = {}, {}
    sampled = set()
    for peer, rows in samples.items():
        for sample in rows:
            raw = sample.get("raw")
            if not isinstance(raw, str) or "mlag-state:" not in raw:
                continue
            entries = {mac.lower(): port.replace("witness-bond", "access-uplink")
                       for mac, port in HOST_ENTRY.findall(raw)}
            sampled.update(entries)
            if low <= sample["started_ns"] and sample["done_ns"] <= high:
                tables[peer], chosen[peer] = entries, sample
    peers, wrong = {}, []
    for peer, hosts in expected.items():
        if peer not in chosen:
            peers[peer] = {"status": "not available: no complete state sample in the recovery window"}
            continue
        raw, entries = chosen[peer]["raw"], tables[peer]
        lacp = router_members(raw)
        observed = {}
        for mac, (bond, member) in hosts.items():
            if mac not in sampled:
                continue  # Older runs did not sample this MAC.
            port = entries.get(mac)
            up = lacp.get(member, {}).get("actor", "")[3:6] == "SCD"
            observed[mac] = {"on_interface": port, "expected": bond, "bond_member": member, "member_up": up}
            if port != bond and not (port == PEER_PORT and not up):
                wrong.append(f"{peer} {mac} on {port or 'no entry'}, expected {bond}"
                             + (f" while bond member {member} is up" if port == PEER_PORT else ""))
        if MOBILE in sampled:
            observed[MOBILE] = {"on_interface": entries.get(MOBILE)}
        peers[peer] = {"sample_s": seconds(chosen[peer]["started_ns"] - start), "hosts": observed}
    mobile = {peer: info["hosts"][MOBILE]["on_interface"] for peer, info in peers.items()
              if MOBILE in info.get("hosts", {})}
    if mobile:
        # The MAC-move host sits on ether5 of the peer it is active on and behind the peer port on the other.
        active = [peer for peer, port in mobile.items() if port == "ether5"]
        if len(active) != 1 or any(port != PEER_PORT for peer, port in mobile.items() if peer not in active):
            wrong.append(f"MAC-move host {MOBILE} on {mobile}, expected ether5 on one MLAG peer "
                         f"and {PEER_PORT} on the other")
    return {"window_s": [seconds(low - start), seconds(high - start)], "peers": peers, "wrong": wrong}


def sync_warnings(logs, nodes, phases, start):
    """Check D: MLAG sync and heartbeat warnings per CHR and phase."""
    names = {address: node for node, address in nodes.items()}
    counts = {node: {} for node in nodes}
    lines = []
    for log in logs:
        text = log["raw"]
        if not any(pattern in text.lower() for pattern in SYNC_WARNINGS):
            continue
        stamp = int(datetime.fromisoformat(log["received_at"]).timestamp() * NS)
        if not (phase := phase_of(stamp, phases)):
            continue
        node = names.get(log["source_ip"], log["source_ip"])
        counts.setdefault(node, {})
        counts[node][phase] = counts[node].get(phase, 0) + 1
        if len(lines) < 10:
            lines.append({"node": node, "phase": phase, "time_s": seconds(stamp - start), "line": text})
    return {"counts": counts, "first_lines": lines}


def available(measure, *args):
    try:
        return measure(*args)
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        return {"status": f"not available: {type(error).__name__}: {error}"}


def forwarding(path, icmp, definitions, start, down, up, end, *, outside, hosts, nodes, recovery=None, stopped=None):
    """All four measurements for one run. recovery is the start of the recovery window, None without a fault.

    stopped is the collectors_stopped time of a run that executed its fault but stopped before the recovery window.
    """
    if stopped is not None:
        # Keep evidence from the fault period: withdrawal runs until the collectors stopped.
        up, end = (up if down < up < stopped else stopped), stopped
        window = "not available: the run stopped before the recovery window"
    elif recovery is not None and recovery < end:
        window = (recovery, end)
    else:
        window = "not available: no fault was executed, so there is no recovery window"
    phases = (("baseline", start, down), ("withdrawal", down, up), ("restoration", up, end))

    def state():
        return host_table({peer: load_jsonl(path / f"state-{peer}.jsonl") for peer in hosts}, hosts, window, start)

    return {
        "phases_s": {label: [seconds(low - start), seconds(high - start)] for label, low, high in phases if high > low},
        "outside_delivery": available(outside_delivery, icmp, outside, phases, start),
        "reflected_copies": available(reflected_copies, icmp, definitions, phases, start),
        "host_table": available(state),
        "sync_warnings": available(lambda: sync_warnings(load_jsonl(path / "syslog.jsonl"), nodes, phases, start)),
    }


def grade(measured, check, expected_flooding=None, *, outside_limit_s):
    """Fail checks from the four measurements. A measurement that is not applicable or not available adds none.

    expected_flooding maps a phase to the streams a case floods there on purpose; those are recorded, not failed."""
    expected_flooding = expected_flooding or {}
    if "status" in measured:
        return
    phases = measured["phases_s"]
    outside = measured["outside_delivery"]
    if "status" not in outside:
        for phase in phases:
            found = [f for f in outside["findings"] if f["phase"] == phase]
            if phase == "baseline":
                # Known unicast must not flood in steady state.
                frames = sum(f["frames"] for f in found)
                check("fail", not frames, f"Baseline: {frames} unicast frames at a host outside the conversation, "
                      "limit 0" + "".join(f"; {f['stream']} at {f['point']}: {f['frames']}" for f in found), phase)
                continue
            expected = [f for f in found if f["stream"] in expected_flooding.get(phase, ())]
            if expected:
                check("fail", True, f"{phase.capitalize()}: expected flooding recorded, not graded"
                      + "".join(f"; {f['stream']} at {f['point']}: {f['frames']} frames over {f['span_s']:.3f} s"
                                for f in expected), phase)
                found = [f for f in found if f not in expected]
            # Flooding right after a table flush is normal; the 100 ms streams re-teach the MAC within one interval.
            longest = max((f["span_s"] for f in found), default=0)
            check("fail", longest <= outside_limit_s,
                  f"{phase.capitalize()}: unicast at a host outside the conversation for {longest:.3f} s, "
                  f"limit {outside_limit_s:g} s" + "".join(f"; {f['stream']} at {f['point']}: {f['frames']} frames "
                                                         f"over {f['span_s']:.3f} s"
                                                         for f in found if f["span_s"] > outside_limit_s), phase)
    reflected = measured["reflected_copies"]
    if "status" not in reflected:
        for phase in phases:
            found = [f for f in reflected["findings"] if f["phase"] == phase]
            check("fail", not found, f"{phase.capitalize()}: {sum(f['sequences'] for f in found)} reflected unicast "
                  "sequences, limit 0" + "".join(f"; {f['stream']} {f['kind']}: sequences {f['first_seqs']}"
                                                 for f in found), phase)
    table = measured["host_table"]
    if "status" not in table and any(info.get("hosts") for info in table["peers"].values()):
        if not table["wrong"]:
            check("fail", True, "Bridge host table after recovery: every traffic host MAC on its expected port",
                  "restoration")
        for wrong in table["wrong"]:
            check("fail", False, f"Bridge host table after recovery: {wrong}", "restoration")
    warnings = measured["sync_warnings"]
    if "status" not in warnings and "baseline" in phases:
        # A peer loss legitimately logs these, so only the baseline is graded.
        counts = {node: phases_of["baseline"] for node, phases_of in warnings["counts"].items()
                  if phases_of.get("baseline")}
        check("fail", not counts, f"Baseline: {sum(counts.values())} MLAG sync or heartbeat warnings in syslog, "
              f"limit 0" + "".join(f"; {node}: {count}" for node, count in sorted(counts.items())), "baseline")


def lacp_system_ids(marks, partner_bonds=None):
    """The LACP system ID each MLAG bond presents on each of its members, read on the partner side at the baseline.

    Linux hosts report the partner's system priority and MAC per bond member in /proc/net/bonding. RouterOS
    partners report partner-sys-id and partner-sys-priority per member port. The readout is the gate state in
    baseline_confirmed, or the host bonds in baseline_bonds. Runs without either have no measurement.
    """
    event = marks.get("baseline_confirmed") or marks.get("baseline_bonds")
    if not event:
        return "not available: the run saved no baseline bond state"
    linux = dict(event.get("bonds") or {})
    for key, host in (("linux", "client 2 bond"), ("linux_client1", "client 1 bond")):
        if isinstance(event.get(key), str):
            linux[host] = event[key]
    bonds = {}
    for host, text in linux.items():
        members = {member: f"{priority}/{mac.lower()}" for member, priority, mac in LINUX_PARTNER.findall(text or "")}
        if members:
            bonds[host] = members
    routers = event.get("routers") or {}
    for label, ports in (partner_bonds or {}).items():
        members = {}
        for node, port in ports:
            seen = {name: f"{priority}/{mac.lower()}" for name, mac, priority in ROUTEROS_PARTNER.findall(routers.get(node) or "")}
            if port in seen:
                members[f"{node}:{port}"] = seen[port]
        if members:
            bonds[label] = members
    return {label: {"members": members, "same": len(members) >= 2 and len(set(members.values())) == 1}
            for label, members in bonds.items()} or "not available: the baseline state holds no partner system ID"


def grade_system_ids(measured, check):
    """Both MLAG peers present the same LACP system ID on each MLAG bond: a baseline check."""
    if isinstance(measured, str):
        return
    for label, bond in measured.items():
        check("fail", bond["same"], f"Both MLAG peers present one LACP system ID on the {label}: "
              + ", ".join(f"{member} {value}" for member, value in sorted(bond["members"].items())), "baseline")


def access_bpdus(bpdus, start, down, up, end):
    """Check E: BPDUs that carry the access switch's bridge ID as sender on the traffic host's MLAG bond.

    Saved Medium runs show no BPDU at all on these captures, so any such frame is a BPDU leaked to the wrong
    dual-connected bond.
    """
    phases = (("baseline", start, down), ("withdrawal", down, up), ("restoration", up, end))
    found = [{"point": cap, "time_s": seconds(stamp - start), "phase": phase_of(stamp, phases)}
             for cap, stamp, bridge in bpdus if cap in HOST_BOND_CAPTURES and bridge == ACCESS_BRIDGE_MAC]
    return {"captures": list(HOST_BOND_CAPTURES), "sender_bridge_mac": ACCESS_BRIDGE_MAC,
            "phases_s": {label: [seconds(low - start), seconds(high - start)] for label, low, high in phases
                         if high > low},
            "by_phase": {label: {"count": sum(f["phase"] == label for f in found),
                                 "first": [f for f in found if f["phase"] == label][:5]} for label, _, _ in phases}}


def grade_access_bpdus(measured, check):
    for phase in measured["phases_s"]:
        found = measured["by_phase"][phase]
        check("fail", not found["count"], f"{phase.capitalize()}: {found['count']} BPDUs from the access switch "
              f"({ACCESS_BRIDGE_MAC}) on the traffic host's MLAG bond, limit 0"
              + "".join(f"; {f['point']} at {f['time_s']:.3f} s" for f in found["first"]), phase)
