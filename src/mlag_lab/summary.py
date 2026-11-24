"""Write results/README.md: one row per tested setup, generated from results/index/phases.jsonl.

Hand-written findings belong in results/notes.md, which is copied in unchanged at the top.
"""

import json
import re
from pathlib import Path

ICONS = {"pass": "✅ PASS", "fail": "❌ FAIL", "incomplete": "⚠️ INCOMPLETE", "invalid": "⚠️ INVALID"}
MODES = {"none": "STP off", "rstp": "RSTP", "mstp": "MSTP"}
GRADED = ("withdrawal", "restoration")
INDICATOR = (
    "**Indicator.** Each test keeps numbered pings running every 100 ms between the hosts, makes one change "
    "(a reboot, a cut link, a moved MAC) and measures how long traffic stops, separately while the change is in "
    "effect and after it is undone. The value shown is the longest interruption, given as lower and upper bounds "
    "from the probe spacing. A setup **passes** only when every phase of every case stays within its limit in every "
    "valid run: 3 s for an MLAG bond member or LACP change, 4 s while LACP times out, 5 s for an MLAG peer reboot "
    "or peer link loss, and no lost probe for a MAC move. Runs with broken evidence, such as a paused probe sender, "
    "count as **invalid** and are neither pass nor fail. A setup with no failure but some invalid or unreached "
    "cases is **incomplete**.",
)


def msti_roots(run_dir):
    """Owner of each MSTI from the saved configs: the device with the lowest MSTI priority."""
    best = {}
    for config in sorted(run_dir.glob("config-*.txt")):
        node = config.stem.removeprefix("config-")
        for ident, priority, vlans in re.findall(
                r"identifier=(\d+) bridge=bridge priority=(0x[0-9A-Fa-f]+) vlan-mapping=(\S+)", config.read_text()):
            if ident != "0" and (ident not in best or int(priority, 16) < best[ident][0]):
                best[ident] = (int(priority, 16), node, vlans)
    return {ident: (node, vlans) for ident, (_, node, vlans) in best.items()}


def describe(setup, run_dir):
    devices = setup.get("devices") or {}
    mode = setup.get("bridge_mode")
    parts = [MODES.get(mode, mode or "bridge mode not recorded")]
    names = {"p1": "MLAG pair", "p2": "MLAG pair", "witness": "access switch"}
    bridges = {node: info.get("bridge", {}) for node, info in devices.items()}
    if mode in ("rstp", "mstp") and bridges:
        root = min(bridges, key=lambda node: int(bridges[node].get("priority", "0x8000"), 16))
        parts.append(f"{names.get(root, root)} is root" + (" of the default instance" if mode == "mstp" else ""))
    if mode == "mstp":
        region = bridges.get("p1", {}).get("region-name", "")
        if region.strip('"'):
            parts.append(f"region {region}")
        for ident, (node, vlans) in sorted(msti_roots(run_dir).items()):
            parts.append(f"MSTI {ident} (VLAN {vlans}) root: {names.get(node, node)}")
    core = bridges.get("p1", {})
    if core.get("mlag-lacp-fallback") == "no":
        parts.append("mlag-lacp-fallback=no")
    if bridges.get("p2", {}).get("mlag-priority", "128") < core.get("mlag-priority", "128") and len(devices) == 2:
        parts.append("CHR 2 is MLAG primary")
    bonds = [bond for info in devices.values() for bond in info.get("bonds", {}).values() if bond.get("mlag-id")]
    if any(bond.get("lacp-strict") == "yes" for bond in bonds):
        parts.append("lacp-strict=yes")
    delays = {bond.get("up-delay") for bond in bonds} - {"0ms", None}
    if delays:
        parts.append(f"up-delay={', '.join(sorted(delays))}")
    return ", ".join(parts)


def bounds(measured):
    lower, upper = measured.get("lower_s"), measured.get("upper_s")
    if upper is None:
        return f"at least {lower:.2f} s"
    return f"up to {upper:.2f} s" if lower == 0 else f"{lower:.2f}–{upper:.2f} s"


