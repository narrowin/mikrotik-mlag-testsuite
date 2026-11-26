"""Replay every saved campaign in one process pool and list what changed against the result.json files on disk."""

import json

from .evaluate import analyze_all, attempt_folders, require_replayable, write_summaries


def campaigns(results):
    return [path for path in sorted(results.iterdir()) if path.is_dir() and next(path.rglob("pcap.sha256"), None)]


def verdict(path):
    file = path / "result.json"
    if not file.exists():
        return None, set()
    result = json.loads(file.read_text())
    return result["status"], {(check["level"], check["ok"], check["detail"]) for check in result["checks"]}


def verify(results, jobs=None):
    """Return the changed runs as text lines: status before and after, then each check that appeared or went."""
    folders = {campaign: attempt_folders(campaign) for campaign in campaigns(results)}
    # A pruned run has no captures left to replay.
    runs = [run for group in folders.values() for run in group if any((run / "captures").glob("*.pcap"))]
    require_replayable(runs)
    before = {run: verdict(run) for run in runs}
    analyze_all(runs, jobs)
    for campaign in folders:
        write_summaries(campaign)
    lines = []
    for run in runs:
        (old, old_checks), (new, new_checks) = before[run], verdict(run)
        if (old, old_checks) == (new, new_checks):
            continue
        lines.append(f"{run.relative_to(results)}: {old} -> {new}")
        lines += [f"  - {level} {'ok' if ok else 'not ok'}: {detail}" for level, ok, detail in sorted(old_checks - new_checks)]
        lines += [f"  + {level} {'ok' if ok else 'not ok'}: {detail}" for level, ok, detail in sorted(new_checks - old_checks)]
    changed = sum(1 for line in lines if not line.startswith("  "))
    lines.append(f"{len(runs)} runs in {len(folders)} campaigns replayed, {changed} changed")
    return changed, lines
