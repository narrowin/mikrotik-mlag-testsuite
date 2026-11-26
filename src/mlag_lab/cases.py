"""Load case intent from YAML and summarize measured phases."""

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Annotated

from pydantic import ConfigDict, Field, TypeAdapter
import yaml

from .direct_topology import DIRECT_FLOWS
from .small_06 import Small06Intent

INTENT_DIR = Path(__file__).with_name("intent")
CASE_INPUTS = tuple(INTENT_DIR / f"{family}.yaml" for family in (
    "small", "medium", "small-link", "planned", "medium-mstp", "two-pair",
))
LIMITS_PATH = INTENT_DIR / "limits.yaml"
INTENT_INPUTS = (*CASE_INPUTS, LIMITS_PATH)
CASE_INTENT_FILE = "case-intent.yaml"
PHASE_KEYS = ("baseline", "calibration", "withdrawal", "restoration")

# Inputs to the legacy fault actuators.
MAC_AGE_TIME, MAC_AGE_DEFAULT = "10s", "5m"
# The same durations as RouterOS returns them in JSON, where Networka reads them back.
AGEING_JSON = {MAC_AGE_TIME: "00:00:10", MAC_AGE_DEFAULT: "00:05:00"}
MAC_AGE_SILENCE_S, MAC_AGE_RETURN_S = 25, 5
FLAP_CYCLES, FLAP_DOWN_S, FLAP_UP_S = 5, 1, 3

Seconds = Annotated[float, Field(strict=True, ge=0, allow_inf_nan=False)]


class CaseLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        result = super().construct_mapping(node, deep)
        if len(result) != len(node.value):
            raise yaml.constructor.ConstructorError(
                None, None, "duplicate mapping key in case intent", node.start_mark
            )
        return result


