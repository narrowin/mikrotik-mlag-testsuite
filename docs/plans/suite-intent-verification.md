# Suite intent in YAML: verification record

This record lists what was checked on branch `codex/suite-yaml-intent` before it went to `main`, and what was not.

## Commits

- 15b2960: the suite before the YAML catalogue (old).
- 1964cc4: replayable YAML intent for SMALL-06 (SMALL-06 reference).
- 3e2489b: all case definitions in the YAML catalogue.
- a8ca74f: each SMALL-06 rule in one place, and Networka's bridge-port check.
- The commit that adds this record: SMALL-06 validation of `limit_s` and stream IDs, and the hint for an outdated `case-intent.yaml`.
- Networka: git commit 8409e4a (0.4.1), resolved from `uv.lock`.

## Evidence

The evidence is in `test-results/suite-yaml-verify/` of the branch worktree.
That folder is gitignored and is not published; it holds full packet captures.
Readers rerun the tests to get their own evidence.

- `offline/README.md`: offline checks on 3e2489b.
- `offline-final/README.md`: offline checks on a8ca74f, with the scripts in `offline-final/scripts/`.
- `live/RECORD.md`: live pass 1 on 3e2489b and the final live pass on a8ca74f.
- `live/final-a8ca74f/`: the final live attempts with their captures merged back.

## Commands

Every branch command ran from the worktree root with `UV_PROJECT_ENVIRONMENT=/var/tmp/uvenv-new uv run --locked`.
The 15b2960 tree ran in its own folder with `UV_PROJECT_ENVIRONMENT=/var/tmp/uvenv-old`.
Every replay used a fresh copy of the attempt, an empty `MLAG_TSHARK_CACHE`, and a `pcap.sha256` check before and after.

```sh
F=test-results/suite-yaml-verify/offline-final/scripts
uv run --locked -q python $F/dump_cases.py > old.json   # in the 15b2960 tree, with uvenv-old
uv run --locked -q python $F/dump_cases.py > new.json
uv run --no-project python $F/compare_cases.py old.json new.json
uv run --locked -q python $F/roundtrip.py
while read label src; do $F/replay.sh $label /path/to/main/checkout/$src & done < $F/inputs.txt; wait
uv run --no-project python $F/cmp.py $F/inputs.txt
$F/flip.sh s06-outage ATTEMPT "d['phases'][0]['limit_s'] = 2.0"
$F/flip.sh calibration ATTEMPT "d['grading_limits']['calibration_cut_s'][0] = 2.2"
$F/pruned.sh
$F/errors.sh
uv run --locked mlag-lab write-intent COPY
uv run --locked mlag-lab evaluate COPY
uv run --locked mlag-lab --help
```

Live runs used `labs/parallel.sh --destroy` inside the OrbStack VM on instances 1 to 3; `live/RECORD.md` holds the exact lines.

## Case catalogue

The catalogue on the branch matches 15b2960: 99 cases in the same order, 100 selectors with an identical map, 891 field comparisons with 0 differences, and 146 phases on both sides.
The suite limits equal the old constants: calibration cut 1.9 to 2.3 s, outside flood 1.0 s, MAC relearn 1.0 s.
All 99 cases round-trip through `save_case` and `recorded_case` with 0 mismatches.
Both results were rerun on the commit that adds this record.

## Old and new graders on the same captures

Eight complete attempts were replayed on 15b2960 and on a8ca74f, the new side after `mlag-lab write-intent` on its copy.

| Attempt | Exit old/new | Status old/new | result.json, timeline.tsv |
| --- | --- | --- | --- |
| small-baseline-1 | 0/0 | pass/pass | identical |
| small-baseline-2 | 0/0 | pass/pass | identical |
| small-baseline-3 | 0/0 | pass/pass | identical |
| small-calibration-1 | 0/0 | pass/pass | identical |
| small-calibration-2 | 0/0 | pass/pass | identical |
| medium-baseline | 0/0 | pass/pass | identical |
| small-06-stp-off | 1/1 | fail/fail | only the added `secondary_reboot_intent` differs; timeline identical |
| small-06-rstp | 0/0 | pass/pass | only the added `secondary_reboot_intent` differs; timeline identical |

On 3e2489b the same attempts also matched 1964cc4 exactly.
These attempts recorded the bridge-port replies under `raw`, so the eight bridge-port rows of the SMALL-06 intent report read unverified ("stats reply has no output").
With the replies renamed to Networka's `output` key in a copy, all eight rows match.

## Limit flips

- SMALL-06 withdrawal `limit_s` 5.0 to 2.0 in a copy's `case-intent.yaml`: the checks "101 withdrawal loss exceeds 2 s" and "201 withdrawal loss exceeds 2 s" and four flood-receiver loss checks appeared, and intent rows 101 and 201 went from match to mismatch. Flows, forwarding, floods, worst loss and timeline stayed the same. The attempt was already a fail, so the status stayed fail.
- `calibration_cut_s` lower bound 1.9 to 2.2: one check ("Measured one-way gap encloses the two-second injection") went from true to false, and the status went from pass to error (exit 0 to 2). Flows, forwarding, floods, injected time and timeline stayed the same.
- SMALL-06 `recovery_consecutive_replies` 10 to 1000 on 3e2489b: the four stable-recovery checks failed.
- SMALL-06 `max_client_outage_seconds` 5 to 0 on 3e2489b changed nothing; a8ca74f removed that duplicate field, and the withdrawal flip above shows `limit_s` is read.

