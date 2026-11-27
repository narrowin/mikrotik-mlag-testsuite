# Agent instructions

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
