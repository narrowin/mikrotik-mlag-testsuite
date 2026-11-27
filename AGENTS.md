# Agent instructions

## Words and decisions

- [GLOSSARY.md](GLOSSARY.md) gives the one word for each thing in this repo. Read it before writing a test, a report or any text, use its terms, and never use a word on an _Avoid_ line. If a term is missing or disputed, ask the operator instead of inventing one.
- [docs/adr/](docs/adr/) records why the repo is shaped as it is. Read the matching ADR before changing what it covers, and do not reopen a decision without new evidence. A decision that is hard to reverse, surprising without context and the result of a real trade-off gets a new ADR.

## Dictated words

The operator dictates. Read these speech-to-text forms as the real names, and write only the real names. Do not treat them as competing terms.

- networker, NetWorker, network (the tool) → Networka; scrapy → Scrapli; PyPy, Pipe → PyPI
- MLEG, M-LAG → MLAG; RootOS → RouterOS; Microtics, microtech, MyCritic, microtik → MikroTik
- RSDP → RSTP; Spanky → spanning tree; 7:26, 726 → 7.26
- tuple lab, medium 2 pair → two-pair lab; simple app, small app → Small lab; lamps → labs
- Container Lab → containerlab; dryo, draw IO → draw.io; NView → NVUE

## Python tooling

Use `uv` for all Python work in this repository. Run project commands, tests, checks and Python subprocesses with `uv run`. Use `uv sync` for project dependencies and `uv run --no-project` for standalone scripts. Apply the same rule to operator examples and CI jobs.

## Numbers in write-ups

Counts of how often a fault showed, and loss ranges, come only from the `nw test` reports (`report.md` and `result.json`) of the named runs. Do not count by hand in notes, reports, tickets or forum posts. Name the lab, the test and the runs. `results/` is the frozen record of the old `mlag-lab` suite; quote it only as that, at a pinned commit.

## Live tests in parallel

Run live tests in the OrbStack VM as described in [Run a lab](docs/tests/README.md#run-a-lab). At most three labs with tests may run in the VM at once, counting the labs of other sessions. A fourth lab distorts the timing of every lab. Check first what is running and deployed. Touch no lab you did not start, and destroy only your own labs with their topology file.

```sh
pgrep -af "nw test"
sudo containerlab inspect --all
```
