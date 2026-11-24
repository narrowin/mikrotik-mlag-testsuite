"""Write the results section of the repository README and its chart from results/index/phases.jsonl.

The README keeps everything between RESULTS_START and RESULTS_END generated; the rest is hand-written.
Suites are grouped by bridge mode and spanning-tree root placement. Variants such as lacp-strict or
mlag-lacp-fallback fold into their group. A group fails if any valid run in it failed, and passes when
none failed and every case it attempted has a valid run.
"""

import json
from datetime import date
from functools import cache
from html import escape
from pathlib import Path

from .summary import GRADED, ICONS, msti_roots, worst_text

RESULTS_START = "<!-- results:start -->"
RESULTS_END = "<!-- results:end -->"
CHART = "reboot-interruption.svg"
VALID = ("pass", "fail")

# Chart colours: light surface, dark and grey ink, hairline grid, green for pass and red for fail.
SURFACE, BORDER, INK, INK_2, MUTED, GRID = "#fcfcfb", "#e1e0d9", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
GOOD, CRITICAL = "#0ca30c", "#d03b3b"
FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'
# Failed checks that mean a frame came back to its sender or reached a host twice, not lost traffic.
LOOP_CHECKS = ("second sighting", "second copy", "reflected")
LOOP_TEXT = "frames looped back to the sender"
UNCHECKED_TEXT = "not tested for looped-back frames"


@cache
def flood_streams(result_file):
    """True when the run sent the numbered broadcast and unknown-unicast streams that show looped-back frames."""
    try:
        floods = json.loads(Path(result_file).read_text()).get("floods")
    except (OSError, ValueError):
        return False
    return isinstance(floods, dict) and any(ident in floods for ident in ("501", "502"))


def looped(rows):
    """True when a failed check in these rows is a looped-back or duplicated frame."""
    return any(any(text in str(check) for text in LOOP_CHECKS)
               for row in rows if row.get("verdict") == "fail" for check in row.get("failed_checks") or [])


def group_label(setup, run_dir):
    """Bridge mode and root placement in a few words, or None when the run did not record its setup."""
    mode = setup.get("bridge_mode")
    bridges = {node: info.get("bridge", {}) for node, info in (setup.get("devices") or {}).items()}
    if mode == "none":
        if bridges.get("witness", {}).get("protocol-mode") in ("rstp", "mstp"):
            return "STP off on the pair, RSTP on the access switch"
        return "STP off"
    if mode not in ("rstp", "mstp") or not bridges:
        return None
    root = min(bridges, key=lambda node: int(bridges[node].get("priority", "0x8000"), 16))
    where = "access switch" if root == "witness" else "MLAG pair"
    if mode == "rstp":
        return f"RSTP, {where} is root"
    if where == "access switch":
        return "MSTP, access switch is root of the default instance"
    if any(node == "witness" for node, _ in msti_roots(run_dir).values()):
        return "MSTP, access switch is root of VLAN 110 only"
    return "MSTP, MLAG pair is root"


def is_reboot(row):
    """Any MLAG peer reboot case, including the two-pair reboots of either pair; not the calibration before reboots."""
    case = row.get("case") or ""
    return "reboot" in case and "calibrat" not in case


def upper(row):
    measured = row.get("measured") or {}
    return measured.get("upper_s") if measured.get("upper_s") is not None else measured.get("lower_s")


def never_forwarded(row):
    return row["run_status"] in VALID and row["phase"] == "baseline" and row["verdict"] == "fail"


