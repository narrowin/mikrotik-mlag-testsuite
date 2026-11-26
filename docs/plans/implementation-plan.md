# Implementation plan: Networka lab tests for the MLAG labs

This plan hands the remaining work to the next implementer. It is the only plan. The older notes in `docs/plans/` are history.

## Outcome

1. Networka `main` holds the test engine. `nw test run` runs a test on a containerlab lab and `nw test replay` judges a saved run again.
2. This repo holds only labs and tests. Each lab is one folder under `tests/`. One command starts the lab and one command runs a test.
3. Every test the operator still wants exists as a test file and has run live.
4. The old suite is deleted: `src/mlag_lab/`, `labs/` and the docs that describe them.
5. No working branch and no lab is left behind.
6. The colleague who brings up the Cumulus lab has a one-page start.

## State at hand-over

Filled in when the clean Small lab has run live. Until then nothing below "Work" has started.

| Part | Where | State |
| --- | --- | --- |
| Device checks, `nw intent run`, ping | Networka `main` | Done |
| Test engine (`labtest.py`, `lab.py`, `traffic.py`, `commands/test.py`) | Networka branch `lab-tests` | Being rebuilt for the clean setup |
| Clean Small lab and the bond member loss test | this repo, branch `codex/suite-yaml-intent`, `tests/small/` | Being built |
| Specification of the clean setup | [clean-setup-spec.md](clean-setup-spec.md) | Written, not proven live |
| What was carried over from the old suite and why it goes | [inherited-parts-audit.md](inherited-parts-audit.md) | Done |

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
- Live tests run with spanning tree off only.
- Text for people fits on one page. YAML is written in block style.
- Work lands on `main`. A branch is deleted as soon as it is merged.
- How to run labs side by side, and the limit of three labs, is in [AGENTS.md](../../AGENTS.md).

## Work

Each package is done when its "done when" line holds on `main` of both repos.

### 1. Close the clean Small lab

- Fix what the reviewers of the clean setup left open. The list is in the hand-over state above.
- Done when: a fresh lab starts with one command, the bond member loss test passes twice, both replays match, and a reviewer finds no duplicate, no unneeded line and no leftover.

### 2. Three more actions in the engine

- Packet loss and delay on a cable, a switch reboot, and a switch power loss.
- The commands and measured times are in `test-results/suite-yaml-verify/actions/research.md`. That file is not in git. Read it first.
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
- The limit for a cable that comes back. The specification sets 4 s.
