"""Acceptance checks for calibration and the original small-lab cases."""

import re

from network_toolkit.platforms.mikrotik_routeros import intent as ros

from .cases import AGEING_JSON, FLAP_CYCLES, MAC_AGE_DEFAULT, MAC_AGE_TIME
from .device_state import BRIDGE, host as host_port, known, mlag
from .evidence import load_jsonl
from .legacy import CLIENT_MAC
from .legacy import FLOWS, MOBILE_MAC
from .measure import number, seconds, within

MOVES = (("to-p2", "withdrawal", "p1-tap4", "p2-tap4"), ("to-p1", "restoration", "p2-tap4", "p1-tap4"))
CLIENT2_MAC = "02:00:00:11:00:12"
# mac-age-relearn: where each stream to the MAC-move host shows up when both peers flood it to the other traffic
# host, and the host's own frames at the CHR TAPs that prove it sends again.
RELEARN_FLOODS = {101: ("c2-bond0",), 102: ("c1-eth1", "c1-eth2")}
HOST_FRAMES = ((201, 8), (202, 8), (101, 0), (102, 0))
HOST_TAPS = ("p1-tap4", "p2-tap4")
# A frame already on the wire when the filter went in may reach a TAP just after the mark.
FILTER_SETTLE_NS = 50_000_000
FLAP_HOSTS = {"client 2": CLIENT2_MAC, "MAC-move host": MOBILE_MAC}


def ageing_readback(readback, value):
    """Networka's ageing-time check per MLAG peer on the saved bridge prints; RouterOS JSON reads 10s as 00:00:10."""
    return {peer: ros.check_property(replies, "/interface/bridge", {"name": BRIDGE}, "ageing-time", AGEING_JSON[value])
            for peer, replies in readback.items()}


def check_calibration(spec, marks, flows, result, check):
    phase = "calibration"
    hold_lo = seconds(marks["up_start"]["mono_ns"] - marks["down_applied"]["mono_ns"])
    hold_hi = seconds(marks["up_applied"]["mono_ns"] - marks["down_start"]["mono_ns"])
    result["injected_s"] = [hold_lo, hold_hi]
    (cut,) = spec.graded_flows
    gaps = flows[cut]["gaps"]
    low, high = spec.grading_limits.calibration_cut_s
    check("error", len(gaps) == 1 and gaps[0]["lower_s"] <= hold_lo
          and gaps[0]["upper_s"] is not None and gaps[0]["upper_s"] >= hold_hi
          and low <= hold_lo <= hold_hi <= high, "Measured one-way gap encloses the two-second injection", phase)
    check("error", bool(gaps) and all(gap["absent_at_source"] == 0 for gap in gaps),
          "Source emitted all numbered calibration requests", phase)
    check("error", all(not flows[ident]["gaps"] for ident in spec.control_flows),
          "Reverse bypass and VLAN flows were unaffected by calibration", phase)


def check_mobile_move(spec, packets, down, up, end, flows, result, check):
    garps, mobile_unicast = packets.garps, packets.mobile_unicast
    windows = {"withdrawal": (down, up), "restoration": (up, end)}
    for label, phase, old, new in MOVES:
        a, b = windows[phase]
        announcements = [t for t in garps[new] if within(t, a, b)]
        check("error", bool(announcements), f"{label} gratuitous ARP arrived at the new TAP", phase)
        if announcements:
            old_count = sum(within(t, announcements[0], b) for t in mobile_unicast[old])
            result.setdefault("moves", {})[label] = {"old_port_unicast_after_garp": old_count}
            check("fail", old_count == 0, f"{label} no unicast after GARP on the old TAP", phase)
        lost = [ident for ident in (*spec.graded_flows, *spec.control_flows)
                if any(phase in gap["phases"] for gap in flows[ident]["gaps"])]
        check("fail", not lost, f"No loss during the {label} move" + (f", lost on {lost}" if lost else ""), phase)