def read_yaml(path):
    try:
        return yaml.load(path.read_text(), Loader=CaseLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: {error}") from error


@dataclass(frozen=True)
class GradingLimits:
    __pydantic_config__ = ConfigDict(extra="forbid")

    calibration_cut_s: tuple[Seconds, Seconds]
    outside_flood_s: Seconds
    mac_relearn_s: Seconds

    def __post_init__(self):
        low, high = self.calibration_cut_s
        if low >= high:
            raise ValueError("Calibration cut lower bound must be below its upper bound")


SUITE_LIMITS = TypeAdapter(GradingLimits).validate_python(read_yaml(LIMITS_PATH))


@dataclass(frozen=True)
class Phase:
    __pydantic_config__ = ConfigDict(extra="forbid")

    key: str
    name: str
    expected: str
    source: str
    limit_s: Seconds | None = None


@dataclass(frozen=True)
class Case:
    __pydantic_config__ = ConfigDict(extra="forbid")

    name: str
    lab: str
    title: str
    action: str = ""
    selectors: tuple[str, ...] = ()
    graded_flows: tuple[int, ...] = ()
    control_flows: tuple[int, ...] = ()
    phases: tuple[Phase, ...] = ()
    grading_limits: GradingLimits = SUITE_LIMITS
    # MikroTik fixes this case checks: (RouterOS version, MikroTik's changelog wording, changelog link).
    # Filled from docs/reference/mlag-fixes.md, rows in state Checked or Indirect only.
    fixes: tuple[tuple[str, str, str], ...] = ()
    reboot_intent: Small06Intent | None = None

    def limit(self, key):
        return next(phase.limit_s for phase in self.phases if phase.key == key)


CASE_SCHEMA = TypeAdapter(Case)


def validate_case(data, source):
    try:
        case = CASE_SCHEMA.validate_python(data)
        _index((case,))
        return case
    except ValueError as error:
        raise ValueError(f"{source}: {error}") from error


def load_cases():
    for path in CASE_INPUTS:
        data = read_yaml(path)
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected a mapping of case names to definitions")
        for name, definition in data.items():
            if not isinstance(definition, dict) or "name" in definition:
                raise ValueError(f"{path}: invalid case definition for {name!r}")
            yield validate_case({"name": name, **definition}, path)


def save_case(spec, path):
    """Save the resolved expectations with the observations for future replay."""
    data = CASE_SCHEMA.dump_python(spec, mode="json", exclude_none=True)
    (path / CASE_INTENT_FILE).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


def recorded_case(spec, path):
    """The rules saved with the attempt. Replay never falls back to the catalogue."""
    source = path / CASE_INTENT_FILE
    if not source.is_file():
        raise ValueError(f"{source}: missing")
    recorded = validate_case(read_yaml(source), source)
    if recorded.name != spec.name:
        raise ValueError(f"{source}: does not identify {spec.name}")
    return recorded


def _changelog(version):
    return f"https://cdn.mikrotik.com/routeros/{version}/CHANGELOG"


def _reboot(name):
    return ("reboot" in name or "power-loss" in name) and "calibrat" not in name


def _baseline(name):
    return name.endswith("-baseline") or name == "baseline"


_STP_REBOOT = ("medium-pair-root-reboot-", "medium-access-root-reboot-", "medium-mstp-pair-root-reboot-",
               "medium-mstp-access-root-reboot-", "reboot-primary", "reboot-secondary", "two-pair-equal-reboot-",
               "two-pair-field-reboot-")
# Each row of docs/reference/mlag-fixes.md in state Checked or Indirect, with the cases that grade it.
FIXES = (
    ("7.25.2", "Dual-bond hosts dropped when an MLAG peer is lost", _reboot),
    ("7.25.2", "Packets looped back to a dual-connected bond", lambda name: True),
    ("7.24.6", "BPDUs leaking to the wrong dual-connected bond (introduced in 7.24)",
     lambda name: not name.startswith("two-pair-") or name.startswith("two-pair-stp-off-")),
    ("7.25.2", "LACP system ID not synchronised when bonds are created before MLAG", lambda name: True),
    ("7.25", "New settings mlag-lacp-fallback and mlag-init-delay",
     lambda name: _reboot(name) or name == "peer-link-loss"),
    ("7.25", "MLAG peer stuck in the disabled state after config changes", _baseline),
    ("7.26beta4", "New setting lacp-strict for 802.3ad bonds", lambda name: name.startswith("two-pair-stp-off-strict-")),
    ("7.24", "STP, BPDU and topology-change handling with MLAG; dual-connected port STP state in sync with the "
     "MLAG peer", lambda name: name.startswith(_STP_REBOOT)),
    ("7.24", "MLAG MAC address handling for ageing, flushing and moving", lambda name: name == "mac-move"),
    ("7.22", "MAC moving between regular ports and bonds", lambda name: name == "mac-move"),
    ("7.22", "MLAG state permanently disabled after changing bridge settings", _baseline),
    ("7.18", "mlag-heartbeat; no peer port reset on heartbeat timeout, a warning is logged",
     lambda name: name in ("peer-link-loss", "primary-sustained-stop")),
    ("7.14", "MLAG connection after a peer link flap (introduced in 7.13)", lambda name: name == "peer-link-loss"),
    ("7.14", "MLAG with MSTP: support and stability", lambda name: name.startswith("medium-mstp-")),
    ("7.17", "Priority setting to elect the MLAG primary", _baseline),
)
def _index(cases):
    index = {}
    for case in cases:
        keys = tuple(phase.key for phase in case.phases)
        if not case.selectors and not keys:
            continue  # Planned case: listed in the index, not yet runnable.
        if keys not in (("baseline",), ("calibration",), ("withdrawal", "restoration")):
            raise ValueError(f"{case.name}: unsupported phases {keys}")
        if set(case.graded_flows) & set(case.control_flows):
            raise ValueError(f"{case.name}: a flow is both graded and a control")
        if case.reboot_intent:
            if any(phase.limit_s is None for phase in case.phases):
                raise ValueError(f"{case.name}: every phase needs limit_s")
            flows = (case.graded_flows, case.control_flows)
            if (not all(flows) or any(len(set(ids)) != len(ids) for ids in flows)
                    or set(case.graded_flows + case.control_flows) - DIRECT_FLOWS.keys()):
                raise ValueError(f"{case.name}: graded_flows and control_flows must each list unique stream IDs "
                                 "of the Small topology")
        for selector in {case.name, *case.selectors}:
            if selector in index:
                raise ValueError(f"Selector {selector} appears in more than one case")
            index[selector] = case
    return index


# The BPDU fix only on the Medium lab and the two-pair deployment: the Small lab has no BPDU check on a bond.
CASES = tuple(replace(case, fixes=tuple(
    (version, wording, _changelog(version)) for version, wording, applies in FIXES
    if case.selectors and applies(case.name)
    and not (wording.startswith("BPDUs leaking") and case.lab != "Medium"))) for case in load_cases())


BY_SELECTOR = _index(CASES)
BY_NAME = {case.name: case for case in CASES}


def case_spec(selector):
    """The case for a descriptive name or an internal runner selector."""
    try:
        return BY_SELECTOR[selector]
    except KeyError:
        raise ValueError(f"No case specification for {selector!r}") from None


def _flow_loss(flow, key, single):
    gaps = [gap for gap in flow["gaps"] if single or key in gap["phases"]]
    if not single and "phase_gaps_s" in flow:
        split = flow["phase_gaps_s"].get(key, [])
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in split]
        # A split outage has exact time bounds per phase but no per-phase probe count.
        probes = None
    else:
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in gaps]
        probes = sum(gap["failed_probes"] for gap in gaps)
    if not spans:
        return None
    return {"lower_s": max(lower for lower, _ in spans),
            "upper_s": None if any(upper is None for _, upper in spans) else max(upper for _, upper in spans),
            "lost_probes": probes,
            # Without split bounds, an outage crossing the restore is reported whole in both phases.
            "spans_both_phases": not single and "phase_gaps_s" not in flow
                                 and any(len(gap["phases"]) > 1 for gap in gaps)}


