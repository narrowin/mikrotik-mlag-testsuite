"""Export every saved run as structured records: one row per run and phase, plus per-stream losses.

The export is derived data, like README.md: rerunning it on the same results gives the same files.
Raw evidence stays where it is. Rows point to committed files by repository path and to packet
captures by the SHA-256 recorded in each run's pcap.sha256.
"""

import csv
import json
import re
from pathlib import Path

from .faults import write_tsv as write_faults
from .measurements import COLUMNS, rows as measurement_rows
from .readme import DEVICES, find_suites, startup_mode

SCHEMA = 1
EVIDENCE_FILES = ("result.json", "timeline.tsv", "events.jsonl", "syslog.jsonl")
BRIDGE_KEYS = ("protocol-mode", "priority", "region-name", "region-revision", "mlag-peer-port", "mlag-priority",
               "mlag-heartbeat", "mlag-init-delay", "mlag-lacp-fallback")
BOND_KEYS = ("slaves", "mode", "mlag-id", "lacp-rate", "lacp-mode", "lacp-strict", "up-delay", "down-delay",
             "transmit-hash-policy", "min-links")
FIELDS = (
    ("schema", "Record format version."),
    ("campaign, suite, run", "Folders under results/. The suite name is the configuration variant under test."),
    ("started", "Suite start time in UTC, from builds.json."),
    ("code_revision", "Runner git commit that produced the run, from builds.json."),
    ("setup.lab", "Small lab or Medium lab."),
    ("setup.routeros", "RouterOS version reported by the CHRs."),
    ("setup.chr_image", "CHR image reference with digest."),
    ("setup.containerlab", "Containerlab version."),
    ("setup.bridge_mode", "Spanning tree protocol-mode applied in the run: none, rstp or mstp."),
    ("setup.stp_root_id", "Root bridge ID the run elected, where the case checks it."),
    ("setup.roles", "MLAG role of each MLAG peer at the start of the run (primary or secondary)."),
    ("setup.devices", "Per RouterOS device: bridge settings (protocol-mode, priority, MSTP region, mlag-peer-port "
                      "for the peer link, mlag-priority, mlag-lacp-fallback, mlag-init-delay) and bond settings "
                      "(bond members as slaves, mlag-id, lacp-rate, lacp-strict, up-delay, transmit-hash-policy), "
                      "read from the saved running config."),
    ("case, case_title, fault", "Case command name, title and what the runner did."),
    ("phase, phase_name", "Phase key (baseline, calibration, withdrawal, restoration) and title. Null for a run "
                          "that stopped before any phase was graded."),
    ("expected, source", "Expected behaviour and its MikroTik manual or standard link, or lab target."),
    ("limit_s", "Loss limit in seconds; 0 means no loss; null for calibration, where the gap must enclose the cut."),
    ("cut_s", "Calibration only: applied one-way cut as [start, end] in seconds."),
    ("window_s", "Phase window in seconds from the baseline."),
    ("measured", "Worst graded stream: lower_s and upper_s bound the outage given the 0.1 s probe spacing "
                 "(upper_s null means open-ended), lost_probes, and spans_both_phases for one outage across "
                 "the loss and return phases. Null means no loss."),
    ("verdict", "Phase verdict: pass, fail, error (evidence invalid) or skipped."),
    ("run_status", "Verdict of the whole run."),
    ("failed_checks", "Plain-language reasons for a fail or error."),
    ("evidence.path", "Run folder in the repository. Read it at the same commit as this export."),
    ("evidence.files", "Committed evidence files in that folder."),
    ("evidence.blobs", "Files not in git, as {name, sha256}. Fetch by hash and verify after download."),
)
FAULT_FIELDS = (
    ("lab, setup, case", "Lab, setup variant as in the results README, and case title. Only valid runs of valid "
                         "suites count."),
    ("fault", "Kind of failed check: loss over the limit, baseline traffic lost before any fault, unicast request "
              "sent back to its sender, flood frame back at its sender or twice at a host, STP root moved, MAC move "
              "check failed, or other."),
    ("phase", "Phase name for loss, which counts once per run and phase. Empty for the other kinds, which count once "
              "per run."),
    ("runs_with_fault, runs_checked", "Runs that failed this check, out of the runs of the same lab, setup and case "
                                      "that ran it. Zero rows are kept only for the looped-frame checks of cases "
                                      "that apply a fault."),
    ("loss_lower_s, loss_upper_s", "Loss only: shortest lower bound and longest upper bound of the worst stream in "
                                   "the runs with the fault. An empty upper bound means open-ended."),
    ("runs", "Repository paths of the runs with the fault, separated by spaces."),
)


def records(text):
    """Split RouterOS `print detail` output into one key=value dictionary per item."""
    items, current = [], None
    for line in text.splitlines():
        if re.match(r"^\s*\d+\s", line):
            current = {}
            items.append(current)
        if current is not None:
            for key, quoted, bare in re.findall(r'([\w-]+)=(?:"([^"]*)"|(\S+))', line):
                current[key] = quoted if quoted or bare == "" else bare
    return items


def device_setup(config):
    bridge, bonds = {}, {}
    for item in records(config.read_text()):
        if "protocol-mode" in item:
            bridge = {key: item[key] for key in BRIDGE_KEYS if key in item}
        elif "slaves" in item and item.get("name"):
            bonds[item["name"]] = {key: item[key] for key in BOND_KEYS if key in item}
    return {"name": DEVICES.get(config.stem.removeprefix("config-"), (config.stem,))[0],
            "bridge": bridge, "bonds": bonds}


def roles(directory):
    found = {}
    for node in ("p1", "p2"):
        state = directory / f"state-{node}.jsonl"
        if state.exists() and (match := re.search(r"mlag-active-role: (\w+)", state.read_text())):
            found[node] = match[1]
    return found


