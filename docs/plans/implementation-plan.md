# Implementation plan: Networka lab tests for the MLAG labs

This plan hands the work to the next implementer. It is the only plan. The older notes in `docs/plans/` are history.

## Outcome

1. Networka `main` holds the test engine. `nw test run` runs a test on a containerlab lab and `nw test replay` judges a saved run again.
2. This repo holds only labs and tests. Each lab is one folder under `tests/`. One command starts the lab and one command runs a test.
3. Every test the operator still wants exists as a test file and has run live.
4. The old suite is deleted: `src/mlag_lab/`, `labs/` and the docs that describe them.
5. No working branch and no lab is left behind.
6. The colleague who brings up the Cumulus lab has a one-page start.

## Order of work

1. Phase 1: finish and validate the prototype, the clean Small lab with one test.
2. Stop. Report to the operator and wait. The operator walks through the run.
3. Phase 2, on the operator's go: bring the rest of the repo to the same form.

## State at hand-over, 26 November 2026, 13:00

| Part | Where | State |
| --- | --- | --- |
| Device checks, `nw intent run`, ping | Networka `origin/main`, `e0c71bf` | Done and pushed |
| Test engine | worktree `/Users/md/git/narrowin/networka.worktrees/lab-tests`, branch `lab-tests`, `95c23b7`, pushed | Ran live on the clean lab. Not reviewed |
| Engine merged with Networka `main` | worktree `/Users/md/git/narrowin/networka.worktrees/merge-main`, branch `merge-main`, `f782c39`, pushed | Conflicts resolved. Ruff, mypy and 1,121 unit tests pass. Not on `main` |
| Clean Small lab and its test | worktree `/Users/md/git/narrowin/mlag-suite-yaml`, branch `codex/suite-yaml-intent`, folder `tests/small/` | Ran live. Findings open |
| This repo's `main` | `origin/main`, `3e96460` | Does not have the clean lab yet |
| Specification of the clean lab | [clean-setup-spec.md](clean-setup-spec.md) | Applied |
| Review findings | [clean-setup-open-findings.md](clean-setup-open-findings.md) | 70 open. None is checked or fixed |
| What was carried over from the old suite | [inherited-parts-audit.md](inherited-parts-audit.md) | Done |

What the live run showed, with Networka `95c23b7` and this repo at `31f19a5`. Every stream sent one ping every 100 ms.

- `start.sh` failed at first, because the folder `tests/small/clab-small-mlag/syslog` did not exist. After it was created by hand, the lab started in 52 s.
- The test passed twice, in 33 s each. The replay gave the same `result.json` and the same `timeline.tsv`.
- Cable from client 1 to switch 1 down and back: no ping lost in either run.
- Cable from client 1 to switch 2 down: 0 and 1 lost pings, at most 0.21 s. Limit 1 s.
- Cable from client 1 to switch 2 back: 24 lost pings in both runs, 2.40 to 2.60 s. Limit 4 s.
- The stream from client 2 to client 3 lost no ping.
- Each switch sent 6 log lines per run, and every log rule passed.
- With one cable taken down by hand, the state check failed, no cable was changed and the verdict was fail.
- Not run: the check that a stopped collector gives the verdict error.
- The run command in the README is not the one that ran. The run added `--locked` and `UV_PROJECT_ENVIRONMENT`.

The evidence is in `test-results/suite-yaml-verify/clean/live-round1/`, which is not in git. `commands.txt` there holds the commands as they ran. No lab of this work is running.

## Guardrails

- Use `uv` for all Python. Networka needs uv 0.13.10. In the VM it is in `/var/tmp/pt1-tools`.
- Live tests run only in the OrbStack VM `mlag-external` (`orb -m mlag-external ...`, the repo paths are the same there) and only with spanning tree off. [AGENTS.md](../../AGENTS.md) holds the rules for labs, with the limit of three labs at once.
- Touch no lab you did not start. `mlag-medium` belongs to another session.
- Do not touch the checkout `/Users/md/git/narrowin/mikrotik-mlag-testsuite`. It holds uncommitted work of another task. Do not touch the untracked files in `/Users/md/git/narrowin/networka`.
- Do not change the old suite before package 5. Reading it is fine.
- Commit only your own files, by explicit path. A commit body says why, what changed, how it was verified and what is not covered. No AI attribution.
- Never commit captures or archives. Evidence stays under `test-results/`.
- Add no new unit test file, mock or fixture unless the operator asks for it.
- A step is done only with its command and output saved as evidence. Say plainly what is not verified.
- For a choice between real alternatives, give one recommendation with its reasons. Ask before anything that is hard to undo.
- Push to `main` only what has run live. Delete a branch as soon as it is merged.

## Rules for every file

1. It stands on its own. No file reads or mentions the old suite.
2. Each fact is written once.
3. Every line is needed. Removing it changes a result, breaks the run, or takes away evidence a person needs.
4. No manual steps. The lab boots in the state the test needs.
5. Every number has its reason next to it.
6. Plain names and one word per thing: ping, stream, cable, switch, client.
7. A change counts as done when it has run live and the replay gives the same result.
8. A count of lost pings is always shown with the ping interval and the time it stands for.
9. Every stream says which way it goes.

## Decisions that hold

- Networka is the engine. A lab repo holds only the topology, the start configuration, the test files and the limits.
- Networka reaches lab nodes over SSH. It does not check or store host keys in a lab.
- Networka pushes no configuration during a test. The start configuration brings the lab into the right state, and every test checks that state before it acts.
- The lab part supports containerlab only.
- Device output is read as structured data where the device offers it.
- The switch logs are collected by one syslog node, saved with every run and read by the judge.
- Text for people fits on one page. YAML is written in block style.

