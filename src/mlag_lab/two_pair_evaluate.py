"""Score the two-pair root cases: service loss per phase and whether STP root stayed on pair A."""

import json
import re

from .cases import case_spec
from .evidence import load_jsonl, packets
from .networka import recorded
from .forwarding_checks import TWO_PAIR_HOSTS, TWO_PAIR_OUTSIDE, TWO_PAIR_PARTNER_BONDS, forwarding, grade
from .forwarding_checks import grade_system_ids, lacp_system_ids
from .legacy_checks import check_calibration
from .measure import number, score_flows, seconds, within
from .reboot_checks import cadence_ok, cadence_text, check_reboot_flows, guest_window, sender_pause_rule
from .report import write_timeline
from .root_evidence import read_root_packets, read_root_state, read_root_syslog, summarize_router
from .root_state import linux_members, router_members, router_state
from .two_pair_topology import (
    ADMIN_MACS, CLIENT_BONDS, MLAG_PRIORITIES, PAIRS, PEER, ROLES, SETUPS, TWO_PAIR_CAPTURES, TWO_PAIR_FLOWS,
    TWO_PAIR_NODES, TWO_PAIR_PROBES, TWO_PAIR_TARGETS, expected_ids, two_pair_lacp_strict, two_pair_mode, two_pair_setup,
)

CARRIERS = dict.fromkeys(TWO_PAIR_NODES, 3)
# Pair B's members of the inter-pair bond: BPDUs from the root pair arrive here.
ROOT_BPDU_POINTS = ("q1-tap2", "q2-tap2")
STP_FIELDS = ("frame.time_epoch", "stp.version", "stp.root.prio", "stp.root.ext", "stp.root.hw", "stp.bridge.hw")


def normalized_id(value):
    return "0x0000." + value[2:] if value and value.startswith("0.") else value


def baseline_issues(name, state, config):
    root_id, pair_ids = expected_ids(name)
    priorities, mode = SETUPS[two_pair_setup(name)], two_pair_mode(name)
    issues = []
    for node, raw in state["routers"].items():
        bridge, ports = router_state(raw)
        text = config[node]
        pair, client = PAIRS[node], CLIENT_BONDS[node]
        required = (f"protocol-mode={mode}", "vlan-filtering=yes", "mlag-peer-port=ether2",
                    f"mlag-priority={MLAG_PRIORITIES[node]}", "mlag-heartbeat=5s", "mlag-init-delay=1m",
                    f"admin-mac={ADMIN_MACS[node]}", "vlan-ids=110 tagged=ether2")
        for setting in required:
            if setting.lower() not in text.lower():
                issues.append(f"{node} configuration did not contain {setting}")
        # RouterOS does not print the bridge priority while spanning tree is off.
        if mode != "none" and not re.search(rf"(?<![-\w])priority={priorities[node]}\b", text):
            issues.append(f"{node} bridge priority is not {priorities[node]}")
        if (bridge.get("mlag-state"), bridge.get("mlag-active-role")) != ("connected", ROLES[node]):
            issues.append(f"{node} MLAG did not establish as {ROLES[node]}: {bridge}")
        strict = re.search(r'name="interpair".*?lacp-strict=(\w+)', text, re.S)
        if not strict or strict[1] != two_pair_lacp_strict(name):
            issues.append(f"{node} inter-pair bond lacp-strict is {strict and strict[1]}, "
                          f"expected {two_pair_lacp_strict(name)}")
        if mode == "none" and "forward-reserved-addresses=yes" in text:
            issues.append(f"{node} forwards reserved addresses with spanning tree off")
        if mode != "none" and normalized_id(bridge.get("bridge-id")) != pair_ids[pair]:
            issues.append(f"{node} bridge ID is {bridge.get('bridge-id')}, expected pair {pair} ID {pair_ids[pair]}")
        if mode != "none" and normalized_id(bridge.get("root-bridge-id")) != root_id:
            issues.append(f"{node} root is {bridge.get('root-bridge-id')}, expected {root_id}")
        if mode != "none" and bridge.get("root-bridge") != ("yes" if pair == "A" else "no"):
            issues.append(f"{node} root-bridge flag does not match pair {pair}: {bridge}")
        if set(ports) != {"ether2", "interpair", client}:
            issues.append(f"{node} bridge membership differs from the baseline: {ports}")
        for port in ("interpair", client):
            if not re.search(rf"\binterface={port}\s+bridge=bridge\b(?:(?!\n\s*\d+ ).)*?\bpvid=110\b", text, re.S):
                issues.append(f"{node}:{port} does not have effective PVID 110")
            if mode != "none" and ports.get(port, {}).get("forwarding") != "yes":
                issues.append(f"{node}:{port} is not forwarding: {ports.get(port)}")
        carrier = summarize_router(raw)["carrier"]
        if len(carrier) != CARRIERS[node] or set(carrier.values()) != {"link-ok"}:
            issues.append(f"{node} guest carrier differs from the baseline: {carrier}")
        members = router_members(raw)
        if set(members) != {"ether3", "ether4"} or any(
            any(member[side][3:6] != "SCD" for side in ("actor", "partner")) for member in members.values()
        ):
            issues.append(f"{node} LACP members are not all eligible: {members}")
    for client, key in (("c1", "linux_client1"), ("c2", "linux")):
        members = linux_members(state[key])
        if set(members) != {"eth1", "eth2"} or any(not all(member.values()) for member in members.values()):
            issues.append(f"Host {client[1]} LACP is not eligible on both members: {members}")
    return issues


