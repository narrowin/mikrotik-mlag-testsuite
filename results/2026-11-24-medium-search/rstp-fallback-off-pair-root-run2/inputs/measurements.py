"""Collect the per-phase loss measurements of every saved run into one table."""

import csv
import json
from pathlib import Path

COLUMNS = ("suite", "run", "case", "bridge_mode", "status", "phase", "phase_start_s", "phase_end_s", "limit_s",
           "verdict", "stream", "role", "loss_lower_s", "loss_upper_s", "lost_probes")


def rows(campaign):
    for result_file in sorted(campaign.glob("*/*/result.json")):
        result = json.loads(result_file.read_text())
        for phase in result.get("phases", []):
            window = phase.get("window_s") or [None, None]
            base = {"suite": result_file.parent.parent.name, "run": result["run"], "case": result.get("name"),
                    "bridge_mode": result.get("bridge_mode"), "status": result["status"], "phase": phase["name"],
                    "phase_start_s": window[0], "phase_end_s": window[1], "limit_s": phase["limit_s"],
                    "verdict": phase["verdict"]}
            losses = [("graded", ident, loss) for ident, loss in phase["loss_s"].items()]
            losses += [("control", ident, loss) for ident, loss in phase["control_loss_s"].items()]
            if not losses:
                yield {**base, "stream": "", "role": "", "loss_lower_s": 0, "loss_upper_s": 0, "lost_probes": 0}
            for role, ident, loss in losses:
                yield {**base, "stream": ident, "role": role, "loss_lower_s": loss["lower_s"],
                       "loss_upper_s": loss["upper_s"], "lost_probes": loss["lost_probes"]}


def write_measurements(campaign):
    """Write measurements.tsv in a campaign folder and return its path."""
    path = campaign / "measurements.tsv"
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows(campaign))
    return path


if __name__ == "__main__":
    import sys
    for folder in sys.argv[1:]:
        print(write_measurements(Path(folder)))
