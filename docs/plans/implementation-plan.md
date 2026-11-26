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

1. Phase 1: finish the clean Small lab and its cable test, plus the single switch reboot brought forward by the operator.
2. Stop. Report to the operator and wait. The operator walks through the run.
3. Phase 2, on the operator's go: bring the rest of the repo to the same form.

## Current state and execution record

On 26 November 2026 the operator moved both working checkouts to local `main` and brought one switch reboot into the Small prototype. The remaining actions and test packages still require the walkthrough and the operator's go.

| Part | Checkout or evidence | State |
| --- | --- | --- |
| Networka engine | `/Users/md/git/narrowin/networka`, local `main` at `f782c39` | Includes the previous engine and merge. Phase 1 edits are in progress. Remote publication awaits review and live proof. |
| Small lab | `/Users/md/git/narrowin/mlag-suite-yaml`, local `main` at `a324af6` | Work in `tests/small/` only. Branch switch preserved the three startup/README edits byte-for-byte. |
| Previous worktrees and branches | [Handover plan at a324af6](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/a324af6/docs/plans/implementation-plan.md) | The three retired Networka worktrees have been audited. The progress note is copied and hash-verified outside them. |
| Review findings | [70 decisions and verification status](clean-setup-open-findings.md) | Wrong-result findings were examined first. Live comparisons and independent verification are in progress. |
| Evidence | `test-results/suite-yaml-verify/clean/phase1-close/` | Keep command output, raw device observations, verdicts and replay comparisons here or under the README-generated run directory. |
| Lab ownership | OrbStack VM `mlag-external` | Only the Small instance started for this prototype is in scope. |

The times below are Europe/Zurich. Evidence paths are relative to the phase 1 evidence directory unless specified. A named verifier is the person or agent who actually checked that entry.

| Time | Work and outcome | Implemented / verified by | Command and output |
| --- | --- | --- | --- |
| 13:07 | Starting Small from an absent generated directory succeeded in 52.126 s. The six nodes ran and both switches were healthy. | Lab author / VM operator | `01-startup-checks.log`, `01-start-live.log` |
| 13:08 | The README run and replay each exited 0. SHA-256 matched across all 28 evidence files. | Lab author / VM operator | `02-readme-live.log`, `02-files-before.sha256`, `02-files-after.sha256` |
| 13:10 | Both local main branches fast-forwarded. The preserved progress note and original have identical SHA-256. | Engine and lab authors / coordinator checked the transcripts | `engine-local-main.console`, `03-lab-local-main.log`, `03-networka-retired-worktrees.log` |
| 13:14 | The production loader confirmed the same ten device preconditions, two streams and four cable steps. Saved RouterOS logs support the heartbeat warning. | Lab author / Networka loader and VM operator | `03-lab-findings-checks.log`, `03-warning-sources.log` |
| 13:16 | A collector file absent at the start was created during the run. The test and replay passed. | Engine author / VM operator | `03-fresh-collector.log` |
| 13:17 | An interrupt during a cable hold saved the restored port's up log before the end markers. The interrupted run exited 130 and replay judged the evidence as error. | Engine author / VM operator and lab reviewer | `03-interrupt-repeat.log` |
| 13:19 | The pinned collector rejected an imudp input without an explicit port. Restoring port 514 allowed the cable test and replay to pass on deployment A. | VM operator / lab reviewer | `03-imudp-diagnostic.log`, `03-run-a.log` |
| 13:20 | Named switch1 reboot settings were fixed before the trial. The adapter uses a single pooled command and the production loader recognises both the new reboot and the previous cable actions. | Lab and engine authors / lab reviewer | `03-scope-and-review-checks.log`, `03-reboot-lab-checks.log`, `03-reboot-platform-checks.log` |
| 13:22 | In deployment B the other nodes received different addresses while the collector retained .10. Removing the collector's syslog tag lost the marker proof. The reviewer raised a stale-topology target-address check before live reboot. | VM operator and lab reviewer / engine author assigned the target check | `03-deploy-b.log`, `03-run-b.log` |
| 13:23 | Restoring the collector's tag let deployment B pass with byte-identical replay. Independently recomputing the three handover runs preserved both passes and the cable precondition failure. | VM operator and engine author / lab reviewer | `03-run-b-with-tag.log`, `03-independent-legacy-replay.log` |
| 13:24 | With all cable steps passing, the closing window caught 6 lost pings from client2 to client3 at one ping every 100 ms, a stop of 0.537 to 0.744 s. Run and replay exited 1 with identical evidence hashes. | VM operator / Sol lab reviewer | `03-closing-loss.log`, `03-closing-loss-before.sha256`, `03-closing-loss-after.sha256` |
| 13:27 | The README candidate cable run and replay passed. The lab reviewer independently recomputed the result and rebuilt an identical report. | VM operator / Sol lab reviewer | `04-candidate-cable.log`, `04-sol-candidate-cable.log`, `test-results/small/run.Jt6mOx/bond-member-loss/` |
| 13:28 | Native uptime proved a new switch1 boot and full lab health returned after 24.002 s. Live and replay gave error with an identical report. The collector had no switch1 end marker, and five different requests reused ping sequence 192 on client2. | VM operator / Sol lab reviewer | `04-candidate-reboot.log`, `test-results/small/run.ugqwRq/switch-reboot/` |
| 13:30 | The switch1 memory log contains the end marker. The collector captured none of its post-boot lines. The switch still has its management address, route and configured remote logging action. | VM operator / Sol lab reviewer | `04-reboot-diagnosis.log` |
| 13:31 | Switch1 reached the collector over its management VRF. Neither the switch management capture nor the collector saw syslog UDP from it. Switch2 delivered its diagnostic markers. | VM operator / Sol lab reviewer | `04-reboot-udp-probe.log` |
| 13:32 | The offline judge named switch2 as unverified when the real cable log was checked with only switch1 expected. It also recorded the missing marker support when the deployed Linux client2 was declared a target. | Sol lab reviewer | `04-sol-w4-offline.log` |
| 13:33 | With the original config unchanged after the test, switching the remote logging action to the main VRF and back to the management VRF restored UDP delivery from switch1. | VM operator / Sol lab reviewer | `04-reboot-action-toggle-retry.log` |
| 13:33 | Rejudging the first reboot distinguished repeated sequences by their ICMP payloads. The original sequence-only loss counts were invalid. For client1 to client2, 7 lost pings at one ping every 100 ms meant a stop of 0.623 to 0.832 s. For client2 to client3, 6 lost pings at that cadence meant a stop of 0.514 to 0.718 s. Source intervals peaked at 112.194 ms and 111.310 ms. The missing end marker still invalidated the run. | Sol engine author / VM packet capture and Sol lab reviewer | `04-engine-replay.log`, `04-reboot-sender-diagnosis.log` |
| 13:35 | A disposable startup scheduler restored switch1's logs after a typed reboot. Both end markers arrived. Live and replay passed with identical result and report bytes. After removing that lab, the lab author put the working scheduler in the startup configuration. | VM operator / Sol lab reviewer | `04-boot-scheduler-live.log`, `test-results/small/run.2Rn1KE/switch-reboot/` |
| 13:36 | Independent engine review accepted the candidate timestamp and payload handling, report and reboot proof for the Small lab. Three historical results and the disposable reboot recomputed to the saved bytes. The 16 existing lab, traffic and intent tests and the strict guide build passed. | Sol lab reviewer | `04-sol-engine-local-checks.log`, `04-sol-engine-evidence-checks.log` |

