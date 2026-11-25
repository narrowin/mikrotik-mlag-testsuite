"""After evaluation, keep only the packets that prove a run's failures and delete the bulk replay evidence."""

from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

from .evidence import CACHE, load_jsonl
from .legacy import NS

CONTEXT_S = 1.0
# Only replay reads these. result.json, timeline.tsv, configs, state, syslog and events stay for export and READMEs.
BULK = ("captures", "probes", "links")


def baseline_ns(run):
    """Second 0 of timeline.tsv and result.json: the last baseline_start event, else the first event."""
    events = load_jsonl(run / "events.jsonl")
    marks = {event["name"]: event for event in events}
    return marks.get("baseline_start", events[0])["epoch_ns"]


def table(value):
    # Some results record a whole check as a status string instead of a table.
    return value if isinstance(value, dict) else {}


def timed_evidence(result):
    """(from_s, to_s, reason) around each timed piece of evidence behind a failed check."""
    limits = {phase["key"]: phase.get("limit_s") or 0.0 for phase in result.get("phases", [])}
    found = []

    def loss(stream, gap, start):
        # A baseline gap has no phase and allows no loss. A gap within its phase limit proves nothing.
        limit = min((limits.get(phase, 0.0) for phase in gap.get("phases", [])), default=0.0)
        lower, upper = gap.get("lower_s") or 0.0, gap.get("upper_s")
        if start is None or (limit and upper is not None and lower <= limit):
            return
        length = upper if upper is not None else lower
        found.append((start - CONTEXT_S, start + length + CONTEXT_S,
                      f"{stream} lost sequences {gap['first_seq']}-{gap['last_seq']}"))

    for stream, flow in table(result.get("flows")).items():
        for gap in flow.get("gaps", []):
            sent = [stamp for point in gap.get("trace_s", {}).values() for side in point.values() for stamp in side]
            loss(stream, gap, min(sent, default=None))
    for stream, flood in table(result.get("floods")).items():
        for receiver, seen in table(flood.get("receivers")).items():
            for gap in seen.get("gaps", []):
                loss(stream, gap, gap.get("from_s"))
            for copy in seen.get("duplicates", []):
                found.append((copy["time_s"] - CONTEXT_S, copy["time_s"] + CONTEXT_S,
                              f"{stream} second copy of seq {copy['seq']} at {receiver}"))
        for copy in flood.get("sender_repeats", []):
            found.append((copy["time_s"] - CONTEXT_S, copy["time_s"] + CONTEXT_S,
                          f"{stream} seq {copy['seq']} back at the sender"))
    for phase in result.get("phases", []):
        if phase.get("verdict") == "fail" and phase.get("window_s"):
            start = phase["window_s"][0]
            found.append((start - CONTEXT_S, start + CONTEXT_S, f"{phase['name']} begins"))
    return found


def tshark(capture, *args):
    done = subprocess.run(["tshark", "-n", "-r", str(capture), *args], capture_output=True, text=True, timeout=120)
    if done.returncode:
        raise ValueError(f"tshark failed on {capture}: {done.stderr.strip()}")
    return done.stdout


def reflected_evidence(result, captures, zero):
    """Reflected unicast findings name sequences, not times: find each copy in the captures."""
    findings = table(table(result.get("forwarding")).get("reflected_copies")).get("findings") or []
    if not findings:
        return []
    labels = {(str(f["stream"]), str(seq)): f"{f['stream']} {f['kind']} seq {seq}"
              for f in findings for seq in f["first_seqs"]}
    query = " || ".join(f"(icmp.ident == {f['stream']} && icmp.seq in {{{', '.join(map(str, f['first_seqs']))}}})"
                        for f in findings)
    found = []
    for capture in captures:
        for line in tshark(capture, "-Y", query, "-T", "fields", "-e", "frame.time_epoch", "-e", "icmp.ident",
                           "-e", "icmp.seq", "-E", "occurrence=f").splitlines():
            stamp, ident, seq = line.split("\t")
            if label := labels.get((ident, seq)):
                at = float((Decimal(stamp) * NS - zero) / NS)
                found.append((at - CONTEXT_S, at + CONTEXT_S, label))
    return found


def merged(windows):
    joined = []
    for start, end, reason in sorted(windows):
        if joined and start <= joined[-1]["to_s"]:
            joined[-1]["to_s"] = max(joined[-1]["to_s"], end)
            joined[-1]["reasons"].setdefault(reason)
        else:
            joined.append({"from_s": start, "to_s": end, "reasons": {reason: None}})
    return [{**window, "reasons": list(window["reasons"])} for window in joined]