def _loss(flows, idents, key, single):
    loss = {}
    for ident in idents:
        flow = flows.get(ident) or flows.get(str(ident))
        if flow and (measured := _flow_loss(flow, key, single)):
            loss[str(ident)] = measured
    return loss


def phase_results(spec, result, checks):
    """Measured loss and a verdict for each phase of one attempt.

    A phase fails on a failed check tagged with it; any untagged evidence error invalidates every phase.
    A single-phase case takes every check as its own. A check tagged with a phase the case lacks, such as a
    baseline flood in a fault case, counts against every phase, even one whose fault was withheld.
    """
    single = len(spec.phases) == 1
    executed = result.get("fault_executed", True)
    flows = result.get("flows", {})
    run_error = any(not c["ok"] and c["level"] in ("error", "inconclusive") and "phase" not in c for c in checks)
    keys = {phase.key for phase in spec.phases}
    stray = [c for c in checks if not c["ok"] and "phase" in c and c["phase"] not in keys]
    summary = []
    for phase in spec.phases:
        own = checks if single else [c for c in checks if c.get("phase") == phase.key] + stray
        failed = {c["level"] for c in own if not c["ok"]}
        if phase.key != "baseline" and not executed and not stray:
            verdict = "skipped"
        elif run_error or failed & {"error", "inconclusive"}:
            verdict = "error"
        elif "fail" in failed:
            verdict = "fail"
        else:
            verdict = "pass"
        loss = _loss(flows, spec.graded_flows, phase.key, single)
        summary.append({
            "key": phase.key, "name": phase.name, "expected": phase.expected, "source": phase.source,
            "limit_s": phase.limit_s, "window_s": None if single else result.get("phases_s", {}).get(phase.key),
            "verdict": verdict,
            "worst_loss_s": ({"lower_s": max(v["lower_s"] for v in loss.values()),
                              "upper_s": None if any(v["upper_s"] is None for v in loss.values())
                              else max(v["upper_s"] for v in loss.values()),
                              "lost_probes": max((v["lost_probes"] for v in loss.values()
                                                  if v["lost_probes"] is not None), default=None),
                              "spans_both_phases": any(v["spans_both_phases"] for v in loss.values())}
                             if loss else None),
            "loss_s": loss,
            "control_loss_s": _loss(flows, spec.control_flows, phase.key, single),
            "failed_checks": [c["detail"] for c in own if not c["ok"]],
        })
    return summary
