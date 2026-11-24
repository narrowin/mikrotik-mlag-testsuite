"""Replay the external-root gate, elections and service bounds from saved evidence."""

import json
import re

from .direct_topology import DIRECT_CAPTURES, DIRECT_CASES, DIRECT_FLOWS, DIRECT_NODES
from .evidence import load_jsonl, packets
from .external_topology import (
    ALL_STP_OFF_CASES, ARCHIVED_EXTERNAL_MANAGEMENT, EXTERNAL_CAPTURES, EXTERNAL_LAB_NAME,
    EXTERNAL_NODES, EXTERNAL_TARGETS, NO_STP_CASES,
    ROOT_ATTACHMENTS, ROOT_MACS, election_ids, preferred_root,
)
from .cases import case_spec
from .legacy_checks import check_calibration
from .measure import number, score_flows, seconds, within
from .reboot_checks import check_power_loss, check_reboot_flows, guest_window, peer_observations
from .report import write_timeline
from .root_evidence import read_root_packets, read_root_state, read_root_syslog, summarize_router
from .root_state import access_guards, linux_members, router_members, router_state, uptime
from .root_topology import (
    ACCESS_ROOT_ID, MEDIUM_CORE_OFF_CASES, MEDIUM_NODES, MEDIUM_STP_OFF_CASES, MEDIUM_TARGETS, ROOT_CAPTURES,
    ROOT_FLOWS, medium_root_id,
)

CARRIER_COUNTS = {"p1": 4, "p2": 4, "witness": 3, "r1": 1, "r2": 1}
MEDIUM_CARRIERS = dict.fromkeys(MEDIUM_NODES, 3)
# Capture points a BPDU reaches only if an MLAG peer relays it: the peer link and the client 2 bond.
PAIR_RELAY_POINTS = ("p1-tap1", "p2-tap1", "p1-tap3", "p2-tap3", "c2-eth1", "c2-eth2", "c2-bond0")
PAIR_BRIDGE_MACS = ("02:00:00:21:00:11", "02:00:00:21:00:12")


def normalized_id(value):
    return "0x0000." + value[2:] if value and value.startswith("0.") else value


