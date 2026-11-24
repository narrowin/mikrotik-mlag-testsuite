# Plan: find an MLAG setup without outages, Small lab first

**Goal.** Find a RouterOS 7.26beta7 configuration where every Small lab case passes. Only then repeat the search in the Medium lab.

**Stop rule.** If no tested Small configuration passes every case, stop and report the closest one. The Medium lab adds an access switch and root choices on top of the same MLAG pair, so a Small failure would carry into it.

**Time box.** 24 November 2026, 12:35–13:30 Zurich time.

## Stage 1: Small lab

Run every case in each configuration. A configuration passes only when every phase of every case passes.

| Group | Cases | Suite |
| --- | --- | --- |
| Original runner | `calibration`, `bond-member-loss`, `lacp-timeout`, `mac-move`, `peer-link-loss` | L2 |
| Direct runner | `baseline`, `reboot-calibration`, `secondary-reboot`, `primary-reboot` | Reboot |

Configurations, in order:

1. **Bridge mode**: STP off (`--bridge-mode none`), RSTP (`rstp`), MSTP (`mstp`, once the runner supports it).
2. **MLAG and LACP settings**, applied to both MLAG peers when a bridge mode fails a case. The candidates come from the MikroTik manual: bond `up-delay`, `lacp-rate`, `mlag-lacp-fallback`, `mlag-init-delay`. Each variant changes one setting from the lab default.

Each run writes its results to `results/2026-11-24-small-search/<mode>-<variant>-<suite>/`, together with the generated README and each device's config.

### Limits and where they come from

MikroTik documents only "brief packet loss" when LACP renegotiates. The limits follow from the protocols the lab uses:

| Change | Limit per phase | Basis |
| --- | --- | --- |
| MLAG bond member down and back | 3 s | LACP short timeout at `lacp-rate=1sec` is 3 s (IEEE 802.1AX). A Linux 802.3ad client waits 2 s (`AD_AGGREGATE_WAIT_TIME`) before adding a returning member; measured 2.1 s here. |
| LACPDUs blocked, then resumed | 4 s, then 3 s | Partner expiry after 3 s plus probe spacing, then the same return as above. |
| MAC move | no lost probe | One gratuitous ARP moves the MAC; nothing has to renegotiate. |
| MLAG peer reboot, peer link loss | 5 s per phase | Clients renegotiate LACP to a new system ID, plus margin. |

Anything near 10 s or more is a failure whatever the basis. The first runs used 1 s limits for member and LACP return, which Codex had set without a source. They are re-scored against these limits.

## Stage 2: Medium lab

Only if Stage 1 found a passing configuration: apply it to the Medium lab and run its baseline, calibration and both MLAG peer reboots for each root placement. Search further only where Medium fails.

## Checkpoints

After each stage, review the verdicts and the generated README. The review checks that the README is readable and that every failure links to its check. Fix the generator before going on.

## Status

Verdicts use the limits above. Evidence folders are under `results/2026-11-24-small-search/`; Medium under `results/2026-11-24-medium-search/`. CHR 1 was MLAG primary in every run except `chr2-primary`.

### Stage 1: Small lab — passed

| Configuration | Original cases incl. `peer-link-loss` | Reboot cases | Result |
| --- | --- | --- | --- |
| **STP off**, lab defaults | PASS. Member back 2.30–2.50 s | PASS. Primary reboot 2.72–2.93 s down, up to 0.21 s back | **Passes every case** |
| **MSTP** (CIST only), lab defaults | PASS. Member back 2.39–2.60 s | PASS. Primary reboot 1.99–2.20 s down | **Passes every case** |
| **RSTP**, lab defaults | **FAIL** in one run: `bond-member-loss` lost 10.63–10.84 s, one outage from member down until after member back. CHR 1 dropped replies for client 1 instead of using the peer link. `peer-link-loss` passed separately. | First primary reboot INVALID: a sender paused over 450 ms. Repeat PASS: 2.91–3.12 s down, up to 0.21 s back (`rstp-default-primary-repeat/`). | **Not clean.** Repeat (2 runs, CHR 1 primary) passed: member down 0.10–0.31 s, back 2.42–2.63 s. The blackhole hit 1 of 3 runs, so it is intermittent. |
| RSTP, `chr2-primary` (`mlag-priority=50` on CHR 2) | PASS. Member back 2.50–2.71 s | not run | Passes the cases run |
| RSTP, `lacp-strict=yes` | PASS. Member back 2.51–2.73 s | not run | Passes the cases run |
| RSTP, `up-delay=3s` | PASS. Member back 2.50–2.71 s; `up-delay` does not shorten the return | not run | Passes the cases run |
| RSTP, `lacp-strict=yes` and `up-delay=3s` | `lacp-timeout` INVALID: state samples more than 1.5 s apart | not run | Dropped |
| STP off, `lacp-strict=yes` or `up-delay=3s` | PASS. Member back 2.71–2.92 s and 2.31–2.51 s | not run | No gain over lab defaults |

