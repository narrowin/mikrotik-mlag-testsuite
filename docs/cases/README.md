# Case index

This page lists every case of the suite by lab. Run the cases of a lab in the order of its table. Before every fault, bring the lab back to its normal state and check that state again. When you compare a run with spanning tree off and a run with RSTP on, keep the same case ID. Record the bridge mode, the bridge that is root and the number of the run separately.

The CLI selector is the name that you pass to `mlag-lab run --case`. It tells the suite which case to run and links the case to its archived evidence. A case marked Pending or Planned has no selector yet.

The [case catalogue](../../src/mlag_lab/intent) defines every case. It has one file per lab and kind of fault. Each new run of a case saves the rules it used in the file `case-intent.yaml`. When the suite scores a saved run again, it uses only that file. A later change to the catalogue therefore does not change the limits of a recorded run. A run without that file stops with an error that names the run.

The catalogue holds what the suite judges from the captured packets. These are the phases, the loss limits, the streams that must recover within a limit and the streams that must lose nothing. The state that the switches and hosts must show before the fault and after it is kept separately. It is Networka intent in [intent/state/](../../src/mlag_lab/intent/state), with one file per lab and one file per setup. Networka collects that state and checks it. Each run saves the result in the folders `gate-baseline/` and `gate-restored/`. The section [Device state and packet grading](../test-framework.md#device-state-and-packet-grading) explains both parts.

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

The Small lab cases run with RSTP unless you choose otherwise. Add `--bridge-mode none` to run them with spanning tree off.

The entry `secondary-reboot` in the [Small catalogue](../../src/mlag_lab/intent/small.yaml) defines SMALL-06. Its loss limits and streams are in the same fields as in every other case. The extra field `reboot_intent` holds only two things. These are the timing of the reboot and the flooded streams that must not come back to their sender. The state that the switches and clients must show is the Small lab check. It consists of [direct.yaml](../../src/mlag_lab/intent/state/direct.yaml), [hosts.yaml](../../src/mlag_lab/intent/state/hosts.yaml) and the file of the bridge mode of the run.

- [Devices of the Small lab](../../labs/small/README.md)
- [Client link loss and return](small-client-link.md)
- [Commands for the reboot cases](../operator-guide.md#reboot-the-direct-client-pair)
- [Results](../../results/2026-11-24-small-lab/README.md)

## Medium lab

| ID | Case | STP off | RSTP, core pair root | RSTP, access switch root |
| --- | --- | --- | --- | --- |
| MEDIUM-01 | Baseline | `medium-stp-off-baseline` | `medium-pair-root-baseline` | `medium-access-root-baseline` |
| MEDIUM-02 | One-way calibration | `medium-stp-off-calibrate` | `medium-pair-root-calibrate` | `medium-access-root-calibrate` |
| MEDIUM-03 | Secondary reboot | `medium-stp-off-reboot-secondary` | `medium-pair-root-reboot-secondary` | `medium-access-root-reboot-secondary` |
| MEDIUM-04 | Primary reboot | `medium-stp-off-reboot-primary` | `medium-pair-root-reboot-primary` | `medium-access-root-reboot-primary` |
| MEDIUM-07 | Both cores down and return | Planned | Planned | Planned |

MEDIUM-08 uses a separate lab with two MLAG pairs. One distributed bond joins the two pairs. The case runs once with the same bridge priority on all switches and once with one priority per pair, as in the field network. The [two-pair page](medium-two-pair-root.md) explains why the case exists, how the lab is built and how to run it.

MEDIUM-08 also has the step `interpair-member-flap` for every two-pair setup, for example `two-pair-equal-interpair-member-flap`. It takes the inter-pair bond member between CHR 1 and CHR 3 down for 8 s and then brings it back. In the four-switch field report, such a member flap set off the problem (catalogue M4).

MEDIUM-05 and MEDIUM-06 are the archived experiments in which each root bridge had a single cable to the MLAG pair.

- [Wiring and placement of the root](medium-spanning-tree.md)
- [Commands](../operator-guide.md#introduce-rstp-after-the-all-bridges-off-run)
- [Archived results](medium-spanning-tree.md#archived-diagnostics)

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

The Large lab is still planned. Each fault will run in both bridge modes, after the baseline of that mode has passed.

- [Devices of the Large lab](../../labs/large/README.md)
- [Definitions of the faults](../reference/site-cases.md#core-and-data-center-outage-matrix)
- [Plan for the two bridge modes](../validation-plan.md#large-lab-bridge-mode-comparison)

## Case fields

Each entry of the catalogue and each saved `case-intent.yaml` has these fields. The saved file also holds `grading_limits` and `fixes` with the values that applied to that run.

| Field | Meaning |
| --- | --- |
| `name` | The name of the case. In the catalogue it is the key of the entry. A saved file holds it as a field. |
| `lab`, `title`, `action` | The lab, a short title, and what the runner does. The README of a run shows all three. |
| `selectors` | The CLI selectors that run the case. No selector and no name appears twice in the catalogue. A case without selectors or phases is planned. |
| `graded_flows` | The streams that the fault is expected to interrupt. The report shows their loss for each phase. The loss must stay within the `limit_s` of that phase. |
| `control_flows` | The streams that must lose nothing. Loss on such a stream fails the case. Some checks use a stream to prove that the measurement works, for example the streams on the direct cable. Loss on such a stream makes the run an error instead. No stream is in both lists. |
| `phases[].key` | The name of the phase. It is `baseline`, `calibration`, or `withdrawal` followed by `restoration`. `withdrawal` is the time after the fault starts, for example after a cable goes down. `restoration` is the time after the fault ends, for example after the cable comes back. |
| `phases[].name`, `expected`, `source` | The title of the phase, the behaviour that the MikroTik manual or a MikroTik support answer predicts, and the link to that source. |
| `phases[].limit_s` | The longest loss in seconds that each graded stream may have in that phase. In cases that send flooded streams, it also limits the loss of those streams at each receiver. `0.0` means that no loss is allowed. A calibration has no `limit_s`. It uses `calibration_cut_s` instead. |
| `grading_limits.calibration_cut_s` | The lower and the upper bound in seconds for the measured one-way cut of a calibration. |
| `grading_limits.outside_flood_s` | The longest time during which unicast traffic may reach a host that is not part of the conversation, for example after the MAC table was flushed. |
| `grading_limits.mac_relearn_s` | The time from the first frame of the silent host until flooding stops and its streams arrive again. It applies to `silent-mobile`. |
| `fixes` | The fixes from MikroTik changelogs that the case checks, each with RouterOS version, wording and link. The code fills this field from [MikroTik MLAG fixes](../reference/mlag-fixes.md). The catalogue does not contain it. |
| `reboot_intent` | Used by SMALL-06 only. It holds the timing of the reboot and the flooded streams that must not come back to their sender. |

When a case sets no `grading_limits`, the values in [limits.yaml](../../src/mlag_lab/intent/limits.yaml) apply.

## Stream IDs

A stream is one series of pings from one host to another. Its stream ID is the ICMP identifier of those pings in the packet captures. The same ID stands for different hosts in different labs and runners. Always read a stream ID together with the lab and the case of its run.

In the tables, `c1` is dc1-traffic-host1 and `c2` is dc1-traffic-host2. `mobile` is dc1-mac-move-host. The tables are printed from the stream tables of the runner in `legacy.py`, `direct_topology.py`, `root_topology.py` and `two_pair_topology.py`.

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

The IDs on this page number the runs of each lab in order. The older IDs BASE, MOVE, L, S, P, G and DC come from the [list of cases and their sources](../case-catalog.md). They show which protocol behaviour and which field report a case covers.

## Future cases

| ID | Case | Question |
| --- | --- | --- |
| FUT-01 | Single-homed endpoint on an MLAG pair | If a device must use one peer only, how do peer-link loss, the loss of the attached chassis and rejoin affect that endpoint and unrelated dual-attached traffic? Compare with the dual-attached baseline. |
