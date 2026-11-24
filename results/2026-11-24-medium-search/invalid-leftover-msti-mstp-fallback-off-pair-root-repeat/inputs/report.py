"""Write machine-readable results and the merged evidence timeline."""

import csv
import json
import xml.etree.ElementTree as ET

from .legacy import NS
from .readme import write_readme


def write_result(path, result):
    (path / "result.json").write_text(json.dumps(result, indent=2) + "\n")


def write_timeline(path, start, timeline):
    with (path / "timeline.tsv").open("w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(("seconds_from_baseline", "source", "event"))
        writer.writerows((f"{(stamp - start) / NS:.9f}", source, event)
                         for stamp, source, event in sorted(timeline))


def write_suite(output):
    schedule = output / "schedule.json"
    found = {f.parent.name: json.loads(f.read_text()) for f in sorted(output.glob("*/result.json"))}
    results = []
    skipped = 0
    if schedule.exists():
        for case in json.loads(schedule.read_text()):
            result = found.pop(case["run"], None)
            if result is None:
                skipped += 1
                result = {**case, "status": "skipped", "checks": [],
                          "reason": "Attempt did not reach evaluation"}
            elif result["case"] != case["case"]:
                result["status"] = "error"
                result["checks"].append({"ok": False, "level": "error", "detail": "Attempt case disagrees with schedule"})
            results.append(result)
    results.extend(found.values())
    global_error = output / "runner-error.txt"
    if global_error.exists() or not results or skipped:
        reason = global_error.read_text().strip() if global_error.exists() else (
            f"{skipped} scheduled attempts did not reach evaluation" if skipped else "No test results"
        )
        results.append({"run": "runner", "status": "error", "checks": [{"ok": False, "level": "error",
                         "detail": reason}]})
    errors = sum(r["status"] == "error" for r in results)
    failures = sum(r["status"] == "fail" for r in results)
    labs = {result.get("lab", "Small lab") for result in results if result["run"] != "runner"}
    lab = next(iter(labs)) if len(labs) == 1 else "MLAG labs"
    lab_key = lab.lower().replace(" lab", "").replace(" ", "-")
    suite = ET.Element("testsuite", name=f"mikrotik-mlag-{lab_key}", tests=str(len(results)),
                       errors=str(errors), failures=str(failures))
    if schedule.exists():
        suite.set("skipped", str(skipped))
    for result in results:
        test = ET.SubElement(suite, "testcase", name=result["run"], classname=f"mikrotik.mlag.{lab_key}")
        properties = ET.SubElement(test, "properties")
        ET.SubElement(properties, "property", name="lab", value=lab)
        if "case_id" in result:
            ET.SubElement(properties, "property", name="case_id", value=result["case_id"])
        if result["status"] == "skipped":
            ET.SubElement(test, "skipped", message=result["reason"])
        elif result["status"] != "pass":
            item = ET.SubElement(test, "error" if result["status"] == "error" else "failure")
            item.text = "\n".join(check["detail"] for check in result["checks"] if not check["ok"])
    ET.indent(suite)
    ET.ElementTree(suite).write(output / "junit.xml", encoding="utf-8", xml_declaration=True)
    summary = {"errors": errors, "failures": failures, "results": results}
    if schedule.exists():
        summary["skipped"] = skipped
    (output / "suite.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_readme(output)
    return 2 if errors else 1 if failures else 0