def baseline_issues(name, state, config):
    medium = name in MEDIUM_TARGETS
    preferred = preferred_root(name)
    root_id, backup_id = election_ids(preferred)
    if medium:
        root_id = medium_root_id(name)
    no_stp = name in NO_STP_CASES
    all_off = name in (*ALL_STP_OFF_CASES, *MEDIUM_STP_OFF_CASES)
    core_off = name in MEDIUM_CORE_OFF_CASES
    issues = []
    for node, raw in state["routers"].items():
        bridge, ports = router_state(raw)
        core = node in ("p1", "p2")
        mode = ("none" if all_off or core and (no_stp or core_off)
                else "mstp" if name.startswith("medium-mstp-") else "rstp")
        bridge_config = config[node].replace("witness-bond", "access-uplink")
        if not re.search(rf"\bprotocol-mode={mode}\b", bridge_config):
            issues.append(f"{node} effective protocol-mode is not {mode}")
        if core:
            role = "primary" if node == "p1" else "secondary"
            if (bridge.get("mlag-state"), bridge.get("mlag-active-role")) != ("connected", role):
                issues.append(f"{node} MLAG did not establish as {role}: {bridge}")
            priority = 10 if node == "p1" else 20
            required = ("mlag-peer-port=ether2", f"mlag-priority={priority}", "mlag-heartbeat=5s",
                        "mlag-init-delay=1m", "vlan-ids=110 tagged=ether2")
            for setting in required:
                if setting not in bridge_config:
                    issues.append(f"{node} configuration did not contain {setting}")
        if all_off or no_stp or core_off and core:
            if mode == "none" and "forward-reserved-addresses=yes" in bridge_config:
                issues.append(f"{node} forwards reserved addresses with mode none")
        else:
            observed_root = normalized_id(bridge.get("root-bridge-id"))
            if observed_root != root_id:
                issues.append(f"{node} root is {observed_root}, expected {root_id}")
            if medium:
                if node == "witness":
                    expected = "yes" if root_id == ACCESS_ROOT_ID else "no"
                    if bridge.get("root-bridge") != expected:
                        issues.append(f"Access switch root-bridge should be {expected}: {bridge}")
                non_edge = ("access-uplink",) if core else ("uplink",)
            else:
                expected_id = root_id if node == preferred else backup_id
                if node in ROOT_MACS and normalized_id(bridge.get("bridge-id")) != expected_id:
                    issues.append(f"{node} external bridge ID is {bridge.get('bridge-id')}, expected {expected_id}")
                root_port = ("none" if node == preferred else "ether2") if node in ROOT_MACS else (
                    "uplink" if node == "witness" else "ether5" if node == ROOT_ATTACHMENTS[preferred] else "ether2"
                )
                if bridge.get("root-port") != root_port:
                    issues.append(f"{node} selected {bridge.get('root-port')} as root port, expected {root_port}")
                non_edge = ("ether5", "access-uplink") if core else ("uplink",) if node == "witness" else ("ether2",)
            if core_off:
                # Campus option 1: the uplink bond is an edge port and the host port has BPDU guard.
                if ports.get("uplink", {}).get("edge-port") != "yes":
                    issues.append(f"Access switch uplink did not operate as an edge port: {ports.get('uplink')}")
                for port, setting in (("uplink", "edge=yes"), ("ether4", "edge=yes"), ("ether4", "bpdu-guard=yes")):
                    if not re.search(rf"\binterface={port}\s+bridge=bridge\b(?:(?!\n\s*\d+ ).)*?\b{setting}(?=\s)",
                                     bridge_config, re.S):
                        issues.append(f"Access switch {port} is not configured with {setting}")
            elif any(ports.get(port, {}).get("edge-port") != "no" for port in non_edge):
                issues.append(f"{node} ports {non_edge} did not operate as non-edge")
        paths = ("access-uplink", "client2", "ether5") if core else (
            ("uplink", "ether4") if node == "witness" else ("ether2",)
        )
        if medium and core:
            paths = ("access-uplink", "client2")
        expected_ports = set(paths) | ({"ether2"} if core else set())
        if set(ports) != expected_ports or "vlan-filtering=yes" not in bridge_config:
            issues.append(f"{node} VLAN filtering or bridge membership differs from the baseline: {ports}")
        for port in paths:
            if not re.search(rf"\binterface={port}\s+bridge=bridge\b(?:(?!\n\s*\d+ ).)*?\bpvid=110\b",
                             bridge_config, re.S):
                issues.append(f"{node}:{port} does not have effective PVID 110")
        carrier = summarize_router(raw)["carrier"]
        expected_carriers = MEDIUM_CARRIERS if medium else CARRIER_COUNTS
        if len(carrier) != expected_carriers[node] or set(carrier.values()) != {"link-ok"}:
            issues.append(f"{node} guest carrier differs from the baseline: {carrier}")
        if mode != "none":
            for port in paths:
                if ports.get(port, {}).get("forwarding") != "yes":
                    issues.append(f"{node}:{port} is not forwarding: {ports.get(port)}")
        expected_members = {"ether3", "ether4"} if core else {"ether2", "ether3"} if node == "witness" else set()
        members = router_members(raw)
        if set(members) != expected_members or any(
            any(member[side][3:6] != "SCD" for side in ("actor", "partner")) for member in members.values()
        ):
            issues.append(f"{node} LACP members are not all eligible: {members}")
    members = linux_members(state["linux"])
    if set(members) != {"eth1", "eth2"} or any(not all(member.values()) for member in members.values()):
        issues.append(f"Client B LACP is not eligible on both members: {members}")
    return issues