def suite_build(suite):
    build = json.loads((suite / "builds.json").read_text()) if (suite / "builds.json").exists() else {}
    versions = sorted({m[1] for text in build.get("routeros", {}).values()
                       if (m := re.search(r"version:\s*(\S+)", text))})
    clab = re.search(r"version:\s*(\S+)", build.get("containerlab", ""))
    return build, {"routeros": ", ".join(versions) or None, "chr_image": build.get("campaign_image"),
                   "containerlab": clab[1] if clab else None}


def evidence(directory, repo_root):
    blobs = []
    if (directory / "pcap.sha256").exists():
        for line in directory.joinpath("pcap.sha256").read_text().splitlines():
            if line.strip():
                digest, name = line.split(maxsplit=1)
                blobs.append({"name": name.lstrip("*"), "sha256": digest})
    files = [name for name in EVIDENCE_FILES if (directory / name).exists()]
    files += sorted(p.name for p in directory.glob("config-*.txt"))
    files += sorted(p.name for p in directory.glob("state-*.jsonl"))
    return {"path": directory.relative_to(repo_root).as_posix(), "files": files, "blobs": blobs}


def suite_rows(campaign, suite, repo_root):
    build, versions = suite_build(suite)
    summary = json.loads((suite / "suite.json").read_text())
    for listed in summary["results"]:
        directory = suite / listed["run"]
        result_file = directory / "result.json"
        result = json.loads(result_file.read_text()) if result_file.exists() else listed
        devices = {p.stem.removeprefix("config-"): device_setup(p) for p in sorted(directory.glob("config-*.txt"))}
        # Older runs did not record the bridge mode; their saved or startup config shows it.
        mode = (result.get("bridge_mode") or devices.get("p1", {}).get("bridge", {}).get("protocol-mode")
                or (startup_mode(suite) or "").split(" ")[0] or None)
        setup = {"lab": result.get("lab"), **versions, "bridge_mode": mode,
                 "stp_root_id": (result.get("election") or {}).get("root"),
                 "roles": roles(directory), "devices": devices}
        base = {"schema": SCHEMA, "campaign": campaign.name, "suite": suite.name, "run": listed["run"],
                "started": build.get("started"), "code_revision": build.get("git_revision"), "setup": setup,
                "case": result.get("name") or result.get("case"), "case_title": result.get("title"),
                "fault": result.get("action")}
        tagged = {detail for phase in result.get("phases", []) for detail in phase["failed_checks"]}
        other = [c["detail"] for c in result.get("checks", []) if not c["ok"] and c["detail"] not in tagged]
        link = evidence(directory, repo_root) if directory.exists() else None
        if not result.get("phases"):
            yield {**base, "phase": None, "verdict": result["status"], "run_status": result["status"],
                   "failed_checks": other or ([listed["reason"]] if listed.get("reason") else []),
                   "evidence": link}
        for phase in result.get("phases", []):
            yield {**base, "phase": phase["key"], "phase_name": phase["name"], "expected": phase["expected"],
                   "source": phase["source"], "limit_s": phase["limit_s"],
                   **({"cut_s": result["injected_s"]} if phase["key"] == "calibration" and result.get("injected_s")
                      else {}),
                   "window_s": phase["window_s"], "measured": phase["worst_loss_s"], "verdict": phase["verdict"],
                   "run_status": result["status"], "failed_checks": phase["failed_checks"] + other,
                   "evidence": link}


def campaigns(results):
    return [child for child in sorted(results.iterdir()) if child.is_dir() and find_suites(child)]


def write_export(results, output=None):
    """Write phases.jsonl, streams.tsv and schema.md for every campaign under results/ and return the folder."""
    results = results.resolve()
    output = (output or results / "index").resolve()
    repo_root = results.parent
    output.mkdir(parents=True, exist_ok=True)
    exported = []
    with (output / "phases.jsonl").open("w") as file:
        for campaign in campaigns(results):
            for suite in find_suites(campaign):
                for row in suite_rows(campaign, suite, repo_root):
                    file.write(json.dumps(row, ensure_ascii=False) + "\n")
                    exported.append(row)
    phase_count = len(exported)
    write_faults(exported, results, output / "faults.tsv")
    with (output / "streams.tsv").open("w", newline="") as file:
        writer = csv.DictWriter(file, ("campaign", *COLUMNS), delimiter="\t")
        writer.writeheader()
        for campaign in campaigns(results):
            writer.writerows({"campaign": campaign.name, **row} for row in measurement_rows(campaign))
    lines = ["# Results index", "", "Generated by `mlag-lab export` from the saved results. Do not edit these files.",
             "", "- `phases.jsonl`: one JSON object per run and phase, with the setup copied onto each row. "
             "Runs that stopped before grading have one row with `phase` null.",
             "- `streams.tsv`: loss bounds per run, phase and probe stream (graded and control), the same columns "
             "as each campaign's `measurements.tsv` plus `campaign`.",
             "- `faults.tsv`: how often each kind of failed check showed, per lab, setup variant and case. Write-ups "
             "quote these counts instead of counting by hand. `results/README.md` shows them per setup group.", "",
             f"## phases.jsonl fields (schema {SCHEMA})", "", "| Field | Meaning |", "| --- | --- |",
             *(f"| `{name}` | {meaning} |" for name, meaning in FIELDS), "",
             "## faults.tsv columns", "", "| Column | Meaning |", "| --- | --- |",
             *(f"| `{name}` | {meaning} |" for name, meaning in FAULT_FIELDS), ""]
    (output / "schema.md").write_text("\n".join(lines))
    return output, phase_count