## Phase 1: finish and validate the prototype

### 1. Close the clean Small lab

Do the steps in this order.

1. Make `tests/small/start.sh` start the lab from a clean checkout with no step by hand. Add `tests/*/clab-*/` to `.gitignore`.
2. Make the commands in `tests/small/README.md` the ones that run as written.
3. Work through [clean-setup-open-findings.md](clean-setup-open-findings.md), the part "wrong-results" first. Check each finding against the files. Fix it, or reject it with one sentence on what it would break. Where a finding needs a live run, remove the line and run the test.
4. Replace `timeline.tsv` by one generated `report.md` per run. It starts with the verdict. Then it shows, per step and stream, the limit against the measured stop, with the lost pings and the ping interval. Then the log rules, each with the line that satisfied it. Then what happened when, in words: state checks, step starts, cable confirmed down or up, stream stops and switch log lines. `nw test replay` builds it again. The data for programs stays in `result.json`, `events.jsonl` and `syslog.log`.
5. Bring `docs/development/lab-tests-design.md` in Networka up to date, or delete it. It still describes numbered streams and a baseline test.
6. Prove everything on a fresh lab. The lab starts with one command. The test passes twice and both replays give the same files. A cable taken down by hand gives fail with no cable changed. A stopped collector gives error.
7. Write `docs/walkthrough-networka-tests.md` again from that run, on one page.
8. Merge. In Networka, merge `lab-tests` into `merge-main` again, run the checks and push it to `origin/main` as a fast-forward. In this repo, push the branch to `origin/main` as a fast-forward and switch this worktree to `main`.
9. Clean up. Delete the branches `lab-tests`, `merge-main` and `codex/lab-access` in Networka with their worktrees, and `codex/suite-yaml-intent` here. The worktree `networka.worktrees/lab-access` holds the untracked file `docs/development/lab-tests-plan.md`, the progress log of the earlier work. Move it out before you delete the worktree, and do not add it to git. Destroy the lab.
10. Update the state table of this plan.

Done when: step 6 holds on what is on `main` in both repos, and a reviewer finds no duplicate, no unneeded line and no leftover in `tests/small/`.

## Stop

After phase 1, stop and report: the verdicts, the measured stops with their ping interval, what was fixed, what was rejected and why, and what is not verified. Do not start phase 2. The operator walks through the run first and then gives the go.

## Phase 2: the rest of the repo

Each package is done when its "done when" line holds on `main` of both repos.

### 2. Three more actions in the engine

- Packet loss and delay on a cable, a switch reboot, and a switch power loss.
- The commands and measured times are in `test-results/suite-yaml-verify/actions/research.md`. That file is not in git. Read it first.
- Measured on RouterOS 7.26beta7: packet loss and delay work with `tc qdisc ... netem` inside the node's network namespace and only affect traffic that leaves the interface. `containerlab tools netem` exits with an error on this kernel.
- Measured: `:execute {/system reboot}` reboots a switch without a prompt. SSH answers again after 17 to 18 s, and the lab is healthy after about 20 s.
- Measured: RouterOS refuses password logins for about 30 s after a quick series of SSH logins. The engine must keep its SSH connections open and must not log in again for every command.
- Not measured: power loss. The prepared script is `power-qmp.sh` in the same folder.
- Found on the way: at 100 % packet loss on one cable the switch kept sending to the client on that cable, and every ping was lost for the 25 s of the trial, at one ping every 100 ms. This needs its own test.
- Each action gets one test on the Small lab.
- Done when: each test has run live, the engine proves that the action took effect, and the test waits for the healthy state before it ends.

### 3. The remaining tests of the Small lab

- The old cases are in `src/mlag_lab/cases.py` and [case-catalog.md](../case-catalog.md). Only the cases with spanning tree off count.
- First write the list of fault kinds, one line each, and ask the operator which ones are wanted.
- Done when: every wanted kind is one test file that has run live.

### 4. The Medium and Large labs

- Build `tests/medium/` and `tests/large/` the way `tests/small/` is built. Do not copy `labs/medium/` or `labs/large/`.
- Done when: each lab starts with one command and its wanted tests have run live.

### 5. Delete the old suite

- Delete `src/mlag_lab/`, `labs/`, the entry points in `pyproject.toml` and the docs that describe them.
- Done when: `git grep mlag_lab` finds nothing and the README describes only the new way.

### 6. One-page start for the Cumulus lab

- The facts are in `test-results/suite-yaml-verify/cumulus/research.md`. That file is not in git. None of them is tested on a device.
- The page says how a lab folder is built, how to add the Cumulus platform to Networka, and which commands give the state as JSON on Cumulus Linux 5.11.
- It names the open points: `nv show mlag -o json` returns plain text on 5.11.3 to 5.11.5, and the containerlab kind needs KVM.
- Done when: the page is in the Networka docs and every command on it is marked as tested or not tested.

### 7. Review of the engine

- One independent review of `labtest.py`, `lab.py`, `traffic.py` and `commands/test.py` for a wrong pass, for lost evidence and for a replay that differs from the run.
- Done when: every finding is fixed or rejected with a reason.

## What the operator still decides

- Which old cases are still wanted (package 3).
- What happens to `results/`, the archived runs of the old suite.
- Whether `labtest.py` gets unit tests.
- The limit for a cable that comes back. The specification sets 4 s, and the runs measured 2.40 to 2.60 s.