#### Findings

- The return of an MLAG bond member always costs 2.3–2.9 s. From carrier return until LACP collects and distributes, CHR 1 neither uses the member nor sends over the peer link. The Linux client's 2 s 802.3ad aggregation wait takes most of that. No RouterOS bond setting tested shortened it.
- The RSTP 10.6 s blackhole hit 1 of 3 RSTP lab-default runs with CHR 1 as primary. The 2 repeats, and the RSTP runs with `lacp-strict` or `up-delay`, had a clean member-down phase. It is intermittent, not fixed by a setting, and was never seen with STP off or MSTP.
- The first RSTP attempt (`rstp-default-l2/`) was invalid. Calibration's reverse bypass stream had one sequence number that was never sent.

### Stage 2: Medium lab — passes only with STP off

| Configuration | Cases | Result |
| --- | --- | --- |
| STP off on all bridges, lab defaults | baseline, calibration, secondary reboot, primary reboot | **PASS** all four. Secondary reboot 2.40–2.60 s down, 0.11–0.32 s back. Primary reboot 1.98–2.19 s down, no loss back. `stp-off/` |
| STP off on all bridges, repeat | baseline, both reboots | **PASS** all three. Secondary reboot 2.52–2.73 s down, up to 0.21 s back. Primary reboot 2.51–2.71 s down, no loss back. `stp-off-repeat/` |

| RSTP, access switch as root | baseline | **FAIL**: 0 of 41 VLAN probes delivered in each direction, so no fault ran. Same as the earlier Medium RSTP finding. `rstp-access-root/` |
| RSTP, MLAG pair as root (rerun) | all four | **FAIL** primary reboot: 11.44–11.65 s down, 6.77–6.98 s back. Baseline, calibration and secondary reboot passed. The first run lost its SSH session to CHR 2 before any test. `rstp-pair-root-run2/` |
| RSTP, MLAG pair as root, `lacp-strict=yes` on the MLAG bonds | all four | **FAIL** primary reboot: 10.49–10.71 s while down and 7.01–7.22 s on return, against 5 s. Baseline, calibration and secondary reboot (1.77–1.98 s down) passed. Matches the earlier Medium RSTP primary-reboot failures. `rstp-lacp-strict-pair-root/` |
| MSTP, MLAG pair as root (rerun) | all four | **FAIL** primary reboot: 10.87–11.08 s down, 6.87–7.09 s back. Baseline, calibration and secondary reboot (2.61–2.82 s down) passed. Same failure as RSTP: with spanning tree on in the Medium lab, an MLAG primary reboot exceeds 10 s. `mstp-pair-root-run2/` |
| MSTP, access switch as root (rerun) | baseline | **FAIL**: 0 of 41 VLAN probes delivered in each direction, same as RSTP with the access switch as root. `mstp-access-root-run2/` |
| MSTP, both root placements, first runs | baseline | First runs stopped by an evaluator bug: the BPDU check accepted only RSTP BPDUs (version 2), not MSTP (version 3). Fixed; the saved baseline then passes every network check. Reruns queued (`mstp-*-run2/`). |

Earlier note: MSTP is not carried to Medium yet: the Medium runner only knows its STP-off and RSTP root variants. RSTP is not carried because it did not pass the Small lab cleanly.

### Stage 2b: Medium lab, MSTP variants

