# Medium MLAG lab

The lab is one MLAG pair of MikroTik CHR switches, `switch1` and `switch2`, joined by a single-member peer link.
Switch1 is configured as MLAG primary (`mlag-priority=10`) and switch2 as MLAG secondary (`mlag-priority=20`).
`access-switch` is a third CHR with one LACP bond, `uplink`, that has one bond member to each peer.
`host1` has one cable to the access switch. `host2` has an LACP bond with one bond member to each peer.
Every bridge runs with spanning tree off, set in the startup config [switch.rsc](lab/switch.rsc).
A collector node, `syslog`, receives the log of all three switches.

## Networka 0.5.2 live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links below open the generated reports; full evidence stays in `test-results/networka-0.5.2-20261127/medium/`. Earlier measurements below remain historical.

- [PASS — baseline](runs/networka-0.5.2-20261127/baseline/report.md)
- [PASS — primary-power-loss](runs/networka-0.5.2-20261127/primary-power-loss/report.md)
- [PASS — primary-reboot](runs/networka-0.5.2-20261127/primary-reboot/report.md)
- [PASS — secondary-power-loss](runs/networka-0.5.2-20261127/secondary-power-loss/report.md)
- [FAIL — secondary-reboot](runs/networka-0.5.2-20261127/secondary-reboot/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium NAME=medium-mlag CONFIG=tests/medium/lab/devices.yml
```

## Streams and state

[lab.yaml](lab/lab.yaml) defines two streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through the switches.
Before and after every test it checks that switch1 is the connected MLAG primary and switch2 the connected MLAG secondary, that all three bridges run with spanning tree off, that both bond members of the access switch uplink are synchronized, collecting and distributing, and that both bond members of host2 have carrier and are eligible.

## Tests and their limits

The limits, hold times and expectations come from the `medium-stp-off-*` cases of the earlier Medium suite and from the Small tests of the same kind in [mobile](../small-mobile/README.md).

| Test | Limits and where they come from |
| --- | --- |
| [Baseline](cases/baseline.yaml) | 4 s with no lost ping on any stream, from `medium-stp-off-baseline`. Each flooded probe from host2 reaches host1 once and never returns to host2, from the same case's single copy of each broadcast. The flood probe is the one of the Small secondary reboot. |
| [Secondary reboot](cases/secondary-reboot.yaml) | Reboot switch2. Each stream may stop for 5 s, over a 16 s hold and a 3 s recovery, from `medium-stp-off-reboot-secondary`. 60 s for the new boot and healthy state, and the flood probe, as in the Small secondary reboot. |
| [Primary reboot](cases/primary-reboot.yaml) | Reboot switch1, with the same limits from `medium-stp-off-reboot-primary`. 60 s for recovery, as in the Small primary reboot. |
| [Secondary power loss](cases/secondary-power-loss.yaml) | Switch2 off for 20 s, then on. Each stream may stop for 5 s, with a 16 s hold and a 3 s recovery, from `medium-stp-off-power-loss-secondary`. 180 s for the cold boot and healthy state, as in the Small power-loss tests. |
| [Primary power loss](cases/primary-power-loss.yaml) | Switch1 off for 20 s, with the same limits from `medium-stp-off-power-loss-primary`. |

## Live verdicts

On 26 November 2026, with Networka 0.5.1, RouterOS 7.26beta7 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`), each test ran on a fresh deployment, primary power loss eight times. Each generated report starts with the verdict below. Each replay exited with the same verdict and gave byte-identical `result.json` and `report.md`.

| Test | Report verdict |
| --- | --- |
| Baseline | PASS |
| Secondary reboot | PASS |
| Primary reboot | PASS |
| Secondary power loss | PASS |
| Primary power loss | PASS, all eight runs |

## Comparison with the earlier Medium suite

The old values are quoted from `results/index/streams.tsv` at commit `5929968`, from the `medium-stp-off-*` rows with bridge mode none, and from each run's `result.json` where noted. Both suites send one ping every 100 ms per stream and grade the stream from host1 to host2 (old stream 101) and back (old stream 201). Old runs: `ext-medium-stp-off` runs 01 and 02, `medium-search/stp-off`, `medium-search/stp-off-repeat` and `power-loss/medium-stp-off`.

