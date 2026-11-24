"""Bracket chassis loss, carrier and target return separately from VLAN outages."""

import json

from .evidence import load_jsonl
from .measure import seconds
from .root_evidence import summarize_router
from .root_state import router_state
from .root_topology import MANAGEMENT_PROBES, POWER_OFF_HOLD_S, ROOT_FLOWS

POWER_MARKS = ("power_off_start", "power_off_applied", "power_off_observed", "power_on_start",
               "power_on_applied", "power_on_observed", "guest_boot_observed")


def guest_window(icmp, target, down, end, check, timeline, *, probes=MANAGEMENT_PROBES):
    ident = probes[target]
    packets = icmp[f"{target}-tap0"]
    requests = sorted((stamps[0], seq) for (probe, kind, seq), stamps in packets.items()
                      if probe == ident and kind == 8 and down <= stamps[0] < end)
    lost, windows = [], []
    for stamp, seq in requests:
        replies = packets.get((ident, 0, seq), [])
        if replies and replies[0] - stamp <= 500_000_000:
            if len(lost) >= 3:
                windows.append((lost[0], lost[-1], replies[0]))
            lost = []
        else:
            lost.append(stamp)
    check("error", len(windows) == 1, f"{target} management TAP shows one closed guest absence")
    if not windows:
        raise ValueError(f"{target} missing independent management-plane guest loss/return bounds")
    first_miss, last_miss, returned = windows[0]
    for stamp, label in ((first_miss, "first missed management request"),
                         (last_miss, "last missed management request"),
                         (returned, "first management response")):
        timeline.append((stamp, f"guest-{target}", label))
    return first_miss, last_miss, returned


def peer_observations(path, target, start, first_miss, last_miss, end, check, timeline, *, direct=False):
    survivor = "p2" if target == "p1" else "p1"
    previous = None
    transitions = []
    absent_roles = set()
    for sample in load_jsonl(path / f"state-{survivor}.jsonl"):
        if "raw" not in sample or sample["done_ns"] < start:
            continue
        bridge, _ = router_state(sample["raw"])
        value = bridge.get("mlag-state"), bridge.get("mlag-active-role"), bridge.get("root-bridge-id")
        if previous is None or value != previous[0]:
            transition = {"mlag_state": value[0], "active_role": value[1], "root_id": value[2],
                          "before_s": seconds((previous[1] if previous else sample["started_ns"]) - start),
                          "by_s": seconds(sample["done_ns"] - start)}
            if sample["done_ns"] <= end:
                transitions.append(transition)
                timeline.append((sample["done_ns"], f"mlag-{survivor}", json.dumps(transition, sort_keys=True)))
        if first_miss <= sample["started_ns"] and sample["done_ns"] <= last_miss:
            absent_roles.add(value)
        previous = (value, sample["started_ns"])

    check("error", bool(absent_roles), f"{survivor} supplied MLAG and root state while {target} was absent")
    endpoints = (("p2", "eth1"), ("witness", "eth1"), ("c2", "eth1")) if target == "p1" else (
        ("p1", "eth1"), ("witness", "eth2"), ("c2", "eth2"))
    if direct:
        endpoints = tuple(("c1" if node == "witness" else node, port) for node, port in endpoints)
    endpoints = (*endpoints, *((target, port) for port in ("tap1", "tap2", "tap3")))
    observations = {f"{node}:{port}": set() for node, port in endpoints}
    for sample in load_jsonl(path / "state-host.jsonl"):
        if ("raw" not in sample or sample["started_ns"] < first_miss or sample["done_ns"] > last_miss):
            continue
        for node, port in endpoints:
            flags = sample["raw"]["links"].get(node, {}).get(port)
            if flags is not None:
                observations[f"{node}:{port}"].add("LOWER_UP" in flags)
    check("error", all(observations.values()), "Observed carrier independently at the surviving ends and CHR TAPs")
    guest_carrier = {}
    router_ports = [(survivor, "ether2")]
    if not direct:
        router_ports.append(("witness", "ether2" if target == "p1" else "ether3"))
    for node, port in router_ports:
        observations_during_absence = {
            summarize_router(sample["raw"])["carrier"].get(port)
            for sample in load_jsonl(path / f"state-{node}.jsonl")
            if "raw" in sample and first_miss <= sample["started_ns"] and sample["done_ns"] <= last_miss
        }
        guest_carrier[f"{node}:{port}"] = sorted(observations_during_absence - {None})
    check("error", all(guest_carrier.values()), "Recorded RouterOS carrier at surviving linked guest ports")
    return {"survivor": survivor, "mlag_transitions": transitions,
            "while_absent": [{"mlag_state": state, "active_role": role, "root_id": root}
                             for state, role, root in sorted(absent_roles, key=repr)],
            "linux_carrier_while_absent": {port: sorted(values) for port, values in observations.items()},
            "routeros_carrier_while_absent": guest_carrier}