def check_member(spec, name, marks, packets, link_events, start, down, up, end, flows, result, check):
    client_icmp, lpdus = packets.client_icmp, packets.lpdus
    for phase in ("withdrawal", "restoration"):
        lost = [ident for ident in spec.control_flows
                if any(phase in gap["phases"] for gap in flows[ident]["gaps"])]
        check("fail", not lost, f"Client 2 and both bypass directions stay up during {phase}"
              + (f", lost on {lost}" if lost else ""), phase)
    if name == "carrier":
        for event_name, phase in (("down", "withdrawal"), ("up", "restoration")):
            event = marks[f"{event_name}_observed"]
            bound = event["max_latency_s"]
            result[f"{event_name}_observation_bound_s"] = bound
            check("error", event["confirmed"] == ["guest", "linux"] and bound <= 0.5,
                  f"{event_name} observed at both drivers within 0.5 s of actuation", phase)
        old_count = sum(within(t, number(marks, "down_observed"), up) for t in client_icmp["p1-tap2"])
        result["withdrawn_tap_unicast_probes"] = old_count
        check("fail", old_count == 0, "No probes to client 1 on the withdrawn CHR TAP", "withdrawal")
    else:
        before = [t for t, actor, _ in lpdus["p1-tap2"] if actor == CLIENT_MAC and within(t, start, down)]
        during = [t for t, actor, _ in lpdus["p1-tap2"] if actor == CLIENT_MAC
                  and within(t, number(marks, "down_applied"), up)]
        after = [t for t, actor, _ in lpdus["p1-tap2"] if actor == CLIENT_MAC
                 and within(t, number(marks, "up_applied"), end)]
        counter = re.search(r"(\d+) pkt \(dropped (\d+)", marks["up_start"]["counters"])
        check("error", before and not during and after and counter and int(counter[2]) > 0,
              "LACP observed before and after; suppressed during the hold with filter drops recorded")
        check("error", "LOWER_UP" in marks["silent_carrier"]["flags"]
              and known(ros.interface_up, marks["silent_carrier"]["routeros_replies"], "ether3") is True
              and all("LOWER_UP" in flags for stamp, flags in link_events["c1"] if within(stamp, down, up)),
              "Client carrier stayed up during silent LACP", "withdrawal")
        observed_states = [(stamp, state) for stamp, actor, state in lpdus["p1-tap2"]
                           if actor != CLIENT_MAC and within(stamp, down, up)]
        expired = next((stamp for stamp, state in observed_states if state & 0x80), None)
        defaulted = next((stamp for stamp, state in observed_states if state & 0x40), None)
        result["silent_lacp"] = {
            "suppressed_frames": int(counter[2]) if counter else None,
            "peer_expired_s": seconds(expired - down) if expired is not None else None,
            "peer_defaulted_s": seconds(defaulted - down) if defaulted is not None else None,
            "old_tap_probes_after_default": (sum(within(t, defaulted, up) for t in client_icmp["p1-tap2"])
                                             if defaulted is not None else None),
        }
        check("fail", expired is not None, "CHR advertised the expired LACP actor state during suppression",
              "withdrawal")
    for ident in spec.graded_flows:
        for gap in flows[ident]["gaps"]:
            for phase in gap["phases"]:
                limit = spec.limit(phase)
                lower, upper = gap["lower_s"], gap["upper_s"]
                if lower > limit:
                    check("fail", False, f"{ident} {phase} loss lasted at least {lower:.3f} s "
                          f"against {limit:.1f} s target", phase)
                elif upper is not None and upper > limit:
                    check("error", False, f"{ident} {phase} loss {lower:.3f}–{upper:.3f} s "
                          f"straddles {limit:.1f} s target", phase)


