"""Score the two-pair root cases: service loss per phase and whether STP root stayed on pair A."""

import json

from .device_state import TWO_PAIR_NODE_READS, grade_gate, known, lacp_system_ids, mlag, stp
from .evidence import load_jsonl, packets
from .networka import recorded
from .forwarding_checks import TWO_PAIR_HOSTS, TWO_PAIR_OUTSIDE, TWO_PAIR_PARTNER_BONDS, forwarding, grade
from .forwarding_checks import grade_system_ids
from .legacy_checks import check_calibration
from .measure import number, score_flows, seconds, within
from .reboot_checks import cadence_ok, cadence_text, check_reboot_flows, guest_window, sender_pause_rule
from .report import write_timeline
from .root_evidence import read_root_packets, read_root_state, read_root_syslog
from .two_pair_topology import (
    PEER, SETUPS, TWO_PAIR_CAPTURES, TWO_PAIR_FLOWS, TWO_PAIR_NODES, TWO_PAIR_PROBES, TWO_PAIR_TARGETS, expected_ids,
    two_pair_mode, two_pair_setup,
)

# Pair B's members of the inter-pair bond: BPDUs from the root pair arrive here.
ROOT_BPDU_POINTS = ("q1-tap2", "q2-tap2")
STP_FIELDS = ("frame.time_epoch", "stp.version", "stp.root.prio", "stp.root.ext", "stp.root.hw", "stp.bridge.hw")


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
            state = known(mlag, sample)
            if state is None or not start <= sample["started_ns"] <= end:
                continue
            bridge = known(stp, sample) or {}
            value = (bridge.get("root_bridge_id"), bridge.get("bridge_id"), state["state"], state.get("role"))
            if value != previous:
                transitions.append({"at_s": seconds(sample["started_ns"] - start), "root_id": value[0],
                                    "bridge_id": value[1], "mlag_state": value[2], "active_role": value[3]})
                previous = value
        history[node] = transitions
    return history


def roots_between(path, node, low, high):
    """Root bridge IDs a switch reported between low and high, and how many samples there could not say."""
    roots = [(known(stp, sample) or {}).get("root_bridge_id")
             for sample in load_jsonl(path / f"state-{node}.jsonl")
             if low <= sample["started_ns"] and sample.get("done_ns", high + 1) <= high]
    return set(roots) - {None}, roots.count(None) if roots else 1


def check_roots(path, node, low, high, root_id, check, phase, text):
    """An undecided sample makes the phase an evidence error; a decided other root fails it."""
    observed, undecided = roots_between(path, node, low, high)
    check("error", not undecided, f"{node} reported a root bridge ID in every sample {text}; {undecided} undecided",
          phase)
    check("fail", observed == {root_id}, f"{node} kept root {root_id} {text}; observed {sorted(observed)}", phase)


def topology_changes(path, node, low, high):
    """The bridge topology-change counter in the samples between low and high."""
    changes = [count for sample in load_jsonl(path / f"state-{node}.jsonl")
               if low <= sample["started_ns"] < high
               and (count := (known(stp, sample) or {}).get("topology_changes")) is not None]
    return [changes[0], changes[-1]] if changes else None


def check_interpair_flap(spec, path, marks, flows, start, down, up, end, stp, root_id, result, check):
    """One inter-pair bond member down and up: service within the member limit, root unchanged, topology changes recorded."""
    for event_name, phase in (("down_observed", "withdrawal"), ("up_observed", "restoration")):
        event = marks.get(event_name, {})
        bound = event.get("max_latency_s")
        check("error", bool(event) and not event["missing"] and bound is not None and bound <= 2,
              f"Inter-pair member {event_name.split('_')[0]} at both CHRs and both veths within 2 s", phase)
    hold = seconds(marks["up_start"]["mono_ns"] - marks["down_applied"]["mono_ns"]) if "down_applied" in marks else None
    windows = {"before": (start, down), "during": (down, up), "after": (up, end)}
    result["interpair_flap"] = {"hold_s": hold, "topology_changes_first_last": {
        node: {label: topology_changes(path, node, low, high) for label, (low, high) in windows.items()}
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
            check_roots(path, node, low, high, root_id, check, phase, f"during {phase}")


def evaluate_two_pair(path, name, checks, result, *, spec):

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
            check("error", False, "The attempt stopped before the baseline was observed")
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
        baseline = grade_gate(path / "gate-baseline", check, "Baseline device state")
        if "baseline_rejected" in marks:
            result["fault_withheld"] = marks["baseline_rejected"]["issues"]
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
        result["sampling"] = read_root_state(path, start, end, target, check, timeline, nodes=TWO_PAIR_NODE_READS,
                                             stp_nodes=TWO_PAIR_NODES if stp else ())
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
        grade(result["forwarding"], check, outside_limit_s=spec.grading_limits.outside_flood_s)
        result["lacp_system_ids"] = lacp_system_ids(baseline, TWO_PAIR_PARTNER_BONDS)
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
        if not executed:
            return
        check("error", "baseline_restored" in marks, "Restore state was captured", "restoration")
        if "baseline_restored" in marks:
            grade_gate(path / "gate-restored", check, "Restoration", "restoration")
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
                check_roots(path, node, low, high, root_id, check, phase, f"while {target} was {moment}")
    finally:
        write_timeline(path, start, timeline)
