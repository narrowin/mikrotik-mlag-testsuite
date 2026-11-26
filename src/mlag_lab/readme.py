"""Write the campaign README from saved results, so every report follows the same evidence.

The README is derived data: rerunning the writer on the same results gives the same file. Hand-written
analysis belongs in notes.md next to it, which the writer copies in unchanged.
"""

import json
import os
import re
from pathlib import Path

from .cases import CASES, case_spec
from .device_state import known, mlag


DEVICES = {
    "p1": ("CHR 1", "dc1-core-mlag1"), "p2": ("CHR 2", "dc1-core-mlag2"),
    "witness": ("Access switch", "dc1-access-switch1"),
    "q1": ("CHR 3", "dc1-access-mlag1"), "q2": ("CHR 4", "dc1-access-mlag2"),
    "r1": ("STP root 1", "dc1-stp-root1"), "r2": ("STP root 2", "dc1-stp-root2"),
    "c1": ("Client 1", "dc1-traffic-host1"), "c2": ("Client 2", "dc1-traffic-host2"),
    "mobile": ("MAC-move host", "dc1-mac-move-host"), "syslog": ("Syslog collector", "dc1-syslog-collector"),
}
MODES = {"none": "STP off", "rstp": "RSTP", "mstp": "MSTP"}
ICONS = {"pass": "✅ PASS", "fail": "❌ FAIL", "error": "⚠️ INVALID", "skipped": "⏭️ NOT RUN"}
ORDER = {"fail": 0, "error": 1, "skipped": 2, "pass": 3}
# Archived runs recorded the Small lab config as peers.rsc.
STARTUP_CONFIGS = ("small.rsc", "peers.rsc", "medium.rsc", "medium-pair-root.rsc", "medium-two-pair.rsc")


def find_suites(path):
    if (path / "suite.json").exists():
        return [path]
    return sorted(child for child in path.iterdir() if child.is_dir() and (child / "suite.json").exists())


def link(text, target, base):
    return f"[{text}]({Path(os.path.relpath(target, base)).as_posix()})"


def slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def seconds(value):
    return f"{value:.2f} s"


def loss_text(loss):
    """Loss bounds: the shortest and longest outage consistent with the 0.1 s probe spacing."""
    if loss is None:
        return "no loss"
    lower, upper = loss["lower_s"], loss["upper_s"]
    if upper is None:
        text = f"at least {seconds(lower)}"
    elif lower == 0:
        text = f"up to {seconds(upper)}"
    else:
        text = f"{lower:.2f} to {seconds(upper)}"
    if probes := loss.get("lost_probes"):
        text += f" ({probes} probe{'s' if probes != 1 else ''})"
    if loss.get("spans_both_phases"):
        text += ", one outage across both phases"
    return text


def limit_text(phase):
    if phase["key"] == "calibration":
        return "gap encloses the cut"
    if phase["limit_s"] == 0:
        return "no loss"
    return f"≤ {phase['limit_s']:g} s"


def check_line(result_file, detail):
    needle = f'"detail": {json.dumps(detail)}'
    for number, line in enumerate(result_file.read_text().splitlines(), 1):
        if needle in line:
            return number
    return None


def startup_mode(suite):
    for name in STARTUP_CONFIGS:
        config = suite / "inputs" / name
        if config.exists() and (match := re.search(r"\bprotocol-mode=(\w+)", config.read_text())):
            return f"{match[1]} (startup config)"
    return None


class Run:
    def __init__(self, suite, directory, result):
        self.suite, self.directory, self.result = suite, directory, result
        self.file = directory / "result.json"
        mode = result.get("bridge_mode") or startup_mode(suite) or "not recorded"
        base = mode.split(" ")[0]
        self.mode = MODES.get(base, base) + mode[len(base):]
        self.phases = result.get("phases", [])

    @property
    def status(self):
        return self.result["status"]


def load_runs(suites):
    runs, suite_errors = [], []
    for suite in suites:
        summary = json.loads((suite / "suite.json").read_text())
        for result in summary["results"]:
            directory = suite / result["run"]
            if (directory / "result.json").exists():
                runs.append(Run(suite, directory, json.loads((directory / "result.json").read_text())))
            elif result.get("status") in ("error", "skipped"):
                suite_errors.append((suite, result))
    return runs, suite_errors


