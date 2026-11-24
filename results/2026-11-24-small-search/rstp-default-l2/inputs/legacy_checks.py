"""Acceptance checks for calibration and the original small-lab cases."""

import re

from .cases import CALIBRATION_CUT_S
from .legacy import CLIENT_MAC
from .measure import number, seconds, within

MOVES = (("to-p2", "withdrawal", "p1-tap4", "p2-tap4"), ("to-p1", "restoration", "p2-tap4", "p1-tap4"))


def check_calibration(spec, marks, flows, result, check):
    phase = "calibration"
    hold_lo = seconds(marks["up_start"]["mono_ns"] - marks["down_applied"]["mono_ns"])
    hold_hi = seconds(marks["up_applied"]["mono_ns"] - marks["down_start"]["mono_ns"])
    result["injected_s"] = [hold_lo, hold_hi]
    (cut,) = spec.graded_flows
    gaps = flows[cut]["gaps"]
    low, high = CALIBRATION_CUT_S
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
              and "status: link-ok" in marks["silent_carrier"]["routeros_status"]
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
