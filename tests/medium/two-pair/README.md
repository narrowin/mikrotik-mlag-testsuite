# Medium lab with two MLAG pairs

Four MikroTik CHR switches form two MLAG pairs. Pair A is `switch-a1` and `switch-a2`, pair B is `switch-b1` and `switch-b2`, and each pair has its own peer link (`ether2`).
Switch-a1 and switch-b1 are configured as MLAG primary (`mlag-priority=10`), switch-a2 and switch-b2 as MLAG secondary (`mlag-priority=20`).
One distributed LACP bond, `inter-pair`, joins the pairs: switch-a1 to switch-b1 and switch-a2 to switch-b2, each on `ether3` (mlag-id 11 on pair A, 21 on pair B).
`host1` has an LACP bond to pair B and `host2` to pair A, so both host streams cross both pairs. A bypass cable joins the hosts outside the switches.
Every bridge runs with spanning tree off and the inter-pair bond with `lacp-strict=no`, both set in the startup config [switch.rsc](switch.rsc).
A collector node, `syslog`, receives the log of all four switches.
The [strict variant](../two-pair-strict/README.md) is the same lab with `lacp-strict=yes`.

## Commands

Use the host tools, the qualified Containerlab build and the `lab_nw` function from the [Small lab guide](../../small/README.md).
Start the lab from the repository root.

```sh
sudo env "CLAB=$CLAB" tests/medium/two-pair/start.sh
```

Run a test and replay it.

```sh
CASE=baseline
mkdir -p test-results/medium
RUN=$(mktemp -d test-results/medium/two-pair.XXXXXX)
lab_nw test run "tests/medium/two-pair/$CASE.yaml" \
  --lab tests/medium/two-pair/clab-medium-two-pair --config tests/medium/two-pair/devices.yml --save "$RUN"
lab_nw test replay "$RUN/$CASE"
```

Remove the lab when finished.

```sh
sudo "$CLAB" destroy -t tests/medium/two-pair/topology.clab.yml --cleanup
```

## Streams and state

[lab.yaml](lab.yaml) defines four streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through both pairs, and both directions on the bypass.
Before and after every test, and after a reboot before the hold, it checks MLAG connected with the configured roles, spanning tree off, `lacp-strict=no` on the inter-pair bond, both inter-pair bond members synchronized, collecting and distributing at all four ends, and both bond members of each host eligible.

## Tests and their limits

The limits, holds and expectations come from the old suite's case catalogue for the `two-pair-stp-off-*` cases (`src/mlag_lab/intent/two-pair.yaml`) and from the Small tests of the same kind.

| Test | What it does | Limit per host stream | Source of limit and holds |
| --- | --- | --- | --- |
| [baseline](baseline.yaml) | 4 s of traffic, then host bond and bridge port checks on all four switches | 0 s | `two-pair-stp-off-baseline`; hold from the [mobile Small baseline](../../small/mobile/baseline.yaml) |
| [calibration](calibration.yaml) | 2 s one-way cut of the forward bypass at host2, 3 s settling, 3 s recovery | 0 s; bypass 2.3 s | `two-pair-stp-off-calibrate`; 2.3 s from the [mobile Small calibration](../../small/mobile/calibration.yaml) |
| [reboot-a-primary](reboot-a-primary.yaml), [reboot-a-secondary](reboot-a-secondary.yaml), [reboot-b-primary](reboot-b-primary.yaml), [reboot-b-secondary](reboot-b-secondary.yaml) | Reboot one switch, wait up to 60 s for the lab state, hold 16 s, then 3 s recovery | 5 s; bypass 0 s | `two-pair-stp-off-reboot-*`; recovery wait from the [mobile Small primary reboot](../../small/mobile/primary-reboot.yaml) |
| [inter-pair-member-flap](inter-pair-member-flap.yaml) | Cable switch-a1 `ether3` to switch-b1 `ether3` down 8 s and back 8 s, then 3 s recovery, sampling the host entries of both hosts on all four switches | 3 s; bypass 0 s | `two-pair-stp-off-interpair-member-flap`; 0.35 s sampling from the [mobile Small member flap](../../small/mobile/member-flap-repeat.yaml) |

A reboot test judges the withdrawal and the return of the switch as one step, so its limit applies to the longest stop of either.

## Live verdicts

Run on 26 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1. Every attempt replayed with byte-identical `result.json` and `report.md`. The verdict and the measured stops are quoted from each generated `report.md`. Evidence is under `test-results/medium-two-pair/4b/`, not in git.