def pause_case(name):
    """The sender pause rule covers the reboot and power-loss cases only."""
    return "reboot" in name or "power-loss" in name


def bypass_kept_pace(flows, bypass=(301, 303)):
    """Both bypass streams exist and kept every send gap at or below 450 ms."""
    return all(ident in flows and not flows[ident]["send_pauses"] for ident in bypass)


def sender_pause_rule(name, flows, definitions, down, end, *, bypass=(301, 303)):
    """Decide per stream whether a send gap above 450 ms is fault outage rather than a broken sender.

    The rule applies only in reboot and power-loss cases, to a stream sent through an LACP bond, when every
    gap of that stream lies inside the fault or return phase, both bypass streams kept every gap at or below
    450 ms, the stream's baseline is clean and good sends bracket each gap. Times are seconds from the
    baseline start. The result is stored on each flow as ``sender_pause``.
    """
    fault_case = pause_case(name)
    bypass_steady = bypass_kept_pace(flows, bypass)
    for ident, flow in flows.items():
        pauses = flow["send_pauses"]
        longest = max(pauses, key=lambda pause: pause["gap_s"], default=None)
        bonded = definitions[ident][0].endswith("-bond0")
        applied = bool(
            pauses and fault_case and bonded and ident not in bypass and bypass_steady
            and flow["baseline_good"] >= 30 and not flow.get("baseline_missed")
            and all(down <= pause["from_s"] and pause["to_s"] <= end
                    and pause["last_good_s"] is not None and pause["first_good_s"] is not None for pause in pauses))
        flow["sender_pause"] = {"longest_send_gap_s": flow["max_send_interval_s"],
                                "longest_pause": longest, "rule_applied": applied}
    return {ident: flow["sender_pause"]["rule_applied"] for ident, flow in flows.items()}


def cadence_ok(flow):
    """The 450 ms send cadence held, or a bonded sender paused only as part of the fault."""
    return flow["max_send_interval_s"] <= 0.45 or flow.get("sender_pause", {}).get("rule_applied", False)


def cadence_text(flow):
    pause = flow.get("sender_pause", {})
    if flow["max_send_interval_s"] > 0.45 and pause.get("rule_applied"):
        return (f"; sender on the LACP bond paused {flow['max_send_interval_s']:.3f} s during the fault, "
                f"bypass streams kept their pace, the pause counts as outage")
    return ""


def graded_gaps(flow):
    """Loss gaps to grade, with each sender pause under the rule merged into one outage.

    The outage spans from the last good send before the pause to the first good send after it.
    """
    gaps = [gap for gap in flow["gaps"] if gap.get("misses")]
    if not flow.get("sender_pause", {}).get("rule_applied"):
        return gaps
    for pause in flow["send_pauses"]:
        low, high = pause["last_good_s"], pause["first_good_s"]
        absorbed = [gap for gap in gaps if low <= gap["first_miss_s"] and gap["last_miss_s"] <= high]
        gaps = [gap for gap in gaps if gap not in absorbed]
        stable = max((gap["stable_window_end_s"] for gap in absorbed if gap["stable_window_end_s"] is not None),
                     default=None)
        gaps.append({"first_seq": pause["last_good_seq"], "last_seq": pause["first_good_seq"],
                     "first_miss_s": low, "last_miss_s": high, "previous_good_s": low, "first_good_s": high,
                     "stable_window_end_s": stable, "sender_pause_s": pause["gap_s"]})
    return sorted(gaps, key=lambda gap: gap["first_miss_s"])