def check_peer_link(spec, path, marks, start, down, up, end, flows, result, check):
    """Peer link cut at both MLAG peers: both ends confirmed, the peers lose and regain ICCP, service within limits."""
    for event_name, phase, state in (("down", "withdrawal", "no-link"), ("up", "restoration", "link-ok")):
        event = marks[f"{event_name}_observed"]
        result[f"{event_name}_observation_bound_s"] = event["max_latency_s"]
        check("error", event["confirmed"] == ["p1-guest", "p1-linux", "p2-guest", "p2-linux"]
              and event["max_latency_s"] is not None and event["max_latency_s"] <= 2,
              f"Peer link {event_name} at both ends of both MLAG peers within 2 s ({state})", phase)
    windows = {"withdrawal": (number(marks, "down_observed"), up), "restoration": (number(marks, "up_observed"), end)}
    states = {}
    for peer in ("p1", "p2"):
        samples = [(s["started_ns"], state["state"]) for s in load_jsonl(path / f"state-{peer}.jsonl")
                   if (state := known(mlag, s))]
        states[peer] = {phase: sorted({state for stamp, state in samples if within(stamp, *windows[phase])})
                        for phase in windows}
        states[peer]["final"] = samples[-1][1] if samples else None
        check("fail", states[peer]["final"] == "connected", f"{peer} mlag-state connected again after the return",
              "restoration")
    result["mlag_state"] = states
    for phase in ("withdrawal", "restoration"):
        lost = [ident for ident in spec.control_flows if any(phase in gap["phases"] for gap in flows[ident]["gaps"])]
        check("error", not lost, f"Bypass streams stayed clean during {phase}" + (f", lost on {lost}" if lost else ""),
              phase)
    for ident in spec.graded_flows:
        for gap in flows[ident]["gaps"]:
            for phase in gap["phases"]:
                limit = spec.limit(phase)
                lower, upper = gap["lower_s"], gap["upper_s"]
                if lower > limit:
                    check("fail", False, f"{ident} {phase} loss lasted at least {lower:.3f} s "
                          f"against {limit:.1f} s target", phase)
                elif upper is not None and upper > limit:
                    check("error", False, f"{ident} {phase} loss {lower:.3f}–{upper:.3f} s "
                          f"straddles {limit:.1f} s target", phase)


def sends(icmp, ident, start, end):
    """Send time of each numbered request of one stream at its source capture."""
    return {seq: frames[0] for (i, kind, seq), frames in icmp[FLOWS[ident][0]].items()
            if i == ident and kind == 8 and within(frames[0], start, end)}


def gap_bounds(window, gap):
    """First and last missed send and the surrounding good sends of one gap; None where the window has none."""
    missing = [seq for seq in range(gap["first_seq"], gap["last_seq"] + 1) if seq in window]
    return (window[missing[0]] if missing else None, window[missing[-1]] if missing else None,
            window.get(gap["first_seq"] - 1), window.get(gap["last_seq"] + 1))


def host_entries(path, peer, mac, start, end):
    """Sample start times and whether the peer's bridge host table held an entry for mac, None when undecided."""
    found = []
    for sample in load_jsonl(path / f"state-{peer}.jsonl"):
        if within(sample["started_ns"], start, end):
            try:
                found.append((sample["started_ns"], host_port(sample, mac) is not None))
            except ValueError:
                found.append((sample["started_ns"], None))
    return found