| Test | Verdict | Measured stop of the host streams |
| --- | --- | --- |
| baseline | PASS | 0 lost |
| calibration, attempt 1 | ERROR | The captured one-way ping gap does not bracket the applied cut. Bypass lost 19 at one ping every 100 ms, 1.88089 to 2.08897 s. |
| calibration, attempt 2 | PASS | Bypass lost 19 at one ping every 100 ms, 1.87993 to 2.09093 s |
| inter-pair-member-flap | PASS | 0 lost. Both host MACs stayed in the host table of all four switches in every sample, 54 samples per switch, longest interval 0.357825 s. |
| reboot-a-primary | PASS | 0 lost |
| reboot-a-secondary | FAIL | host1 to host2 lost 179 at one ping every 100 ms, 18.5386 to 18.7434 s. host2 to host1 lost 179, 18.5526 to 18.7573 s. |
| reboot-b-primary | PASS | 0 lost |
| reboot-b-secondary | FAIL | host2 to host1 lost 180 at one ping every 100 ms, 18.2347 to 18.4413 s. host1 to host2 is unverified: sender cadence was invalid in this step. |

The calibration error came from Networka's bracket check. The first lost request was sent 102 ms after the rule was installed, and the check allows one 100 ms interval.

## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8`: the per-run rows of `results/index/phases.jsonl` and the fault rows of `results/index/faults.tsv`, Medium lab, STP off, cases `two-pair-stp-off-*`.
Runs are named by suite and run folder: `d1` and `d2` are `2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/01-*` and `02-*`, `f1` is `debian-two-pair-stp-off-flap-once/01-*`, `t1` is `2026-11-24-two-pair/stp-off/01-*`, and `g1` is `2026-11-24-two-pair/invalid-priority-gate-stp-off/01-*`.
Old stops are the worst graded stream per phase, with probes every 100 ms.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | d1, d2, t1 pass, no loss. g1 error: the bridge priority gate withheld the fault. | PASS, no loss | Same result |
| calibration | d1 pass, 1.872019 to 2.081 s, 19 probes. d2 pass, 1.978537 to 2.184975 s, 20 probes. t1 pass, 1.889029 to 2.100212 s, 19 probes. | ERROR, then PASS, 1.87993 to 2.09093 s, 19 pings | Loss is in the old range. The error is Networka's start-time check, described above, which the old suite did not have. |
| inter-pair-member-flap | f1 pass, down 0.212446 to 0.417557 s, back 0.104846 to 0.310466 s. d1 pass, down 0.102805 to 0.308185 s, back 0.104577 to 0.309174 s. d2 pass, down 0.316025 to 0.527068 s, back 0.206342 to 0.411297 s. | PASS, 0 lost | The host traffic does not cross the flapped member, see below. The old run's host-table size is not in the export. The new run checks that both host entries stay present on all four switches. |
| reboot-a-primary | faults.tsv: loss over the limit in Pair A primary down, 3 of 3 runs, 19.668 to 23.344 s | PASS, 0 lost | No host traffic passes switch-a1, see below |
| reboot-a-secondary | d1, d2 pass, no loss in either phase. t1 did not reach evaluation. | FAIL, 18.5526 to 18.7573 s (host2 to host1) | The host traffic passes switch-a2 |
| reboot-b-primary | faults.tsv: loss over the limit in Pair B primary down, 2 of 2 runs, 20.664 to 22.177 s | PASS, 0 lost | No host traffic passes switch-b1 |
| reboot-b-secondary | d1, d2 pass, no loss in either phase | FAIL, 18.2347 to 18.4413 s; host1 to host2 unverified | The host traffic passes switch-b2. The old hosts pinned each other's address as a permanent neighbour. These hosts resolve it, and host1's ping sender stalled during the outage. |

The old suite graded withdrawal and return as two phases. Here one reboot step covers both.

The reboot results swap roles because of the host bond hash, not because RouterOS changed.
The old hosts used `xmit_hash_policy layer2+3` (`labs/shared/client-network.sh`), and the old fault report states that no test traffic used the secondaries' links. [Fault 2](../../../docs/plans/routeros-failures-report.md#fault-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch)
These hosts use the Linux default `layer2`, like the Small lab, and both send and receive on `eth2`, the cable to the MLAG secondary.
After the runs, host1 `eth2` had sent 5218 packets and `eth1` 489, and host2 `eth2` 5135 and `eth1` 580 (`test-results/medium-two-pair/04-member-counters.log`).
So the host traffic crosses switch-a2, switch-b2 and their inter-pair cable, and the primary reboots and the flap of the primaries' cable lose nothing.
The secondary FAIL is the same RouterOS fault the old suite found on the primaries: the other pair keeps sending into the rebooting switch for about 20 s. The surviving peer logged `MLAG: remote heartbeat timeout` 11 to 13 s after the reboot was dispatched.
A lab in which host traffic crosses every switch would need a second stream pair on the other bond member. That is an open choice for the operator.