def bpdu_coverage(path, name, start, end):
    """Root IDs carried by RSTP BPDUs on each inter-pair cable end; pair B must hear pair A as root.
    With spanning tree off, any BPDU on any capture point is unexpected."""
    if two_pair_mode(name) == "none":
        unexpected = [point for point in TWO_PAIR_CAPTURES if any(
            within(stamp, start, end) for stamp, _ in packets(path / "captures" / f"{point}.pcap",
                                                              ("frame.time_epoch",), "stp"))]
        return {"roots": {}, "missing": [], "unexpected": unexpected}
    root_id, _ = expected_ids(name)
    seen = {}
    for point in ("p1-tap2", "p2-tap2", *ROOT_BPDU_POINTS):
        roots = {}
        for stamp, (version, priority, extension, root, sender) in packets(
            path / "captures" / f"{point}.pcap", STP_FIELDS, "stp"
        ):
            if version in ("2", "3") and priority and extension and within(stamp, start, end):
                identity = f"{int(priority, 0) + int(extension, 0):#06x}.{root.lower()}"
                roots.setdefault(identity, set()).add(sender.lower())
        seen[point] = {identity: sorted(senders) for identity, senders in roots.items()}
    received = any(root_id in seen[point] for point in ROOT_BPDU_POINTS)
    return {"roots": seen, "missing": [] if received else ["pair B inter-pair members"], "unexpected": []}


def root_history(path, start, end):
    """Each switch's reported bridge ID, root ID and MLAG role, as transitions on the scoring clock."""
    history = {}
    for node in TWO_PAIR_NODES:
        previous, transitions = None, []
        for sample in load_jsonl(path / f"state-{node}.jsonl"):
            if "raw" not in sample or not start <= sample["started_ns"] <= end:
                continue
            bridge, _ = router_state(sample["raw"])
            value = (normalized_id(bridge.get("root-bridge-id")), normalized_id(bridge.get("bridge-id")),
                     bridge.get("mlag-state"), bridge.get("mlag-active-role"))
            if value != previous:
                transitions.append({"at_s": seconds(sample["started_ns"] - start), "root_id": value[0],
                                    "bridge_id": value[1], "mlag_state": value[2], "active_role": value[3]})
                previous = value
        history[node] = transitions
    return history


def roots_between(path, node, low, high):
    return {
        normalized_id(router_state(sample["raw"])[0].get("root-bridge-id"))
        for sample in load_jsonl(path / f"state-{node}.jsonl")
        if "raw" in sample and low <= sample["started_ns"] and sample["done_ns"] <= high
    } - {None}


def fdb_counters(path, node, low, high):
    """Bridge host table size and bridge topology-change counter in the samples between low and high."""
    entries, changes = [], []
    for sample in load_jsonl(path / f"state-{node}.jsonl"):
        if "raw" not in sample or not low <= sample["started_ns"] < high:
            continue
        if count := re.search(r"^host-entries=(\d+)", sample["raw"], re.M):
            entries.append(int(count[1]))
        if (counter := router_state(sample["raw"])[0].get("topology-changes", "")).isdigit():
            changes.append(int(counter))
    return {"samples_with_host_count": len(entries),
            "host_entries_min_max": [min(entries), max(entries)] if entries else None,
            "topology_changes_first_last": [changes[0], changes[-1]] if changes else None}