def build_groups(rows, results):
    """Group suites by lab and setup. Returns the groups and the number of suites without a recorded setup."""
    suites = {}
    for row in rows:
        if row["run"] != "runner":
            suites.setdefault((row["campaign"], row["suite"]), []).append(row)
    groups, unrecorded = {}, 0
    for (campaign, suite), suite_rows in suites.items():
        if suite.startswith("invalid-"):
            continue
        known = next((row for row in suite_rows if (row.get("setup") or {}).get("lab")), None)
        label = known and group_label(known["setup"], results / campaign / suite / known["run"])
        if not label:
            unrecorded += 1
            continue
        group = groups.setdefault((known["setup"]["lab"], label), {"rows": [], "runs": {}, "suites": 0, "dark": 0})
        group["rows"] += suite_rows
        group["suites"] += any(row["run_status"] in VALID for row in suite_rows)
        group["dark"] += any(never_forwarded(row) for row in suite_rows)
        for row in suite_rows:
            group["runs"][(campaign, suite, row["run"])] = row["run_status"]
    out = []
    for (lab, label), group in groups.items():
        valid = [row for row in group["rows"] if row["run_status"] in VALID]
        if not valid:
            continue
        statuses = list(group["runs"].values())
        failed = any(row["verdict"] == "fail" for row in valid)
        attempted = {row["case"] for row in group["rows"] if row.get("case")}
        covered = {row["case"] for row in valid if row.get("case")}
        graded = [row for row in valid if row["phase"] in GRADED and upper(row) is not None]
        pool = [row for row in graded if row["verdict"] == "fail"] if failed else graded
        if pool:
            worst = max(pool, key=upper)
            worst = (upper(worst), worst)
        else:
            dark = [row for row in valid if never_forwarded(row)]
            worst = (None, dark[0]) if dark else None
        reboots = [row for row in graded if is_reboot(row)]
        paths = lambda chosen: {row["evidence"]["path"] for row in chosen if (row.get("evidence") or {}).get("path")}
        flooded = lambda chosen: any(flood_streams(results.parent / path / "result.json") for path in paths(chosen))
        out.append({
            "lab": lab, "label": label,
            "result": "fail" if failed else "pass" if attempted <= covered else "incomplete",
            "passed": statuses.count("pass"), "failed": statuses.count("fail"),
            "invalid": len(statuses) - statuses.count("pass") - statuses.count("fail"),
            "suites": group["suites"], "dark": group["dark"], "worst": worst,
            "reboot": max(map(upper, reboots)) if reboots else None,
            "reboot_fail": any(row["verdict"] == "fail" for row in reboots),
            "loop_fail": looped(valid), "reboot_loop": looped(reboots),
            "flood": flooded(valid), "reboot_flood": flooded(reboots),
            "unchecked": False, "reboot_unchecked": False,
        })
    # Compare like with like: a setup that never ran the looped-back-frame check cannot pass against a setup
    # in the same lab that did run it. It is incomplete until it runs the same checks.
    for g in out:
        others = [o for o in out if o["lab"] == g["lab"]]
        if g["result"] == "pass" and not g["flood"] and any(o["flood"] for o in others):
            g["result"], g["unchecked"] = "incomplete", True
        # The chart compares reboots only, so it needs the same rule for the reboot runs.
        g["reboot_unchecked"] = (g["reboot"] is not None and not g["reboot_fail"] and not g["reboot_flood"]
                                 and any(o["reboot_flood"] for o in others))
    order = {"pass": 0, "incomplete": 1, "fail": 2}
    key = lambda g: (g["lab"], order[g["result"]], g["worst"][0] if g["worst"] and g["worst"][0] is not None else 99)
    return sorted(out, key=key), unrecorded


def dark_note(g):
    """Say how many suites never forwarded VLAN traffic, when only some of them did not."""
    return f"VLAN never forwarded in {g['dark']} of {g['suites']} suites" if 0 < g["dark"] < g["suites"] else ""


def chart_note(g, limit):
    """The reason under a setup's label when its bar alone would mislead."""
    if g["reboot_unchecked"]:
        return UNCHECKED_TEXT
    if g["reboot_loop"] and g["reboot"] is not None and g["reboot"] <= limit:
        return f"loss within limit; {LOOP_TEXT}"
    return dark_note(g)


