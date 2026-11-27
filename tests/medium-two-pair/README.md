# Medium lab with two MLAG pairs

Four MikroTik CHR switches form two MLAG pairs. Pair A is `switch-a1` and `switch-a2`, pair B is `switch-b1` and `switch-b2`, and each pair has its own peer link (`ether2`).
Switch-a1 and switch-b1 are configured as MLAG primary (`mlag-priority=10`), switch-a2 and switch-b2 as MLAG secondary (`mlag-priority=20`).
One distributed LACP bond, `inter-pair`, joins the pairs: switch-a1 to switch-b1 and switch-a2 to switch-b2, each on `ether3` (mlag-id 11 on pair A, 21 on pair B).
`host1` has an LACP bond to pair B and `host2` to pair A, so both host streams cross both pairs. A bypass cable joins the hosts outside the switches.
Every bridge runs with spanning tree off and the inter-pair bond with `lacp-strict=no`, both set in the startup config [switch.rsc](lab/switch.rsc).
The bridge settings, the host bond hash (`layer2+3`), the host MACs and addresses and the permanent neighbour entries follow the old two-pair suite, so both host streams use the cables to the MLAG primaries.
A collector node, `syslog`, receives the log of all four switches.
The [strict variant](../medium-two-pair-strict/README.md) is the same lab with `lacp-strict=yes`.

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium-two-pair NAME=medium-two-pair CONFIG=tests/medium-two-pair/lab/devices.yml
```

## Streams and state

[lab.yaml](lab/lab.yaml) defines four streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through both pairs, and both directions on the bypass.
Before and after every test, and after a reboot before the hold, it checks MLAG connected with the configured roles, spanning tree off, `lacp-strict=no` on the inter-pair bond, both inter-pair bond members synchronized, collecting and distributing at all four ends, and both bond members of each host eligible.

## Tests and their limits

The limits, holds and expectations come from the old suite's case catalogue for the `two-pair-stp-off-*` cases (`src/mlag_lab/intent/two-pair.yaml`) and from the Small tests of the same kind.

| Test | What it does | Limit per host stream | Source of limit and holds |
| --- | --- | --- | --- |
| [baseline](cases/baseline.yaml) | 4 s of traffic, then host bond and bridge port checks on all four switches | 0 s | `two-pair-stp-off-baseline`; hold from the [mobile Small baseline](../small-mobile/cases/baseline.yaml) |
| [calibration](cases/calibration.yaml) | 2 s one-way cut of the forward bypass at host2, 3 s settling, 3 s recovery | 0 s; bypass 2.3 s | `two-pair-stp-off-calibrate`; 2.3 s from the [mobile Small calibration](../small-mobile/cases/calibration.yaml) |
| [reboot-a-primary](cases/reboot-a-primary.yaml), [reboot-a-secondary](cases/reboot-a-secondary.yaml), [reboot-b-primary](cases/reboot-b-primary.yaml), [reboot-b-secondary](cases/reboot-b-secondary.yaml) | Reboot one switch, wait up to 60 s for the lab state, hold 16 s, then 3 s recovery | 5 s; bypass 0 s | `two-pair-stp-off-reboot-*`; recovery wait from the [mobile Small primary reboot](../small-mobile/cases/primary-reboot.yaml) |
| [inter-pair-member-flap](cases/inter-pair-member-flap.yaml) | Cable switch-a1 `ether3` to switch-b1 `ether3` down 8 s and back 8 s, then 3 s recovery, sampling the host entries of both hosts on all four switches | 3 s; bypass 0 s | `two-pair-stp-off-interpair-member-flap`; 0.35 s sampling from the [mobile Small member flap](../small-mobile/cases/member-flap-repeat.yaml) |

A reboot test judges the withdrawal and the return of the switch as one step, so its limit applies to the longest stop of either.

## Live verdicts

Run on 27 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`). Every attempt replayed with byte-identical `result.json` and `report.md`. The verdict and the measured stops are quoted from each generated `report.md`, at one ping every 100 ms. Evidence is under `test-results/medium-two-pair/r3/4b/`, not in git.

| Test | Verdict | Longest measured stop of the host streams |
| --- | --- | --- |
| baseline | PASS | 0 lost |
| calibration | PASS | Bypass lost 19, 1.87313 to 2.08089 s |
| inter-pair-member-flap | FAIL | Member down: host1 to host2 lost 78, 8.02404 to 8.23448 s; host2 to host1 lost 78, 8.01614 to 8.21984 s. The same outage runs into the member back step. Both host MACs stayed in every host-table sample. |
| reboot-a-primary | FAIL | host1 to host2 lost 159, 16.4552 to 16.6658 s; host2 to host1 lost 158, 16.3528 to 16.5577 s |
| reboot-a-secondary | PASS | 0 lost |
| reboot-b-primary | FAIL | host1 to host2 lost 173, 17.9267 to 18.133 s; host2 to host1 lost 173, 17.8922 to 18.1011 s |
| reboot-b-secondary | PASS | 0 lost |

