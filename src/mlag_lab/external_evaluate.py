"""Replay the external-root gate, elections and service bounds from saved evidence."""

import json

from .cases import case_spec
from .device_state import DEVICES, MEDIUM_NODE_READS, SMALL_NODE_READS, bridge_port, gate_roles, grade_gate
from .device_state import lacp_system_ids
from .direct_topology import DIRECT_CAPTURES, DIRECT_CASES, DIRECT_FLOWS, DIRECT_NODES
from .direct_topology import DIRECT_FLOOD_FLOWS, DIRECT_FLOOD_RECEIVERS
from .evidence import load_jsonl, packets
from .networka import recorded
from .external_topology import (
    ALL_STP_OFF_CASES, ARCHIVED_EXTERNAL_MANAGEMENT, EXTERNAL_CAPTURES, EXTERNAL_LAB_NAME,
    EXTERNAL_NODES, EXTERNAL_TARGETS, NO_STP_CASES, ROOT_ATTACHMENTS, ROOT_MACS, election_ids, preferred_root,
)
from .flood_checks import check_floods
from .forwarding_checks import DIRECT_OUTSIDE, MEDIUM_HOSTS, MEDIUM_OUTSIDE, SMALL_HOSTS, forwarding, grade
from .forwarding_checks import MEDIUM_PARTNER_BONDS, grade_system_ids
from .forwarding_checks import access_bpdus, grade_access_bpdus
from .legacy import FLOOD_SENDER_MEMBERS
from .legacy_checks import check_calibration
from .measure import number, score_flows, seconds, within
from .reboot_checks import cadence_ok, cadence_text, check_power_loss, check_reboot_flows, guest_window
from .reboot_checks import bypass_kept_pace, pause_case, peer_observations, sender_pause_rule
from .report import write_timeline
from .root_evidence import read_root_packets, read_root_state, read_root_syslog
from .root_topology import (
    MEDIUM_CORE_OFF_CASES, MEDIUM_NODES, MEDIUM_STP_OFF_CASES, MEDIUM_TARGETS, ROOT_CAPTURES, ROOT_FLOWS,
    medium_mode, medium_root_id,
)
# Capture points a BPDU reaches only if an MLAG peer relays it: the peer link and the client 2 bond.
PAIR_RELAY_POINTS = ("p1-tap1", "p2-tap1", "p1-tap3", "p2-tap3", "c2-eth1", "c2-eth2", "c2-bond0")
PAIR_BRIDGE_MACS = ("02:00:00:21:00:11", "02:00:00:21:00:12")


def direct_role_issues(name, roles, target, mode):
    """Opposite MLAG roles, one shared root with spanning tree on, and the target in the role its case reboots.

    roles holds each MLAG peer's role and root bridge ID as Networka read them in the gate.
    """
    issues = []
    found = {node: value["role"] for node, value in roles.items()}
    roots = {value["root_id"] for value in roles.values()}
    if set(found.values()) != {"primary", "secondary"} or mode != "none" and (len(roots) != 1 or None in roots):
        issues.append(f"Expected complementary MLAG roles and a shared RSTP root: {roles}")
    intent = case_spec(name).reboot_intent
    target_role = intent.fault.reboot_role if intent else name.rsplit("-", 1)[1]
    if target_role in ("primary", "secondary") and found.get(target) != target_role:
        issues.append(f"{target} did not hold the intended MLAG role for {name}")
    return issues


def grade_state(path, name, folder, check, label, phase=None, *, direct, target, mode):
    """Replay one saved gate, plus the role and root checks of the direct runner, into suite checks."""
    report = grade_gate(path / folder, check, label, phase)
    if direct and report is not None:
        roles = gate_roles(report, {node: DEVICES[node] for node in DIRECT_NODES})
        for issue in direct_role_issues(name, roles, target, mode):
            check("fail", False, f"{label}: {issue}", phase)
    return report


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
    # Nothing is required: RouterOS sends no BPDUs from edge ports, and every access switch port is an edge port.
    unexpected = sorted(point for point, roots in seen.items() if point in PAIR_RELAY_POINTS or any(
        sender in PAIR_BRIDGE_MACS for senders in roots.values() for sender in senders))
    return {"roots": seen, "missing": [], "unexpected": unexpected}


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


