"""Cut one saved run's packet captures to a time window and pack them for a ticket or bug report."""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

from .evidence import capture_hashes, load_jsonl
from .legacy import NS

MARGIN_S = 2.0


def baseline_ns(run):
    """Second 0 of timeline.tsv: the last baseline_start event, else the first event, as the evaluators choose it."""
    events = load_jsonl(run / "events.jsonl")
    marks = {event["name"]: event for event in events}
    return marks.get("baseline_start", events[0])["epoch_ns"]


def fault_window(result):
    """From MARGIN_S before the fault to the end of the return phase, in seconds from the baseline."""
    phases = result.get("phases_s")
    if not phases:
        raise ValueError(f"result.json of {result['run']} has no fault phases; pass --from and --to")
    return min(start for start, _ in phases.values()) - MARGIN_S, max(end for _, end in phases.values())


def epoch(ns):
    return f"{ns // NS}.{ns % NS:09d}"


def utc(ns):
    return datetime.fromtimestamp(ns / NS, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def anonymous(info):
    # The archive goes to outside parties: keep the local user out of the tar headers.
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def cut(run, start_s=None, end_s=None, output=None):
    """Write <output>.tar.gz with every capture cut to the window. Return the archive path and a summary line."""
    captures = sorted((run / "captures").glob("*.pcap"))
    if not captures:
        raise ValueError(f"{run} has no packet captures in captures/")
    editcap = shutil.which("editcap")
    if editcap is None:
        raise ValueError("editcap not found: it ships with Wireshark and TShark")
    result = json.loads((run / "result.json").read_text())
    if start_s is None or end_s is None:
        fault_start, fault_end = fault_window(result)
        start_s = fault_start if start_s is None else start_s
        end_s = fault_end if end_s is None else end_s
    if end_s <= start_s:
        raise ValueError(f"Window end {end_s} s is not after its start {start_s} s")
    zero = baseline_ns(run)
    begin, end = zero + round(start_s * NS), zero + round(end_s * NS)
    name = f"{run.parent.name}-{run.name}-{start_s:.1f}s-{end_s:.1f}s"
    output = output or Path("test-results") / "cuts" / f"{name}.tar.gz"
    with tempfile.TemporaryDirectory() as scratch:
        folder = Path(scratch) / name
        (folder / "captures").mkdir(parents=True)
        for capture in captures:
            # -F pcap keeps the input format: editcap's default pcapng would add the local host's OS and tool names.
            command = [editcap, "-F", "pcap", "-A", epoch(begin), "-B", epoch(end), str(capture),
                       str(folder / "captures" / capture.name)]
            done = subprocess.run(command, capture_output=True, text=True, timeout=60)
            if done.returncode:
                raise ValueError(f"editcap failed on {capture}: {done.stderr.strip()}")
        (folder / "pcap.sha256").write_text(capture_hashes(folder, [capture.stem for capture in captures]))
        if (run / "pcap.sha256").exists():
            shutil.copy(run / "pcap.sha256", folder / "source.sha256")
        window = {
            "run": "/".join(run.resolve().parts[-3:]), "case": result["case"], "status": result["status"],
            "from_s": start_s, "to_s": end_s, "from_utc": utc(begin), "to_utc": utc(end),
            "note": "Seconds count from the run's baseline start, as in its timeline.tsv. "
                    "pcap.sha256 lists these cut captures; source.sha256 lists the full captures of the run.",
        }
        (folder / "cut.json").write_text(json.dumps(window, indent=2) + "\n")
        output.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(output, "w:gz") as archive:
            archive.add(folder, arcname=name, filter=anonymous)
    full = sum(capture.stat().st_size for capture in captures)
    return output, (f"{output}: {len(captures)} captures, {start_s:.1f} to {end_s:.1f} s from the baseline "
                    f"({window['from_utc']} to {window['to_utc']}), {output.stat().st_size / 1e6:.2f} MB packed "
                    f"from {full / 1e6:.2f} MB of captures")