def group_runs(runs):
    groups = {}
    for run in runs:
        key = (run.result.get("lab", "Unknown lab"), run.result.get("title", run.result.get("case")), run.mode)
        groups.setdefault(key, []).append(run)
    order = {case.title: index for index, case in enumerate(CASES)}
    return dict(sorted(groups.items(), key=lambda item: (order.get(item[0][1], len(order)), item[0][1],
                                                          item[0][2] != "STP off")))


def counted(runs):
    """Leave out an errored run that was repeated as <run>-retry; it stays evidence but counts as neither pass nor fail."""
    retried = {(run.suite, run.directory.name.removesuffix("-retry")) for run in runs
               if run.directory.name.endswith("-retry")}
    return [run for run in runs if not (run.status == "error" and (run.suite, run.directory.name) in retried)]


def group_status(runs):
    statuses = {run.status for run in counted(runs)}
    for status in ("fail", "error"):
        if status in statuses:
            return status
    return "skipped" if statuses == {"skipped"} else "pass"


def phase_summary(runs, index):
    phases = [run.phases[index] for run in counted(runs) if len(run.phases) > index]
    losses = [phase["worst_loss_s"] for phase in phases if phase["worst_loss_s"]]
    worst = None
    if losses:
        worst = {"lower_s": max(loss["lower_s"] for loss in losses),
                 "upper_s": None if any(loss["upper_s"] is None for loss in losses)
                 else max(loss["upper_s"] for loss in losses),
                 "lost_probes": max((loss.get("lost_probes") or 0 for loss in losses), default=0) or None,
                 "spans_both_phases": any(loss.get("spans_both_phases") for loss in losses)}
    verdicts = [phase["verdict"] for phase in phases]
    status = next((s for s in ("fail", "error") if s in verdicts), "skipped" if set(verdicts) == {"skipped"} else "pass")
    return phases[0] if phases else None, status, worst, verdicts


def run_label(run, runs):
    suites = sorted({r.suite for r in runs})
    position = [r for r in runs if r.suite == run.suite].index(run) + 1
    return f"run {position}" if len(suites) == 1 else f"{run.suite.name} run {position}"


def cell(run, index, base):
    if len(run.phases) <= index:
        return "—"
    phase = run.phases[index]
    text = f"{ICONS[phase['verdict']]} · {loss_text(phase['worst_loss_s'])}"
    if phase["key"] == "calibration" and (cut := run.result.get("injected_s")):
        text += f" for a {seconds(sum(cut) / 2)} cut (accepted 1.9 to 2.3 s)"
    if phase["verdict"] in ("fail", "error") and phase["failed_checks"]:
        line = check_line(run.file, phase["failed_checks"][0])
        target = f"{Path(os.path.relpath(run.file, base)).as_posix()}" + (f"#L{line}" if line else "")
        text += f" · [failed check]({target})"
    return text


def tldr_line(key, runs):
    _, title, mode = key
    status = group_status(runs)
    passed = sum(run.status == "pass" for run in runs)
    runs = counted(runs)
    head = f"**{ICONS[status]} · {title} · {mode}**"
    if status == "pass":
        worst = [w for i in range(len(runs[0].phases)) if (w := phase_summary(runs, i)[2])]
        longest = max(worst, key=lambda w: (w["upper_s"] is None, w["upper_s"] or 0, w["lower_s"]), default=None)
        if runs[0].phases and runs[0].phases[0]["key"] == "calibration":
            return f"{head} — {passed} of {len(runs)} runs passed; measured {loss_text(longest)} for a 2 s cut."
        return (f"{head} — {passed} of {len(runs)} runs passed; "
                + (f"longest loss {loss_text(longest)}." if longest else "no loss."))
    parts = []
    for i in range(max(len(run.phases) for run in runs)):
        phase, verdict, worst, verdicts = phase_summary(runs, i)
        if verdict in ("fail", "error"):
            count = sum(v == verdict for v in verdicts)
            measured = f"lost {loss_text(worst)} against {limit_text(phase)}" if verdict == "fail" else "evidence invalid"
            parts.append(f"{phase['name']}: {measured}, failed in {count} of {len(runs)} runs")
    other = sorted({detail for run in runs for detail in case_checks(run)})
    if other and not parts:
        parts.append(f"failed check: {other[0]}")
    return f"{head} — " + "; ".join(parts) + "."