def check_mac_age(spec, path, marks, packets, start, down, up, end, flows, result, check):
    """MAC-move host silent past bridge ageing: flooding is recorded; relearn and delivery after its first frame."""
    icmp = packets.icmp
    measured = result["mac_age"] = {}
    for label, value in (("bridge_ageing_set", MAC_AGE_TIME), ("bridge_ageing_restored", MAC_AGE_DEFAULT)):
        found = ageing_readback(marks.get(label, {}).get("readback") or {}, value)
        measured[label] = {peer: result.observed if result.verdict != "error" else result.reason
                           for peer, result in found.items()}
        check("error", set(found) == {"p1", "p2"} and all(result.verdict == "pass" for result in found.values()),
              f"Both MLAG peers read back ageing-time={value}: {measured[label]}")
    check("error", "neighbours_pinned" in marks and "neighbours_unpinned" in marks,
          "Neighbour entries were pinned for the silence and removed afterwards")
    counters = marks["up_start"].get("counters", {})
    dropped = {port: int(match[1]) if (match := re.search(r"\(dropped (\d+)", text)) else None
               for port, text in counters.items()}
    measured["filter_drops"] = dropped
    check("error", (dropped.get("eth1") or 0) > 0, f"The filter dropped the host's frames on its active member: {dropped}")
    frames = sorted(stamp for tap in HOST_TAPS for (ident, kind, _), stamps in icmp[tap].items()
                    if (ident, kind) in HOST_FRAMES for stamp in stamps)
    leaked = [stamp for stamp in frames if within(stamp, number(marks, "down_applied") + FILTER_SETTLE_NS, up)]
    check("error", not leaked, f"No frame from the host reached a CHR TAP while it was silent ({len(leaked)} seen)",
          "withdrawal")
    first = next((stamp for stamp in frames if stamp >= up), None)
    measured["first_host_frame_s"] = seconds(first - start) if first is not None else None
    check("error", first is not None, "A frame from the host reached a CHR TAP after the filter was removed",
          "restoration")

    tables = measured["host_table"] = {}
    for peer in ("p1", "p2"):
        samples = host_entries(path, peer, MOBILE_MAC, start, end)
        aged = next((stamp for stamp, present in samples if present is False and within(stamp, down, up)), None)
        back = next((stamp for stamp, present in samples if present and first is not None and stamp >= first), None)
        tables[peer] = {"aged_out_s": seconds(aged - start) if aged is not None else None,
                        "back_s": seconds(back - start) if back is not None else None}
        check("error", aged is not None, f"{peer} aged the host MAC out of its bridge host table while it was silent",
              "withdrawal")
    if first is None:
        return

    floods = measured["flooding"] = {}
    for ident, points in RELEARN_FLOODS.items():
        seen = sorted(stamp for point in points for (i, kind, _), stamps in icmp[point].items()
                      if i == ident and kind == 8 for stamp in stamps if within(stamp, start, end))
        silent = [stamp for stamp in seen if within(stamp, down, up)]
        after = [stamp for stamp in seen if stamp >= first]
        stopped = seconds(after[-1] - first) if after else 0.0
        floods[ident] = {"captures": list(points), "baseline_frames": sum(stamp < down for stamp in seen),
                         "silent_frames": len(silent),
                         "silent_first_s": seconds(silent[0] - start) if silent else None,
                         "silent_last_s": seconds(silent[-1] - start) if silent else None,
                         "after_first_frame": len(after), "stopped_after_first_frame_s": stopped}
        limit = spec.grading_limits.mac_relearn_s
        check("fail", stopped <= limit, f"{ident} stopped flooding to the other traffic host {stopped:.3f} s "
              f"after the host's first frame, target {limit:.1f} s", "restoration")

    resumed = measured["delivered_after_first_frame_s"] = {}
    for ident in spec.graded_flows:
        flow, window = flows[ident], sends(icmp, ident, start, end)
        silence = [gap for gap in flow["gaps"] if "withdrawal" in gap["phases"]]
        # The silence is the fault: split its outage at the filter removal, so each phase shows its own part.
        split = {"withdrawal": [], "restoration": []}
        for gap in flow["gaps"]:
            if silence and gap is silence[-1]:
                first_miss, last_miss, prev, nxt = gap_bounds(window, gap)
                both = prev is not None and nxt is not None
                parts = (("withdrawal", min(up, last_miss or up) - max(down, first_miss or up),
                          min(up, nxt) - max(down, prev) if both else None),
                         ("restoration", (last_miss or up) - max(up, first_miss or up),
                          nxt - max(up, prev) if both else None))
                for phase, lower, upper in parts:
                    if phase not in gap["phases"]:
                        continue
                    split[phase].append({"first_seq": gap["first_seq"], "last_seq": gap["last_seq"],
                                         "lower_s": seconds(max(0, lower)),
                                         "upper_s": seconds(max(0, upper)) if upper is not None else None})
            else:
                for phase in gap["phases"]:
                    split[phase].append({key: gap[key] for key in ("first_seq", "last_seq", "lower_s", "upper_s")})
        flow["phase_gaps_s"] = split
        check("error", bool(silence), f"{ident} lost the probes sent while the host was silent", "withdrawal")
        if not silence:
            continue
        good = silence[-1]["last_seq"] + 1
        reply = icmp[FLOWS[ident][0]].get((ident, 0, good)) if good in window else None
        latency = seconds(reply[0] - first) if reply else None
        resumed[ident] = latency
        limit = spec.grading_limits.mac_relearn_s
        check("fail", latency is not None and latency <= limit,
              f"{ident} delivered again {latency if latency is not None else 'never'} s after the host's first frame, "
              f"target {limit:.1f} s", "restoration")
        later = [gap["first_seq"] for gap in flow["gaps"] if gap["first_seq"] > silence[-1]["last_seq"]]
        check("fail", not later, f"{ident} lost no probe after it delivered again"
              + (f", lost from seq {later}" if later else ""), "restoration")
    for phase in ("withdrawal", "restoration"):
        lost = [ident for ident in spec.control_flows
                if any(phase in gap["phases"] for gap in flows[ident]["gaps"])]
        check("fail", not lost, f"Stream 302 and both bypass directions stay up during {phase}"
              + (f", lost on {lost}" if lost else ""), phase)


