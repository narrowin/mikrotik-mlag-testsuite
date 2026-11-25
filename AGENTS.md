# Agent instructions

## Python tooling

Use `uv` for all Python work in this repository. Run project commands, tests, checks and Python subprocesses with `uv run`. Use `uv sync` for project dependencies and `uv run --no-project` for standalone scripts. Apply the same rule to operator examples and CI jobs.

## Numbers in write-ups

Counts of how often a fault showed, and loss ranges across runs, come only from `mlag-lab export`: the Faults across runs section of `results/README.md` and `results/index/faults.tsv`. Do not count by hand in notes, reports, tickets or forum posts. Quote the generated row at a pinned commit and name its lab, setup and case. If a write-up needs a count the export does not produce, add it to the export first.