def check_interpair_flap(spec, path, marks, flows, start, down, up, end, stp, root_id, result, check):
    """One inter-pair bond member down and up: service within the member limit, root unchanged, FDB counters recorded."""
    for event_name, phase in (("down_observed", "withdrawal"), ("up_observed", "restoration")):
        event = marks.get(event_name, {})
        bound = event.get("max_latency_s")
        check("error", bool(event) and not event["missing"] and bound is not None and bound <= 2,
              f"Inter-pair member {event_name.split('_')[0]} at both CHRs and both veths within 2 s", phase)
    hold = seconds(marks["up_start"]["mono_ns"] - marks["down_applied"]["mono_ns"]) if "down_applied" in marks else None
    windows = {"before": (start, down), "during": (down, up), "after": (up, end)}
    result["interpair_flap"] = {"hold_s": hold, "fdb": {node: {label: fdb_counters(path, node, low, high)
                                                               for label, (low, high) in windows.items()}
                                                        for node in TWO_PAIR_NODES}}
    for ident, flow in flows.items():
        if ident in spec.control_flows:
            check("error", not flow["gaps"], f"{ident} independent bypass stayed clean")
            continue
        for gap in flow["gaps"]:
            for phase in gap["phases"]:
                limit = spec.limit(phase)
                lower, upper = gap["lower_s"], gap["upper_s"]
                if lower > limit:
                    check("fail", False, f"{ident} {phase} loss ≥ {lower:.3f} s exceeds {limit:g} s", phase)
                elif upper is None or upper > limit:
                    check("inconclusive", False, f"{ident} {phase} loss overlaps the {limit:g} s threshold", phase)
    result["root_history"] = root_history(path, start, end)
    if not stp:
        return
    for node in TWO_PAIR_NODES:
        for phase, low, high in (("withdrawal", down, up), ("restoration", up, end)):
            observed = roots_between(path, node, low, high)
            check("fail", observed == {root_id}, f"{node} kept root {root_id} during {phase}; observed {sorted(observed)}",
                  phase)