def direct_baseline_issues(name, state, config, target, mode):
    issues = []
    bridges = {}
    for node, raw in state["routers"].items():
        bridge, ports = router_state(raw)
        bridges[node] = bridge
        if f"protocol-mode={mode}" not in config[node] or bridge.get("mlag-state") != "connected":
            issues.append(f"{node} protocol-mode={mode} and connected MLAG were not verified: {bridge}")
        for bond in ("client1", "client2"):
            port = ports.get(bond, {})
            if mode != "none" and (port.get("edge-port") != "yes" or port.get("forwarding") != "yes"):
                issues.append(f"{node}:{bond} is not a forwarding edge port: {port}")
        members = router_members(raw)
        if set(members) != {"ether3", "ether4"} or any(
            any(member[side][3:6] != "SCD" for side in ("actor", "partner")) for member in members.values()
        ):
            issues.append(f"{node} LACP members are not all eligible: {members}")
    roles = {state.get("mlag-active-role") for state in bridges.values()}
    roots = {state.get("root-bridge-id") for state in bridges.values()}
    if roles != {"primary", "secondary"} or mode != "none" and (len(roots) != 1 or None in roots):
        issues.append(f"Expected complementary MLAG roles and a shared RSTP root: {bridges}")
    if name.endswith(("-primary", "-secondary")) and bridges.get(target, {}).get(
        "mlag-active-role"
    ) != name.rsplit("-", 1)[1]:
        issues.append(f"{target} did not hold the intended MLAG role for {name}")
    for client, key in (("c1", "linux_client1"), ("c2", "linux")):
        members = linux_members(state[key])
        if set(members) != {"eth1", "eth2"} or any(not all(member.values()) for member in members.values()):
            issues.append(f"{client} LACP is not eligible on both members: {members}")
    return issues


def pair_bpdus(path, start, end):
    """Every BPDU seen per capture point, and the points that show an MLAG peer sending or relaying one."""
    fields = ("frame.time_epoch", "stp.version", "stp.root.prio", "stp.root.ext", "stp.root.hw", "stp.bridge.hw")
    seen = {}
    for point in ROOT_CAPTURES:
        roots = {}
        for stamp, (version, priority, extension, root, sender) in packets(
            path / "captures" / f"{point}.pcap", fields, "stp"
        ):
            if within(stamp, start, end):
                identity = (f"{int(priority, 0) + int(extension, 0):#06x}.{root.lower()}" if priority and extension
                            else f"version {version}")
                roots.setdefault(identity, {}).setdefault(sender.lower(), 0)
                roots[identity][sender.lower()] += 1
        if roots:
            seen[point] = roots
    received = any(ACCESS_ROOT_ID in seen.get(point, {}) for point in ("witness-tap1", "witness-tap2"))
    unexpected = sorted(point for point, roots in seen.items() if point in PAIR_RELAY_POINTS or any(
        sender in PAIR_BRIDGE_MACS for senders in roots.values() for sender in senders))
    return {"roots": seen, "missing": [] if received else ["access uplink"], "unexpected": unexpected}


