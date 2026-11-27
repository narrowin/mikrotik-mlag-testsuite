# Reboot and power loss timing: a CHR reboot is as short as the MLAG heartbeat timeout

A rebooted CHR answers on its management address again after about 15 s, which is the MLAG heartbeat timeout of the old suite's configuration.
So the surviving MLAG peer sees the timeout only at the edge or not at all.
A power loss keeps the switch away more than twice as long, yet costs less traffic, because every neighbour sees carrier go down at once.

[ADR 0015](../adr/0015-reboot-and-power-loss-are-separate-tests-and-a-reboot-is-a-real-routeros-reboot.md) records why both tests are kept.
This page records the timing behind it.

## Source

- All runs are from the old suite on 24 November 2026, RouterOS 7.26beta7 CHR, spanning tree off, one ping every 100 ms per stream.
- The time away is the difference of the first missed management ping and the first reply after it, both taken from `guest_absence_s` in the run's `result.json` at commit `95c7482`.
- Outages come from `results/index/streams.tsv` at the same commit.
- The old suite set `mlag-heartbeat=5s`. The [bridge CLI reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/) says a peer logs a warning after three missed heartbeat intervals, which is 15 s with that setting.

## Time away and outage

| Lab and fault | Run | Time away | Worst outage while down / back |
| --- | --- | --- | --- |
| Small, MLAG primary reboot | `2026-11-24-small-search/none-default-reboot/01-primary-reboot` | 15.42 s | 2.71–2.93 s / 0.00–0.21 s |
| Small, MLAG secondary reboot | `2026-11-24-small-search/none-default-reboot/01-secondary-reboot` | 15.34 s | none / none |
| Medium, MLAG primary reboot | `2026-11-24-medium-search/stp-off/01-medium-stp-off-reboot-primary` | 15.62 s | 1.98–2.19 s / none |
| Medium, MLAG secondary reboot | `2026-11-24-medium-search/stp-off/01-medium-stp-off-reboot-secondary` | 15.64 s | 2.40–2.60 s / 0.11–0.32 s |
| Medium, MLAG primary reboot | `2026-11-24-medium-search/stp-off-repeat/01-medium-stp-off-reboot-primary` | 15.74 s | 2.51–2.71 s / none |
| Medium, MLAG secondary reboot | `2026-11-24-medium-search/stp-off-repeat/01-medium-stp-off-reboot-secondary` | 15.71 s | 2.52–2.73 s / 0.00–0.21 s |
| Two-pair, pair A MLAG primary reboot | `2026-11-24-two-pair/stp-off/01-two-pair-stp-off-reboot-a-primary` | 20.39 s | 19.67–19.88 s / none |
| Small, MLAG primary power loss | `2026-11-24-power-loss/small-stp-off/01-primary-power-loss` | 37.00 s | 0.33–0.59 s / 0.00–0.20 s |
| Small, MLAG secondary power loss | `2026-11-24-power-loss/small-stp-off/01-secondary-power-loss` | 38.34 s | none / none |
| Medium, MLAG primary power loss | `2026-11-24-power-loss/medium-stp-off/01-medium-stp-off-power-loss-primary` | 38.22 s | none / none |
| Medium, MLAG secondary power loss | `2026-11-24-power-loss/medium-stp-off/01-medium-stp-off-power-loss-secondary` | 38.04 s | none / 0.00–0.21 s |

- Every one-pair reboot run above passed against 5 s per step.
- Every power loss run above passed against 5 s per step.
- The two-pair reboot failed; its outage is [Finding 2](mlag-bond-without-lacp-partner-keeps-forwarding.md#finding-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch).
- The power loss held the guest off for 20 s before it booted again.

## What the timing means

- In a reboot every virtual link keeps carrier, so the hosts and the access switch notice the missing switch only through the fast LACP timeout of 3 s.
- In a power loss every neighbour sees carrier go down at once and drops the bond member at once.
- That is why a reboot costs more than a power loss in the runs above, although the switch is away less than half as long.
- With the switch away for about as long as the heartbeat timeout, the surviving MLAG peer stays `connected` in many reboot runs and logs only `MLAG: remote heartbeat timeout` in some.
- ADR 0015 gives the count of saved Medium reboot runs that never left `connected`.
- A slower hardware reboot would leave the survivor alone past the heartbeat timeout; the power loss tests cover that time.

## Not verified

- How long a CRS326 or CCR2004 takes to reboot. The repository has no hardware boot time.
- Whether a survivor that does see the heartbeat timeout after a reboot resyncs MLAG more slowly. The old plan to hold the rebooted guest off for 20 s was not built.