def chart_svg(groups):
    """Horizontal bars: longest traffic stop during an MLAG peer reboot, per lab and setup group, against 5 s."""
    labs = sorted({g["lab"] for g in groups})
    shown = {lab: [g for g in groups if g["lab"] == lab and (g["reboot"] is not None or g["dark"])] for lab in labs}
    limit, top = 5.0, max([15.0] + [g["reboot"] for g in groups if g["reboot"] is not None])
    width, left, right, row_h, bar_h = 920, 360, 190, 34, 18
    scale = (width - left - right) / top
    x = lambda seconds: left + seconds * scale
    bars, guides, texts, y = [], [], [], 104
    value_x = width - 24
    for lab in labs:
        if not shown[lab]:
            continue
        texts.append(f'<text x="24" y="{y + 18}" font-size="14" font-weight="600" fill="{INK}">{escape(lab)}</text>')
        y += 30
        first = y
        for g in shown[lab]:
            mid = y + row_h / 2
            note = chart_note(g, limit)
            texts.append(f'<text x="{left - 12}" y="{mid + (0 if note else 4.5)}" font-size="13" fill="{INK_2}" '
                         f'text-anchor="end">{escape(g["label"])}</text>')
            if note:
                texts.append(f'<text x="{left - 12}" y="{mid + 13}" font-size="11" fill="{MUTED}" text-anchor="end">{escape(note)}</text>')
            if g["reboot"] is None:
                texts.append(f'<text x="{value_x}" y="{mid + 4.5}" font-size="13" font-weight="600" fill="{INK}" '
                             f'text-anchor="end">✗ VLAN never forwarded</text>')
            else:
                fail = g["reboot_fail"] or g["reboot"] > limit
                end = x(g["reboot"])
                r = min(4, end - left)
                colour = CRITICAL if fail else MUTED if g["reboot_unchecked"] else GOOD
                bars.append(f'<path d="M{left},{mid - bar_h / 2} H{end - r} a{r},{r} 0 0 1 {r},{r} V{mid + bar_h / 2 - r} '
                             f'a{r},{r} 0 0 1 -{r},{r} H{left} Z" fill="{colour}"/>')
                value = f'{"✗" if fail else "?" if g["reboot_unchecked"] else "✓"} {g["reboot"]:.2f} s'
                texts.append(f'<text x="{value_x}" y="{mid + 4.5}" font-size="13" font-weight="600" fill="{INK}" text-anchor="end" '
                             f'style="font-variant-numeric: tabular-nums">{value}</text>')
            y += row_h
        guides.append(f'<line x1="{x(limit)}" y1="{first - 4}" x2="{x(limit)}" y2="{y + 4}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        y += 14
    texts.append(f'<text x="{value_x}" y="98" font-size="12" fill="{MUTED}" text-anchor="end">Longest stop</text>')
    ticks = [s for s in range(0, int(top) + 1, 5)]
    grid = "".join(f'<line x1="{x(s)}" y1="104" x2="{x(s)}" y2="{y - 10}" stroke="{GRID}" stroke-width="1"/>'
                   f'<text x="{x(s)}" y="{y + 6}" font-size="12" fill="{MUTED}" text-anchor="middle" '
                   f'style="font-variant-numeric: tabular-nums">{s} s</text>' for s in ticks)
    height = y + 24
    head = (f'<text x="24" y="34" font-size="18" font-weight="700" fill="{INK}">How long traffic stops when one MLAG switch reboots</text>'
            f'<text x="24" y="58" font-size="13" fill="{INK_2}">Each bar is the longest stop in any valid run, counting both the primary '
            f'and the secondary reboot.</text>'
            f'<text x="24" y="76" font-size="13" fill="{INK_2}">The dashed line marks the 5 s limit. Red: a check failed. '
            f'Grey: not tested for looped-back frames.</text>'
            f'<text x="{x(limit) + 6}" y="98" font-size="12" fill="{INK}">limit 5 s</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'font-family=\'{FONT}\' role="img" aria-label="Traffic stop during an MLAG peer reboot per setup">'
            f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{SURFACE}" stroke="{BORDER}"/>'
            f'{grid}{"".join(bars)}{"".join(guides)}{head}{"".join(texts)}</svg>\n')


def day(value):
    return f"{value.day} {value:%B %Y}"


def runs_text(g):
    text = f"{g['passed']} passed, {g['failed']} failed"
    return text + (f", {g['invalid']} invalid or not reached" if g["invalid"] else "")


def longest_text(g):
    note = dark_note(g)
    text = f"{note}. Where it forwarded: {worst_text(g['worst'])}" if note else worst_text(g["worst"])
    worst = g["worst"]
    within = worst and worst[0] is not None and worst[1].get("limit_s") and worst[0] <= worst[1]["limit_s"]
    if g["result"] == "fail" and g["loop_fail"] and within:
        return f"Failed: {LOOP_TEXT}. Loss within limit: {text}"
    if g["unchecked"]:
        return f"{text}. {UNCHECKED_TEXT.capitalize()}"
    return text


def section(groups, unrecorded, rows, results):
    valid = [row for row in rows if row["run_status"] in VALID and (row.get("setup") or {}).get("routeros")]
    lines = [RESULTS_START,
             "<!-- Generated by `mlag-lab export` from results/index/phases.jsonl. Edit the generator, not this section. -->",
             ""]
    if valid:
        routeros = ", ".join(sorted({row["setup"]["routeros"] for row in valid}))
        images = ", ".join(sorted({row["setup"]["chr_image"].split("@")[0] for row in valid if row["setup"].get("chr_image")}))
        clab = ", ".join(sorted({row["setup"]["containerlab"] for row in valid if row["setup"].get("containerlab")}))
        days = sorted({date.fromisoformat(row["started"][:10]) for row in valid if row.get("started")})
        tested = f"Tested on RouterOS {routeros}" + (f" (`{images}`)" if images else "") + (f" with Containerlab {clab}" if clab else "")
        if days:
            tested += f" on {day(days[0])}" if len(days) == 1 else f" from {day(days[0])} to {day(days[-1])}"
        lines += [f"{tested}. `mlag-lab export` generates this section from the [results index]({results.name}/index/schema.md).", ""]
    if not groups:
        return "\n".join(lines + ["No valid runs yet.", "", RESULTS_END])
    lines += [f"[![How long traffic stops when one MLAG switch reboots]({results.name}/index/{CHART})]({results.name}/README.md)", ""]
    for lab in sorted({g["lab"] for g in groups}):
        anchor = lab.lower().replace(" ", "-")
        lines += [f"### {lab}", "", "| Result | Setup | Runs | Longest interruption |", "| --- | --- | --- | --- |"]
        for g in (g for g in groups if g["lab"] == lab):
            lines.append(f"| {ICONS[g['result']]} | {g['label']} | {runs_text(g)} | {longest_text(g)} |")
        lines += ["", f"The [{lab} results]({results.name}/README.md#{anchor}) list every setup variant and run.", ""]
    lines.append("A setup fails if any valid run failed. It passes when none failed and every case it attempted has a valid run. "
                 "Otherwise it is incomplete. Invalid runs, such as runs with a paused probe sender, count as neither pass nor fail. "
                 "A setup that was never tested for looped-back frames, while another setup in the same lab was, is incomplete: "
                 "its green result would only mean the check did not run.")
    lines += ["", ("Suites marked invalid" + (f" and {unrecorded} suites that did not record their bridge mode" if unrecorded else "")
                   + f" appear only in the [results overview]({results.name}/README.md). It also gives the recommendation and "
                   "the limit for each case."), "", RESULTS_END]
    return "\n".join(lines)


def write_overview(results):
    """Write <results>/index/reboot-interruption.svg and refresh the results section of the README next to <results>."""
    results = Path(results).resolve()
    rows = [json.loads(line) for line in (results / "index" / "phases.jsonl").read_text().splitlines() if line]
    groups, unrecorded = build_groups(rows, results)
    (results / "index" / CHART).write_text(chart_svg(groups))
    readme = results.parent / "README.md"
    if not readme.exists():
        return groups
    text = readme.read_text()
    start = text.find(RESULTS_START)
    if start == -1:
        return groups
    end = text.find(RESULTS_END, start)
    if end == -1:
        raise ValueError(f"{readme}: {RESULTS_START} has no {RESULTS_END} after it")
    readme.write_text(text[:start] + section(groups, unrecorded, rows, results) + text[end + len(RESULTS_END):])
    return groups