def epoch(ns):
    return f"{ns // NS}.{ns % NS:09d}"


def utc(ns):
    return datetime.fromtimestamp(ns / NS, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def anonymous(info):
    # proof.tar.gz goes to outside parties: keep the local user out of the tar headers.
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def pack(run, result, captures):
    """Write run/proof.tar.gz: every capture cut to the windows around the failure evidence."""
    zero = baseline_ns(run)
    windows = merged(timed_evidence(result) + reflected_evidence(result, captures, zero))
    name = f"{run.parent.name}-{run.name}"
    with tempfile.TemporaryDirectory() as scratch:
        folder = Path(scratch) / name
        (folder / "captures").mkdir(parents=True)
        ranges = []
        for window in windows:
            begin, end = zero + round(window["from_s"] * NS), zero + round(window["to_s"] * NS)
            window.update(from_utc=utc(begin), to_utc=utc(end))
            ranges.append(f"(frame.time_epoch >= {epoch(begin)} && frame.time_epoch < {epoch(end)})")
        query = " || ".join(ranges)
        for capture in captures:
            target = folder / "captures" / capture.name
            if query:
                # -F pcap keeps the input format: pcapng would add the local host's OS and tool names.
                tshark(capture, "-Y", query, "-F", "pcap", "-w", str(target))
            else:
                shutil.copyfile(capture, target)
        (folder / "pcap.sha256").write_text("".join(f"{digest(capture)}  captures/{capture.name}\n"
                                                    for capture in sorted((folder / "captures").iterdir())))
        if (run / "pcap.sha256").exists():
            shutil.copyfile(run / "pcap.sha256", folder / "source.sha256")
        note = ("Seconds count from the run's baseline start, as in its timeline.tsv. pcap.sha256 lists these "
                "captures; source.sha256 lists the full captures, which were deleted after the run.")
        if not windows:
            note += " No failed check carried a time, so the captures are whole."
        (folder / "proof.json").write_text(json.dumps(
            {"run": "/".join(run.resolve().parts[-3:]), "case": result["case"], "status": result["status"],
             "windows": windows, "note": note}, indent=2) + "\n")
        partial = run / "proof.tar.gz.partial"
        with tarfile.open(partial, "w:gz") as archive:
            archive.add(folder, arcname=name, filter=anonymous)
        partial.replace(run / "proof.tar.gz")
    return windows


def prune(run):
    """Pack the proof of a failed run, then delete every run's bulk evidence and its TShark cache entries."""
    captures = sorted((run / "captures").glob("*.pcap"))
    if not captures:
        return f"{run}: no packet captures left"
    if not (run / "result.json").exists():
        return f"{run}: not evaluated, captures kept"
    result = json.loads((run / "result.json").read_text())
    line = f"{run}: {result['status']}, captures deleted"
    if result["status"] == "fail":
        windows = pack(run, result, captures)
        seconds = sum(window["to_s"] - window["from_s"] for window in windows)
        kept = f"{len(windows)} windows, {seconds:.1f} s" if windows else "whole captures"
        line += f", proof.tar.gz {(run / 'proof.tar.gz').stat().st_size / 1e6:.2f} MB ({kept})"
    for capture in captures:
        sha = digest(capture)
        for cached in (CACHE / sha[:2]).glob(f"{sha}-*"):
            cached.unlink()
    for folder in BULK:
        shutil.rmtree(run / folder, ignore_errors=True)
    return line


def keep_proof(run, result):
    """Runner hook after analyze(): prune the attempt but never let pruning end the suite."""
    try:
        print(prune(run), file=sys.stderr)
    except Exception as error:  # noqa: BLE001 - deletion only follows a written proof, so any failure keeps captures
        print(f"{run}: proof not written, captures kept: {error}", file=sys.stderr)
    return result


def attempt(run):
    try:
        return True, prune(run)
    except Exception as error:  # noqa: BLE001 - one run's failure must not stop the others
        return False, f"{run}: proof not written, captures kept: {error}"


def prune_all(path, jobs=None):
    """Prune every run below path that still has captures. Return whether all succeeded and one line per run."""
    runs = sorted({capture.parent.parent for capture in path.rglob("captures/*.pcap")})
    with ProcessPoolExecutor(jobs) as pool:
        outcomes = list(pool.map(attempt, runs, chunksize=1))
    return all(ok for ok, _ in outcomes), [line for _, line in outcomes]