def check_member_flaps(spec, path, events, packets, start, up, recovery, end, flows, result, check):
    """Five member flaps: loss per flap within the member limit, client 2 and bypass clean, host entries kept."""
    downs = [event for event in events if event["name"] == "down_start"]
    check("error", len(downs) == FLAP_CYCLES == sum(event["name"] == "up_start" for event in events),
          f"{FLAP_CYCLES} member flaps were applied")
    if not downs:
        return
    cycle = 0
    for event in events:
        cycle += event["name"] == "down_start"
        if event["name"] in ("down_observed", "up_observed"):
            change = event["name"].split("_")[0]
            bound = event["max_latency_s"]
            check("error", event["confirmed"] == ["guest", "linux"] and bound <= 0.5,
                  f"Flap {cycle} {change} observed at both drivers within 0.5 s",
                  "restoration" if change == "up" and cycle == FLAP_CYCLES else "withdrawal")
    # Flap N runs from its down to the next flap's down; the last one runs to the recovery window.
    bounds = [event["epoch_ns"] for event in downs[1:]] + [recovery]
    flaps = result["flaps"] = [{"flap": index + 1, "down_s": seconds(event["epoch_ns"] - start), "loss_s": {}}
                               for index, event in enumerate(downs)]
    for ident in (*spec.graded_flows, *spec.control_flows):
        window = sends(packets.icmp, ident, start, end)
        for gap in flows[ident]["gaps"]:
            first_miss, _, prev, _ = gap_bounds(window, gap)
            at = first_miss if first_miss is not None else prev if prev is not None else start
            index = next((n for n, bound in enumerate(bounds) if at < bound), len(bounds) - 1)
            flaps[index]["loss_s"].setdefault(str(ident), []).append(
                {key: gap[key] for key in ("first_seq", "last_seq", "failed_probes", "lower_s", "upper_s")})
            if ident not in spec.graded_flows:
                continue
            for phase in gap["phases"]:
                limit = spec.limit(phase)
                lower, upper = gap["lower_s"], gap["upper_s"]
                if lower > limit:
                    check("fail", False, f"{ident} flap {index + 1} loss lasted at least {lower:.3f} s "
                          f"against {limit:.1f} s target", phase)
                elif upper is not None and upper > limit:
                    check("error", False, f"{ident} flap {index + 1} loss {lower:.3f}–{upper:.3f} s "
                          f"straddles {limit:.1f} s target", phase)
    for phase in ("withdrawal", "restoration"):
        lost = [ident for ident in spec.control_flows
                if any(phase in gap["phases"] for gap in flows[ident]["gaps"])]
        check("fail", not lost, f"Client 2 and both bypass directions stay up during {phase}"
              + (f", lost on {lost}" if lost else ""), phase)
    windows = {"withdrawal": (downs[0]["epoch_ns"], up), "restoration": (up, end)}
    tables = result["host_table"] = {}
    for peer in ("p1", "p2"):
        for host, mac in FLAP_HOSTS.items():
            samples = host_entries(path, peer, mac, downs[0]["epoch_ns"], end)
            missing = [stamp for stamp, present in samples if present is False]
            undecided = [stamp for stamp, present in samples if present is None]
            tables.setdefault(peer, {})[host] = {
                "mac": mac, "samples": len(samples), "missing_samples": len(missing),
                "first_missing_s": seconds(missing[0] - start) if missing else None}
            check("error", bool(samples), f"{peer} bridge host table for {host} was sampled during the flaps")
            for phase, (low, high) in windows.items():
                unknown = sum(within(stamp, low, high) for stamp in undecided)
                check("error", not unknown, f"{peer} bridge host table for {host} decided in every sample during "
                      f"{phase}; {unknown} undecided", phase)
                gone = [stamp for stamp in missing if within(stamp, low, high)]
                check("fail", not gone, f"{peer} kept the bridge host table entry for {host} ({mac}) during {phase}"
                      + (f", missing in {len(gone)} samples from {seconds(gone[0] - start)} s" if gone else ""), phase)