def evaluate_two_pair(path, name, checks, result):
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
    try:
        if "runner_error" in marks:
            check("error", False, marks["runner_error"]["detail"])
        if "baseline_observed" not in marks:
            return
        baseline_end = number(marks, "baseline_observed")
        target = TWO_PAIR_TARGETS[name]
        root_id, pair_ids = expected_ids(name)
        stp = two_pair_mode(name) != "none"
        if stp:
            result["election"] = {"setup": two_pair_setup(name), "priorities": SETUPS[two_pair_setup(name)],
                                  "root": root_id, "pair_ids": pair_ids}
        else:
            result["bridge_modes"] = dict.fromkeys(TWO_PAIR_NODES, "none")
        before = marks["baseline_observed"]
        config = json.loads((path / "effective-config.json").read_text())
        for issue in baseline_issues(name, before, config):
            check("fail", False, issue)
        if "baseline_rejected" in marks:
            result["fault_withheld"] = marks["baseline_rejected"]["issues"]
        result["baseline_state"] = {node: summarize_router(raw) for node, raw in before["routers"].items()}
        wire = bpdu_coverage(path, name, start, baseline_end)
        result["baseline_bpdus"] = wire
        if stp:
            check("fail", not wire["missing"], f"Baseline BPDUs for root {root_id} reached pair B: {wire['missing']}")
        else:
            check("fail", not wire["unexpected"], f"No spanning-tree frames in the baseline: {wire['unexpected']}")
        stopped = marks["collectors_stopped"]
        check("error", abs(stopped["clock_delta_ns"]) < 50_000_000, "Host clocks agreed within 50 ms")
        check("error", not stopped["early_exits"], "All capture and probe collectors stayed up")
        down = marks.get("down_start", before)["epoch_ns"]
        recovery = marks.get("recovery_start", before)["epoch_ns"]
        end = marks.get("recovery_end", before)["epoch_ns"]
        icmp, frames, _, _ = read_root_packets(path, TWO_PAIR_CAPTURES, start, down, check, timeline,
                                             reference_root=False, probes=TWO_PAIR_PROBES)
        executed = "down_start" in marks
        result["fault_executed"] = executed
        first_miss = last_miss = up = down
        if target and "guest_boot_observed" in marks:
            first_miss, last_miss, up = guest_window(icmp, target, down, end, check, timeline, probes=TWO_PAIR_PROBES)
            result["guest_absence_s"] = [seconds(stamp - start) for stamp in (first_miss, last_miss, up)]
        elif "up_start" in marks:
            up = number(marks, "up_start")
        actions = (("withdrawal", down, up), ("restoration", up, recovery))
        result["phases_s"] = {phase: [seconds(a - start), seconds(b - start)] for phase, a, b in actions}
        result["sampling"] = read_root_state(path, start, end, target, check, timeline, nodes=CARRIERS)
        nodes = recorded(TWO_PAIR_NODES, manifest)
        result["syslog"] = read_root_syslog(path, target, check, timeline, nodes=nodes,
                                            label=manifest["topology"])
        if "syslog_rebind_requested" in marks:
            check("error", result["syslog"]["target_after_rebind_received"],
                  f"{target} emitted the post-observation syslog rebind marker")
        flows = score_flows(icmp, start, end, actions, timeline, definitions=TWO_PAIR_FLOWS, detailed=True)
        result["flows"] = flows
        result["forwarding"] = forwarding(path, icmp, TWO_PAIR_FLOWS, start, down, up, end, outside=TWO_PAIR_OUTSIDE,
                                          hosts=TWO_PAIR_HOSTS, nodes=nodes,
                                          recovery=recovery if executed else None, stopped=stopped["epoch_ns"]
                                          if executed and "recovery_end" not in marks else None)
        grade(result["forwarding"], check)
        result["lacp_system_ids"] = lacp_system_ids(marks, TWO_PAIR_PARTNER_BONDS)
        grade_system_ids(result["lacp_system_ids"], check)
        result["sender_pause_rule"] = sender_pause_rule(name if executed else "", flows, TWO_PAIR_FLOWS,
                                                        seconds(down - start), seconds(end - start))
        for ident, flow in flows.items():
            bypass = ident in (301, 303)
            check("error", flow["sent"] >= 30 and cadence_ok(flow),
                  f"{ident} at least 30 emits and cadence within 450 ms{cadence_text(flow)}")
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
        if not executed:
            return
        check("error", "baseline_restored" in marks, "Restore state was captured", "restoration")
        if "baseline_restored" in marks:
            restored = bpdu_coverage(path, name, recovery, end)
            result["restored_bpdus"] = restored
            check("fail", not restored["missing"] and not restored["unexpected"],
                  f"Restored BPDUs: missing {restored['missing']}, unexpected {restored['unexpected']}", "restoration")
        if not stp:
            scoring = bpdu_coverage(path, name, start, end)["unexpected"]
            result["stp_frames_during_scoring"] = scoring
            check("fail", not scoring, f"No spanning-tree frames throughout the scoring window: {scoring}")
        if name.endswith("-calibrate"):
            check_calibration(spec, marks, flows, result, check)
            return
        if name.endswith("-interpair-member-flap"):
            check_interpair_flap(spec, path, marks, flows, start, down, up, end, stp, root_id, result, check)
            return
        check_reboot_flows(spec, flows, icmp, start, seconds(down - start), seconds(first_miss - start),
                           seconds(last_miss - start), seconds(up - start), seconds(end - start), check,
                           definitions=TWO_PAIR_FLOWS)
        result["root_history"] = root_history(path, start, end)
        result["survivor"] = PEER[target]
        if "guest_boot_observed" not in marks or not stp:
            return
        # The rebooting switch reports its own view while it boots; the other three show where the root is.
        for node in TWO_PAIR_NODES:
            if node == target:
                continue
            for phase, low, high, moment in (("withdrawal", down, up, "absent"), ("restoration", up, end, "returning")):
                observed = roots_between(path, node, low, high)
                check("fail", observed == {root_id},
                      f"{node} kept root {root_id} while {target} was {moment}; observed {sorted(observed)}", phase)
    finally:
        write_timeline(path, start, timeline)