def bpdu_coverage(path, name, start, end):
    if name in MEDIUM_CORE_OFF_CASES:
        return pair_bpdus(path, start, end)
    medium = name in MEDIUM_TARGETS
    preferred = preferred_root(name)
    attached = ROOT_ATTACHMENTS[preferred]
    root_id = election_ids(preferred)[0]
    no_stp = name in NO_STP_CASES
    capture_points = ("r1-tap1", "r2-tap1", "p1-tap4", "p2-tap4", "p1-tap1", "p2-tap1",
                      "witness-tap1", "witness-tap2")
    fields = ("frame.time_epoch", "stp.version", "stp.root.prio", "stp.root.ext", "stp.root.hw", "stp.bridge.hw")
    seen = {}
    if name in (*ALL_STP_OFF_CASES, *MEDIUM_STP_OFF_CASES):
        unexpected = [
            point for point in (ROOT_CAPTURES if medium else EXTERNAL_CAPTURES)
            if any(within(stamp, start, end) for stamp, _ in packets(
                path / "captures" / f"{point}.pcap", ("frame.time_epoch",), "stp"
            ))
        ]
        return {"roots": {}, "missing": [], "unexpected": unexpected}
    if medium:
        root_id = medium_root_id(name)
        capture_points = ("witness-tap1", "witness-tap2")
    for point in capture_points:
        roots = {}
        for stamp, (version, priority, extension, root, sender) in packets(
            path / "captures" / f"{point}.pcap", fields, "stp"
        ):
            if version in ("2", "3") and priority and extension and within(stamp, start, end):
                identity = f"{int(priority, 0) + int(extension, 0):#06x}.{root.lower()}"
                roots.setdefault(identity, set()).add(sender.lower())
        seen[point] = {identity: sorted(senders) for identity, senders in roots.items()}
    if medium:
        missing = [] if any(root_id in roots for roots in seen.values()) else ["access uplink"]
        unexpected = []
    elif no_stp:
        missing = [point for point in ("r1-tap1", "r2-tap1") if not seen[point]]
        unexpected = sorted({(point, sender) for point, roots in seen.items() for senders in roots.values()
                             for sender in senders if (
                                 point.startswith(("p1-tap1", "p2-tap1"))
                                 or sender in ("02:00:00:21:00:11", "02:00:00:21:00:12")
                                 or point.startswith("witness-") and sender in ROOT_MACS.values()
                             )})
    else:
        required = (f"{preferred}-tap1", f"{attached}-tap4", "witness")
        received = {point for point, roots in seen.items() if root_id in roots}
        if received.intersection(("witness-tap1", "witness-tap2")):
            received.add("witness")
        missing = [point for point in required if point not in received]
        unexpected = []
    return {"roots": seen, "missing": missing, "unexpected": unexpected}


def broadcast_counts(path, start, end):
    counts = {}
    for origin, address in (("c1", "10.110.0.11"), ("c2", "10.110.0.12")):
        counts[origin] = [
            sum(within(stamp, start, end) for stamp, _ in packets(
                path / "captures" / f"{point}.pcap", ("frame.time_epoch",),
                f"arp.opcode == 1 && eth.dst == ff:ff:ff:ff:ff:ff && arp.src.proto_ipv4 == {address}",
            ))
            for point in ("c1-eth1", "c2-bond0")
        ]
    return counts


def election_samples(path, start, end):
    summaries = {}
    for node in EXTERNAL_NODES:
        roots = {}
        for sample in load_jsonl(path / f"state-{node}.jsonl"):
            if "raw" in sample and start <= sample["started_ns"] <= sample["done_ns"] <= end:
                bridge, _ = router_state(sample["raw"])
                identity = normalized_id(bridge.get("root-bridge-id"))
                if identity:
                    roots.setdefault(identity, [sample["started_ns"], sample["done_ns"]])[1] = sample["done_ns"]
        summaries[node] = roots
    return summaries


