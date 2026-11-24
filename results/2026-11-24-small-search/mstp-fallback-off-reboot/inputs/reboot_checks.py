"""Bracket chassis loss, carrier and target return separately from VLAN outages."""

import json

from .evidence import load_jsonl
from .measure import seconds
from .root_evidence import summarize_router
from .root_state import router_state
from .root_topology import MANAGEMENT_PROBES, ROOT_FLOWS


def guest_window(icmp, target, down, end, check, timeline):
    ident = MANAGEMENT_PROBES[target]
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


def check_reboot_flows(spec, flows, icmp, start, down, first_miss, last_miss, returned, end, check, *,
                       definitions=ROOT_FLOWS):
    for ident, flow in flows.items():
        if ident in spec.control_flows:
            check("error", not flow["gaps"], f"{ident} independent bypass stayed clean")
            continue
        if ident not in spec.graded_flows:
            raise ValueError(f"{spec.id} grades neither as service nor control flow: {ident}")
        gap_phases = {"withdrawal": [], "restoration": []}
        for gap in flow["gaps"]:
            if not gap.get("misses"):
                continue
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
                                          "upper_s": round(upper, 6) if upper is not None else None})
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
