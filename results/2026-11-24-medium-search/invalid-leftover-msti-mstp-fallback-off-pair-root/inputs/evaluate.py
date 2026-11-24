"""Select the case evaluator and score a saved attempt."""

import json
import re
import subprocess

from .cases import BY_NAME, case_spec, phase_results
from .direct_topology import DIRECT_CASES
from .evidence import load_jsonl, read_legacy_packets, read_legacy_state
from .external_evaluate import evaluate_external
from .external_topology import EXTERNAL_CASES
from .legacy import CASES, case_captures
from .legacy_checks import check_calibration, check_member, check_mobile_move, check_peer_link
from .measure import number, score_flows, seconds
from .readme import write_readme
from .report import write_timeline, write_result, write_suite
from .root_evaluate import evaluate_root
from .root_topology import MEDIUM_TARGETS, ROOT_CASES


def case_id(path):
    manifest = path / "attempt.json"
    if manifest.exists():
        name = json.loads(manifest.read_text())["case"]
    else:
        match = re.fullmatch(r"[0-9]+-(.+)", path.name)
        name = match[1] if match else None
    if name in BY_NAME:
        name = BY_NAME[name].selectors[0]
    if name not in CASES and not (
        manifest.exists() and name in (*ROOT_CASES, *EXTERNAL_CASES, *DIRECT_CASES, *MEDIUM_TARGETS)
    ):
        raise ValueError(f"Unknown case ID: {name!r} in {path}")
    return name


def evaluate_legacy(path, name, checks, result):
    spec = case_spec(name)
    events = load_jsonl(path / "events.jsonl")
    marks = {event["name"]: event for event in events}
    timeline = [(e["epoch_ns"], "action", json.dumps(e, sort_keys=True)) for e in events]
    if "runner_error" in marks:
        raise RuntimeError(marks["runner_error"]["detail"])
    start = number(marks, "baseline_start")
    end = number(marks, "recovery_end")
    down = number(marks, "down_start")
    up = number(marks, "up_start")
    recovery = number(marks, "recovery_start")
    def check(level, ok, message, phase=None):
        checks.append({"level": level, "ok": bool(ok), "detail": message} | ({"phase": phase} if phase else {}))
    check("error", abs(marks["collectors_stopped"]["clock_delta_ns"]) < 50_000_000,
          "Host wall clock and monotonic clock agree within 50 ms")
    check("error", not marks["collectors_stopped"].get("early_exits"), "All capture and probe processes stayed up")
    actions = (("withdrawal", down, up), ("restoration", up, recovery))
    result["phases_s"] = {label: [seconds(lo - start), seconds(hi - start)] for label, lo, hi in actions}

    packets = read_legacy_packets(path, check, timeline, case_captures(name))
    link_events = read_legacy_state(path, name, marks, start, down, up, check, timeline)

    flows = score_flows(packets.icmp, start, end, actions, timeline)
    result["flows"] = flows
    for ident, flow in flows.items():
        check("error", flow["baseline_good"] >= 30, f"{ident} has usable baseline cadence")
        check("error", flow["max_send_interval_s"] <= 0.45,
              f"{ident} consecutive sends stayed within 450 ms")
        check("error", not any(not gap["phases"] for gap in flow["gaps"]),
              f"{ident} has no separate loss away from the fault")
        check("error", not flow["capture_mismatches"], f"{ident} reply paths agree across endpoint captures")
        check("error" if name == "calibrate" else "fail", flow["recovery_good"] >= 20,
              f"{ident} recovered delivery within the observation window", "restoration")
        check("fail", not flow["duplicates"], f"{ident} duplicate-free")

    if name == "calibrate":
        check_calibration(spec, marks, flows, result, check)
    elif name == "mobile-move":
        check_mobile_move(spec, packets, down, up, end, flows, result, check)
    elif name == "peer-link-loss":
        check_peer_link(spec, path, marks, start, down, up, end, flows, result, check)
    else:
        check_member(spec, name, marks, packets, link_events, start, down, up, end, flows, result, check)
    write_timeline(path, start, timeline)


def bridge_mode(path):
    """Requested bridge mode, else the single protocol-mode both MLAG peers ran with."""
    manifest = path / "attempt.json"
    if manifest.exists() and (mode := json.loads(manifest.read_text()).get("bridge_mode")):
        return mode
    config = path / "effective-config.json"
    if config.exists():
        modes = {match[1] for node, text in json.loads(config.read_text()).items()
                 if node in ("p1", "p2") and (match := re.search(r"\bprotocol-mode=(\w+)", text))}
        if len(modes) == 1:
            return modes.pop()
    return None


def write_configs(path, checks):
    """Save each device's effective configuration as readable text and compare it with the requested mode."""
    config = path / "effective-config.json"
    if not config.exists():
        return
    effective = json.loads(config.read_text())
    for node, text in effective.items():
        (path / f"config-{node}.txt").write_text(text if text.endswith("\n") else text + "\n")
    manifest = path / "attempt.json"
    requested = json.loads(manifest.read_text()).get("bridge_mode") if manifest.exists() else None
    if requested:
        running = {node: match[1] for node, text in effective.items() if node in ("p1", "p2")
                   and (match := re.search(r"\bprotocol-mode=(\w+)", text))}
        checks.append({"level": "error", "ok": set(running.values()) == {requested},
                       "detail": f"Both MLAG peers ran protocol-mode={requested}: {running}"})


def analyze(path):
    name = spec = None
    checks = []
    result = {"run": path.name, "case": name, "checks": checks}
    try:
        name = case_id(path)
        result["case"] = name
        spec = case_spec(name)
        result.update(name=spec.name, lab=f"{spec.lab} lab", title=spec.title, action=spec.action)
        if name in (*EXTERNAL_CASES, *DIRECT_CASES, *MEDIUM_TARGETS):
            evaluator = evaluate_external
        else:
            evaluator = evaluate_root if name in ROOT_CASES else evaluate_legacy
        evaluator(path, name, checks, result)
        result["bridge_mode"] = bridge_mode(path)
        write_configs(path, checks)
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        checks.append({"level": "error", "ok": False, "detail": str(error)})
    failures = {check["level"] for check in checks if not check["ok"]}
    if "error" in failures:
        result["status"] = "error"
    elif "fail" in failures:
        result["status"] = "fail"
    elif "inconclusive" in failures:
        result["status"] = "error"
    else:
        result["status"] = "pass"
    if spec is not None:
        result["phases"] = phase_results(spec, result, checks)
    write_result(path, result)
    return result


def replay(path):
    if not path.is_dir():
        raise ValueError(f"Evidence directory does not exist: {path}")
    if any((path / name).exists() for name in ("events.jsonl", "attempt.json", "captures")):
        return {"pass": 0, "fail": 1, "error": 2}[analyze(path)["status"]]
    attempts = [child for child in sorted(path.iterdir()) if child.is_dir() and (
        re.match(r"[0-9]+-", child.name) or (child / "attempt.json").exists() or (child / "events.jsonl").exists())]
    suites = [child for child in sorted(path.iterdir()) if child.is_dir() and (
        (child / "schedule.json").exists() or (child / "suite.json").exists())]
    if suites and not attempts:
        status = max(replay(suite) for suite in suites)
        write_readme(path)
        return status
    for child in attempts:
        analyze(child)
    return write_suite(path)