def case_checks(run):
    tagged = {detail for phase in run.phases for detail in phase["failed_checks"]}
    return [c["detail"] for c in run.result.get("checks", []) if not c["ok"] and c["detail"] not in tagged]


def first_role(state):
    """The first MLAG role in a state log. Networka reads saved replies; the archived text logs in results/ show it
    as a `mlag-active-role:` line."""
    for line in state.read_text().splitlines():
        sample = json.loads(line)
        if "replies" in sample:
            if role := (known(mlag, sample) or {}).get("role"):
                return role
        elif match := re.search(r"mlag-active-role: (\w+)", sample.get("raw") or ""):
            return match[1]
    return None


def setup_rows(suites, runs, base):
    builds = [json.loads((s / "builds.json").read_text()) for s in suites if (s / "builds.json").exists()]
    rows = []
    labs = sorted({run.result.get("lab", "") for run in runs} - {""})
    rows.append(("Lab", ", ".join(labs) or "not recorded"))
    nodes = {}
    for build in builds:
        nodes.update(build.get("images", {}))
    chrs = [n for n, image in nodes.items() if "mikrotik/chr" in image.get("reference", "")]
    hosts = [n for n in nodes if n not in chrs]
    names = lambda ids: ", ".join(f"{DEVICES.get(n, (n, n))[0]} ({DEVICES.get(n, (n, n))[1]})" for n in ids)
    if nodes:
        rows.append(("Devices", f"{len(nodes)}: {len(chrs)} RouterOS CHRs — {names(chrs)}; "
                                f"{len(hosts)} Linux containers — {names(hosts)}"))
    versions = sorted({f"{m[1]} (build {b[1]})" if (b := re.search(r"build-time:\s*(.+?)\s*$", text, re.M)) else m[1]
                       for build in builds for text in build.get("routeros", {}).values()
                       if (m := re.search(r"version:\s*(\S+)", text))})
    rows.append(("RouterOS", "; ".join(versions) or "not recorded"))
    images = sorted({build["campaign_image"] for build in builds if build.get("campaign_image")})
    if images:
        rows.append(("CHR image", "; ".join(f"`{image}`" for image in images)))
    clab = sorted({m[1] for build in builds if (m := re.search(r"version:\s*(\S+)", build.get("containerlab", "")))})
    platforms = sorted({build["platform"] for build in builds if build.get("platform")})
    rows.append(("Lab platform", f"Containerlab {', '.join(clab) or 'version not recorded'} on "
                                 f"{', '.join(platforms) or 'an unrecorded platform'}"))
    rows.append(("Bridge modes", ", ".join(sorted({run.mode for run in runs})) or "not recorded"))
    roles = {}
    for run in runs:
        for node in ("p1", "p2", "q1", "q2"):
            state = run.directory / f"state-{node}.jsonl"
            if node not in roles and state.exists() and (role := first_role(state)):
                roles[node] = role
    settings = {}
    for run in runs:
        for config in sorted((*run.directory.glob("config-p*.txt"), *run.directory.glob("config-q*.txt"))):
            text = config.read_text()
            for key in ("lacp-strict", "up-delay", "mlag-priority", "mlag-lacp-fallback", "mlag-init-delay"):
                for value in re.findall(rf"\b{key}=(\S+)", text):
                    settings.setdefault(key, set()).add(value)
    if settings:
        rows.append(("MLAG and bond settings", "; ".join(f"`{key}` {', '.join(sorted(values))}"
                                                        for key, values in settings.items())))
    if roles:
        rows.append(("MLAG roles", ", ".join(f"{DEVICES[n][0]} is MLAG {r}" for n, r in sorted(roles.items()))
                     + ". Peer link: ether2 on each MLAG peer (mlag-peer-port)."))
    started = sorted(build["started"][:10] for build in builds if build.get("started"))
    if started:
        rows.append(("Date", started[0] if started[0] == started[-1] else f"{started[0]} to {started[-1]}"))
    configs = []
    for suite in suites:
        inputs = suite / "inputs"
        for name in (*STARTUP_CONFIGS, "small.clab.yml", "medium.clab.yml", "medium-pair-root.clab.yml", "medium-two-pair.clab.yml",
                     "client-network.sh"):
            if (inputs / name).exists():
                configs.append(link(name if len(suites) == 1 else f"{suite.name}/{name}", inputs / name, base))
    rows.append(("Device configs", " · ".join(configs) + (" · " if configs else "")
                 + "running config of each device per run, linked in each case section"))
    return rows