Each row is one setup; "pair root" means the MLAG pair is root of the default MSTP instance (CIST). MSTI 1 carries VLAN 110. Saved configs confirm every setting. Exact per-stream bounds are in `results/2026-11-24-medium-search/measurements.tsv`. Limits: 5 s per reboot phase.

| Setup | Primary reboot (down / back) | Secondary reboot (down / back) | Result |
| --- | --- | --- | --- |
| MSTP defaults, pair root | 10.87–11.08 s / 6.87–7.09 s | 2.61–2.82 s / none | **FAIL** |
| MSTP defaults, access switch root | — | — | **FAIL**: VLAN never forwards |
| Region `mlag-lab`, MSTI 1 on the pair (0x1000), access switch 0x8000 | 12.83–13.08 s / 2.68–2.94 s | passed | **FAIL** |
| Same, access switch root of both instances | — | — | **FAIL**: VLAN never forwards |
| `mlag-lacp-fallback=no`, pair root | 12.16–12.36 s / 5.01–5.21 s | 2.29–2.50 s / none | **FAIL** |
| `mlag-lacp-fallback=no`, access switch root | not reached | INVALID: CHR 2 boot not confirmed | Inconclusive; the baseline did forward |
| Region, MSTI 1 on the pair, fallback off | 11.26–11.47 s / 4.88–5.09 s | 2.81–3.02 s / up to 0.22 s | **FAIL** |
| Region, access switch root of both instances, fallback off | 2.92–3.12 s / up to 0.21 s | 11.35–11.55 s / 0.21–0.41 s | **FAIL** (secondary) |
| **Split root**: pair root of the default instance, access switch root of MSTI 1 (0x0000), fallback off, region blank, 2 runs | 2.71–2.92 s / none; 3.02–3.23 s / 0.11–0.32 s | 2.50–2.71 s / none; 2.82–3.02 s / up to 0.14 s | **PASS** twice |
| **Split root**, fallback off, region `mlag-lab` rev 1 | 2.18–2.39 s / none | 2.50–2.71 s / up to 0.21 s | **PASS** |
| Split root, fallback **on** | INVALID: a sender paused over 450 ms; measured 2.66–2.86 s / up to 0.20 s | 2.30–2.51 s / none | Inconclusive, within limits |
| RSTP, pair root, fallback off | 11.01–11.22 s / 4.92–5.13 s | 3.03–3.24 s / none | **FAIL** |

Earlier accidental runs with leftover MSTI settings are kept under `invalid-leftover-msti-*` and not used.

The Medium CHR 2 stopped accepting the `admin` login after repeated reboots at 14:42; the lab was redeployed from `labs/medium/medium.clab.yml` at 14:52 and runs from then on started from a fresh deployment.

### Small lab with `mlag-lacp-fallback=no`

| Mode | Original cases | Reboot cases |
| --- | --- | --- |
| RSTP | **PASS** all five | **PASS** all four |
| MSTP | INVALID: calibration had loss on stream 202 outside the fault | Primary reboot INVALID: a sender paused over 450 ms; others passed |

## Result

- **Works in both labs:** STP off on every bridge with lab defaults. Reboots cost 2.0–2.9 s, a bond member's return 2.3–2.9 s.
- **Works with MSTP in Medium:** the split root, with the MLAG pair as root of the default instance, the access switch as root of an MSTI carrying the service VLAN, and `mlag-lacp-fallback=no` on both MLAG peers. It passed three times: twice with a blank region, once with a named region. Primary reboots cost 2.2–3.2 s, secondary 2.5–3.0 s, and returns at most 0.3 s. Whether fallback off is needed is open; the fallback-on run was invalid but within limits.
- **Fails:** MSTP or RSTP with the MLAG pair as root of the service VLAN. A primary reboot costs 10.9–13.1 s. Fallback off, a named region or `lacp-strict` does not change that.
- **Small lab:** passes with STP off, MSTP and RSTP when fallback is off. RSTP with defaults had one intermittent 10.6 s blackhole.
- **Next:** repeat split root with fallback on; test the split root with the access switch as root of the default instance and the pair as MSTI root; port the split root to the Large lab plan.

Lab state: Small lab at defaults; Medium lab freshly deployed at 14:52 and at its defaults after the last revert.
