"""Count how often each kind of failed check showed across the saved runs.

Every count a write-up quotes about a fault, such as "in 3 of 3 runs" or a loss range over several runs,
comes from here and not from hand counting. A fault counts once per run, and loss once per run and phase,
out of the valid runs of the same lab, setup and case that ran that check. Invalid suites and runs that
stopped before grading are left out, as in the README tables.

`mlag-lab export` writes the counts per setup variant to results/index/faults.tsv and per setup group to
the faults section of results/README.md.
"""

import csv
import json
from functools import cache
from pathlib import Path

from .overview import VALID, flood_streams, group_label
from .summary import bounds, describe

KINDS = {
    "loss": "Loss over the limit",
    "baseline": "Baseline traffic lost before any fault",
    "reflected": "Unicast request sent back to its sender",
    "flood": "Flood frame back at its sender or twice at a host",
    "root": "STP root moved to another bridge during the fault",
    "move": "MAC move check failed",
    "other": "Other failed check",
}
# Rows with no fault are kept only for the looped-frame checks of cases that apply a fault, where a zero is itself
# a finding.
ZERO_KEPT = ("reflected", "flood")
FAULT_PHASES = ("withdrawal", "restoration")
COLUMNS = ("lab", "setup", "case", "fault", "phase", "runs_with_fault", "runs_checked",
           "loss_lower_s", "loss_upper_s", "runs")


def kind(detail, phase):
    """The kind of a failed check, from the wording the evaluators give it."""
    if "reflected unicast" in detail:
        return "reflected"
    if "second sighting" in detail or "second copy" in detail:
        return "flood"
    if phase == "baseline" and "baseline loss-free" in detail:
        return "baseline"
    if " kept root " in detail:
        return "root"
    if " move" in detail or "GARP" in detail:
        return "move"
    # Current evaluators say "exceeds"; older runs say "against ... target".
    if " loss " in detail and (" exceeds " in detail or " target" in detail):
        return "loss"
    return "other"


@cache
def ran_reflected_check(result_file):
    """True when the run graded unicast requests that come back to their sender."""
    try:
        checks = json.loads(Path(result_file).read_text()).get("checks") or []
    except (OSError, ValueError):
        return False
    return any("reflected unicast" in check.get("detail", "") for check in checks)


def runs(rows, results):
    """One record per valid run with its lab, setup labels, case title and graded phase rows."""
    found = {}
    for row in rows:
        if row["run"] == "runner" or row["suite"].startswith("invalid-") or row["run_status"] not in VALID:
            continue
        path = (row.get("evidence") or {}).get("path")
        if not path or not (row.get("setup") or {}).get("lab"):
            continue
        run = found.setdefault(path, {"path": path, "rows": []})
        run["rows"].append(row)
    for run in found.values():
        first = run["rows"][0]
        run_dir = results.parent / run["path"]
        run["lab"] = first["setup"]["lab"]
        run["group"] = group_label(first["setup"], run_dir) or describe(first["setup"], run_dir)
        run["setup"] = describe(first["setup"], run_dir)
        run["case"] = (first.get("case_title") or first.get("case") or "").split(" · ")[0]
        result_file = run_dir / "result.json"
        run["checked"] = {"reflected": ran_reflected_check(result_file), "flood": flood_streams(result_file)}
    return sorted(found.values(), key=lambda run: run["path"])


def facts(run):
    """(kind, phase name) pairs this run was checked for, each with whether it failed and the worst loss."""
    out = {}
    for row in run["rows"]:
        if row.get("phase") is None:
            continue
        failed = {kind(detail, row["phase"]) for detail in row.get("failed_checks") or []} if row["verdict"] == "fail" else set()
        if row["phase"] == "baseline":
            out.setdefault(("baseline", ""), [False, None])[0] |= "baseline" in failed
        elif row.get("limit_s") is not None:
            entry = out.setdefault(("loss", row["phase_name"]), [False, None])
            if "loss" in failed:
                entry[0], entry[1] = True, row.get("measured")
        for name in ("reflected", "flood"):
            if run["checked"][name]:
                out.setdefault((name, ""), [False, None])[0] |= name in failed
        for name in ("root", "move", "other"):
            if name in failed:
                out.setdefault((name, ""), [False, None])[0] = True
    return out