def write_readme(path, title=None):
    """Write README.md in a suite or campaign directory and return its path."""
    path = path.resolve()
    suites = find_suites(path)
    runs, suite_errors = load_runs(suites)
    groups = group_runs(runs)
    lab = ", ".join(sorted({run.result.get("lab", "") for run in runs} - {""})) or "MLAG lab"
    versions = sorted({m[1] for s in suites if (s / "builds.json").exists()
                       for text in json.loads((s / "builds.json").read_text()).get("routeros", {}).values()
                       if (m := re.search(r"version:\s*(\S+)", text))})
    lines = [f"# {title or lab} results · {path.name}" + (f" · RouterOS {', '.join(versions)}" if versions else ""), "",
             "Generated by `mlag-lab run` and `mlag-lab evaluate` from the saved results. Do not edit this file; "
             "write analysis in `notes.md`.", "", "## Setup", "", "| | |", "| --- | --- |"]
    lines += [f"| {name} | {value} |" for name, value in setup_rows(suites, runs, path)]
    lines += ["", "## TL;DR", ""]
    ordered = sorted(groups.items(), key=lambda item: (ORDER[group_status(item[1])], item[0]))
    lines += [f"- {tldr_line(key, runs)}" for key, runs in ordered] or ["- No case reached evaluation."]
    lines += ["", "## Summary", "",
              "| Result | Case | Bridge mode | Failure phase: limit → measured | Return phase: limit → measured | Runs passed |",
              "| --- | --- | --- | --- | --- | --- |"]
    for key, group in groups.items():
        _, case_title, mode = key
        heading = f"{case_title} · {mode}"
        columns = []
        for i in range(2):
            phase, verdict, worst, _ = phase_summary(group, i)
            columns.append("n/a (single phase)" if phase is None else
                           f"{ICONS[verdict].split(' ')[0]} {phase['name']}: {limit_text(phase)} → {loss_text(worst)}")
        passed = sum(run.status == "pass" for run in group)
        lines.append(f"| {ICONS[group_status(group)]} | [{case_title}](#{slug(heading)}) | {mode} | "
                     f"{columns[0]} | {columns[1]} | {passed} of {len(counted(group))} |")
    lines += ["", "## Cases", ""]
    for key, group in groups.items():
        _, case_title, mode = key
        command = group[0].result.get("name", group[0].result.get("case"))
        lines += [f"### {case_title} · {mode}", "",
                  f"{group[0].result.get('action', '')} Run it with `mlag-lab run --case {command}`.", ""]
        labels = [run_label(run, group) for run in group]
        lines += ["| Phase | Expected | Limit | " + " | ".join(label.capitalize() for label in labels) + " |",
                  "| --- | --- | --- | " + " | ".join("---" for _ in group) + " |"]
        details = []
        for i in range(max(len(run.phases) for run in group)):
            phase = phase_summary(group, i)[0]
            source = (f" [Source]({phase['source']})" if phase["source"].startswith("http")
                      else "" if "lab target" in phase["expected"].lower() else f" ({phase['source']})")
            short = re.split(r"(?<=\.)\s", phase["expected"], maxsplit=1)[0]
            lines.append(f"| {phase['name']} | {short} | {limit_text(phase)} | "
                         + " | ".join(cell(run, i, path) for run in group) + " |")
            details.append(f"- **{phase['name']}:** {phase['expected']}{source}")
        if fixes := fixes_text(command):
            details.append(f"- **MikroTik fixes this case checks:** {fixes}")
        lines += ["", *details, ""]
        for run, label in zip(group, labels):
            files = [link("verdict", run.file, path)]
            if (run.directory / "timeline.tsv").exists():
                files.append(link("timeline", run.directory / "timeline.tsv", path))
            files += [link(f"{DEVICES.get(node, (node, node))[0]} config", config, path)
                      for node, config in sorted((p.stem.removeprefix("config-"), p)
                                                 for p in run.directory.glob("config-*.txt"))]
            other = case_checks(run)
            extra = ""
            if other:
                line = check_line(run.file, other[0])
                target = Path(os.path.relpath(run.file, path)).as_posix() + (f"#L{line}" if line else "")
                extra = f" Other failed checks: {len(other)}, first: [{other[0]}]({target})."
            lines.append(f"- {label.capitalize()} ({ICONS[run.status]}): " + " · ".join(files) + extra)
        lines.append("")
    notes = path / "notes.md"
    lines += ["## Analysis (written by hand)", ""]
    lines += [notes.read_text().strip(), ""] if notes.exists() else ["No analysis has been written yet.", ""]
    lines += ["## Evidence", "", "| Suite | Started | Code revision | Runs | Files |", "| --- | --- | --- | --- | --- |"]
    for suite in suites:
        build = json.loads((suite / "builds.json").read_text()) if (suite / "builds.json").exists() else {}
        count = sum(run.suite == suite for run in runs)
        files = [link(name, suite / name, path) for name in ("suite.json", "junit.xml", "builds.json")
                 if (suite / name).exists()]
        if (suite / "inputs").exists():
            files.append(link("inputs", suite / "inputs", path))
        started = build.get("started", "")
        started = f"{started[:10]} {started[11:16]} UTC" if started else "—"
        lines.append(f"| {link(suite.name, suite, path)} | {started} | "
                     f"{(build.get('git_revision') or '—')[:12]} | {count} | {' · '.join(files)} |")
    for suite, result in suite_errors:
        detail = "; ".join(c["detail"] for c in result.get("checks", []) if not c["ok"]) or result.get("reason", "")
        lines.append(f"\n{ICONS[result['status']]} · {suite.name} · {result['run']}: {detail}")
    readme = path / "README.md"
    readme.write_text("\n".join(lines).rstrip() + "\n")
    return readme


