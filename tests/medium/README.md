# Medium MLAG lab

The lab is one MLAG pair of MikroTik CHR switches, `switch1` and `switch2`, joined by a single-member peer link.
Switch1 is configured as MLAG primary (`mlag-priority=10`) and switch2 as MLAG secondary (`mlag-priority=20`).
`access-switch` is a third CHR with one LACP bond, `uplink`, that has one bond member to each peer.
`host1` has one cable to the access switch. `host2` has an LACP bond with one bond member to each peer.
A bypass cable joins host1 and host2 outside the switches.
Every bridge runs with spanning tree off, set in the startup config [switch.rsc](switch.rsc).
A collector node, `syslog`, receives the log of all three switches.

## Commands

Use the host tools, the qualified Containerlab build and the uv environment from the [Small lab guide](../small/README.md).
Start the lab from the repository root.

```sh
sudo env "CLAB=$CLAB" tests/medium/start.sh
```

Run a test and replay it. `lab_nw` is the function from the Small lab guide.

```sh
CASE=baseline
mkdir -p test-results/medium
RUN=$(mktemp -d test-results/medium/run.XXXXXX)
lab_nw test run "tests/medium/$CASE.yaml" \
  --lab tests/medium/clab-medium-mlag --config tests/medium/devices.yml --save "$RUN"
lab_nw test replay "$RUN/$CASE"
```

Remove the lab when finished.

```sh
sudo "$CLAB" destroy -t tests/medium/topology.clab.yml --cleanup
```

## Streams and state

[lab.yaml](lab.yaml) defines four streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through the switches, and both directions on the bypass.
Before and after every test it checks that switch1 is the connected MLAG primary and switch2 the connected MLAG secondary, that all three bridges run with spanning tree off, that both bond members of the access switch uplink are synchronized, collecting and distributing, and that both bond members of host2 have carrier and are eligible.

## Tests and their limits

The limits, hold times and expectations come from the `medium-stp-off-*` cases of the earlier Medium suite and from the Small tests of the same kind in [mobile](../small/mobile/README.md).

| Test | Limits and where they come from |
| --- | --- |
| [Baseline](baseline.yaml) | 4 s with no lost ping on any stream, from `medium-stp-off-baseline`. Each flooded probe from host2 reaches host1 once and never returns to host2, from the same case's single copy of each broadcast. The flood probe is the one of the Small secondary reboot. |
| [Calibration](calibration.yaml) | A 2 s one-way cut of the forward bypass at host2:eth3, then 3 s restored and 3 s more, from `medium-stp-off-calibrate`. The cut stream may stop for 2.3 s, the 2 s cut plus up to three ping intervals, as in the Small reboot calibration. The other streams lose nothing. |
| [Secondary reboot](secondary-reboot.yaml) | Reboot switch2. Each switched stream may stop for 5 s and the bypass for 0 s, over a 16 s hold and a 3 s recovery, from `medium-stp-off-reboot-secondary`. 60 s for the new boot and healthy state, and the flood probe, as in the Small secondary reboot. |
| [Primary reboot](primary-reboot.yaml) | Reboot switch1, with the same limits from `medium-stp-off-reboot-primary`. 60 s for recovery, as in the Small primary reboot. |
| [Secondary power loss](secondary-power-loss.yaml) | Switch2 off for 20 s, then on. Each switched stream may stop for 5 s and the bypass for 0 s, with a 16 s hold and a 3 s recovery, from `medium-stp-off-power-loss-secondary`. 180 s for the cold boot and healthy state, as in the Small power-loss tests. |
| [Primary power loss](primary-power-loss.yaml) | Switch1 off for 20 s, with the same limits from `medium-stp-off-power-loss-primary`. |

## Live verdicts

On 26 November 2026, with Networka 0.5.1 and RouterOS 7.26beta7, each test ran on a fresh deployment, primary power loss twice. Each generated report starts with the verdict below. Each replay exited with the same verdict and gave byte-identical `result.json` and `report.md`.

| Test | Report verdict |
| --- | --- |
| Baseline | PASS |
| Calibration | PASS |
| Secondary reboot | PASS |
| Primary reboot | PASS |
| Secondary power loss | PASS |
| Primary power loss | PASS, both runs |

## Comparison with the earlier Medium suite

