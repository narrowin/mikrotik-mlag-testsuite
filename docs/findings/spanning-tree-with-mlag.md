# Spanning tree with MLAG: only spanning tree off passed every Medium run

On RouterOS 7.26beta7, the Medium lab passed every reboot only with spanning tree off.
With RSTP or MSTP and the MLAG pair as root of VLAN 110, every MLAG primary reboot went over the 5 s limit.
With the access switch as root, VLAN 110 often did not forward at all.
The Small lab passed with spanning tree off, MSTP and RSTP, but RSTP with default settings had one long outage.

[ADR 0006](../adr/0006-spanning-tree-off-is-the-reference-and-rstp-is-tested-with-the-root-on-and-outside-the-mlag-pair.md) records the decision that followed: spanning tree off is the reference, and RSTP is tested with the root on and outside the MLAG pair.
This page records the measurements behind it.

## Source

- All runs are from the old suite on 24 and 25 November 2026, RouterOS 7.26beta7 CHR, one ping every 100 ms per stream.
- Single-run outages come from `results/index/streams.tsv` at commit `95c7482`, named by campaign, suite and run under `results/`.
- Counts of how often a fault showed come from [Faults across runs](../../results/README.md#faults-across-runs) and `results/index/faults.tsv` at the same commit.
- Verdicts per suite come from the generated [Medium lab](../../results/README.md#medium-lab) and [Small lab](../../results/README.md#small-lab) tables.
- The old suite's limits were 3 s per step for a bond member down and back, 4 s for blocked LACPDUs and 3 s after they resume, 0 for a MAC move and 5 s per step for an MLAG peer reboot and a peer link loss.
- Some verdicts differ from what the old plans said, because the old suite later added forwarding checks and judged the saved runs again.

## Medium lab

The Medium lab is one MLAG pair with an access switch below it.
Each row is one run; the outage is the worst stream of that step.

| STP mode and settings | Run | Primary reboot, down / back | Secondary reboot, down / back |
| --- | --- | --- | --- |
| Spanning tree off | `2026-11-24-medium-search/stp-off` | 1.98–2.19 s / none | 2.40–2.60 s / 0.11–0.32 s |
| Spanning tree off | `2026-11-24-medium-search/stp-off-repeat` | 2.51–2.71 s / none | 2.52–2.73 s / 0.00–0.21 s |
| RSTP, MLAG pair as root | `2026-11-24-medium-search/rstp-pair-root-run2` | 11.44–11.65 s / 6.77–6.98 s | 1.88–2.08 s / 0.11–0.31 s |
| RSTP, MLAG pair as root, `lacp-strict=yes` | `2026-11-24-medium-search/rstp-lacp-strict-pair-root` | 10.49–10.71 s / 7.01–7.22 s | 1.77–1.98 s / 0.00–0.14 s |
| RSTP, MLAG pair as root, `mlag-lacp-fallback=no` | `2026-11-24-medium-search/rstp-fallback-off-pair-root-run2` | 11.01–11.22 s / 4.92–5.13 s | 3.03–3.24 s / none |
| MSTP, MLAG pair as root | `2026-11-24-medium-search/mstp-pair-root-run2` | 10.87–11.08 s / 6.87–7.09 s | 2.61–2.82 s / none |
| MSTP, MLAG pair as root, `mlag-lacp-fallback=no` | `2026-11-24-medium-search/mstp-fallback-off-pair-root-clean` | 12.16–12.36 s / 5.01–5.21 s | 2.29–2.50 s / none |
| MSTP, region `mlag-lab`, MLAG pair root of both instances | `2026-11-24-medium-search/mstp-region-msti-pair-root` | 12.87–13.08 s / 2.72–2.94 s | 1.99–2.20 s / 0.10–0.31 s |
| Same, `mlag-lacp-fallback=no` | `2026-11-24-medium-search/mstp-region-msti-fallback-off-pair-root-run2` | 11.26–11.47 s / 4.88–5.09 s | 2.81–3.02 s / 0.00–0.22 s |
| MSTP, region `mlag-lab`, access switch root of both instances, `mlag-lacp-fallback=no` | `2026-11-24-medium-search/mstp-region-msti-fallback-off-access-root-run2` | 2.92–3.12 s / 0.00–0.21 s | 11.35–11.55 s / 0.21–0.41 s |

- Both spanning-tree-off suites passed every test they ran.
- Every run with the MLAG pair as root of VLAN 110 went over 5 s while the MLAG primary was down.
- Neither `lacp-strict=yes`, `mlag-lacp-fallback=no` nor a named MSTP region kept the MLAG primary reboot within 5 s.
- With the access switch as root of both MSTP instances, the MLAG secondary reboot went over 5 s instead.
- Each RSTP MLAG secondary reboot in the table also sent a unicast request back to its sender, in 1 of 1 run per setting, as described in [Finding 1](mlag-bond-without-lacp-partner-keeps-forwarding.md#finding-1-frames-sent-back-out-a-dual-connected-mlag-bond).
- MikroTik documents that a connected MLAG pair uses one shared system ID as RSTP bridge ID and LACP system ID, so with the pair as root both MLAG peers report themselves as root.

### Access switch as root

- RSTP with the access switch as root lost baseline traffic before any fault in 1 of 1 runs.
- MSTP with the access switch as root of the default instance lost baseline traffic in 2 of 2 runs.
- Waiting 60 s after the bridge change before the baseline helped only sometimes: RSTP lost baseline traffic in 1 of 2 runs and MSTP in 1 of 2 runs.
- MSTP with the access switch as root of the default instance and the MLAG pair as root of MSTI 1 lost baseline traffic in 1 of 1 runs.

### Split root

The split root is MSTP with the MLAG pair as root of the default instance and the access switch as root of MSTI 1, which carries VLAN 110.

- Its MLAG primary reboots stayed within 5 s in every run, for example 2.71–2.92 s in `2026-11-24-medium-search/mstp-split-root-fallback-off` run 01.
- Its MLAG secondary reboots sent a unicast request back to its sender:
  - with `mlag-lacp-fallback=yes` in 1 of 4 runs;
  - with `mlag-lacp-fallback=no` in 2 of 2 runs;
  - with the region `mlag-lab` and `mlag-lacp-fallback=no` in 1 of 3 runs.
- So no split-root form passed every run.
- The suite `2026-11-24-medium-search/mstp-split-root-fallback-on-repeat` passed all of its tests, but its first suite with the same settings did not.
- MSTP and the split root are not ported to the current labs, as [ADR 0006](../adr/0006-spanning-tree-off-is-the-reference-and-rstp-is-tested-with-the-root-on-and-outside-the-mlag-pair.md) says.

## Two MLAG pairs with RSTP

- With RSTP and the MLAG pair as root, the reboot of pair A's MLAG primary went over the limit in 2 of 2 runs, with outages of 16.290 to 17.594 s while it was down.
- In 2 of 2 of those runs the STP root moved to another bridge during the fault.
- With spanning tree off the same reboot also fails, as [Finding 2](mlag-bond-without-lacp-partner-keeps-forwarding.md#finding-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch) describes.

## Small lab

The Small lab is one MLAG pair with three dual-connected hosts.

### RSTP: one long outage on a bond member loss

- RSTP with the MLAG pair as root went over the limit in 1 of 4 runs of the bond member loss and return, with an outage of 10.632 to 10.840 s.
- That run is `2026-11-24-small-search/rstp-default-l2-run2`, test `01-bond-member-loss`.
- It was one outage from the bond member going down until after it came back, against 3 s per step.
- In it switch1 dropped the replies for `client1` instead of sending them over the peer link.
- It did not show with spanning tree off or MSTP.
- RSTP runs with other settings did not show it, but each of them ran once.

### Bond member return

Every Small run below lost pings for more than 2 s when the bond member came back.
From carrier return until LACP collects and distributes, the MLAG peer neither uses the bond member nor sends over the peer link.
The Linux 802.3ad bond waits 2 s (`AD_AGGREGATE_WAIT_TIME`) before it adds a returning bond member, which is most of that time.
No RouterOS bond setting tried shortened it.

| STP mode and settings | Run | Bond member back | Verdict |
| --- | --- | --- | --- |
| Spanning tree off | `2026-11-24-small-search/none-default-l2` | 2.30–2.50 s | PASS |
| Spanning tree off, `lacp-strict=yes` | `2026-11-24-small-search/none-lacp-strict-l2` | 2.71–2.92 s | PASS |
| Spanning tree off, `up-delay=3s` | `2026-11-24-small-search/none-bond-up-delay-3s-l2` | 2.31–2.51 s | PASS |
| MSTP | `2026-11-24-small-search/mstp-default-l2` | 2.39–2.60 s | PASS |
| MSTP, `mlag-lacp-fallback=no` | `2026-11-24-small-search/mstp-fallback-off-l2-run2` | 2.43–2.64 s | PASS |
| RSTP | `2026-11-24-small-search/rstp-default-member-repeat`, run 01 | 2.42–2.63 s | PASS |
| RSTP | `2026-11-24-small-search/rstp-default-member-repeat`, run 02 | 2.30–2.50 s | PASS |
| RSTP, switch2 as MLAG primary | `2026-11-24-small-search/rstp-chr2-primary-l2` | 2.50–2.71 s | PASS |
| RSTP, `lacp-strict=yes` | `2026-11-24-small-search/rstp-lacp-strict-l2` | 2.51–2.73 s | PASS |
| RSTP, `up-delay=3s` | `2026-11-24-small-search/rstp-bond-up-delay-3s-l2` | 2.50–2.71 s | PASS |
| RSTP, `mlag-lacp-fallback=no` | `2026-11-24-small-search/rstp-fallback-off-l2` | 2.39–2.60 s | PASS |

### MLAG primary reboot

| STP mode and settings | Run | Primary down / back | Verdict |
| --- | --- | --- | --- |
| Spanning tree off | `2026-11-24-small-search/none-default-reboot` | 2.71–2.93 s / 0.00–0.21 s | PASS |
| MSTP | `2026-11-24-small-search/mstp-default-reboot` | 1.99–2.20 s / 0.00–0.21 s | PASS |
| MSTP, `mlag-lacp-fallback=no` | `2026-11-24-small-search/mstp-fallback-off-reboot` | 2.92–3.14 s / 0.29–0.40 s | PASS |
| RSTP | `2026-11-24-small-search/rstp-default-reboot` | 2.81–3.02 s / 0.00–0.18 s | PASS |
| RSTP | `2026-11-24-small-search/rstp-default-primary-repeat` | 2.91–3.12 s / 0.00–0.21 s | PASS |
| RSTP, `mlag-lacp-fallback=no` | `2026-11-24-small-search/rstp-fallback-off-reboot` | 1.77–1.98 s / 0.00–0.21 s | PASS |

- The Small lab has no switch below the MLAG pair, so its RSTP and MSTP results do not carry to Medium.
- MSTP and RSTP with `mlag-lacp-fallback=no` passed every test they ran on Small, per the generated [Small lab](../../results/README.md#small-lab) table.

## Current labs

The current RSTP labs repeat the MLAG-pair-as-root tests with Networka; their results are in the [README results table](../../README.md#results).
