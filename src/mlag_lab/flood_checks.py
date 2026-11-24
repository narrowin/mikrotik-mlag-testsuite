"""Exactly-once delivery of the broadcast and unknown-unicast streams from traffic host 1.

What each capture point legitimately sees of one numbered flood frame:
- Traffic host 1 sends it on bond0, so it appears once on exactly one bond member (c1-eth1 or c1-eth2).
  The MLAG peers never send it back on the other member of the same MLAG bond, so a second sighting at
  the sender's members is a frame returned to its source.
- Traffic host 2 has an 802.3ad bond. It is a dual-connected MLAG bond, so it gets one copy on one member,
  and its bond0 capture shows that one copy.
- The MAC-move host has an active-backup bond on ether5 of each MLAG peer, a regular bridge port without
  mlag-id. Both MLAG peers flood to their own ether5, so each link and each CHR TAP toward the host
  carries one copy. The bond drops the copy on its backup link, so bond0 shows one copy and each bond
  member capture also shows one.
Saved Small lab ARP requests of traffic host 1 confirm this: one copy at c1-eth1 and none at c1-eth2, one at
c2-bond0, one at mobile-bond0, and one each at p1-tap4 and p2-tap4.

In the baseline every receiving capture must show exactly one copy and the sender's members exactly one
sighting. In the fault and return phases a second copy or a second sighting fails, and missing copies are
loss graded against the case's phase limit. For the MAC-move host with per-member captures, a copy on
either link counts as delivered: the check grades the MLAG peers' flooding, not the host bond's choice of
its active link.
"""

import json

from .measure import seconds, within


def flood_gaps(window, good, start, actions, timeline, label):
    """Runs of undelivered sequence numbers, with bounds taken from the send times as score_flows does."""
    seen = sorted(window)
    gaps = []
    n = seen[0] if seen else 0
    while seen and n <= seen[-1]:
        if n in good:
            n += 1
            continue
        first = n
        while n <= seen[-1] and n not in good:
            n += 1
        missing = [seq for seq in range(first, n) if seq in window]
        prev, nxt = window.get(first - 1), window.get(n)
        falls_after = window[missing[0]] if missing else prev
        edges = [window[missing[-1]]] if missing else []
        if nxt is not None:
            edges.append(nxt)
        until = max(edges, default=falls_after)
        gap = {"first_seq": first, "last_seq": n - 1, "from_s": seconds(falls_after - start),
               "missed": len(missing), "absent_at_source": n - first - len(missing),
               "lower_s": seconds(window[missing[-1]] - window[missing[0]]) if missing else 0,
               "upper_s": seconds(nxt - prev) if prev is not None and nxt is not None else None,
               "phases": [phase for phase, a, b in actions if until >= a and falls_after < b]}
        gaps.append(gap)
        timeline.append((falls_after, label, json.dumps(gap, sort_keys=True)))
    return gaps


def pause_outages(gaps, pauses, window, good, start, actions):
    """Merge each sender pause into one outage from the last delivered send before it to the first after it."""
    delivered = sorted(window[seq] for seq in good)
    for a, b in pauses:
        low = max((stamp for stamp in delivered if stamp <= a), default=None)
        high = min((stamp for stamp in delivered if stamp >= b), default=None)
        if low is None or high is None:
            continue
        gaps = [gap for gap in gaps if not seconds(low - start) <= gap["from_s"] <= seconds(high - start)]
        seqs = {stamp: seq for seq, stamp in window.items()}
        gaps.append({"first_seq": seqs[low], "last_seq": seqs[high], "from_s": seconds(low - start),
                     "missed": sum(low < window[seq] < high for seq in window), "absent_at_source": 0,
                     "lower_s": seconds(high - low), "upper_s": seconds(high - low), "sender_pause_s": seconds(b - a),
                     "phases": [phase for phase, x, y in actions if high >= x and low < y]})
    return sorted(gaps, key=lambda gap: gap["from_s"])