The old values are quoted from `results/index/streams.tsv` at commit `5929968`, from the `medium-stp-off-*` rows with bridge mode none, and from each run's `result.json` where noted. Both suites send one ping every 100 ms per stream and grade the stream from host1 to host2 (old stream 101) and back (old stream 201). Old runs: `ext-medium-stp-off` runs 01 and 02, `medium-search/stp-off`, `medium-search/stp-off-repeat` and `power-loss/medium-stp-off`.

| Test | Old verdict and stops | New verdict and stops | Difference and reason |
| --- | --- | --- | --- |
| Baseline | PASS in every listed suite, no loss | PASS, no loss, flood probes pass | None. |
| Calibration | PASS. Cut stream: 1.984803–2.194556 s (20 lost), 1.978936–2.183955 s (20 lost), 1.882424–2.086205 s (19 lost) | PASS. Cut stream: 1.88187–2.08819 s (19 lost) | None. |
| Secondary reboot | PASS. Secondary down, host1 to host2: 2.914058–3.120603, 3.014945–3.221008, 2.390703–2.593125, 2.519232–2.728218 s. Secondary back: no loss in `ext` runs 01 and 02, 0.105286–0.319104 s in `stp-off`, 0–0.210774 s in `stp-off-repeat` | PASS. host1 to host2 2.50509–2.71263 s (26 lost), host2 to host1 2.39518–2.59804 s (25 lost), one stop each, none on return | Within the old stops. The new reboot step covers both old phases, and here no second stop occurred. |
| Primary reboot | PASS. Primary down, host1 to host2: 2.187891–2.394104, 2.185535–2.391265, 1.980901–2.191478, 2.507501–2.7121 s. Primary back: no loss | PASS. host1 to host2 2.29315–2.50014 s (26 lost), host2 to host1 2.2906–2.49546 s (25 lost) | Within the old stops. |
| Secondary power loss | PASS. Secondary off: index 0–0.136906 / 0–0.147169 s and 0–0.126443 / 0–0.115665 s, none in `power-loss`. `result.json` of `ext` run 01 gives one failed probe per stream, 0–0.201683 s. Secondary back: none, 0–0.212253 s, 0–0.205269 s | PASS. Power lost: host1 to host2 1 lost, 0–0.207847 s. Power restored: no loss | Same single lost ping as the old `result.json`. The old index upper bounds below 0.2 s disagree with the old `result.json` of the same run; that is an old export issue. |
| Primary power loss | PASS. Primary off: no loss in `ext` run 01 and `power-loss`; 0–0.414994 s in `ext` run 02. Primary back: no loss, except 0–0.414994 s for `ext` run 02 | PASS. Power lost: host1 to host2 0.314335–0.518716 s (5 lost), host2 to host1 0.208425–0.416858 s (3 lost). Power restored: 0.519087–0.733542 s (6 lost) and 0.611747–0.81489 s (7 lost) | Same verdict, longer stops. See below. |

Primary power loss in detail:

- The phase limits differ. The old withdrawal phase ran from power off until the runner saw the new boot; the new power-lost step ends at power on. The `ext` run 02 `result.json` places its only stop, 3 failed probes at 0.207495–0.414987 s, in the withdrawal phase at 49.01 s, 19.7 s after power on and before the boot was observed at 50.76 s. In the new run the stop on return came 16.2 s after power on, also before the boot was observed. Both are the stop when switch1 rejoins as MLAG primary. The old index repeats the run 02 stop in its Primary back row, which its `result.json` does not.
- At power off, `ext` runs 01 and 02 and `power-loss` lost no ping. The new run lost 4 pings from host1 to host2 and 3 back right after switch2 logged `"bridge" peer link down`. In both suites switch2 logged it within 0.9 s of the start of the withdrawal.
- Setup differences that could explain the longer stops, not traced: the old lab forwarded through its own QEMU data-link wrapper with bridge learning off (see the native CHR qualification in [the implementation plan](../../docs/plans/implementation-plan.md)), the new lab uses native Containerlab CHR links with learning on; the old hosts had permanent neighbour entries for each other, the new hosts resolve with ARP.
- A second primary power-loss run on a fresh deployment also gave PASS with byte-identical replay. Power lost: host2 to host1 lost 1 ping, 0–0.206274 s, and host1 to host2 none. Power restored: 0.311132–0.517113 s and 0.311195–0.513456 s (4 lost each), 19.9 s after power on. The stop at power off seen in the first run did not repeat, so it varies between runs. The stop on return stays above the old stops; its cause is not traced.

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) explains the evidence and replay.
