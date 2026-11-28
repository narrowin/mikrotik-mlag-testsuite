# Medium MLAG lab

The lab is one MLAG pair of MikroTik CHR switches, `switch1` and `switch2`, joined by a single-member peer link.
Switch1 is configured as MLAG primary (`mlag-priority=10`) and switch2 as MLAG secondary (`mlag-priority=20`).
`access-switch` is a third CHR with one LACP bond, `uplink`, that has one bond member to each peer.
`host1` has one cable to the access switch. `host2` has an LACP bond with one bond member to each peer.
Every bridge runs with spanning tree off, set in the startup config [switch.rsc](lab/switch.rsc).
A collector node, `syslog`, receives the log of all three switches.

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and [image-proof.json](runs/live-20261128-image-dbd8a548/image-proof.json) records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/medium/`.

- [PASS — baseline](runs/live-20261128-image-dbd8a548/baseline/report.md)
- [PASS — primary-power-loss](runs/live-20261128-image-dbd8a548/primary-power-loss/report.md)
- [PASS — primary-reboot](runs/live-20261128-image-dbd8a548/primary-reboot/report.md)
- [PASS — secondary-power-loss](runs/live-20261128-image-dbd8a548/secondary-power-loss/report.md)
- [PASS — secondary-reboot](runs/live-20261128-image-dbd8a548/secondary-reboot/report.md)

secondary-reboot passed. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 it failed.

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium NAME=medium-mlag CONFIG=tests/medium/lab/devices.yml
```

## Streams and state

[lab.yaml](lab/lab.yaml) defines two streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through the switches.
Before and after every test it checks that switch1 is the connected MLAG primary and switch2 the connected MLAG secondary, that all three bridges run with spanning tree off, that both bond members of the access switch uplink are synchronized, collecting and distributing, and that both bond members of host2 have carrier and are eligible.

## Tests and their limits

The limits, hold times and expectations come from the `medium-stp-off-*` cases of the earlier Medium suite and from the Small tests of the same kind in [Small with a MAC-move host](../small-mac-move/README.md).

| Test | Limits and where they come from |
| --- | --- |
| [Baseline](tests/baseline.yaml) | 4 s with no lost ping on any stream, from `medium-stp-off-baseline`. Each flooded probe from host2 reaches host1 once and never returns to host2, from the same case's single copy of each broadcast. The flood probe is the one of the Small secondary reboot. |
| [Secondary reboot](tests/secondary-reboot.yaml) | Reboot switch2. Each stream may stop for 5 s, over a 16 s hold and a 3 s recovery, from `medium-stp-off-reboot-secondary`. 60 s for the new boot and healthy state, and the flood probe, as in the Small secondary reboot. |
| [Primary reboot](tests/primary-reboot.yaml) | Reboot switch1, with the same limits from `medium-stp-off-reboot-primary`. 60 s for recovery, as in the Small primary reboot. |
| [Secondary power loss](tests/secondary-power-loss.yaml) | Switch2 off for 20 s, then on. Each stream may stop for 5 s, with a 16 s hold and a 3 s recovery, from `medium-stp-off-power-loss-secondary`. 180 s for the cold boot and healthy state, as in the Small power-loss tests. |
| [Primary power loss](tests/primary-power-loss.yaml) | Switch1 off for 20 s, with the same limits from `medium-stp-off-power-loss-primary`. |

## Comparison with the earlier Medium suite

The old values are quoted from `results/index/streams.tsv` at commit `5929968`, from the `medium-stp-off-*` rows with bridge mode none, and from each run's `result.json` where noted. Both suites send one ping every 100 ms per stream and grade the stream from host1 to host2 (old stream 101) and back (old stream 201). Old runs: `ext-medium-stp-off` runs 01 and 02, `medium-search/stp-off`, `medium-search/stp-off-repeat` and `power-loss/medium-stp-off`. New values are from the reports of the 28 November runs listed above.

| Test | Old verdict and stops | New verdict and stops | Difference and reason |
| --- | --- | --- | --- |
| Baseline | PASS in every listed suite, no loss | PASS, no lost ping, flood probes pass | None. |
| Secondary reboot | PASS. Secondary down, host1 to host2: 2.914058–3.120603, 3.014945–3.221008, 2.390703–2.593125, 2.519232–2.728218 s. Secondary back: no loss in `ext` runs 01 and 02, 0.105286–0.319104 s in `stp-off`, 0–0.210774 s in `stp-off-repeat` | PASS. host1 to host2 2.71068–2.91781 s (27 lost), host2 to host1 2.71023–2.91409 s (27 lost). No flood probe returned to the sender | Within the range of the old stops. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 it failed. |
| Primary reboot | PASS. Primary down, host1 to host2: 2.187891–2.394104, 2.185535–2.391265, 1.980901–2.191478, 2.507501–2.7121 s. Primary back: no loss | PASS. host1 to host2 2.50827–2.71444 s (33 lost), host2 to host1 2.51727–2.72257 s (32 lost) | Close to the longest old stop, 2.507501–2.7121 s. |
| Secondary power loss | PASS. Secondary off: index 0–0.136906 / 0–0.147169 s and 0–0.126443 / 0–0.115665 s, none in `power-loss`. `result.json` of `ext` run 01 gives one failed probe per stream, 0–0.201683 s. Secondary back: none, 0–0.212253 s, 0–0.205269 s | PASS. Power lost: host2 to host1 1 lost, 0–0.210114 s. Power restored: no lost ping | One lost ping, as in the old `result.json`. The old index upper bounds below 0.2 s disagree with the old `result.json` of the same run; that is an old export issue. |
| Primary power loss | PASS. Primary off: no loss in `ext` run 01 and `power-loss`; 0–0.414994 s in `ext` run 02. Primary back: no loss, except 0–0.414994 s for `ext` run 02 | PASS. Power lost: host2 to host1 1 lost, 0–0.208934 s. Power restored: no lost ping | Same verdict. The one lost ping at power off is within the old `ext` run 02 stop of 0–0.414994 s. |

Primary power loss in detail:

- The phase limits differ. The old withdrawal phase ran from power off until the runner saw the new boot; the new power-lost step ends at power on. The `ext` run 02 `result.json` places its only stop, 3 failed probes at 0.207495–0.414987 s, in the withdrawal phase at 49.01 s, 19.7 s after power on and before the boot was observed at 50.76 s. That is the stop when switch1 rejoins as MLAG primary. The old index repeats the run 02 stop in its Primary back row, which its `result.json` does not.
- The old QEMU wrapper cannot account for a difference. It put each veth and TAP on a private two-port bridge with learning off and LACP, LLDP and STP forwarding on, and it set 10 Gbit/s full duplex. A two-port bridge sends every frame to its only other port whether or not it learns, and native CHR links also forward LACP and LLDP at 10 Gbit/s full duplex.
- One remaining difference is the order: Networka pauses the guest and then withdraws carrier, while the old runner withdrew carrier and then paused, both within 0.17 s.

The [Networka lab test guide](https://narrowin.github.io/networka/lab-tests/) explains the evidence and replay.