def summarise(rows, results):
    suites = {}
    for row in rows:
        key = (row["campaign"], row["suite"])
        suite = suites.setdefault(key, {"runs": {}, "rows": [], "setup": row["setup"], "lab": row["setup"].get("lab")})
        suite["runs"][row["run"]] = row["run_status"]
        suite["rows"].append(row)
    table = []
    for (campaign, name), suite in suites.items():
        statuses = list(suite["runs"].values())
        valid = [s for s in statuses if s in ("pass", "fail")]
        if name.startswith("invalid-") or not valid:
            result = "invalid"
        else:
            result = "fail" if "fail" in valid else "pass" if len(valid) == len(statuses) else "incomplete"
        worst = None
        for row in suite["rows"]:
            measured = row.get("measured")
            if row["phase"] in GRADED and measured and row["run_status"] in ("pass", "fail"):
                upper = measured.get("upper_s") if measured.get("upper_s") is not None else measured.get("lower_s")
                if worst is None or upper > worst[0]:
                    worst = (upper, row)
        if result == "fail":
            failed = [row for row in suite["rows"] if row["verdict"] == "fail" and row["phase"] == "baseline"]
            if failed and (worst is None or worst[1]["verdict"] != "fail"):
                worst = (None, failed[0])
        first = next(iter(suite["runs"]))
        run_dir = results / campaign / name / first
        lab = suite["lab"] or ("Small lab" if "small" in campaign else "Medium lab" if "medium" in campaign else campaign)
        table.append({
            "lab": lab, "campaign": campaign, "suite": name, "result": result,
            "setup": describe(suite["setup"], run_dir),
            "runs": f"{statuses.count('pass')} passed, {statuses.count('fail')} failed"
                    + (f", {len(statuses) - len(valid)} invalid or not reached" if len(valid) < len(statuses) else ""),
            "worst": worst,
            "cases": {row["case"] for row in suite["rows"] if row["run_status"] in ("pass", "fail")},
            "attempted": {row["case"] for row in suite["rows"] if row.get("case")},
        })
    return table


def worst_text(worst):
    if worst is None:
        return "no loss"
    upper, row = worst
    case = (row.get("case_title") or row["case"]).split(" · ")[0]
    if row["phase"] == "baseline":
        return f"{case}: VLAN traffic did not forward"
    limit = f" (limit {row['limit_s']:g} s)" if row.get("limit_s") else ""
    return f"{case}, {row['phase_name']}: {bounds(row['measured'])}{limit}"


def setup_verdicts(table):
    """Combine suites with the same lab and setup description: a setup fails if any suite fails.

    It passes if at least one suite passed in full and every case attempted in any of its suites has a valid run,
    even when a repeat has invalid runs. Otherwise it is incomplete.
    """
    setups = {}
    for row in table:
        if row["result"] == "invalid":
            continue
        setups.setdefault((row["lab"], row["setup"]), []).append(row)
    verdicts = {}
    for key, rows in setups.items():
        results = {row["result"] for row in rows}
        attempted = set().union(*(row["attempted"] for row in rows))
        covered = set().union(*(row["cases"] for row in rows))
        verdicts[key] = "fail" if "fail" in results else "pass" if "pass" in results and attempted <= covered else "incomplete"
    return verdicts, setups