def evaluate_external(path, name, checks, result):
    spec = case_spec(name)

    def check(level, ok, detail, phase=None):
        checks.append({"level": level, "ok": bool(ok), "detail": detail} | ({"phase": phase} if phase else {}))

    events = load_jsonl(path / "events.jsonl")
    marks = {event["name"]: event for event in events}
    timeline = [(e["epoch_ns"], "action", json.dumps(e, sort_keys=True)) for e in events]
    start = marks.get("baseline_start", events[0])["epoch_ns"]
    manifest = json.loads((path / "attempt.json").read_text())
    if "devices" in manifest:
        result["devices"] = manifest["devices"]
    reset = marks.get("configuration_applied", {}).get("replies", {})
    decision = marks.get("baseline_confirmed") or marks.get("baseline_rejected")
    if decision and "started_mono_ns" in reset:
        reset_start = reset["started_mono_ns"]
        reset_end = reset["completed_mono_ns"]
        probe_start = marks["baseline_start"]["mono_ns"]
        probe_end = marks["baseline_observed"]["mono_ns"]
        verdict = decision["mono_ns"]
        result["initial_validation_s"] = {
            "management_reset": seconds(reset_end - reset_start),
            "settle_and_start_observers": seconds(probe_start - reset_end),
            "probe_window_and_readback": seconds(probe_end - probe_start),
            "check_wire_links_and_delivery": seconds(verdict - probe_end),
            "reset_to_verdict": seconds(verdict - reset_start),
        }
    try:
        if "runner_error" in marks:
            check("error", False, marks["runner_error"]["detail"])
        if "baseline_observed" not in marks:
            return
        baseline_end = number(marks, "baseline_observed")
        direct = name in DIRECT_CASES
        medium = name in MEDIUM_TARGETS
        direct_mode = manifest.get("bridge_mode", "rstp")
        all_off = name in (*ALL_STP_OFF_CASES, *MEDIUM_STP_OFF_CASES) or direct and direct_mode == "none"
        target = manifest["target"] if direct else (MEDIUM_TARGETS if medium else EXTERNAL_TARGETS)[name]
        captures = DIRECT_CAPTURES if direct else ROOT_CAPTURES if medium else EXTERNAL_CAPTURES
        definitions = DIRECT_FLOWS if direct else ROOT_FLOWS
        preferred = preferred_root(name)
        root_id, backup_id = election_ids(preferred)
        if direct:
            result["bridge_modes"] = {"cores": direct_mode, "clients": "direct-host-lag"}
        elif all_off:
            result["bridge_modes"] = dict.fromkeys(MEDIUM_NODES if medium else EXTERNAL_NODES, "none")
        elif medium:
            result["election"] = {"root": medium_root_id(name)}
            if name in MEDIUM_CORE_OFF_CASES:
                result["bridge_modes"] = {"cores": "none", "witness": "rstp"}
                guards = reset.get("access_guards") or access_guards(reset.get("access_guards_raw", ""))
                result["access_guards"] = guards
                check("error", guards == {"uplink_edge": "yes", "ether4_edge": "yes", "ether4_bpdu_guard": "yes",
                                          "ether4_loop_protect": "on"},
                      f"Access switch read back uplink edge, host port BPDU guard and loop protect: {guards}")
        elif name in NO_STP_CASES:
            result["bridge_modes"] = {"cores": "none", "witness_and_roots": "rstp"}
        else:
            result["election"] = {"preferred": preferred, "root": root_id, "backup": backup_id}
        before = marks["baseline_observed"]
        config = json.loads((path / "effective-config.json").read_text())
        issues = (direct_baseline_issues(name, before, config, target, direct_mode) if direct
                  else baseline_issues(name, before, config))
        for issue in issues:
            check("fail", False, issue)
        if "baseline_rejected" in marks:
            result["fault_withheld"] = marks["baseline_rejected"]["issues"]
        result["baseline_state"] = {node: summarize_router(raw) for node, raw in before["routers"].items()}
        if not direct:
            wire = bpdu_coverage(path, name, start, baseline_end)
            result["baseline_bpdus"] = wire
            # Keep BPDU findings independent of the forwarding verdict.
            check("fail", not wire["missing"] and not wire["unexpected"],
                  f"Baseline BPDU coverage missing {wire['missing']}, unexpected {wire['unexpected']}")
        if "broadcast_end" in marks:
            counts = broadcast_counts(path, number(marks, "broadcast_start"), number(marks, "broadcast_end"))
            result["broadcast_requests_at_endpoints"] = counts
            check("fail", all(pair == [3, 3] for pair in counts.values()),
                  f"Each of three broadcast requests per direction crossed once: {counts}")
        stopped = marks["collectors_stopped"]
        check("error", abs(stopped["clock_delta_ns"]) < 50_000_000, "Host clocks agreed within 50 ms")
        check("error", not stopped["early_exits"], "All capture and probe collectors stayed up")
        faults = ("attachment_down_start", "down_start", "power_off_start")
        down = next((marks[key] for key in faults if key in marks), before)["epoch_ns"]
        recovery = marks.get("recovery_start", before)["epoch_ns"]
        end = marks.get("recovery_end", before)["epoch_ns"]
        icmp, frames, _, _ = read_root_packets(path, captures, start, down, check, timeline,
                                             reference_root=False)
        if name in MEDIUM_CORE_OFF_CASES:
            scoring = pair_bpdus(path, start, end)
            result["bpdus_during_scoring"] = scoring["roots"]
            check("fail", not scoring["unexpected"],
                  f"Neither MLAG peer sent or relayed a BPDU throughout the scoring window: {scoring['unexpected']}")
        if all_off:
            bpdu_points = sorted({point for stamp, point, _ in timeline
                                  if point.startswith("bpdu-") and within(stamp, start, end)})
            result["stp_frames_during_scoring"] = bpdu_points
            check("fail", not bpdu_points, f"No spanning-tree frames throughout the scoring window: {bpdu_points}")
        executed = any(key in marks for key in faults)
        result["fault_executed"] = executed
        first_miss = last_miss = up = down
        if target and "guest_boot_observed" in marks:
            first_miss, last_miss, up = guest_window(icmp, target, down, end, check, timeline)
            result["peer"] = peer_observations(path, target, start, first_miss, last_miss, end, check, timeline,
                                               direct=direct)
            result["guest_absence_s"] = [seconds(stamp - start) for stamp in (first_miss, last_miss, up)]
        if target and "power_off_start" in marks:
            result["power"] = check_power_loss(marks, start, target, check)
        if "attachment_up_start" in marks:
            last_miss = number(marks, "attachment_up_start")
            up = number(marks, "attachment_up_applied")
        elif "up_start" in marks:
            up = number(marks, "up_start")
        actions = (("withdrawal", down, up), ("restoration", up, recovery))
        result["phases_s"] = {phase: [seconds(a - start), seconds(b - start)] for phase, a, b in actions}
        carriers = dict.fromkeys(DIRECT_NODES, 4) if direct else MEDIUM_CARRIERS if medium else CARRIER_COUNTS
        result["sampling"] = read_root_state(path, start, end, target, check, timeline, nodes=carriers)
        if direct:
            nodes, label = DIRECT_NODES, "mlag-small"
        elif medium:
            nodes, label = MEDIUM_NODES, manifest["topology"]
        elif manifest["topology"] in (EXTERNAL_LAB_NAME, "dc1-mlag-external"):
            nodes, label = EXTERNAL_NODES, manifest["topology"]
        else:
            nodes, label = ARCHIVED_EXTERNAL_MANAGEMENT, "mlag-external"
        result["syslog"] = read_root_syslog(path, target, check, timeline, nodes=nodes, label=label)
        if "syslog_rebind_requested" in marks:
            check("error", result["syslog"]["target_after_rebind_received"],
                  f"{target} emitted the post-observation syslog rebind marker")
        flows = score_flows(icmp, start, end, actions, timeline, definitions=definitions, detailed=True)
        result["flows"] = flows
        for ident, flow in flows.items():
            bypass = ident in (301, 303)
            check("error", flow["sent"] >= 30 and flow["max_send_interval_s"] <= 0.45,
                  f"{ident} at least 30 emits and cadence within 450 ms")
            check("error", not flow["capture_mismatches"], f"{ident} endpoint capture agreement")
            check("error" if bypass else "fail", flow["baseline_good"] >= 30 and not flow["baseline_missed"],
                  f"{ident} baseline loss-free, {flow['baseline_good']} delivered, {flow['baseline_missed']} missed")
            check("error" if bypass else "fail", not flow["duplicates"], f"{ident} duplicate-free")
            if executed:
                check("error" if bypass else "fail", flow["stable_recovery"],
                      f"{ident} delivered ten consecutive probes after recovery", "restoration")
            for gap in flow["gaps"]:
                for sequence, miss in gap.get("misses", {}).items():
                    miss["frames"] = {label: frames[ident, kind, sequence]
                                      for label, kind in (("request", 8), ("reply", 0))}
        if "fault_withheld" in result and all(c["ok"] for c in checks if c["level"] == "fail"):
            check("error", False, f"Live baseline gate withheld the fault despite the closed captures: "
                  f"{result['fault_withheld']}")
        for issue in marks.get("baseline_restored", {}).get("issues", []):
            check("fail", False, f"Restoration: {issue}", "restoration")
        if executed:
            check("error", "baseline_restored" in marks, "Restore state was captured", "restoration")
            if "baseline_restored" in marks and not direct:
                restored_wire = bpdu_coverage(path, name, recovery, end)
                result["restored_bpdus"] = restored_wire
                check("fail", not restored_wire["missing"] and not restored_wire["unexpected"],
                      f"Restored BPDU coverage missing {restored_wire['missing']}, "
                      f"unexpected {restored_wire['unexpected']}", "restoration")
            if name.endswith("-calibrate"):
                check_calibration(spec, marks, flows, result, check)
            else:
                check_reboot_flows(spec, flows, icmp, start, seconds(down - start), seconds(first_miss - start),
                                   seconds(last_miss - start), seconds(up - start), seconds(end - start), check,
                                   definitions=definitions)
        if "attachment_down_observed" in marks:
            hold_start = number(marks, "attachment_down_applied")
            hold_end = number(marks, "attachment_up_start")
            roots = election_samples(path, hold_start, hold_end)
            result["attachment_hold_roots"] = roots
            # The surviving core and witness must both receive the elected backup.
            backup = "r1" if preferred == "r2" else "r2"
            survivor = ROOT_ATTACHMENTS[backup]
            expected = {backup: backup_id, survivor: backup_id, "witness": backup_id}
            if not target:
                expected[ROOT_ATTACHMENTS[preferred]] = backup_id
                restored = marks.get("baseline_restored", {}).get("routers", {})
                for core in ("p1", "p2"):
                    before_uptime = uptime(before["routers"][core])
                    after_uptime = uptime(restored[core]) if core in restored else None
                    check("error", before_uptime is not None and after_uptime is not None
                          and after_uptime - before_uptime >= hold_end - hold_start - 1_000_000_000,
                          f"{core} was up throughout the attachment-only fault", "withdrawal")
            for node, identity in expected.items():
                check("fail", identity in roots[node], f"{node} elected {identity} during attachment withdrawal",
                      "withdrawal")
        elif target and executed and not (direct or medium or all_off or name in NO_STP_CASES):
            roots = election_samples(path, first_miss, last_miss)
            result["reboot_hold_roots"] = roots
            for node in (ROOT_ATTACHMENTS[preferred], "witness", preferred):
                check("fail", set(roots[node]) == {root_id},
                      f"{node} kept the preferred root {root_id} during the guest absence; "
                      f"observed {sorted(roots[node])}", "withdrawal")
        elif direct and target and "peer" in result:
            survivor = result["peer"]["survivor"]
            observations = [
                router_state(sample["raw"])[1]
                for sample in load_jsonl(path / f"state-{survivor}.jsonl")
                if "raw" in sample and first_miss <= sample["started_ns"] <= sample["done_ns"] <= last_miss
            ]
            check("error", bool(observations), f"{survivor} supplied direct-edge port state during the guest absence",
                  "withdrawal")
            for bond in ("client1", "client2"):
                check("fail", all(ports.get(bond, {}).get("forwarding") == "yes" for ports in observations),
                      f"{survivor}:{bond} stayed forwarding while {target} was absent", "withdrawal")
    finally:
        write_timeline(path, start, timeline)