TEST_ORDER = (
    "Run the labs in order. Each lab adds devices and protocols on top of the one before, so a failure in a "
    "smaller lab is fixed or explained there first.",
    "",
    "1. **Small lab**: run every case with STP off and with RSTP (`--bridge-mode none` and `--bridge-mode rstp`).",
    "2. **Medium lab**: start only after every Small case passes in both bridge modes.",
    "3. **Large lab**: start only after every Medium case passes.",
)


def fixes_text(selector):
    """The MikroTik changelog lines a case checks, each linked to its changelog."""
    try:
        fixes = case_spec(selector).fixes
    except ValueError:
        return ""
    return "; ".join(f"{wording} ([{version}]({link}))" for version, wording, link in fixes)


def phase_cell(phase):
    limit = "" if phase.key == "calibration" else f" Limit: {'no loss' if phase.limit_s == 0 else f'{phase.limit_s:g} s'}."
    return f"**{phase.name}.** {phase.expected}{limit}"


def write_case_index(path, cases):
    """Write the case index from the case specification."""
    lines = ["# Case index", "", "Generated from `src/mlag_lab/cases.py`. "
             "Change the specification, not this file.", "", "## Test order", "", *TEST_ORDER]
    for lab in ("Small", "Medium", "Large"):
        rows = [case for case in cases if case.lab == lab]
        lines += ["", f"## {lab} lab", "",
                  "| Case | What the runner does | First phase | Second phase | MikroTik fixes checked | Command name |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for case in rows:
            phases = [phase_cell(phase) for phase in case.phases] + ["—"] * (2 - len(case.phases))
            command = f"`{case.name}`" if case.selectors else "Planned"
            fixes = fixes_text(case.name) or "—"
            lines.append(f"| {case.title} | {case.action} | {phases[0]} | {phases[1]} | {fixes} | {command} |")
    path.write_text("\n".join(lines) + "\n")
    return path