def tldr_lines(table):
    verdicts, setups = setup_verdicts(table)
    labs = sorted({lab for lab, _ in verdicts})
    lines = []
    passing = {lab: sorted(setup for (l, setup), v in verdicts.items() if l == lab and v == "pass") for lab in labs}
    covered = {key: len(set().union(*(row["cases"] for row in rows))) for key, rows in setups.items()}
    both = sorted(set.intersection(*(set(names) for names in passing.values()))) if len(labs) > 1 else []
    if both:
        lines.append(f"- ✅ **Passes every case in both labs:** {'; '.join(both)}.")
    for lab in labs:
        names = passing[lab]
        total = sum(1 for l, _ in verdicts if l == lab)
        if names:
            listed = "; ".join(f"{name} ({covered[(lab, name)]} cases)" for name in names)
            lines.append(f"- ✅ **{lab}: {len(names)} of {total} setups pass every case they ran:** {listed}.")
        failed = [(setup, row) for (l, setup), v in verdicts.items() if l == lab and v == "fail"
                  for row in setups[(l, setup)] if row["result"] == "fail"]
        graded = [(setup, row) for setup, row in failed if row["worst"] and row["worst"][0] is not None]
        if graded:
            setup, row = max(graded, key=lambda item: item[1]["worst"][0])
            count = len({setup for setup, _ in failed})
            lines.append(f"- ❌ **{lab}: {count} of {total} setups fail.** Longest interruption: {worst_text(row['worst'])}, "
                         f"with {setup}.")
        elif failed:
            lines.append(f"- ❌ **{lab}: {len({setup for setup, _ in failed})} of {total} setups fail.**")
    open_count = sum(1 for v in verdicts.values() if v == "incomplete") + sum(1 for r in table if r["result"] == "invalid")
    if open_count:
        lines.append(f"- ⚠️ **{open_count} setups or suites are incomplete or invalid** and need repeats. See the tables.")
    return lines


def write_summary(results):
    """Write results/README.md from results/index/phases.jsonl and results/notes.md."""
    results = Path(results)
    rows = [json.loads(line) for line in (results / "index" / "phases.jsonl").read_text().splitlines() if line]
    table = summarise(rows, results)
    notes = results / "notes.md"
    lines = ["# MLAG lab results", "",
             "Generated by `mlag-lab export` from `results/index/`. Do not edit this file; write findings in "
             "`results/notes.md`.", ""]
    lines += ["## TL;DR", "", *tldr_lines(table), ""]
    if notes.exists():
        # notes.md starts with its own title for standalone reading; the page already has one.
        text = notes.read_text().strip()
        lines += [text.split("\n", 1)[1].strip() if text.startswith("# ") else text, ""]
    counts = []
    for lab in sorted({row["lab"] for row in table}):
        found = [row["result"] for row in table if row["lab"] == lab]
        counts.append(f"- **{lab}:** {len(found)} setup{'s' if len(found) != 1 else ''} tested: {found.count('pass')} pass, {found.count('fail')} fail, "
                      f"{found.count('incomplete')} incomplete, {found.count('invalid')} invalid.")
    lines += ["## At a glance", "", *counts, ""]
    lines += ["## How to read the tables", "", *INDICATOR, ""]
    order = {"pass": 0, "fail": 1, "incomplete": 2, "invalid": 3}
    for lab in sorted({row["lab"] for row in table}):
        rows_lab = sorted((row for row in table if row["lab"] == lab),
                          key=lambda row: (order[row["result"]], row["campaign"], row["suite"]))
        lines += [f"## {lab}", "", "| Result | Setup | Runs | Longest interruption | Details |", "| --- | --- | --- | --- | --- |"]
        for row in rows_lab:
            link = f"[{row['suite']}]({row['campaign']}/{row['suite']}/README.md)"
            lines.append(f"| {ICONS[row['result']]} | {row['setup']} | {row['runs']} | {worst_text(row['worst'])} | {link} |")
        lines.append("")
    lines += ["## Where the data is", "",
              "- **Per setup:** each folder linked above has a generated README with every case, phase and run, plus "
              "the verdict, timeline and device configs of each run.",
              "- **All runs as data:** `results/index/phases.jsonl` (one record per run and phase) and "
              "`results/index/streams.tsv` (loss per probe stream). Field definitions: `results/index/schema.md`.",
              "- **Raw packet captures:** kept in the lab and not committed, as set by `.gitignore`.", ""]
    path = results / "README.md"
    path.write_text("\n".join(lines))
    return path