Sol took over the Phase 1 handoff on local main, with separate lab, engine and VM roles. Sol High continued the lab review after the candidate runs.

The next checkpoint is a fresh candidate reboot with working log coverage and valid ping measurements in both directions. Then verify the final cable passes and replays, the fail with an untouched cable, and the stopped-collector error on the coordinated local main commits. Complete the walkthrough and bring publication and cleanup to the operator.

### Named switch reboot brought forward

Reboot only `switch1` of the owned Small lab, independent of its elected role. Both streams traverse dual-attached clients and may use that switch. Before running the test the operator's coordinator set a provisional 4 s outage limit per stream, allowing one fast LACP timeout plus one message interval. Keep its measured verdict at that limit. Allow 60 s for boot and health recovery, covering the previous 21 s recovery, a possible 30 s SSH login cooldown and a 5 s retry. After recovery observe another 5 s, longer than one fast LACP timeout.

The RouterOS adapter issues one typed background reboot through the pooled client. Prove a new boot from native uptime before and after, including elapsed time since dispatch. Retain the samples and the successful recovery-state evidence for replay. See the retained research in `test-results/suite-yaml-verify/actions/research.md`, section 2, and its two raw timelines.

## Previous live evidence

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

The evidence is in `test-results/suite-yaml-verify/clean/live-round1/`, which is not in git. `commands.txt` there holds the commands as they ran. That handover run was torn down.

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
8. Publish the validated local main commits in both repositories as fast-forwards after the operator approves. The earlier handover branches have already been integrated locally. Check that the published engine and lab revisions are the ones proven live.
9. Clean up. Delete the branches `lab-tests`, `merge-main` and `codex/lab-access` in Networka with their worktrees, and `codex/suite-yaml-intent` here. The worktree `networka.worktrees/lab-access` holds the untracked file `docs/development/lab-tests-plan.md`, the progress log of the earlier work. Move it out before you delete the worktree, and do not add it to git. Destroy the lab.
10. Update the state table of this plan.

Done when: step 6 holds on what is on `main` in both repos, and a reviewer finds no duplicate, no unneeded line and no leftover in `tests/small/`.

## Stop

After phase 1, stop and report: the verdicts, the measured stops with their ping interval, what was fixed, what was rejected and why, and what is not verified. Do not start phase 2. The operator walks through the run first and then gives the go.

## Phase 2: the rest of the repo

Each package is done when its "done when" line holds on `main` of both repos.

### 2. Remaining engine actions after the walkthrough

- Packet loss and delay on a cable and switch power loss remain here. One RouterOS reboot of switch1 on the Small lab was brought forward to phase 1.
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