def check_reboot_flows(spec, flows, icmp, start, down, first_miss, last_miss, returned, end, check, *,
                       definitions=ROOT_FLOWS):
    for ident, flow in flows.items():
        if ident in spec.control_flows:
            check("error", not flow["gaps"], f"{ident} independent bypass stayed clean")
            continue
        if ident not in spec.graded_flows:
            raise ValueError(f"{spec.id} grades neither as service nor control flow: {ident}")
        gap_phases = {"withdrawal": [], "restoration": []}
        for gap in graded_gaps(flow):
            stable = gap["stable_window_end_s"]
            gap["stable_before_target_return"] = stable is not None and stable <= last_miss
            for phase, (sure_start, sure_end), (may_start, may_end) in (
                ("withdrawal", (down, last_miss), (down, returned)),
                ("restoration", (returned, end), (last_miss, end)),
            ):
                first, last = gap["first_miss_s"], gap["last_miss_s"]
                if last < may_start or first > may_end:
                    continue
                prev = gap["previous_good_s"]
                nxt = gap["first_good_s"]
                lower = max(0, min(sure_end, last) - max(sure_start, first))
                upper = max(0, min(may_end, nxt) - max(may_start, prev)) if prev is not None and nxt is not None else None
                gap_phases[phase].append({"first_seq": gap["first_seq"], "last_seq": gap["last_seq"],
                                          "lower_s": round(lower, 6),
                                          "upper_s": round(upper, 6) if upper is not None else None}
                                         | ({"sender_pause_s": gap["sender_pause_s"]} if "sender_pause_s" in gap else {}))
                limit = spec.limit(phase)
                if lower > limit:
                    check("fail", False, f"{ident} {phase} loss ≥ {lower:.3f} s exceeds {limit:g} s", phase)
                elif upper is None or upper > limit:
                    check("inconclusive", False, f"{ident} {phase} loss overlaps the {limit:g} s threshold", phase)
        flow["phase_gaps_s"] = gap_phases
        source, dest = definitions[ident][:2]
        sent, received = icmp[source], icmp[dest]
        good_while_absent = {
            seq for (probe, kind, seq), stamps in sent.items()
            if probe == ident and kind == 8 and first_miss <= seconds(stamps[0] - start) <= last_miss
            and (ident, 8, seq) in received and (ident, 0, seq) in received and (ident, 0, seq) in sent
            and 0 <= sent[(ident, 0, seq)][0] - stamps[0] <= 500_000_000
            and seconds(sent[(ident, 0, seq)][0] - start) <= last_miss
        }
        flow["good_while_target_absent"] = len(good_while_absent)
        flow["stable_while_target_absent"] = any(
            all(n in good_while_absent for n in range(seq, seq + 10)) for seq in good_while_absent
        )


def check_power_loss(marks, start, target, check):
    """Confirm the emulated power loss: carrier lost and back on every link, a paused guest, a fresh boot."""
    missing = [name for name in POWER_MARKS if name not in marks]
    check("error", not missing, "All power-loss marks recorded")
    if missing:
        return None
    check("error", all(marks[name]["target"] == target for name in POWER_MARKS), f"Every power-loss mark names {target}")
    off, on, boot = marks["power_off_observed"], marks["power_on_observed"], marks["guest_boot_observed"]
    for event, change, state in ((off, "lost", "paused"), (on, "regained", "running")):
        bound = event["max_latency_s"]
        check("error", not event["missing"] and bound is not None and bound <= 1.0,
              f"Every data link of {target} and its neighbours {change} carrier within 1 s")
        check("error", (event["qemu_status"] or {}).get("status") == state, f"QEMU reported {target} {state}")
    hold = seconds(marks["power_on_start"]["mono_ns"] - marks["power_off_applied"]["mono_ns"])
    check("error", hold >= POWER_OFF_HOLD_S, f"{target} stayed off for at least {POWER_OFF_HOLD_S} s")
    check("error", boot["uptime_ns"] < boot["prior_uptime_ns"]
          and boot["query_start_ns"] >= marks["power_on_start"]["epoch_ns"], f"{target} guest uptime reset after power on")

    def at(stamp):
        return seconds(stamp - start)

    cut, restore = marks["power_off_applied"], marks["power_on_applied"]
    return {
        "target": target,
        "off_start_s": at(marks["power_off_start"]["epoch_ns"]),
        "links_down_done_s": at(cut["links"]["done_ns"]),
        "qmp_stop_s": [at(cut["qmp"]["started_ns"]), at(cut["qmp"]["done_ns"])],
        "neighbour_nics_down_s": {nic: at(reply["done_ns"]) for nic, reply in cut["neighbour_qmp"].items()},
        "off_applied_s": at(cut["epoch_ns"]),
        "off_confirmed_latency_s": off["max_latency_s"],
        "hold_s": hold,
        "on_start_s": at(marks["power_on_start"]["epoch_ns"]),
        "qmp_reset_s": at(restore["qmp"]["system_reset"]["done_ns"]),
        "qmp_cont_s": at(restore["qmp"]["cont"]["done_ns"]),
        "links_up_done_s": at(restore["links"]["done_ns"]),
        "on_applied_s": at(restore["epoch_ns"]),
        "on_confirmed_latency_s": on["max_latency_s"],
        "boot_observed_s": at(boot["query_end_ns"]),
        "post_boot_uptime_s": seconds(boot["uptime_ns"]),
        "neighbour_carrier_off": {"linux": off["linux_flags"], "routeros": off["routeros_status"]},
    }