After the runs host1 had sent 5908 packets on `eth1` and 545 on `eth2`, host2 5943 on `eth1` and 534 on `eth2`, so the host traffic used the primaries (`test-results/medium-two-pair/r3/03-cases-4b.log`).

## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8`: the per-run rows of `results/index/phases.jsonl` and the fault rows of `results/index/faults.tsv`, Medium lab, STP off, cases `two-pair-stp-off-*`.
`d1` and `d2` are `2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/01-*` and `02-*`, `f1` is `2026-11-24-forwarding-checks/debian-two-pair-stp-off-flap-once/01-*`, `t1` is `2026-11-24-two-pair/stp-off/01-*`, and `g1` is `2026-11-24-two-pair/invalid-priority-gate-stp-off/01-*`.
Old stops are the worst graded stream per phase. The old suite graded a reboot's withdrawal and return as two phases; here one step covers both.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | d1, d2, t1 pass, no loss. g1 error: the bridge priority gate withheld the fault. | PASS, no loss | Same |
| calibration | d1 pass, 1.872019 to 2.081 s. d2 pass, 1.978537 to 2.184975 s. t1 pass, 1.889029 to 2.100212 s. | PASS, 1.87313 to 2.08089 s | Same |
| inter-pair-member-flap | f1 pass, down 0.212446 to 0.417557 s, back 0.104846 to 0.310466 s. d1 pass, down 0.102805 to 0.308185 s, back 0.104577 to 0.309174 s. d2 pass, down 0.316025 to 0.527068 s, back 0.206342 to 0.411297 s. | FAIL, the whole 8 s down hold | See the flap section below. Not caused by the host setup or the bridge settings. |
| reboot-a-primary | faults.tsv: loss over the limit in Pair A primary down, 3 of 3 runs, 19.668 to 23.344 s | FAIL, 16.3528 to 16.6658 s | Same fault. The stop is 3 to 7 s shorter, see below. |
| reboot-a-secondary | d1, d2 pass, no loss in either phase. t1 did not reach evaluation. | PASS, 0 lost | Same |
| reboot-b-primary | faults.tsv: loss over the limit in Pair B primary down, 2 of 2 runs, 20.664 to 22.177 s | FAIL, 17.8922 to 18.133 s | Same fault. The stop is 2 to 4 s shorter, see below. |
| reboot-b-secondary | d1, d2 pass, no loss in either phase | PASS, 0 lost | Same |

Primary reboots: the other pair keeps sending into the rebooting switch, as in the old suite. [Fault 2](../../docs/plans/routeros-failures-report.md#fault-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch)
The stop ends when the rebooted switch forwards again, about 1 s after its peer logged `"bridge" peer link down`.
The new stops are shorter than the old range. The old switches ran behind a QEMU wrapper and these run as native Containerlab CHRs, which may restart faster. That cause is not verified.

### Inter-pair member flap

When the cable switch-a1 `ether3` to switch-b1 `ether3` goes down, both switches log `inter-pair link down`, and the host streams stop until the cable returns.
ICMP captures on every switch port in a diagnostic run show host1's requests arriving at switch-b1 `ether4` throughout the down hold, but none leaving switch-b1 on any port, the peer link included (`test-results/medium-two-pair/r3/flap-caps*/`).
Host-table samples show switch-b1 moving host2's entry from `inter-pair` to the peer port `ether2` within about 2 s, and it still forwards nothing to the peer port (`test-results/medium-two-pair/r2/03-flap-samples.log`).
In old run d2 the streams returned 0.45 s after the cable went down, and a sample 0.8 s after it showed the old primary with host2's entry on `ether2` (`results/2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/02-two-pair-stp-off-interpair-member-flap/timeline.tsv`).
The first flap failure used the default bridge settings. Setting the old suite's bridge options in the startup config (fixed `admin-mac`, `frame-types=admit-only-vlan-tagged` on the bridge and the peer port, `edge=yes` on the host bond) still stopped traffic for 5.1 s in one diagnostic run and 8.0 s in another and in the recorded run. Those options are kept, because they match the old suite.
The two other differences from the old lab do not explain it.
After repeating the old runner's reset over SSH (`lacp-strict=no` on the inter-pair bond, bridge disabled, `protocol-mode=none priority=0x8000`, 2 s wait, bridge enabled), the flap still stopped traffic for the whole down hold in 3 of 3 runs, 8.01868 to 8.33904 s. The host table, bridge ports, MLAG monitor and inter-pair member flags of switch-b1 were the same before and after the reset (`test-results/medium-two-pair/r4/`).
The old QEMU wrapper only advertised 10 Gbit/s full duplex on the guest NICs (`labs/shared/qemu-data-link.sh`), which the native CHR also reports. Its two-port bridges forwarded STP, LACP and LLDP and did not learn (`labs/shared/forward-control.sh`), which cannot change where a two-port bridge forwards.
The FAIL is therefore a RouterOS finding: when a switch's only member of a distributed MLAG bond goes down, it keeps dropping that bond's traffic for as long as the member stays down. It does not send it over the peer link, although its host table already points the destination at the peer port.
