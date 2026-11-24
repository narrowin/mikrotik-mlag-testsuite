"""Shared probe measurements and time arithmetic."""

import json

from .legacy import FLOWS, NS

# Longest gap between two sends of one stream that still counts as a steady sender.
SEND_GAP_LIMIT_NS = 450_000_000


def number(table, name):
    return table[name]["epoch_ns"]


def within(value, start, end):
    return start <= value < end


def seconds(value):
    return round(value / NS, 6)


def score_flows(icmp, start, end, actions, timeline, *, definitions=FLOWS, detailed=False):
    flows = {}
    for ident, (source, dest, _, name) in definitions.items():
        sent, received = icmp[source], icmp[dest]
        window = {seq: frames[0] for (i, kind, seq), frames in sent.items()
                  if i == ident and kind == 8 and within(frames[0], start, end)}
        seen = list(sorted(window))
        bad = {}
        good = set()
        duplicates = []
        capture_mismatches = []
        for seq in seen:
            outbound, reply = (ident, 8, seq), (ident, 0, seq)
            if len(sent.get(reply, [])) > 1 or len(received.get(outbound, [])) > 1:
                duplicates.append(seq)
            if reply in sent and (outbound not in received or reply not in received):
                capture_mismatches.append(seq)
            if outbound not in received:
                bad[seq] = "request absent at destination"
            elif reply not in received:
                bad[seq] = "reply absent at destination"
            elif reply not in sent:
                bad[seq] = "reply absent at source"
            elif sent[reply][0] - window[seq] > 0.5 * NS:
                bad[seq] = "late reply"
            else:
                good.add(seq)
        gaps = []
        if seen:
            n = seen[0]
            while n <= seen[-1]:
                if n in good:
                    n += 1
                    continue
                first = n
                while n <= seen[-1] and n not in good:
                    n += 1
                missing = [seq for seq in range(first, n) if seq in window]
                prev, nxt = window.get(first - 1), window.get(n)
                lo = window[missing[-1]] - window[missing[0]] if missing else 0
                hi = nxt - prev if prev is not None and nxt is not None else None
                representative = missing[0] if missing else first
                paths = {}
                for cap, data in icmp.items():
                    sightings = {str(kind): [seconds(t - start) for t in data.get((ident, kind, representative), [])]
                                 for kind in (8, 0)}
                    if any(sightings.values()):
                        paths[cap] = sightings
                falls_after = window[missing[0]] if missing else (prev if prev is not None else start)
                # An outage crossing restoration belongs to both transitions.
                edges = [window[missing[-1]]] if missing else []
                if nxt is not None:
                    edges.append(nxt)
                until = max(edges, default=end)
                phases = [phase for phase, a, b in actions if until >= a and falls_after < b]
                gap = {"first_seq": first, "last_seq": n - 1, "failed_probes": len(missing),
                       "absent_at_source": n - first - len(missing), "lower_s": seconds(lo),
                       "upper_s": seconds(hi) if hi is not None else None, "phases": phases,
                       "trace_seq": representative, "trace_s": paths,
                       "where": sorted({bad[s] for s in missing})}
                if detailed and missing:
                    stable = next((seq for seq in seen if seq >= n
                                   and all(q in good for q in range(seq, seq + 10))), None)
                    gap.update(
                        first_miss_s=seconds(window[missing[0]] - start),
                        last_miss_s=seconds(window[missing[-1]] - start),
                        previous_good_s=seconds(prev - start) if prev is not None else None,
                        first_good_s=seconds(nxt - start) if nxt is not None else None,
                        stable_delivery_s=seconds(window[stable] - start) if stable is not None else None,
                        stable_window_end_s=seconds(window[stable + 9] - start) if stable is not None else None,
                        misses={seq: {"where": bad[seq], "request": [
                            cap for cap, frames in icmp.items() if (ident, 8, seq) in frames
                        ], "reply": [
                            cap for cap, frames in icmp.items() if (ident, 0, seq) in frames
                        ]} for seq in missing},
                    )
                gaps.append(gap)
                timeline.append((falls_after, f"icmp-{ident}", json.dumps(gap, sort_keys=True)))
        ordered = [start, *sorted(window.values()), end]
        max_send_interval = max(b - a for a, b in zip(ordered, ordered[1:]))
        # Every send gap above the 450 ms cadence limit, with the good sends that bracket it.
        by_time = sorted((stamp, seq) for seq, stamp in window.items())
        bounds = [(start, None), *by_time, (end, None)]
        send_pauses = []
        for (a, before), (b, after) in zip(bounds, bounds[1:]):
            if b - a <= SEND_GAP_LIMIT_NS:
                continue
            last_good = max(((window[q], q) for q in good if window[q] <= a), default=None)
            first_good = min(((window[q], q) for q in good if window[q] >= b), default=None)
            send_pauses.append({
                "from_s": seconds(a - start), "to_s": seconds(b - start), "gap_s": seconds(b - a),
                "after_seq": before, "before_seq": after,
                "last_good_s": seconds(last_good[0] - start) if last_good else None,
                "last_good_seq": last_good[1] if last_good else None,
                "first_good_s": seconds(first_good[0] - start) if first_good else None,
                "first_good_seq": first_good[1] if first_good else None,
            })
        flows[ident] = {"description": name, "sent": len(window), "missed": len(bad),
                        "duplicates": duplicates, "gaps": gaps,
                        "capture_mismatches": capture_mismatches,
                        "max_send_interval_s": seconds(max_send_interval),
                        "send_pauses": send_pauses,
                        "baseline_good": sum(window[q] < actions[0][1] for q in good),
                        "recovery_good": sum(window[q] >= actions[-1][2] for q in good)}
        if detailed:
            flows[ident]["baseline_missed"] = sum(window[q] < actions[0][1] for q in bad)
            flows[ident]["stable_recovery"] = any(
                window[q] >= actions[-1][2] and all(seq in good for seq in range(q, q + 10))
                for q in good
            )
    return flows
