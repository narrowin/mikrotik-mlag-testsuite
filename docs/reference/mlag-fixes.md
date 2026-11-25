# MikroTik MLAG fixes and the tests that check them

[Case catalogue](../case-catalog.md) · [Case index](../cases/README.md) · [Research](research.md)

This page lists every MLAG line in the RouterOS changelogs from 7.14 to 7.26beta7 and names the test in this suite that checks it. The changelogs were read on 24 November 2026 from MikroTik's download server. The fix text is MikroTik's own wording.

All tests here run on RouterOS **7.26beta7** on CHR. A pass shows that the fixed behaviour holds in RouterOS's software bridge. It does not cover the switch chip on CRS hardware.

## How to read the state column

| State | Meaning |
| --- | --- |
| **Checked** | A case that runs today grades this behaviour. |
| **Indirect** | A case that runs today would fail if the fault came back, but no check names it. |
| **In progress** | The check or case is being added. |
| **Not checked** | No test yet. The row names what is missing. |
| **Hardware only** | The fix is in the switch chip or hardware offload path. CHR cannot show it. |

## Fixes in the 7.25 and 7.26 lines

| What MikroTik fixed | Listed in | Test in this suite | State and result on 7.26beta7 |
| --- | --- | --- | --- |
| Dual-bond hosts dropped when an MLAG peer is lost | [7.25.2], [7.26beta7] | Reboot and power loss of each MLAG peer on the Small, Medium and two-pair labs: `primary-reboot`, `secondary-reboot`, `primary-power-loss`, `secondary-power-loss`, `medium-*-reboot-*`, `two-pair-*-reboot-*`. Hosts on MLAG bonds must forward again within 5 s. Catalogue M6. | **Checked, and it fails on the two-pair lab.** With STP off on one MLAG pair, reboots and power loss stay within 5 s on the Small and Medium labs. With STP off on the two-pair lab, an MLAG primary reboot of either pair stops streams 101 and 201 for about 20 s against 5 s, and the secondary reboots lose nothing. With RSTP or MSTP and the pair as root, an MLAG primary reboot exceeds 5 s. Counts, loss ranges and runs: [Faults across runs](../../results/README.md#faults-across-runs). |
| Packets looped back to a dual-connected bond | [7.25.2], [7.26beta7] | Every case fails on a duplicate ping. The Medium STP-off baseline requires each ARP broadcast exactly once. Check B (reflected copies) and the broadcast and unknown-unicast streams add direct proof. Catalogue M6, BASE-03. | **Checked, and it fails.** With STP off on the Small lab, a broadcast or unknown-unicast frame from client 1 (streams 501 and 502) came back to client 1's own bond members in `member-flap-repeat`, `secondary-reboot` and `secondary-power-loss`, and client 2 got a second copy in `primary-reboot`. Loss stayed within the limit in these runs. With RSTP or MSTP on the Medium lab, a unicast request came back to client 2 in MLAG peer reboots. With STP off, check B found no unicast request sent back. Counts and runs: [Faults across runs](../../results/README.md#faults-across-runs). Each run's `result.json` names the sequence numbers. |
| BPDUs leaking to the wrong dual-connected bond (introduced in 7.24) | [7.24.6], [7.25.1], [7.26beta5], [7.26beta7] | The STP-off cases require zero spanning-tree frames on every port. Catalogue S2. | **Checked** with STP off: no BPDU on any port. **Not checked** with RSTP or MSTP: no check yet proves that the access switch's BPDUs stay off the traffic host's MLAG bond in the Medium lab. The captures for it already exist. |
| Wrong root-path-cost when the root bridge is on a single-connected port | [7.25.2], [7.26beta4], [7.26beta5], [7.26beta7] | The archived single-homed root experiments (MEDIUM-05, MEDIUM-06). Catalogue S3. | **Not checked.** The archived runs can be replayed, but no case that runs today has a single-connected root. |
| LACP system ID not synchronised when bonds are created before MLAG | [7.25.2], [7.26beta7] | Every lab's startup config creates the bonds before the bridge with `mlag-peer-port`, so every deploy uses the fixed order. The baseline requires both bond members of each host to collect and distribute, which a Linux LACP bond does only when both MLAG peers present one system ID. Catalogue L3. | **Checked.** In the STP-off runs of 24 November both bond members of every host saw one LACP system ID from the two MLAG peers, for example 65535/52:54:00:d7:0b:02 on client 1 in the Small lab. |
| Rate limit for MLAG FDB sync warnings, with the failing MAC and VID | [7.25.2], [7.26beta7] | Check D counts `failed to sync`, `attempting to resync` and `heartbeat timeout` lines in the syslog of every run. Catalogue P2. | **Checked** in the baseline phase: no warning in any STP-off run of 24 November. Warnings during a fault are recorded, not graded. |
| MLAG restarting when hardware offloading is re-enabled | [7.25.2], [7.26beta5] | None. Catalogue H1. | **Hardware only.** |
| VLAN-tagged traffic looped back in MLAG on CRS8xx | [7.24.6], [7.25], [7.26beta3] | None. Catalogue H1. | **Hardware only.** |
| Better FDB synchronisation between MLAG peers when VLANs are added | [7.25], [7.25.1] | None. Catalogue M5, P3. | **Not checked.** Needs a second VLAN in the Small lab. |
| New settings `mlag-lacp-fallback` and `mlag-init-delay` | [7.25] | `reboot-primary-no-fallback` and the fallback-off suites compare both fallback values. The return phase of every reboot and the 65 s return window of `peer-link-loss` cover `mlag-init-delay`. Catalogue L1. | **Checked.** `mlag-lacp-fallback=no` did not shorten the primary reboot outage with the pair as root. |
| MLAG peer stuck in the disabled state after config changes | [7.25] | Before every run the runner disables the bridge, sets the bridge mode and priority, enables it and requires `mlag-state` connected. Catalogue P3. | **Indirect.** Every one of the 196 runs with a verdict started from such a reset. No case edits ports or VLANs under load. |
| VRRP MAC behaviour in MLAG | [7.25] | None. Catalogue G1, G3. | **Not checked.** Needs VRRP gateways. |
| MVRP with MLAG dual bonds | [7.25] | None. Catalogue X2. | **Not checked.** |
| New setting `lacp-strict` for 802.3ad bonds | [7.26beta4] | The `lacp-strict` suites on the Small lab and `two-pair-stp-off-strict-*`. | **Checked.** |

## Fixes in 7.14 to 7.24

| What MikroTik fixed | Listed in | Test in this suite | State and result on 7.26beta7 |
| --- | --- | --- | --- |
| STP, BPDU and topology-change handling with MLAG; dual-connected port STP state in sync with the MLAG peer | [7.24] | Reboots with RSTP and MSTP on the Medium and two-pair labs. Catalogue S1. | **Checked, and it fails.** While the MLAG primary reboots, the secondary sends no BPDUs, the next bridge elects a new root and traffic stops for longer than 5 s. Counts and loss ranges: [Faults across runs](../../results/README.md#faults-across-runs). |
| MLAG MAC address handling for ageing, flushing and moving | [7.24] | `mac-move` moves a MAC between the two MLAG peers and back. `mac-age-relearn` adds ageing. Catalogue M1, M2, MOVE-01. | **Checked** for the move: the later runs, including the STP-off runs with the flood streams, passed with no loss and no frame to the old port. **In progress** for ageing. |
| Better MLAG host ageing and deletion | [7.24.1] | Same cases as the row above, plus check C on the bridge host table after recovery. Catalogue M1, M3. | **Checked** after recovery: in every STP-off run of 24 November with a recovery window, each traffic host MAC sat on its expected port on both MLAG peers. **In progress** for ageing. |
| Forwarding through the peer port after disabling MLAG | [7.24] | None. Catalogue P3. | **Not checked.** |
| Stuck MLAG session with mismatched L2MTU (introduced in 7.23) | [7.24] | None. Catalogue P3. | **Not checked.** |
| MLAG for CRS8xx | [7.24.1] | None. | **Hardware only.** |
| MAC synchronisation between MLAG peers, local and static MACs, `aged` and `aged-peer` flags | [7.22], [7.22.2], [7.23] | Check C reads the bridge host table on both MLAG peers. Catalogue M3, M7. | **In progress.** |
| MAC moving between regular ports and bonds | [7.22] | `mac-move`: the MAC-move host sits on a regular bridge port of each MLAG peer. Catalogue MOVE-01. | **Checked** between regular ports on two peers. A move between a regular port and an MLAG bond is not tested. |
| MLAG state permanently disabled after changing bridge settings | [7.22] | The bridge reset before every run. | **Indirect**, as above. |
| Host learning in MLAG reworked | [7.20] | Checks A and C. | **In progress.** |
| `mlag-heartbeat`; no peer port reset on heartbeat timeout, a warning is logged | [7.18] | `peer-link-loss` holds the peer link down for three heartbeat intervals and requires `mlag-state` connected after the return. `primary-sustained-stop` holds the primary stopped with carrier up. Check D counts the warnings. Catalogue P1, P2. | **Checked** for the peer link: passed in all three bridge modes, including the STP-off runs with the flood streams, with no loss. Check D grades the warning count in the baseline only. |
| MLAG connection after a peer link flap (introduced in 7.13) | [7.14] | `peer-link-loss`. Catalogue P1. | **Checked.** Passed in all three bridge modes. |
| MLAG with MSTP: support and stability | [7.14], [7.18] | The MSTP cases on the Small and Medium labs. Catalogue S4. | **Checked.** Small lab passes. On the Medium lab only the split-root setup passes. |
| Priority setting to elect the MLAG primary | [7.17] | Every baseline requires one primary and one secondary. One Small suite swaps the priorities. | **Checked.** |
| MLAG system ID re-synchronised when the bridge MAC changes | [7.17] | None. | **Not checked.** |
| Port ID when adding a port on the non-primary MLAG peer | [7.20] | None. Catalogue P3. | **Not checked.** |
| Stability when removing MLAG configuration | [7.16] | None. | **Not checked.** |

## What this shows

- Of the 14 lines in the 7.25 and 7.26 table, 7 are checked today, 1 is covered indirectly, 4 are not checked and 2 are hardware only.
- Two fixes listed for 7.25.2 and 7.26beta7 fail on 7.26beta7 with STP off. Flood frames return to a dual-connected bond after a member flap and around an MLAG peer reboot or power loss on the Small lab. A primary reboot on the two-pair lab stops traffic for about 20 s. Counts: [Faults across runs](../../results/README.md#faults-across-runs).
- BPDUs on the wrong MLAG bond with RSTP or MSTP still have no direct check, although the captures for it already exist.
- The area MikroTik changed in 7.24, spanning tree state in sync with the MLAG peer, is where this suite still measures the longest outages on 7.26beta7.
- Fixes for config edits under load, VRRP, MVRP and a single-connected root have no test here.

## Changelog sources

Each link is the plain-text changelog on MikroTik's download server.

[7.14]: https://cdn.mikrotik.com/routeros/7.14/CHANGELOG
[7.16]: https://cdn.mikrotik.com/routeros/7.16/CHANGELOG
[7.17]: https://cdn.mikrotik.com/routeros/7.17/CHANGELOG
[7.18]: https://cdn.mikrotik.com/routeros/7.18/CHANGELOG
[7.20]: https://cdn.mikrotik.com/routeros/7.20/CHANGELOG
[7.22]: https://cdn.mikrotik.com/routeros/7.22/CHANGELOG
[7.22.2]: https://cdn.mikrotik.com/routeros/7.22.2/CHANGELOG
[7.23]: https://cdn.mikrotik.com/routeros/7.23/CHANGELOG
[7.24]: https://cdn.mikrotik.com/routeros/7.24/CHANGELOG
[7.24.1]: https://cdn.mikrotik.com/routeros/7.24.1/CHANGELOG
[7.24.6]: https://cdn.mikrotik.com/routeros/7.24.6/CHANGELOG
[7.25]: https://cdn.mikrotik.com/routeros/7.25/CHANGELOG
[7.25.1]: https://cdn.mikrotik.com/routeros/7.25.1/CHANGELOG
[7.25.2]: https://cdn.mikrotik.com/routeros/7.25.2/CHANGELOG
[7.26beta3]: https://cdn.mikrotik.com/routeros/7.26beta3/CHANGELOG
[7.26beta4]: https://cdn.mikrotik.com/routeros/7.26beta4/CHANGELOG
[7.26beta5]: https://cdn.mikrotik.com/routeros/7.26beta5/CHANGELOG
[7.26beta7]: https://cdn.mikrotik.com/routeros/7.26beta7/CHANGELOG

The 7.15 changelog has three more MLAG lines that add log events and config validation. They need no test.