def evaluate_external(path, name, checks, result, *, spec):
    intent = spec.reboot_intent

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
            check("error", False, "The attempt stopped before the baseline was observed")
            return
        baseline_end = number(marks, "baseline_observed")
        direct = name in DIRECT_CASES
        medium = name in MEDIUM_TARGETS
        direct_mode = manifest.get("bridge_mode", "rstp")
        all_off = name in (*ALL_STP_OFF_CASES, *MEDIUM_STP_OFF_CASES) or direct and direct_mode == "none"
        target = manifest["target"] if direct else (MEDIUM_TARGETS if medium else EXTERNAL_TARGETS)[name]
        captures = DIRECT_CAPTURES if direct else ROOT_CAPTURES if medium else EXTERNAL_CAPTURES
        definitions = DIRECT_FLOWS if direct else ROOT_FLOWS
        flood_flows = DIRECT_FLOOD_FLOWS if direct else {}
        recovery_probes, recovery_label = 10, "ten"
        if intent:
            flood_flows = intent.flood_flows
            recovery_probes = intent.traffic.recovery_consecutive_replies
            recovery_label = intent.traffic.recovery_count_label
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
        elif name in NO_STP_CASES:
            result["bridge_modes"] = {"cores": "none", "witness_and_roots": "rstp"}
        else:
            result["election"] = {"preferred": preferred, "root": root_id, "backup": backup_id}
        before = marks["baseline_observed"]
        baseline = grade_state(path, name, "gate-baseline", check, "Baseline device state", direct=direct,
                               target=target, mode=direct_mode)
        if "baseline_rejected" in marks:
            result["fault_withheld"] = marks["baseline_rejected"]["issues"]
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
        bpdus = []
        icmp, frames, _, _ = read_root_packets(path, captures, start, down, check, timeline,
                                             reference_root=False, floods=flood_flows,
                                             bpdus=bpdus)
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
        if direct:
            stp_nodes = () if direct_mode == "none" else DIRECT_NODES
        elif name in MEDIUM_CORE_OFF_CASES:
            stp_nodes = ("witness",)
        else:
            stp_nodes = () if medium_mode(name) == "none" else MEDIUM_NODES
        result["sampling"] = read_root_state(path, start, end, target, check, timeline,
                                             nodes=SMALL_NODE_READS if direct else MEDIUM_NODE_READS,
                                             stp_nodes=stp_nodes)
        if direct:
            nodes, label = recorded(DIRECT_NODES, manifest), manifest["topology"]
        elif medium:
            nodes, label = recorded(MEDIUM_NODES, manifest), manifest["topology"]
        elif manifest["topology"] in (EXTERNAL_LAB_NAME, "dc1-mlag-external"):
            nodes, label = EXTERNAL_NODES, manifest["topology"]
        else:
            nodes, label = ARCHIVED_EXTERNAL_MANAGEMENT, "mlag-external"
        result["syslog"] = read_root_syslog(path, target, check, timeline, nodes=nodes, label=label)
        if "syslog_rebind_requested" in marks:
            check("error", result["syslog"]["target_after_rebind_received"],
                  f"{target} emitted the post-observation syslog rebind marker")
        flows = score_flows(icmp, start, end, actions, timeline, definitions=definitions, detailed=True,
                            recovery_probes=recovery_probes)
        result["flows"] = flows
        result["forwarding"] = forwarding(
            path, icmp, definitions, start, down, up, end, outside=DIRECT_OUTSIDE if direct else MEDIUM_OUTSIDE,
            hosts=SMALL_HOSTS if direct else MEDIUM_HOSTS, nodes=nodes, recovery=recovery if executed else None,
            stopped=stopped["epoch_ns"] if executed and "recovery_end" not in marks else None)
        grade(result["forwarding"], check, outside_limit_s=spec.grading_limits.outside_flood_s)
        result["lacp_system_ids"] = lacp_system_ids(baseline, None if direct else MEDIUM_PARTNER_BONDS)
        grade_system_ids(result["lacp_system_ids"], check)
        if not direct:
            result["access_bpdus"] = access_bpdus(bpdus, start, down, up, end)
            grade_access_bpdus(result["access_bpdus"], check)
        bypass_streams = spec.control_flows if intent else (301, 303)
        result["sender_pause_rule"] = sender_pause_rule(name if executed else "", flows, definitions,
                                                        seconds(down - start), seconds(end - start),
                                                        bypass=bypass_streams)
        for ident, flow in flows.items():
            bypass = ident in bypass_streams
            check("error", flow["sent"] >= 30 and cadence_ok(flow),
                  f"{ident} at least 30 emits and cadence within 450 ms{cadence_text(flow)}")
            check("error", not flow["capture_mismatches"], f"{ident} endpoint capture agreement")
            check("error" if bypass else "fail", flow["baseline_good"] >= 30 and not flow["baseline_missed"],
                  f"{ident} baseline loss-free, {flow['baseline_good']} delivered, {flow['baseline_missed']} missed")
            check("error" if bypass else "fail", not flow["duplicates"], f"{ident} duplicate-free")
            if executed:
                check("error" if bypass else "fail", flow["stable_recovery"],
                      f"{ident} delivered {recovery_label} consecutive probes after recovery", "restoration")
            for gap in flow["gaps"]:
                for sequence, miss in gap.get("misses", {}).items():
                    miss["frames"] = {label: frames[ident, kind, sequence]
                                      for label, kind in (("request", 8), ("reply", 0))}
        if "fault_withheld" in result and all(c["ok"] for c in checks if c["level"] == "fail"):
            check("error", False, f"Live baseline gate withheld the fault despite the closed captures: "
                  f"{result['fault_withheld']}")
        if executed:
            check("error", "baseline_restored" in marks, "Restore state was captured", "restoration")
            if "baseline_restored" in marks:
                grade_state(path, name, "gate-restored", check, "Restoration", "restoration", direct=direct,
                            target=target, mode=direct_mode)
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
        if direct and target and "peer" in result:
            survivor = result["peer"]["survivor"]
            bonds = ("client1", "client2")
            observations, undecided = [], 0
            for sample in load_jsonl(path / f"state-{survivor}.jsonl"):
                if first_miss <= sample["started_ns"] <= sample.get("done_ns", last_miss + 1) <= last_miss:
                    try:
                        observations.append({bond: bridge_port(sample, bond)["forwarding"] for bond in bonds})
                    except ValueError:
                        undecided += 1
            check("error", bool(observations) and not undecided,
                  f"{survivor} supplied direct-edge port state in every sample during the guest absence; "
                  f"{undecided} undecided", "withdrawal")
            for bond in bonds:
                check("fail", all(ports[bond] for ports in observations),
                      f"{survivor}:{bond} stayed forwarding while {target} was absent", "withdrawal")
        if direct:
            result["floods"] = check_floods(path, spec, icmp, start, end, actions, DIRECT_FLOOD_RECEIVERS,
                                            FLOOD_SENDER_MEMBERS, flood_flows, timeline, check,
                                            pause_window=(down, end) if executed and pause_case(name)
                                            and bypass_kept_pace(flows, bypass_streams) else None)
    finally:
        write_timeline(path, start, timeline)