def score_floods(spec, icmp, start, end, actions, receivers, senders, flows, timeline, check, pause_window=None):
    single = len(spec.phases) == 1
    fault = actions[0][1]
    floods = {}
    for ident, (source, _, name) in flows.items():
        window = {seq: frames[0] for (i, kind, seq), frames in icmp[source].items()
                  if i == ident and kind == 8 and within(frames[0], start, end)}
        ordered = [start, *sorted(window.values()), end]
        flood = {"description": name, "sent": len(window),
                 "max_send_interval_s": seconds(max(b - a for a, b in zip(ordered, ordered[1:]))),
                 "baseline_exceptions": [], "sender_repeats": [], "receivers": {}}

        def phase_of(stamp):
            return next((phase for phase, a, b in actions if stamp < b), actions[-1][0])

        def copies(point, seq):
            return len(icmp[point].get((ident, 8, seq), []))

        for seq, stamp in sorted(window.items()):
            sightings = sum(copies(point, seq) for point in senders)
            at = {point: copies(point, seq) for points in receivers.values() for point in points}
            if single or stamp < fault:
                if sightings != 1 or any(count != 1 for count in at.values()):
                    flood["baseline_exceptions"].append({"seq": seq, "time_s": seconds(stamp - start),
                                                         "sender_members": sightings, "receivers": at})
            elif sightings > 1:
                flood["sender_repeats"].append({"seq": seq, "time_s": seconds(stamp - start),
                                                "phase": phase_of(stamp), "sightings": sightings})
        exceptions = flood["baseline_exceptions"]
        # Sender pause rule: a gap above 450 ms of the bonded sender inside the fault or return phase counts as
        # outage when the bypass streams kept their pace (pause_window is set) and the baseline was clean.
        pauses = [(a, b) for a, b in zip(ordered, ordered[1:]) if b - a > 450_000_000]
        applied = bool(pauses and window and pause_window and not exceptions
                       and all(pause_window[0] <= a and b <= pause_window[1] for a, b in pauses))
        flood["sender_pause"] = {"longest_send_gap_s": flood["max_send_interval_s"], "rule_applied": applied}
        check("error", window and (flood["max_send_interval_s"] <= 0.45 or applied),
              f"{ident} {name} was sent with consecutive sends within 450 ms"
              + (f"; sender on the LACP bond paused {flood['max_send_interval_s']:.3f} s during the fault, "
                 f"bypass streams kept their pace, the pause counts as outage" if applied else ""))
        check("fail", not exceptions,
              f"{ident} {name}: each receiving capture got one copy and the sender's bond members showed one "
              f"frame in the baseline" + (f", {len(exceptions)} exceptions from seq {exceptions[0]['seq']}"
                                          if exceptions else ""))
        if single:
            floods[ident] = flood
            continue
        for phase in spec.phases:
            repeats = [r["seq"] for r in flood["sender_repeats"] if r["phase"] == phase.key]
            check("fail", not repeats, f"{ident} {name}: no second sighting at the sender's bond members during "
                  f"{phase.key}" + (f", seq {repeats[:10]}" if repeats else ""), phase.key)
        for host, points in receivers.items():
            duplicates = [{"seq": seq, "time_s": seconds(stamp - start), "phase": phase_of(stamp),
                           "copies": {point: copies(point, seq) for point in points}}
                          for seq, stamp in sorted(window.items()) if stamp >= fault
                          and any(copies(point, seq) > 1 for point in points)]
            good = {seq for seq in window if any(copies(point, seq) for point in points)}
            gaps = flood_gaps(window, good, start, actions, timeline, f"flood-{ident}-{host.replace(' ', '-')}")
            if applied:
                gaps = pause_outages(gaps, pauses, window, good, start, actions)
            flood["receivers"][host] = {"captures": list(points), "delivered": len(good),
                                        "duplicates": duplicates, "gaps": gaps}
            for phase in spec.phases:
                seqs = [d["seq"] for d in duplicates if d["phase"] == phase.key]
                check("fail", not seqs, f"{ident} {name}: {host} got no second copy during {phase.key}"
                      + (f", seq {seqs[:10]}" if seqs else ""), phase.key)
            for gap in gaps:
                if not gap["phases"] and gap["from_s"] >= seconds(fault - start):
                    check("error", False, f"{ident} {name}: {host} lost copies away from the fault, "
                          f"seq {gap['first_seq']}–{gap['last_seq']}")
                for phase in gap["phases"]:
                    limit = spec.limit(phase)
                    lower, upper = gap["lower_s"], gap["upper_s"]
                    if lower > limit or limit == 0:
                        check("fail", False, f"{ident} {name}: {host} {phase} loss lasted at least {lower:.3f} s "
                              f"against {limit:.1f} s target", phase)
                    elif upper is None or upper > limit:
                        check("error", False, f"{ident} {name}: {host} {phase} loss {lower:.3f}–"
                              f"{upper if upper is not None else 'open'} s straddles {limit:.1f} s target", phase)
        floods[ident] = flood
    return floods


def check_floods(path, spec, icmp, start, end, actions, receivers, senders, flows, timeline, check, pause_window=None):
    """Grade the flood streams of a run that sent them; earlier runs record them as not available."""
    if not all((path / "probes" / f"{ident}.log").exists() for ident in flows):
        return "not available"
    return score_floods(spec, icmp, start, end, actions, receivers, senders, flows, timeline, check, pause_window)
