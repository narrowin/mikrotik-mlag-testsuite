# Move the test suite's intent to YAML

## Decision

**Two-way door.** Move the case definitions on a feature branch and compare them before switching the suite over. Live verification uses dedicated disposable labs.

**Problem.** SMALL-06 defines its acceptance rules in YAML, while the rest of the suite defines case expectations in Python.

**Desired outcome.** Each case has one readable YAML definition. The runner and grader use that definition when collecting and replaying evidence.

| Option | Impact | Confidence | Ease | ICE |
| --- | --- | --- | --- | --- |
| Move case definitions and keep the current graders | 9, one authoring format across the suite | 9, a local draft matched all 99 case definitions and 100 selector mappings | 7, changes the registry and how attempts save their inputs | 567 |
| Rewrite the runners and graders together | 9, could standardize more of the suite | 4, existing measurement behavior would need requalification | 2, requires changes to the fault and measurement code | 72 |

Move the definitions first. Keep the existing check functions responsible for measuring what happened. SMALL-06 demonstrates that changing only a YAML limit changes the relevant verdict on the same packet capture. [SMALL-06 definition](../../src/mlag_lab/intent/small.yaml) · [Verification](small-06-yaml-closeout.md)

## Migration and acceptance

1. **Move the catalogue.** Group the existing case definitions by lab and fault family. Keep selector aliases, descriptions, traffic IDs, phase limits and planned or archived entries. Put shared acceptance limits in one YAML file. Keep case input separate from the code that operates the lab or measures packets.
2. **Save the rules with the observations.** Write each attempt's resolved YAML before applying the fault. Make all grader entry points use the recorded intent on replay. Replay stops with an error that names a missing `case-intent.yaml`. `mlag-lab write-intent` writes the current catalogue rules into an older attempt explicitly. Pruned attempts keep their saved verdict; a pruned SMALL-06 attempt gains its intent report, written to `result.json`.
3. **Check parity.** Compare all case fields and selectors with the original catalogue. Run the old and new graders on copies of the same complete captures. Check that packet measurements, verdicts and timelines agree. Edit one limit in a replay copy and verify that only the expected results change. Verify that missing required evidence remains visible as unverified.
4. **Rerun the live entry points.** Start with representative baseline and fault cases on the Small direct, Small link fault, Medium, root-pair and two-pair runners. Use fresh instances, the pinned image and the clean baseline gates. Run independent suites in parallel within the lab host limit, and use `--destroy`. Record every run and its outcome. Archived selectors and planned Large cases remain available for documentation or replay where evidence exists.
5. **Switch over and clean up.** Remove the Python case declarations after parity and live verification. Keep the committed YAML and retained evidence. Remove the temporary deployments, replay copies and test environments.

## Branch verification

The catalogue matches all 99 existing definitions and 100 selector mappings, and every definition round-trips through the saved YAML. SMALL-06 keeps its outage limits and streams in the same case fields as every other case. Its `reboot_intent` holds only the reboot timing, the switch and client state and the flood streams. The bridge-port forwarding check is Networka's `check_bridge_port_forwarding`, pinned at Networka commit 8409e4a.

Eight complete attempts replayed on 15b2960 and on this branch gave identical exit codes, verdicts, timelines and `result.json`, except the added SMALL-06 intent report. Attempts saved before the Networka check recorded the bridge-port replies under `raw`, so those eight rows now report unverified. With the replies renamed to Networka's `output` key in a copy, the rows match as before. A failed run names its flood captures inside `proof.tar.gz`, live and on replay.

Lowering the recorded SMALL-06 withdrawal limit from 5 to 2 seconds failed the 101 and 201 outage checks and kept the packet measurements. Raising the calibration lower bound from 1.9 to 2.2 seconds changed one check. A pruned SMALL-06 attempt without flood evidence writes its flood rows as unverified.

Fresh live qualification is the remaining gate before adopting the branch. It must exercise the Networka bridge-port read in the Small secondary reboot.
