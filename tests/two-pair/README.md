# Medium lab with two MLAG pairs

Four MikroTik CHR switches form two MLAG pairs. Pair A is `switch-a1` and `switch-a2`, pair B is `switch-b1` and `switch-b2`, and each pair has its own peer link (`ether2`).
Switch-a1 and switch-b1 are configured as MLAG primary (`mlag-priority=10`), switch-a2 and switch-b2 as MLAG secondary (`mlag-priority=20`).
One distributed LACP bond, `inter-pair`, joins the pairs: switch-a1 to switch-b1 and switch-a2 to switch-b2, each on `ether3` (mlag-id 11 on pair A, 21 on pair B).
`host1` has an LACP bond to pair B and `host2` to pair A, so both host streams cross both pairs.
Every bridge runs with spanning tree off and the inter-pair bond with `lacp-strict=no`, both set in the startup config [switch.rsc](lab/switch.rsc).
The bridge settings, the host bond hash (`layer2+3`), the host MACs and addresses and the permanent neighbour entries follow the old two-pair suite, so both host streams use the cables to the MLAG primaries.
A collector node, `syslog`, receives the log of all four switches.
The [strict variant](../two-pair-strict/README.md) is the same lab with `lacp-strict=yes`.

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and [image-proof.json](runs/live-20261128-image-dbd8a548/image-proof.json) records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/two-pair/`.

- [PASS — baseline](runs/live-20261128-image-dbd8a548/baseline/report.md)
- [PASS — inter-pair-member-flap](runs/live-20261128-image-dbd8a548/inter-pair-member-flap/report.md)
- [FAIL — reboot-a-primary](runs/live-20261128-image-dbd8a548/reboot-a-primary/report.md)
- [PASS — reboot-a-secondary](runs/live-20261128-image-dbd8a548/reboot-a-secondary/report.md)
- [FAIL — reboot-b-primary](runs/live-20261128-image-dbd8a548/reboot-b-primary/report.md)
- [PASS — reboot-b-secondary](runs/live-20261128-image-dbd8a548/reboot-b-secondary/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/two-pair NAME=two-pair CONFIG=tests/two-pair/lab/devices.yml
```

## Streams and state

[lab.yaml](lab/lab.yaml) defines two streams, one ping every 100 ms each: host1 to host2 and host2 to host1 through both pairs.
Before and after every test, and after a reboot before the hold, it checks MLAG connected with the configured roles, spanning tree off, `lacp-strict=no` on the inter-pair bond, both inter-pair bond members synchronized, collecting and distributing at all four ends, and both bond members of each host eligible.

## Tests and their limits

The limits, holds and expectations come from the old suite's case catalogue for the `two-pair-stp-off-*` cases ([`src/mlag_lab/intent/two-pair.yaml`](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/src/mlag_lab/intent/two-pair.yaml)) and from the Small tests of the same kind.

| Test | What it does | Limit per host stream | Source of limit and holds |
| --- | --- | --- | --- |
| [baseline](tests/baseline.yaml) | 4 s of traffic, then host bond and bridge port checks on all four switches | 0 s | `two-pair-stp-off-baseline`; hold from the [MAC-move lab baseline](../small-mac-move/tests/baseline.yaml) |
| [reboot-a-primary](tests/reboot-a-primary.yaml), [reboot-a-secondary](tests/reboot-a-secondary.yaml), [reboot-b-primary](tests/reboot-b-primary.yaml), [reboot-b-secondary](tests/reboot-b-secondary.yaml) | Reboot one switch, wait up to 60 s for the lab state, hold 16 s, then 3 s recovery | 5 s | `two-pair-stp-off-reboot-*`; recovery wait from the [mobile Small primary reboot](../small-mac-move/tests/primary-reboot.yaml) |
| [inter-pair-member-flap](tests/inter-pair-member-flap.yaml) | Cable switch-a1 `ether3` to switch-b1 `ether3` down 8 s and back 8 s, then 3 s recovery, sampling the host entries of both hosts on all four switches | 3 s | `two-pair-stp-off-interpair-member-flap`; 0.35 s sampling from the [mobile Small member flap](../small-mac-move/tests/member-flap-repeat.yaml) |

A reboot test judges the withdrawal and the return of the switch as one step, so its limit applies to the longest stop of either.

## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8`: the per-run rows of `results/index/phases.jsonl` and the fault rows of `results/index/faults.tsv`, Medium lab, STP off, cases `two-pair-stp-off-*`.
`d1` and `d2` are `2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/01-*` and `02-*`, `f1` is `2026-11-24-forwarding-checks/debian-two-pair-stp-off-flap-once/01-*`, `t1` is `2026-11-24-two-pair/stp-off/01-*`, and `g1` is `2026-11-24-two-pair/invalid-priority-gate-stp-off/01-*`.
Old stops are the worst graded stream per phase. The old suite graded a reboot's withdrawal and return as two phases; here one step covers both.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | d1, d2, t1 pass, no loss. g1 error: the bridge priority gate withheld the fault. | PASS, no loss | Same |
| inter-pair-member-flap | f1 pass, down 0.212446 to 0.417557 s, back 0.104846 to 0.310466 s. d1 pass, down 0.102805 to 0.308185 s, back 0.104577 to 0.309174 s. d2 pass, down 0.316025 to 0.527068 s, back 0.206342 to 0.411297 s. | PASS. Down: host1 to host2 0 to 0.202643 s (1 lost), host2 to host1 0.103072 to 0.309124 s (2 lost). Back: host1 to host2 1.45541 to 1.66019 s (15 lost), host2 to host1 1.35402 to 1.56082 s (14 lost) | Same verdict; the stop at member down is within the old 0.1 to 0.5 s, and the stop at member back is longer than the old 0.1 to 0.4 s. See the flap section below. |
| reboot-a-primary | faults.tsv: loss over the limit in Pair A primary down, 3 of 3 runs, 19.668 to 23.344 s | FAIL, 16.2435 to 16.4562 s | Same fault, below the old range. |
| reboot-a-secondary | d1, d2 pass, no loss in either phase. t1 did not reach evaluation. | PASS, 0 lost | Same |
| reboot-b-primary | faults.tsv: loss over the limit in Pair B primary down, 2 of 2 runs, 20.664 to 22.177 s | FAIL, 16.5525 to 16.8001 s | Same fault, below the old range. |
| reboot-b-secondary | d1, d2 pass, no loss in either phase | PASS, 0 lost | Same |

Primary reboots: the other pair keeps sending into the rebooting switch, as in the old suite. [Finding 2](../../docs/findings/mlag-bond-without-lacp-partner-keeps-forwarding.md#finding-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch)
The stop ends within about 0.2 s of its peer logging `"bridge" peer link down`.
In one run each, both stops are below the old ranges.

### Inter-pair member flap

Before the bypass cable was removed ([ADR 0018](../../docs/adr/0018-labs-have-no-bypass-cable-between-hosts.md)), the flap stopped the host streams for the whole 8 s down hold in every recorded run, and the cause was not found.
The runs without the bypass cable pass: the Networka 0.5.2 run of 27 November 2026 and the live run listed above, where member down stopped the host streams for at most 0.31 s against the 3 s limit.
Whether the bypass cable caused the 8 s stop is not proven, because no run tested that alone.
The diagnosis of the 8 s stop stays in the evidence under `test-results/medium-two-pair/`.
