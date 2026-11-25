"""Evaluate calibration and chassis cases with protocol and flow evidence."""

import json
import re

from .evidence import load_jsonl
from .networka import recorded
from .forwarding_checks import MEDIUM_HOSTS, MEDIUM_OUTSIDE, MEDIUM_PARTNER_BONDS, forwarding, grade
from .forwarding_checks import access_bpdus, grade_access_bpdus, grade_system_ids, lacp_system_ids
from .cases import case_spec
from .legacy_checks import check_calibration
from .measure import number, score_flows, seconds
from .reboot_checks import cadence_ok, cadence_text, check_reboot_flows, guest_window, peer_observations
from .reboot_checks import sender_pause_rule
from .report import write_timeline
from .root_evidence import read_root_packets, read_root_state, read_root_syslog
from .root_state import verify_root
from .root_topology import ROOT_CAPTURES, ROOT_CAPTURES_V1, ROOT_FLOWS, ROOT_ID, ROOT_NODES, target_for


def evaluate_root(path, name, checks, result):
    spec = case_spec(name)
    events = load_jsonl(path / "events.jsonl")
    marks = {event["name"]: event for event in events}
    if "runner_error" in marks:
        raise RuntimeError(marks["runner_error"]["detail"])

    def check(level, passed, message, phase=None):
        checks.append({"level": level, "ok": bool(passed), "detail": message} | ({"phase": phase} if phase else {}))

    timeline = [(e["epoch_ns"], "action", json.dumps(e, sort_keys=True)) for e in events]
    start = number(marks, "baseline_start")
    end = number(marks, "recovery_end")
    down = number(marks, "down_start")
    recovery = number(marks, "recovery_start")
    manifest = json.loads((path / "attempt.json").read_text())
    captures = ROOT_CAPTURES_V1 if manifest["schema"] == 1 else ROOT_CAPTURES
    target = target_for(name)
    bpdus = []
    icmp, frames, legs, iccp = read_root_packets(path, captures, start, down, check, timeline, bpdus=bpdus)
    if target:
        if manifest["target"] != target or marks["down_start"]["target"] != target:
            raise ValueError("Guest target disagrees with the selected case")
        first_miss, last_miss, up = guest_window(icmp, target, down, end, check, timeline)
        result["guest"] = {"target": target, "first_missed_management_request_s": seconds(first_miss - start),
                           "last_missed_management_request_s": seconds(last_miss - start),
                           "first_returned_management_reply_s": seconds(up - start)}
        if name == "primary-sustained-stop":
            stopped, resumed = marks["guest_stopped"], marks["guest_resumed"]
            pause = seconds(marks["guest_resume_requested"]["mono_ns"] - stopped["mono_ns"])
            check("error", stopped["target"] == resumed["target"] == target and pause >= 35
                  and stopped["status"]["status"] == "paused" and resumed["status"]["running"],
                  f"{target} QEMU confirmed sustained pause and resume")
            result["guest"]["confirmed_pause_s"] = pause
            first_miss, last_miss, up = stopped["qmp"]["done_ns"], resumed["qmp"]["started_ns"], resumed["qmp"]["done_ns"]
            result["guest"]["qmp_resume_bounds_s"] = [seconds(last_miss - start), seconds(up - start)]
        else:
            boot = marks["guest_boot_observed"]
            check("error", boot["target"] == target and boot["uptime_ns"] < boot["prior_uptime_ns"],
                  f"{target} guest uptime reset after the request")
            result["guest"]["boot_confirmed_s"] = seconds(boot["query_end_ns"] - start)
            result["guest"]["post_boot_uptime_s"] = seconds(boot["uptime_ns"])
        if name == "reboot-primary-no-fallback":
            config = json.loads((path / "effective-config.json").read_text())
            check("error", all("mlag-lacp-fallback=no" in config[node] for node in ("p1", "p2")),
                  "Both peers used mlag-lacp-fallback=no for the paired reboot")
        result["peer"] = peer_observations(path, target, start, first_miss, last_miss, end, check, timeline)
        config = json.loads((path / "effective-config.json").read_text())
        if mac := re.search(r"^peer-link-mac=([0-9a-f:]+)", config[target], re.I | re.M):
            point = f"{result['peer']['survivor']}-tap1"
            stamps = sorted(set(iccp[point, mac[1].lower()]))
            before, after = max((t for t in stamps if t < first_miss), default=None), next(
                (t for t in stamps if t >= first_miss + 2_000_000_000), None)
            result["peer"]["target_iccp"] = {
                "point": point, "source": mac[1].lower(),
                "last_before_management_loss_s": seconds(before - start) if before is not None else None,
                "first_after_management_loss_s": seconds(after - start) if after is not None else None,
            }
    else:
        up = number(marks, "up_start")
    actions = (("withdrawal", down, up), ("restoration", up, recovery))
    result["phases_s"] = {label: [seconds(lo - start), seconds(hi - start)] for label, lo, hi in actions}
    stopped = marks["collectors_stopped"]
    check("error", abs(stopped["clock_delta_ns"]) < 50_000_000,
          "Host wall clock and monotonic clock agree within 50 ms")
    check("error", not stopped["early_exits"], "All packet, probe and link collectors stayed up")
    for marker in ("baseline_confirmed", "baseline_restored"):
        if marker == "baseline_restored" and "baseline_restoration_failed" in marks:
            check("fail", False, marks["baseline_restoration_failed"]["detail"], "restoration")
            continue
        try:
            verify_root(marks[marker]["routers"], marks[marker]["linux"])
        except RuntimeError as error:
            check("error", False, f"{marker}: {error}")
        else:
            check("error", True, f"{marker}: complementary roles, shared root, forwarding and all live LACP members")
    result["root_baseline"] = {"root_id": ROOT_ID, "witness_bpdu_legs": legs}
    result["sampling"] = read_root_state(path, start, end, target, check, timeline)
    nodes = recorded(ROOT_NODES, manifest)
    result["syslog"] = read_root_syslog(path, target, check, timeline, nodes=nodes, label=manifest["topology"])
    if "syslog_rebind_requested" in marks:
        check("error", result["syslog"]["target_after_rebind_received"],
              f"{target} emitted the verification marker after the post-observation syslog rebind")
    flows = score_flows(icmp, start, end, actions, timeline, definitions=ROOT_FLOWS, detailed=True)
    result["flows"] = flows
    result["forwarding"] = forwarding(path, icmp, ROOT_FLOWS, start, down, up, end, outside=MEDIUM_OUTSIDE,
                                      hosts=MEDIUM_HOSTS, nodes=nodes, recovery=recovery)
    grade(result["forwarding"], check)
    result["lacp_system_ids"] = lacp_system_ids(marks, MEDIUM_PARTNER_BONDS)
    grade_system_ids(result["lacp_system_ids"], check)
    result["access_bpdus"] = access_bpdus(bpdus, start, down, up, end)
    grade_access_bpdus(result["access_bpdus"], check)
    result["sender_pause_rule"] = sender_pause_rule(name, flows, ROOT_FLOWS, seconds(down - start),
                                                    seconds(end - start))
    for ident, flow in flows.items():
        check("error", flow["baseline_good"] >= 30 and not flow["baseline_missed"],
              f"{ident} has a clean baseline with at least 30 successful probes")
        check("error", cadence_ok(flow), f"{ident} send cadence stayed within 450 ms{cadence_text(flow)}")
        check("error", not flow["capture_mismatches"], f"{ident} request and reply captures agree")
        check("fail" if target and ident in (101, 201) else "error", not flow["duplicates"],
              f"{ident} duplicate-free")
        check("fail" if target and ident in (101, 201) else "error", flow["stable_recovery"],
              f"{ident} delivered ten consecutive probes during recovery", "restoration")
        for gap in flow["gaps"]:
            for sequence, miss in gap.get("misses", {}).items():
                miss["frames"] = {
                    label: frames[ident, kind, sequence] for label, kind in (("request", 8), ("reply", 0))
                }
    if name == "root-calibrate":
        check_calibration(spec, marks, flows, result, check)
    else:
        check_reboot_flows(spec, flows, icmp, start, seconds(down - start), seconds(first_miss - start),
                           seconds(last_miss - start), seconds(up - start), seconds(end - start), check)
    write_timeline(path, start, timeline)