def count(rows, results, level):
    """Fault rows grouped by lab, setup (level "group" or "setup") and case, sorted for stable output."""
    table = {}
    for run in runs(rows, results):
        for (name, phase), (failed, measured) in facts(run).items():
            key = (run["lab"], run[level], run["case"], name, phase)
            entry = table.setdefault(key, {"checked": 0, "failed": [], "lower": None, "upper": None, "open": False,
                                           "faulted": False})
            entry["checked"] += 1
            entry["faulted"] |= any(row.get("phase") in FAULT_PHASES for row in run["rows"])
            if not failed:
                continue
            entry["failed"].append(run["path"])
            if measured and measured.get("lower_s") is not None:
                lower, upper = measured["lower_s"], measured.get("upper_s")
                entry["lower"] = lower if entry["lower"] is None else min(entry["lower"], lower)
                if upper is None:
                    entry["open"] = True
                else:
                    entry["upper"] = upper if entry["upper"] is None else max(entry["upper"], upper)
    out = []
    for (lab, setup, case, name, phase), entry in sorted(table.items()):
        if not entry["failed"] and not (name in ZERO_KEPT and entry["faulted"]):
            continue
        out.append({"lab": lab, "setup": setup, "case": case, "fault": KINDS[name], "phase": phase,
                    "runs_with_fault": len(entry["failed"]), "runs_checked": entry["checked"],
                    "loss_lower_s": entry["lower"], "loss_upper_s": None if entry["open"] else entry["upper"],
                    "runs": entry["failed"]})
    return out


def write_tsv(rows, results, path):
    """Write the per-setup fault counts as a tab-separated file."""
    with Path(path).open("w", newline="") as file:
        writer = csv.DictWriter(file, COLUMNS, delimiter="\t")
        writer.writeheader()
        for row in count(rows, results, "setup"):
            writer.writerow({**row, "loss_lower_s": "" if row["loss_lower_s"] is None else f"{row['loss_lower_s']:.3f}",
                             "loss_upper_s": "" if row["loss_upper_s"] is None else f"{row['loss_upper_s']:.3f}",
                             "runs": " ".join(row["runs"])})


def loss_text(row):
    if row["loss_lower_s"] is None:
        return ""
    return bounds({"lower_s": row["loss_lower_s"], "upper_s": row["loss_upper_s"]})


def section(rows, results):
    """Markdown lines for results/README.md: fault counts per lab and setup group, with links to each run."""
    lines = ["## Faults across runs", "",
             "How often each kind of failed check showed, out of the valid runs of the same lab, setup group and case "
             "that ran that check. Loss counts once per run and phase, and its range runs from the shortest lower bound "
             "to the longest upper bound of the worst stream in the runs with the fault. Zero rows are listed only for "
             "the looped-frame checks of cases that apply a fault. `results/index/faults.tsv` splits these rows by "
             "setup variant. Quote these counts, not hand counts.", ""]
    table = count(rows, results, "group")
    for lab in sorted({row["lab"] for row in table}):
        lines += [f"### {lab} faults", "", "| Fault | Setup | Case | Runs with the fault | Loss | Runs |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for row in (row for row in table if row["lab"] == lab):
            fault = row["fault"] + (f", {row['phase']}" if row["phase"] else "")
            # Evidence paths are relative to the repository; this page sits in results/.
            links = " ".join(f"[{n}]({path.removeprefix(results.name + '/')})" for n, path in enumerate(row["runs"], 1))
            lines.append(f"| {fault} | {row['setup']} | {row['case']} | {row['runs_with_fault']} of "
                         f"{row['runs_checked']} | {loss_text(row) or '—'} | {links or '—'} |")
        lines.append("")
    return lines
