# Agent instructions

## Python tooling

Use `uv` for all Python work in this repository. Run project commands, tests, checks and Python subprocesses with `uv run`. Use `uv sync` for project dependencies and `uv run --no-project` for standalone scripts. Apply the same rule to operator examples and CI jobs.

## Numbers in write-ups

Counts of how often a fault showed, and loss ranges across runs, come only from `mlag-lab export`: the Faults across runs section of `results/README.md` and `results/index/faults.tsv`. Do not count by hand in notes, reports, tickets or forum posts. Quote the generated row at a pinned commit and name its lab, setup and case. If a write-up needs a count the export does not produce, add it to the export first.

## Live tests in parallel

Run independent live suites at the same time with `labs/parallel.sh`, never one after another. Run it inside the OrbStack VM from the worktree root, on lab instances 1 to 3, one campaign per instance, campaigns separated by `--`, with `--destroy`. Run at most 3 labs with cases in the VM at once, counting labs of other sessions. A fourth lab with cases distorts timing: at four labs, power-loss boots and bond member restorations that fell at the same moment in several labs stalled the probes for up to 508 ms. Check first that no other session is running a campaign, and never use instance 0 of a lab another session has deployed. Give each worktree its own `UV_PROJECT_ENVIRONMENT` and `MLAG_LABS_COPY`, because the defaults are shared by every checkout in the VM. Destroy only the labs you deployed, with the variables they were deployed with, and never with `containerlab destroy --name`.

```sh
pgrep -af "mlag-lab|campaign.sh"
sudo containerlab inspect --all
labs/parallel.sh --destroy \
  1 small /var/tmp/c-small-1 "baseline:--bridge-mode none --case baseline" -- \
  2 small /var/tmp/c-small-2 "baseline:--bridge-mode none --case baseline" -- \
  3 medium /var/tmp/c-medium-3 "stp-off:--case medium-stp-off-baseline"
```
