"""Explain the SMALL-06 intent from the saved Networka gates and the packet grader's measurements."""

from collections import defaultdict
import json
from math import isfinite

from network_toolkit import intent as networka

from .device_state import BRIDGE, DEVICES, ROUTEROS, reading, relative, replay_gate
from .evidence import load_jsonl
from .legacy import FLOOD_SENDER_MEMBERS
from .reboot_checks import cadence_ok

VERDICTS = {"pass": "match", "fail": "mismatch", "error": "unverified"}


def duration(value):
    return type(value) in (int, float) and isfinite(value) and value >= 0


def mapping(value):
    return value if isinstance(value, dict) else {}


def phase_window(phase):
    window = phase.get("window_s")
    if (isinstance(window, (list, tuple)) and len(window) == 2 and all(duration(edge) for edge in window)
            and window[0] < window[1]):
        return window
    return None


def secondary_reboot_intent(path, spec, result):
    """Build an additive report: device state from the Networka gates, traffic from the graded flows."""
    intent = spec.reboot_intent
    fault, traffic = intent.fault, intent.traffic
    rows = []
    marks = defaultdict(list)

    def record(phase, target, expected, observed, matched, evidence, **details):
        rows.append({"phase": phase, "target": target, "expected": expected, "observed": observed,
                     "verdict": {True: "match", False: "mismatch", None: "unverified"}[matched],
                     "evidence": evidence, **details})

    def event(name):
        records = marks[name]
        if len(records) == 1:
            line, fields = records[0]
            return fields, f"events.jsonl:{line} ({name})"
        return {}, f"events.jsonl ({name}: {len(records)} observations)"

    try:
        for line, fields in enumerate(load_jsonl(path / "events.jsonl"), 1):
            marks[fields["name"]].append((line, fields))
        target = json.loads((path / "attempt.json").read_text()).get("target")
    except (OSError, KeyError, ValueError, TypeError, AttributeError):
        target = None
    peers = ("p1", "p2")
    valid_target = target in peers
    for phase, folder in (("baseline", "gate-baseline"), ("restoration", "gate-restored")):
        evidence = f"{folder}/{networka.RESULTS_FILE}"
        try:
            report = replay_gate(path / folder)
        except networka.IntentError as error:
            record(phase, folder, "saved Networka intent", None, None, folder,
                   reason=relative(error.message, path / folder))
            continue
        for number, (item, found) in enumerate(report.results):
            rows.append({"phase": phase, "target": item.name, "expected": found.expected, "observed": found.observed,
                         "verdict": VERDICTS[found.verdict], "evidence": f"{evidence}#/items/{number}",
                         **({"reason": found.reason} if found.reason else {})})
        for node in peers:
            expected_role = fault.reboot_role if node == target else fault.surviving_role
            replies = reading(report.evidence, DEVICES[node], "collect_bridge", BRIDGE)
            found = networka.check_mlag(replies, ROUTEROS, BRIDGE, {"connected": True, "role": expected_role})
            record(phase, f"{node} MLAG role", {"role": expected_role if valid_target else None, "connected": True},
                   found.observed, found.verdict == "pass" if valid_target and found.verdict != "error" else None,
                   f"{folder}/{networka.EVIDENCE_FILE}#/devices/{DEVICES[node]}",
                   **({"reason": found.reason} if found.reason else {}))

    down, started_at = event("down_start")
    boot, boot_at = event("guest_boot_observed")
    prior, after = down.get("prior_uptime_ns"), boot.get("uptime_ns")
    stamps = down.get("epoch_ns"), boot.get("query_start_ns"), boot.get("epoch_ns")
    known = (valid_target and down.get("target") in peers and boot.get("target") in peers
             and all(type(value) is int and value >= 0 for value in (prior, after, *stamps))
             and boot.get("prior_uptime_ns") == prior and stamps[0] <= stamps[1] <= stamps[2])
    record("withdrawal", "observed secondary reboot", "uptime resets on the selected secondary",
           {"selected": target, "command_target": down.get("target"), "boot_target": boot.get("target"),
            "prior_uptime_ns": prior, "uptime_ns": after},
           down["target"] == boot["target"] == target and after < prior if known else None,
           f"attempt.json#/target, {started_at}, {boot_at}")

    flows = mapping(result.get("flows"))
    measured_phases = defaultdict(list)
    phase_results = result.get("phases")
    if isinstance(phase_results, list):
        for phase in phase_results:
            if isinstance(phase, dict) and phase.get("key") in ("withdrawal", "restoration"):
                measured_phases[phase["key"]].append(phase)
    phases = {key: entries[0] for key, entries in measured_phases.items() if len(entries) == 1}
    # A collector or grading error can leave partially populated results behind.
    packets_usable = result.get("status") in ("pass", "fail")
    for ident in (*spec.graded_flows, *spec.control_flows):
        flow = mapping(flows.get(ident, flows.get(str(ident))))
        evidence = f"result.json#/flows/{ident}"
        usable = (packets_usable and type(flow.get("sent")) is int and flow["sent"] >= 30
                  and duration(flow.get("max_send_interval_s")) and isinstance(flow.get("sender_pause", {}), dict)
                  and cadence_ok(flow) and flow.get("capture_mismatches") == [])
        missed, good = flow.get("baseline_missed"), flow.get("baseline_good")
        record("baseline", str(ident), "loss-free", {"delivered": good, "missed": missed},
               missed == 0 if usable and type(missed) is int and type(good) is int and good + missed >= 30 else None,
               evidence)
        if ident in spec.control_flows:
            missed = flow.get("missed")
            record("scoring window", str(ident), "loss-free bypass", missed,
                   missed == 0 if usable and type(missed) is int else None, evidence + "/missed")
            continue
        for phase in spec.phases:
            key, limit = phase.key, phase.limit_s
            gaps = mapping(flow.get("phase_gaps_s")).get(key)
            window = phase_window(phases.get(key, {}))
            match = None
            if window and isinstance(gaps, list):
                loss = mapping(mapping(phases[key].get("loss_s")).get(str(ident)))
                lower, upper = (loss.get("lower_s"), loss.get("upper_s")) if gaps else (0, 0)
                if duration(lower) and lower > limit:
                    match = False
                elif usable and duration(lower) and duration(upper) and lower <= upper <= limit:
                    match = True
            record(key, str(ident), f"outage ≤ {limit:g} s", {"window_s": window, "gaps": gaps},
                   match, evidence + f"/phase_gaps_s/{key}")
        recovered = flow.get("stable_recovery")
        record("recovery window", str(ident), f"{traffic.recovery_count_label} consecutive replies", recovered,
               recovered if usable and type(recovered) is bool and event("recovery_end")[0] else None,
               evidence + "/stable_recovery")

    floods = mapping(result.get("floods"))
    # The prune packs the captures of every failed run into proof.tar.gz, so live and replay name the same place.
    proof = "proof.tar.gz: " if result.get("status") == "fail" else ""
    sender_captures = ", ".join(f"captures/{point}.pcap" for point in FLOOD_SENDER_MEMBERS)
    for ident in traffic.no_sender_return_streams:
        flow = mapping(floods.get(ident, floods.get(str(ident))))
        repeats = flow.get("sender_repeats")
        usable = (packets_usable and type(flow.get("sent")) is int and flow["sent"] > 0
                  and duration(flow.get("max_send_interval_s")) and isinstance(flow.get("sender_pause", {}), dict)
                  and cadence_ok(flow))
        valid_repeats = [
            item for item in repeats if isinstance(item, dict) and item.get("phase") in ("withdrawal", "restoration")
            and type(item.get("seq")) is int
            and type(item.get("sightings")) is int and item["sightings"] > 1 and duration(item.get("time_s"))
        ] if isinstance(repeats, list) else []
        for phase in spec.phases:
            key = phase.key
            observed = [item for item in valid_repeats if item["phase"] == key]
            complete = isinstance(repeats, list) and len(valid_repeats) == len(repeats)
            evidence = f"result.json#/floods/{ident}/sender_repeats" if repeats is not None else "result.json#/floods"
            if observed:
                evidence += f", {proof}{sender_captures}"
            match = False if observed else True if complete and usable and phase_window(phases.get(key, {})) else None
            record(key, str(ident), "no flood frame returned to sender",
                   observed if observed or complete else None, match, evidence)

    verdicts = {row["verdict"] for row in rows}
    verdict = "mismatch" if "mismatch" in verdicts else "unverified" if "unverified" in verdicts else "match"
    return {"verdict": verdict, "assertions": rows}
