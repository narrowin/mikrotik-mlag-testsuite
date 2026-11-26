# Suite intent and device state: verification record

This record lists what was checked on branch `codex/suite-yaml-intent` before it went to `main`, and what was not.
The branch moves the case definitions into a YAML catalogue and moves every device-state read and check to Networka's intent layer.
[Device state and packet grading](../test-framework.md#device-state-and-packet-grading)

## Commits

| Commit | Content |
| --- | --- |
| 15b2960 | The suite before the YAML catalogue (old side of the comparisons). |
| 1964cc4 | Replayable YAML intent for SMALL-06 (SMALL-06 reference). |
| 3e2489b | All case definitions in the YAML catalogue. |
| a8ca74f | Each SMALL-06 rule in one place, and Networka's bridge-port check. |
| a5fa732 | SMALL-06 validation of `limit_s` and stream IDs. |
| 4763100 | Device state through Networka intent; the suite's text parsers deleted. The live-tested code commit. |
| 6ed3de9 | Docs only: the Small lab walkthrough and two doc fixes. |

Networka is pinned at f80876d, the commit the live waves ran.
Networka `main` is now at 8bceb5b, which adds docs and Linux error-message changes only.
The pin stays on f80876d.

## Evidence

The evidence is in `test-results/suite-yaml-verify/` of the branch worktree.
That folder is gitignored and is not published; it holds full packet captures.
Readers rerun the tests to get their own evidence.

- `offline/`, `offline-final/`: catalogue and replay checks on 3e2489b and a8ca74f, with the scripts in `offline-final/scripts/`.
- `networka-json/`: the Networka JSON reads on a live CHR (states 1 to 4) and probes 2 to 4.
- `networka-adopt/`: the gate comparison on the live JSON states and the Linux bond comparison, with scripts.
- `live/RECORD.md`: every live pass, with the exact commands.
- `live/final-4763100/`: the final live attempts with their captures, `w1-replay.txt` and `w2-replay.txt`.
- `/var/tmp/adopt-scratch/dryrun.py`: the offline dry run of every runner, outside the repository.

## Commands

Offline commands ran from the worktree root with `uv run --locked` and a project environment of their own.
Every replay used a fresh copy of the attempt and a `pcap.sha256` check before and after.

```sh
F=test-results/suite-yaml-verify/offline-final/scripts
A=test-results/suite-yaml-verify/networka-adopt/scripts
uv run --locked -q python $F/dump_cases.py > new.json   # and in the old tree, with its own environment
uv run --no-project python $F/compare_cases.py old.json new.json
uv run --locked -q python $F/roundtrip.py
uv run --locked python $A/compare_states.py
uv run --locked python $A/linux_bonds.py
uv run --locked python $A/probe_extra.py
uv run --locked python /var/tmp/adopt-scratch/dryrun.py OUT
uv run --locked mlag-lab export COPY_OF_RESULTS
uv run --locked mlag-lab --help
```

The live waves ran inside the OrbStack VM with uv 0.13.10 first in `PATH`, `UV_PROJECT_ENVIRONMENT=/var/tmp/syv-venv` and `MLAG_LABS_COPY=/var/tmp/syv-labs`:

```sh
labs/parallel.sh --destroy \
  1 small /var/tmp/syv/w1-small-link "link:--bridge-mode none --case carrier --case silent-lacp --case peer-link-loss --case silent-mobile --case carrier-flap" -- \
  2 medium /var/tmp/syv/w1-medium "medium:--case medium-stp-off-baseline --case medium-stp-off-reboot-secondary --case medium-stp-off-power-loss-primary --case medium-core-off-baseline" -- \
  3 medium-two-pair /var/tmp/syv/w1-two-pair "two-pair:--case two-pair-stp-off-baseline --case two-pair-stp-off-strict-baseline --case two-pair-stp-off-interpair-member-flap --case two-pair-stp-off-reboot-a-secondary"
labs/parallel.sh 1 small /var/tmp/syv/w2-small-direct "direct:--bridge-mode none --case direct-baseline --case direct-reboot-secondary --case direct-power-loss-primary" &
labs/parallel.sh --destroy 2 medium-pair-root /var/tmp/syv/w2-root-pair "root:--case root-calibrate --case reboot-secondary --case reboot-primary-no-fallback" &
wait
```

`live/RECORD.md` holds the teardown and the vrf ping commands.

## Verified offline

- Catalogue: 99 cases in the same order and 100 selectors with an identical map, against 15b2960 (checked on a8ca74f) and against a5fa732 (checked on 4763100). The only field that differs from a5fa732 is the SMALL-06 `expected_state`, which moved into the Small gate. All 99 cases round-trip through `save_case` and `recorded_case`.
- Old and new graders on a8ca74f: eight complete attempts gave the same exit and status on 15b2960 and a8ca74f. `result.json` and `timeline.tsv` were identical, apart from the added SMALL-06 report.
- Limit flips on a8ca74f: the SMALL-06 withdrawal `limit_s` 5.0 to 2.0 added the expected loss checks, and the calibration lower bound 1.9 to 2.2 turned the calibration check false and the status from pass to error.
- Gate on the live JSON states: steady and restored pass, as the old parser did, and 31 values per switch equal the old parser's. With ether3 down the gate fails on the ether3 member and on bridge port client1 not forwarding; the old parser shifted columns and missed the port. With ether3 returning, the member without an LACP partner is unverified.
- Linux bonds: 554 members in 277 distinct bonding texts from `results/` give the same member state and partner system ID as the old parser.
- Dry run: a stub Networka client answered from the live JSON captures and from replies in the captured shapes. Every runner's sampler, gate collection, gate save and evaluator ran for every gate combination without a crash: Small direct and link-fault with each bridge mode, root-pair with and without fallback, the 6 Medium setups and the 4 two-pair setups. It reproduces the `read_host_bonds` crash of the first live wave on 136b656.
- Export: `mlag-lab export` on a copy of the committed `results/` writes the same files as a5fa732 and grades nothing.
- An attempt saved with text state stops `mlag-lab evaluate` with one error and leaves its files unchanged.

## Networka live probes

- JSON reads in 4 states of a live Small lab (steady, ether3 down, ether3 returning, restored): every reply decoded, `compare.tsv` and `summary.tsv` in `networka-json/`.
- `nw intent run` and `nw intent replay` on the Small lab: 44 pass, 0 fail, 0 error in steady state, and 40 pass, 4 fail, 0 error with ether3 down. Replay gave the same results.
- Ping over SSH: the Linux ping passed against a reachable host and failed against an unreachable one, with the same results on replay. The first RouterOS ping parser expected a totals row, but RouterOS returns one row per probe and no totals row; Networka now counts the per-probe rows.
- vrf ping on 4763100: both CHRs pinged the other peer's management address with `vrf: mgmt` and passed, and the replay was identical.

## Final live validation on 4763100

Every attempt's `case-intent.yaml` equals the catalogue, and `pcap.sha256` checks.
For every saved gate, `nw intent replay` gives the saved verdict and exit code.
`mlag-lab evaluate` on a copy gives the live exit code and byte-identical `result.json` and `timeline.tsv` for all 20 attempts.
Baseline cases have no restored gate by design.

| Runner | Attempt | Verdict | Gates (baseline/restored) | Gate replay, evaluate identical |
| --- | --- | --- | --- | --- |
| Small link fault | bond-member-loss | fail (network) | pass/pass | yes |
| Small link fault | lacp-timeout | pass | pass/pass | yes |
| Small link fault | peer-link-loss | pass | pass/pass | yes |
| Small link fault | mac-age-relearn | pass | pass/pass | yes |
| Small link fault | member-flap-repeat | fail (network) | pass/pass | yes |
| Medium | medium-stp-off-baseline | pass | pass/– | yes |
| Medium | medium-stp-off-reboot-secondary | pass | pass/pass | yes |
| Medium | medium-stp-off-power-loss-primary | pass | pass/pass | yes |
| Medium | medium-core-off-baseline | error (evidence) | pass/– | yes |
| Medium | medium-core-off-baseline-retry | pass | pass/– | yes |
| Two-pair | two-pair-stp-off-baseline | pass | pass/– | yes |
| Two-pair | two-pair-stp-off-strict-baseline | pass | pass/– | yes |
| Two-pair | two-pair-stp-off-interpair-member-flap | pass | pass/pass | yes |
| Two-pair | two-pair-stp-off-reboot-a-secondary | pass | pass/pass | yes |
| Small direct | baseline | pass | pass/– | yes |
| Small direct | secondary-reboot | fail (network) | pass/pass | yes |
| Small direct | primary-power-loss | fail (network) | pass/pass | yes |
| Root-pair (RSTP) | root-calibrate | pass | pass/pass | yes |
| Root-pair (RSTP) | reboot-secondary | pass | pass/pass | yes |
| Root-pair (RSTP) | reboot-primary-no-fallback | fail (network) | pass/pass | yes |

The Medium core-off baseline error was the host observer: one poll took 1.65 s while three labs ran.
The runner repeated it once, and the retry passed.

## Network failures

Each failure is a packet finding with every gate passing.
The rows below are the exported `results/index/faults.tsv` rows at 6ed3de9, which hold the committed archives only, not these runs.

- bond-member-loss: flood frame 501 came back at its sender in restoration, seq 160. Row: `Small lab | STP off | MLAG bond member loss and return | Flood frame back at its sender or twice at a host | | 0 | 2`.
- member-flap-repeat: flood frames 501 and 502 came back at their sender. Row: `Small lab | STP off | Repeated MLAG bond member flap | Flood frame back at its sender or twice at a host | | 4 | 4`.
- secondary-reboot: flood frames 501 and 502 came back at their sender in withdrawal, seq 246 to 247. Row: `Small lab | STP off | MLAG secondary reboot | Flood frame back at its sender or twice at a host | | 2 | 2`.
- primary-power-loss: flood frames 501 and 502 came back at their sender in withdrawal, seq 425. Row: `Small lab | STP off | MLAG primary power loss | Flood frame back at its sender or twice at a host | | 0 | 2`.
- reboot-primary-no-fallback: streams 101 and 201 lost at least 12.1 s in withdrawal against 5 s, and 2 unicast requests of stream 201 came back to their sender, seq 260 to 261. Rows: `Medium lab | RSTP, MLAG pair is root, mlag-lacp-fallback=no | MLAG primary reboot | Loss over the limit | Primary down | 1 | 1` and `... | Unicast request sent back to its sender | | 1 | 1`.

bond-member-loss and primary-power-loss showed the flood-return fault for the first time in those cases.
One run cannot tell whether the fault became more frequent.

## Remaining gaps

- Attempts saved before 4763100 (attempt schema below 3, RouterOS text state) cannot be graded again; their saved verdicts stand.
- Two checks compare switches and stay in the suite, on the gates' saved replies: the Small lab's opposite MLAG roles and shared root, and the LACP system ID both MLAG peers present.
- Linux bond checks ran through nsenter and Networka's Linux normalizers, not through Networka SSH; ping over SSH was proven.
- A bond member without an LACP partner is unverified in Networka, so that item grades as an evidence error, not a fail.
- The two-pair inter-pair flap no longer records the bridge host table size; Networka has no collector for it.
- `mlag-lab export` keeps one regex, for the MLAG role in the committed text archives.
- The committed `results/index/phases.jsonl` was already stale in 4 rows before this branch.
- The runner has no option to keep captures; the replays relied on a hard-link watcher (`live/tools/shadow.py`).
- The runner re-executes itself as root, which leaves root-owned `__pycache__` in the venv, so a later `uv sync` needs `sudo chown -R` on the venv first.
- The VM needs uv 0.13.10 or later, which Networka's lock requires.
- Cumulus Linux has a section in Networka's intent guide but no platform module.
- Moving the probe and capture measurement into Networka is a possible next step; it has not been decided.
