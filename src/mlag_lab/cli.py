"""Operator entry point for live attempts and offline replay."""

from datetime import datetime, timezone
from enum import Enum
import os
from pathlib import Path
import shutil
import sys
from typing import Annotated

import typer

from .direct_topology import DIRECT_CASES
from .evaluate import replay
from .legacy import CASE_NAMES, CASES
from .root_topology import MEDIUM_TARGETS, ROOT_CASES
from .two_pair_topology import TWO_PAIR_TARGETS

app = typer.Typer(no_args_is_help=True)
LABS = Path(__file__).resolve().parents[2] / "labs"

# Descriptive Small lab names first. The internal selectors stay accepted.
Case = Enum("Case", {name: name for name in (*CASE_NAMES, *CASES, *ROOT_CASES, *MEDIUM_TARGETS, *DIRECT_CASES,
                                               *TWO_PAIR_TARGETS)},
            type=str)


class BridgeMode(str, Enum):
    rstp = "rstp"
    none = "none"
    mstp = "mstp"


@app.command()
def run(
    output: Annotated[Path | None, typer.Option(
        help="Fresh evidence directory. Defaults to test-results/<UTC time> in the current directory.")] = None,
    lab_dir: Annotated[Path, typer.Option(
        help="labs/ folder of the checkout that deployed the topology.")] = LABS,
    case: Annotated[list[Case] | None, typer.Option(help="Select one or more cases.")] = None,
    repeat: Annotated[int, typer.Option(min=1)] = 1,
    username: Annotated[str, typer.Option()] = "admin",
    bridge_mode: Annotated[BridgeMode, typer.Option(
        help="Spanning tree protocol-mode on both Small lab MLAG peers.")] = BridgeMode.rstp,
):
    """Run cases on the dedicated Linux lab host."""
    from .run import run_suite, select_topology
    cases = [CASE_NAMES.get(item.value, item.value) for item in case or []]
    try:
        select_topology(cases, bridge_mode.value)
        if output is None:
            output = Path("test-results") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output, lab_dir = output.resolve(), lab_dir.resolve()
        if sys.platform == "linux":
            if os.geteuid() != 0:
                restart_as_root(output, lab_dir, cases, repeat, username, bridge_mode.value)
        status = run_suite(lab_dir, output, cases, repeat, username, bridge_mode.value)
    except (OSError, ValueError) as error:
        typer.echo(str(error), err=True)
        status = 2
    raise typer.Exit(status)


def restart_as_root(output, lab_dir, cases, repeat, username, bridge_mode):
    """Run this command again under sudo with the same interpreter, absolute paths and uv settings."""
    uv = os.environ.get("UV") or shutil.which("uv")
    if uv:
        # The runner calls uv inside the lab namespaces, where sudo's PATH may not find it.
        os.environ["UV"] = os.path.abspath(uv)
    arguments = ["--output", str(output), "--lab-dir", str(lab_dir), "--repeat", str(repeat),
                 "--username", username, "--bridge-mode", bridge_mode]
    for name in cases:
        arguments += ["--case", name]
    preserved = ",".join(name for name in ("MLAG_SSH_PASSWORD", "UV_PROJECT_ENVIRONMENT", "UV") if name in os.environ)
    os.execvp("sudo", ["sudo", *([f"--preserve-env={preserved}"] if preserved else []),
                       sys.executable, "-m", "mlag_lab.cli", "run", *arguments])


@app.command()
def evaluate(evidence: Annotated[Path, typer.Argument(help="Evidence suite or one saved attempt.")]):
    """Rebuild JSON verdicts, timelines and JUnit from saved evidence."""
    try:
        status = replay(evidence)
    except (OSError, ValueError) as error:
        typer.echo(str(error), err=True)
        status = 2
    raise typer.Exit(status)


@app.command()
def export(
    results: Annotated[Path, typer.Argument(help="results/ folder with one folder per campaign.")] = Path("results"),
    output: Annotated[Path | None, typer.Option(help="Output folder. Defaults to <results>/index.")] = None,
):
    """Write phases.jsonl, streams.tsv and schema.md: one structured record per run and phase."""
    from .export import write_export
    try:
        folder, count = write_export(results, output)
        if output is None:
            # The summary and the README section read <results>/index, so skip them for another output folder.
            from .summary import write_summary
            from .overview import write_overview
            write_summary(results)
            write_overview(results)
    except (OSError, ValueError, KeyError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(2)
    typer.echo(f"{folder}: {count} phase rows")


def main():
    app()


if __name__ == "__main__":
    main()