| Test | Old verdict and stops | New verdict and stops | Difference and reason |
| --- | --- | --- | --- |
| Baseline | PASS in every listed suite, no loss | PASS, no loss, flood probes pass | None. |
| Secondary reboot | PASS. Secondary down, host1 to host2: 2.914058–3.120603, 3.014945–3.221008, 2.390703–2.593125, 2.519232–2.728218 s. Secondary back: no loss in `ext` runs 01 and 02, 0.105286–0.319104 s in `stp-off`, 0–0.210774 s in `stp-off-repeat` | PASS. host1 to host2 2.50509–2.71263 s (26 lost), host2 to host1 2.39518–2.59804 s (25 lost), one stop each, none on return | Within the old stops. The new reboot step covers both old phases, and here no second stop occurred. |
| Primary reboot | PASS. Primary down, host1 to host2: 2.187891–2.394104, 2.185535–2.391265, 1.980901–2.191478, 2.507501–2.7121 s. Primary back: no loss | PASS. host1 to host2 2.29315–2.50014 s (26 lost), host2 to host1 2.2906–2.49546 s (25 lost) | Within the old stops. |
| Secondary power loss | PASS. Secondary off: index 0–0.136906 / 0–0.147169 s and 0–0.126443 / 0–0.115665 s, none in `power-loss`. `result.json` of `ext` run 01 gives one failed probe per stream, 0–0.201683 s. Secondary back: none, 0–0.212253 s, 0–0.205269 s | PASS. Power lost: host1 to host2 1 lost, 0–0.207847 s. Power restored: no loss | Same single lost ping as the old `result.json`. The old index upper bounds below 0.2 s disagree with the old `result.json` of the same run; that is an old export issue. |
| Primary power loss | PASS. Primary off: no loss in `ext` run 01 and `power-loss`; 0–0.414994 s in `ext` run 02. Primary back: no loss, except 0–0.414994 s for `ext` run 02 | PASS. Run 1, power lost: host1 to host2 0.314335–0.518716 s (5 lost), host2 to host1 0.208425–0.416858 s (3 lost). Power restored: 0.519087–0.733542 s (6 lost) and 0.611747–0.81489 s (7 lost) | Same verdict. The stop on return matches; the stop at power off is new. See below. |

Primary power loss in detail:

- The phase limits differ. The old withdrawal phase ran from power off until the runner saw the new boot; the new power-lost step ends at power on. The `ext` run 02 `result.json` places its only stop, 3 failed probes at 0.207495–0.414987 s, in the withdrawal phase at 49.01 s, 19.7 s after power on and before the boot was observed at 50.76 s. In new run 1 the stop on return came 16.2 s after power on, also before the boot was observed. Both are the stop when switch1 rejoins as MLAG primary. The old index repeats the run 02 stop in its Primary back row, which its `result.json` does not.
- Seven more runs after the first all gave PASS with byte-identical replay. Runs 6 to 8 had permanent neighbour entries pinned by hand on both hosts, as the old hosts set them.

  | Run | Power lost, host1 to host2 / back | Power restored, host1 to host2 / back |
  | --- | --- | --- |
  | 2 | 0 s / 0–0.206274 s | 0.311132–0.517113 s / 0.311195–0.513456 s |
  | 3 | 0 s / 0 s | 0.108028–0.314934 s / 0.106158–0.310578 s |
  | 4 | 0–0.207196 s / 0 s | 0.206185–0.412382 s / 0.213941–0.419793 s |
  | 5 | 0.206608–0.411136 s / 0.313976–0.520281 s | 0.206928–0.413758 s / 0.213459–0.419364 s |
  | 6 | 0–0.206964 s / 0–0.204813 s | 0 s / 0 s |
  | 7 | 0.309575–0.512759 s / 0.316843–0.521208 s | 0–0.206469 s / 0 s |
  | 8 | 0.20693–0.41032 s / 0.210411–0.415251 s | 0.211309–0.414797 s / 0.208066–0.411351 s |

- The stop on return spans the old `ext` run 02 stop of 0.207495–0.414987 s, so it matches the old suite within run-to-run spread.
- The stop at power off is real and intermittent. Whenever it occurs, it starts 0.1 to 0.3 s after switch2 logs `"bridge" peer link down`, the moment the old case text describes: switch2 "reverts its MLAG bonds to its own LACP system ID", and the partners "renegotiate LACP, with brief loss". It is not tied to how late switch2 sees the peer link go down: it occurred with 0.48 s and 0.88 s detection and was absent with 0.53 to 0.69 s.
- Permanent neighbour entries do not remove it: runs 7 and 8 stopped at power off with both entries pinned.
- The old QEMU wrapper cannot account for it. It put each veth and TAP on a private two-port bridge with learning off and LACP, LLDP and STP forwarding on, and it set 10 Gbit/s full duplex. A two-port bridge sends every frame to its only other port whether or not it learns, and native CHR links also forward LACP and LLDP at 10 Gbit/s full duplex.
- Not traced: why the old `ext` runs 01 and 02 and the `power-loss` run never showed the stop at power off. One remaining difference is the order: Networka pauses the guest and then withdraws carrier, while the old runner withdrew carrier and then paused, both within 0.17 s.

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) explains the evidence and replay.