## Pruned attempt

The pruned attempt `results/2026-11-24-small-search/none-default-reboot/01-secondary-reboot` has no captures and no `proof.tar.gz`.
On a copy without `case-intent.yaml`, `evaluate` exits 2 with an error that names the missing file and `mlag-lab write-intent`.
After `write-intent`, `evaluate` exits 0 and `result.json` gains only `secondary_reboot_intent`.
That report is unverified: 33 rows match and 12 are unverified, including the 501 and 502 flood rows.
A second `evaluate` leaves `result.json` unchanged.

## Bad case-intent.yaml

Each check ran `uv run --locked mlag-lab evaluate COPY` on a copy of the final SMALL-06 attempt on the commit that adds this record.
Each run exited 2 and wrote status error with a message that names the file and the field.

- `limit_s` deleted from the withdrawal phase: "secondary-reboot: every phase needs limit_s".
- Stream 999 added to `control_flows`: "secondary-reboot: graded_flows and control_flows must each list unique stream IDs of the Small topology".
- The 3e2489b `case-intent.yaml`: "saved by an older suite with reboot_intent.traffic fields client_streams, loss_free_bypass_streams, max_client_outage_seconds; delete PATH/case-intent.yaml and run `mlag-lab write-intent PATH`".
- After deleting that file and running `write-intent`, `evaluate` exited 1, the attempt's fail verdict.

The catalogue load runs the same check, so a bad entry in `intent/small.yaml` stops the suite with the same message.

## Live pass 1 on 3e2489b

| Runner | Attempt | Verdict | case-intent.yaml matches catalogue | Replay identical |
| --- | --- | --- | --- | --- |
| Small direct | direct/01-baseline | pass | yes | yes |
| Small direct | direct/01-secondary-reboot | fail (network) | yes | verdict, checks, timeline and exit yes; flood evidence label differed |
| Medium | stp-off/01-medium-stp-off-baseline | pass | yes | yes |
| Medium | stp-off/01-medium-stp-off-reboot-secondary | pass | yes | yes |
| Two-pair | stp-off/01-two-pair-stp-off-baseline | pass | yes | yes |
| Two-pair | stp-off/01-two-pair-stp-off-reboot-a-secondary | pass | yes | yes |
| Small link fault | baseline/01-baseline | pass | yes | yes |
| Small link fault | link/01-bond-member-loss | pass | yes | yes |
| Small link fault | link/01-peer-link-loss | pass | yes | yes |

The label difference came from the prune writing `proof.tar.gz` after the live analysis; a8ca74f fixed it.
On a8ca74f the nine pass-1 attempts were replayed offline: the seven other attempts gave `result.json` and timeline identical to live, and SMALL-06, after `write-intent`, kept its verdict, checks and timeline.

## Final live pass on a8ca74f

| Runner | Attempt | Verdict | case-intent.yaml matches catalogue | Exit, result.json, timeline.tsv identical on replay |
| --- | --- | --- | --- | --- |
| Small direct | direct/01-baseline | pass | yes | yes |
| Small direct | direct/01-secondary-reboot | fail (network) | yes | yes |
| Root-pair (RSTP) | root/01-root-calibrate | pass | yes | yes |
| Medium | stp-off/01-medium-stp-off-baseline | pass | yes | yes |

The four attempts were replayed again on the commit that adds this record, and exit, `result.json` and `timeline.tsv` were byte-identical to live.
In the Small secondary reboot, Networka read the bridge ports of both CHRs before and after the reboot, and all eight bridge-port rows match.
Rows 41 and 43 name `proof.tar.gz: captures/c1-eth1.pcap, captures/c1-eth2.pcap` live and on replay.

## Known network fault

The Small secondary reboot fails in withdrawal because flood frames 501 and 502 were seen twice at the sender's bond members.
This is the known network fault in this `results/index/faults.tsv` row at a8ca74f: `Small lab | STP off | MLAG secondary reboot | Flood frame back at its sender or twice at a host | | 2 | 2`.
It is not an evidence error.

## Remaining gaps

- `write-intent` writes the current catalogue rules, not the rules in force when a 1964cc4-era attempt ran.
- The flood evidence label names `proof.tar.gz` for every failed run, even if packing `proof.tar.gz` then fails.
- One pruned attempt without `case-intent.yaml` stops a campaign replay until `write-intent` runs.
- The runner has no option to keep captures; the replays relied on a hard-link watcher (`live/tools/shadow.py`).
- The runner re-executes itself as root, which leaves root-owned `__pycache__` in the venv, so a later `uv sync` needs `sudo chown -R` on the venv first.
- Root-pair ran only `root-calibrate`, under RSTP.
- Two-pair and the legacy Small runner ran live on 3e2489b only; on the new code they were replayed offline.
- Each live case ran once.
- The eight-attempt old-versus-new replay and the limit flips ran on a8ca74f and were not repeated on the commit that adds this record, which only adds validation.
