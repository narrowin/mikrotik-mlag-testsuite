# Case index

Run these stages in order. Restore and verify the baseline before every fault. Keep the case ID when comparing STP disabled and RSTP enabled. Record mode, root placement and repeat separately.

CLI selectors map each case to the existing runner and archived evidence. Pending selectors identify planned work.

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

The [SMALL-06 case definition](../../src/mlag_lab/small-06.yaml) specifies the reboot,
the required switch and client state, and the traffic checks. The runner saves
a copy with each attempt so a replay uses the recorded expectations.

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

## Broader catalogue

The IDs above track operator runs by lab and sequence. Existing BASE, MOVE, L, S, P, G and DC catalogue IDs track protocol and field-report coverage. [Catalogue and sources](../case-catalog.md)

## Future cases

| ID | Case | Question |
| --- | --- | --- |
| FUT-01 | Single-homed endpoint on an MLAG pair | If a device must use one peer only, how do peer-link loss, the loss of the attached chassis and rejoin affect that endpoint and unrelated dual-attached traffic? Compare with the dual-attached baseline. |
