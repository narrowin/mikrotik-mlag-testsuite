# Case index

Run these stages in order. Restore and verify the baseline before every fault. Keep the case ID when comparing STP disabled and RSTP enabled. Record mode, root placement and repeat separately.

CLI selectors map each case to the existing runner and archived evidence. Pending selectors identify planned work.

Case definitions are grouped by lab and fault family in the [intent catalogue](../../src/mlag_lab/intent).
Every new attempt saves its resolved rules as `case-intent.yaml`. The evaluator grades a replay only from
that file, so later changes to the catalogue do not change the recorded limits. An attempt without the file
stops with an error that names it.

The catalogue holds what the suite grades from packets: phases, loss limits, graded and control streams.
The switch and host state each case requires before the fault and after recovery is Networka intent in
[intent/state/](../../src/mlag_lab/intent/state), one file per lab and one per setup. Networka collects
and checks it; each attempt saves the result in `gate-baseline/` and `gate-restored/`.
[Device state and packet grading](../test-framework.md#device-state-and-packet-grading)

## Small lab

| ID | Case | CLI selector |
| --- | --- | --- |
| SMALL-01 | Baseline readiness | `direct-baseline` |
| SMALL-02 | One-way loss calibration | `direct-calibrate` |
| SMALL-03 | Client link loss and return | `carrier` |
| SMALL-04 | LACP timeout and recovery | `silent-lacp` |
| SMALL-05 | MAC move and relearning | `mobile-move` |
| SMALL-06 | Secondary core reboot | `direct-reboot-secondary` |
| SMALL-07 | Primary core reboot | `direct-reboot-primary` |
| SMALL-08 | Peer link loss and return | `peer-link-loss` |
| SMALL-09 | Silent host past bridge ageing, then relearn (catalogue M2) | `silent-mobile` (`mac-age-relearn`) |
| SMALL-10 | Repeated MLAG bond member flap (catalogue M4, one pair) | `carrier-flap` (`member-flap-repeat`) |

Small lab selectors default to RSTP. Use `--bridge-mode none` to test with STP off.

The `secondary-reboot` entry in the [Small catalogue](../../src/mlag_lab/intent/small.yaml) defines SMALL-06.
Its outage limits and streams sit in the same fields as every other case. `reboot_intent` holds only the
reboot timing and the flood streams that must not return to the sender. The switch and client state it
requires is the Small gate: [direct.yaml](../../src/mlag_lab/intent/state/direct.yaml),
[hosts.yaml](../../src/mlag_lab/intent/state/hosts.yaml) and the file of the run's bridge mode.

[Inventory](../../labs/small/README.md) · [Link-loss procedure](small-client-link.md) · [Reboot commands](../operator-guide.md#reboot-the-direct-client-pair) · [Results](../../results/2026-11-24-small-lab/README.md)

## Medium lab

| ID | Case | STP off | RSTP, core pair root | RSTP, access switch root |
| --- | --- | --- | --- | --- |
| MEDIUM-01 | Baseline | `medium-stp-off-baseline` | `medium-pair-root-baseline` | `medium-access-root-baseline` |
| MEDIUM-02 | One-way calibration | `medium-stp-off-calibrate` | `medium-pair-root-calibrate` | `medium-access-root-calibrate` |
| MEDIUM-03 | Secondary reboot | `medium-stp-off-reboot-secondary` | `medium-pair-root-reboot-secondary` | `medium-access-root-reboot-secondary` |
| MEDIUM-04 | Primary reboot | `medium-stp-off-reboot-primary` | `medium-pair-root-reboot-primary` | `medium-access-root-reboot-primary` |
| MEDIUM-07 | Both cores down and return | Planned | Planned | Planned |

MEDIUM-08 uses a separate two-pair deployment: two MLAG pairs joined by one distributed bond, with equal bridge priorities and with the field per-pair priorities. [Why, setup and commands](medium-two-pair-root.md)

MEDIUM-08 also has the step `interpair-member-flap` for every two-pair setup, for example `two-pair-equal-interpair-member-flap`. It takes the inter-pair bond member between CHR 1 and CHR 3 down for 8 s and up again, the trigger of the four-switch report (catalogue M4).

MEDIUM-05 and MEDIUM-06 identify the archived single-homed root attachment experiments. [Wiring and root placement](medium-spanning-tree.md) · [Commands](../operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) · [Archived results](medium-spanning-tree.md#archived-diagnostics)

## Large lab

| ID | Case | Catalogue reference | CLI selector |
| --- | --- | --- | --- |
| LARGE-01 | Two-site baseline and calibration | BASE-06 | Pending |
| LARGE-02 | Interconnect member loss and return | L2 | Pending |
| LARGE-03 | Access or core chassis loss, including crossed failures | DC-01–02, DC-06 | Pending |
| LARGE-04 | Both cores at one site down and return | DC-04, DC-07 | Pending |
| LARGE-05 | DCI partition and restoration | DC-03 | Pending |
| LARGE-06 | Whole-site loss and restoration | DC-05 | Pending |
| LARGE-07 | Active firewall CHR loss and return | BASE-05, G1 | Pending |

Run the same faults in both bridge modes after each passes baseline. The Large lab remains planned.

[Inventory](../../labs/large/README.md) · [Fault definitions](../reference/site-cases.md#core-and-data-center-outage-matrix) · [Bridge-mode plan](../validation-plan.md#large-lab-bridge-mode-comparison)

## Case fields

Each catalogue entry and each saved `case-intent.yaml` has these fields. The saved file also carries
`grading_limits` and `fixes` as resolved for that attempt.

| Field | Meaning |
| --- | --- |
| `name` | Case name: the catalogue key. Saved files carry it as a field. |
| `lab`, `title`, `action` | Lab, short title and what the runner does, as shown in run READMEs. |
| `selectors` | CLI selectors that run the case. Every selector and name is unique across the catalogue. A case without selectors or phases is planned. |
| `graded_flows` | Streams the fault is expected to hit. Their loss is reported per phase and must stay within that phase's `limit_s`. |
| `control_flows` | Streams that must lose nothing. Loss fails the case or, where the check uses the stream to prove the evidence, as for the bypass, makes the run an error. A stream is never both graded and a control. |
| `phases[].key` | `baseline`, `calibration`, or `withdrawal` followed by `restoration`. |
| `phases[].name`, `expected`, `source` | Phase title, the behaviour the manual or a support answer predicts, and the link to that source. |
| `phases[].limit_s` | Longest allowed loss in seconds for each graded stream in that phase. It also bounds flood-stream loss at each receiver in cases that send floods. `0.0` means no loss. Calibration has none and uses `calibration_cut_s`. |
| `grading_limits.calibration_cut_s` | Lower and upper bound in seconds for the measured one-way cut of a calibration. |
| `grading_limits.outside_flood_s` | Longest time unicast may reach a host outside the conversation, for example after a table flush. |
| `grading_limits.mac_relearn_s` | Time from the silent host's first frame until flooding stops and its streams deliver again (`silent-mobile`). |
| `fixes` | MikroTik changelog fixes the case checks: RouterOS version, wording and link. The code fills it from [MikroTik MLAG fixes](../reference/mlag-fixes.md); it is not written in the catalogue. |
| `reboot_intent` | SMALL-06 only: reboot timing and the flood streams that must not return to the sender. |

`grading_limits` defaults to [limits.yaml](../../src/mlag_lab/intent/limits.yaml).

## Stream IDs

A stream ID is the ICMP identifier in the packet captures. The same ID means different endpoints in different
labs and runners, so read a stream ID with the lab and case of its run. `c1` is dc1-traffic-host1, `c2`
dc1-traffic-host2 and `mobile` dc1-mac-move-host. The tables are printed from the runner's flow tables
(`legacy.py`, `direct_topology.py`, `root_topology.py`, `two_pair_topology.py`).

### Small lab, link and MAC cases (`calibrate`, `mobile-move`, `carrier`, `silent-lacp`, `peer-link-loss`, `silent-mobile`, `carrier-flap`)

| Stream | From | To | Path |
| --- | --- | --- | --- |
| 101 | `c1` bond0 | `mobile` bond0 10.110.0.50 | MLAG pair |
| 102 | `c2` bond0 | `mobile` bond0 10.110.0.50 | MLAG pair |
| 201 | `mobile` bond0 | `c1` bond0 10.110.0.11 | MLAG pair |
| 202 | `mobile` bond0 | `c2` bond0 10.110.0.12 | MLAG pair |
| 301 | `c1` eth3 | `c2` eth3 198.51.100.2 | bypass link, no switch |
| 302 | `c1` bond0 | `c2` bond0 10.110.0.12 | MLAG pair |
| 303 | `c2` eth3 | `c1` eth3 198.51.100.1 | bypass link, no switch |
| 501 | `c1` bond0 | 10.110.0.255 (broadcast) | flooded by the MLAG pair |
| 502 | `c1` bond0 | 10.110.0.99 (unknown unicast) | flooded by the MLAG pair |

### Small lab, direct cases (`direct-*`: baseline, calibration, reboots, power loss)

| Stream | From | To | Path |
| --- | --- | --- | --- |
| 101 | `c1` bond0 | `c2` bond0 10.110.0.12 | MLAG pair |
| 201 | `c2` bond0 | `c1` bond0 10.110.0.11 | MLAG pair |
| 301 | `c1` eth3 | `c2` eth3 198.51.100.2 | bypass link, no switch |
| 303 | `c2` eth3 | `c1` eth3 198.51.100.1 | bypass link, no switch |
| 501 | `c1` bond0 | 10.110.0.255 (broadcast) | flooded by the MLAG pair |
| 502 | `c1` bond0 | 10.110.0.99 (unknown unicast) | flooded by the MLAG pair |

### Root-pair and Medium labs

| Stream | From | To | Path |
| --- | --- | --- | --- |
| 101 | `c1` eth1 | `c2` bond0 10.110.0.12 | access switch and MLAG pair |
| 201 | `c2` bond0 | `c1` eth1 10.110.0.11 | access switch and MLAG pair |
| 301 | `c1` eth3 | `c2` eth3 198.51.100.2 | bypass link, no switch |
| 303 | `c2` eth3 | `c1` eth3 198.51.100.1 | bypass link, no switch |

### Two-pair deployment

| Stream | From | To | Path |
| --- | --- | --- | --- |
| 101 | `c1` bond0 | `c2` bond0 10.110.0.12 | both MLAG pairs and the inter-pair bond |
| 201 | `c2` bond0 | `c1` bond0 10.110.0.11 | both MLAG pairs and the inter-pair bond |
| 301 | `c1` eth3 | `c2` eth3 198.51.100.2 | bypass link, no switch |
| 303 | `c2` eth3 | `c1` eth3 198.51.100.1 | bypass link, no switch |

## Broader catalogue

The IDs above track operator runs by lab and sequence. Existing BASE, MOVE, L, S, P, G and DC catalogue IDs track protocol and field-report coverage. [Catalogue and sources](../case-catalog.md)

## Future cases

| ID | Case | Question |
| --- | --- | --- |
| FUT-01 | Single-homed endpoint on an MLAG pair | If a device must use one peer only, how do peer-link loss, the loss of the attached chassis and rejoin affect that endpoint and unrelated dual-attached traffic? Compare with the dual-attached baseline. |
