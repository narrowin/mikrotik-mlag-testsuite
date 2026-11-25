# Findings and recommendation

These notes explain causes and give the recommendation. They hold no counts of how often a fault showed and no loss ranges across runs: `mlag-lab export` writes those in the **Faults across runs** section below and in `results/index/faults.tsv`. Quote those, and link single-run details to their run.

## Recommendation

**For the shortest MLAG failover, run the MLAG pair and the bridges directly attached to it with spanning tree off** (`protocol-mode=none`, `forward-reserved-addresses=no`). With one MLAG pair, MLAG peer reboots and power loss stay within the 5 s limit in both labs, and a peer link cut or MAC move loses nothing. Two problems remain on 7.26beta7: when a switch or bond member comes back, broadcast frames loop back to the host that sent them, and with two MLAG pairs a primary reboot of either pair stops traffic for about 20 s.

**This is outside MikroTik's documented design.** The MLAG manual describes MLAG with STP, RSTP or MSTP and never with spanning tree off. Cisco, Arista, Aruba and Juniper all keep spanning tree on for MLAG pairs and turn it off only on the peer link. With spanning tree off, RouterOS ignores `bpdu-guard` and `edge`, so loop protection has to come from `loop-protect` on the access ports, storm control on CRS hardware, or spanning tree on the access switches. Use it where every device below the pair attaches over an MLAG bond, as in a data centre, and see the campus section otherwise. [MikroTik MLAG](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) · [Bridging: forward-reserved-addresses, bpdu-guard](https://manual.mikrotik.com/docs/bridging-and-switching/) · [Loop Protect](https://help.mikrotik.com/docs/spaces/ROS/pages/23396469/Loop+Protect) · [Cisco vPC design guide](https://www.cisco.com/c/dam/en/us/td/docs/switches/datacenter/sw/design/vpc_design/vpc_best_practices_design_guide.pdf)

With spanning tree on, the result depends on which bridge is root for the service VLAN:

- **MLAG pair is root (RSTP or MSTP):** an MLAG primary reboot stops traffic for longer than the 5 s limit in every variant tried (`mlag-lacp-fallback=no`, named MSTP region, MSTI per VLAN, `lacp-strict`). The bridge ID does not change. The saved captures show the cause: only the MLAG primary sends BPDUs, and while it reboots the secondary still reports itself as connected secondary and sends none. The next bridge's root information then expires and it elects a new root. In `rstp-pair-root-run2` the access switch made itself root 6 s after the last BPDU. In the two-pair lab, pair B did the same, with equal priorities and with per-pair priorities alike.
- **Access switch is root of everything:** baseline traffic on VLAN 110 was lost before any fault in most suites. The cause is not traced. In those baselines the bridge port monitor shows both MLAG peers' `access-uplink` as root port and forwarding for most samples, so a blocked port does not explain it. Do not report it until it is traced.
- **MSTP split root:** MLAG pair as root of the default instance, the access switch as root of the MSTI that carries the service VLAN. An MLAG primary reboot stays within the limit, but some MLAG secondary reboots send a unicast request back to its sender, so the setup fails. It is a workaround, not a design: the service VLAN's root sits on a switch outside the pair, and if that switch is lost the root moves back to the pair.

## Campus: where spanning tree goes

In a campus, users can create loops below the MLAG pair, so the pair cannot simply drop loop protection. Spanning tree cannot be carried through an STP-off pair safely: `forward-reserved-addresses=yes` would relay BPDUs, but it also relays LACP, 802.1X and the address MikroTik uses for MLAG and LLDP, and MikroTik advises it only for transparent bridging and analysis.

| Option | Where spanning tree runs | Loop protection | Status |
| --- | --- | --- | --- |
| **1. Boundary at the access uplinks** | Off on the MLAG pair; RSTP on each access switch, with its uplink bond as edge | `bpdu-guard` and `loop-protect` on user ports, storm control on CRS hardware | **Passed in the Medium lab.** The results table gives its runs and longest interruption. The access uplink forwarded. A user loop was not tested: the access switch has no spare port pair. |
| **2. RSTP on the pair, edge toward access** | RSTP on the pair and the access switches; `edge=yes` on the pair's MLAG bonds toward the access switches | Spanning tree everywhere except across those edge bonds, where the access switch's BPDUs are ignored | Untested in the Medium lab. MikroTik suggests `edge=yes` on MLAG bonds only toward devices that do not run RSTP or MSTP, such as servers; the Small lab already uses it that way. Using it toward a spanning-tree access switch goes against that guidance. |
| **3. Standard design** | RSTP or MSTP everywhere, MLAG pair as root | Full spanning tree | Tested: an MLAG primary reboot exceeds the 5 s limit. Safe, but slow. |
| 4. Transparent pair | Off on the pair with `forward-reserved-addresses=yes` | One spanning tree through the pair | Not recommended: undocumented for MLAG and relays LACP and MLAG frames. |

**What option 1 showed:**

- **Why the earlier layout failed:** an access switch uplink that is not an edge port waits for an RSTP agreement from the switch above. With spanning tree off on the MLAG pair, none arrives, so the uplink stayed discarding. With `edge=yes` on the uplink it forwarded at once in every run.
- **The MLAG pair does not relay BPDUs** with `protocol-mode=none` and `forward-reserved-addresses=no`: BPDUs from the access switch reached the pair's ports and went no further.
- **Edge ports send no BPDUs.** `bpdu-guard` therefore only catches another switch plugged in below that sends its own BPDUs. A cable looped between two ports of the same access switch would be caught only by `loop-protect`, which is untested.

**Next tests:** a user loop on the access switch (a patch between two ports, which needs a topology change) to check that `bpdu-guard` or `loop-protect` disables the loop port and not the uplink, and option 2. The lab cannot test loops between two access switches, storm control (CHR has no switch chip) or hardware-offloaded MLAG.

## What these results do not cover

- **Power loss:** tested virtually with spanning tree off: every data link of one CHR drops carrier, the guest stops for 20 s, then boots. All cases passed in both labs. Power off itself cost no loss; the only loss in the Small lab came when the MLAG primary returned. That is less than a reboot, likely because carrier loss removes the bond member at once (inferred, not measured). A physical bench test with real switches still needs hardware.
- **Large lab and real hardware:** not run yet.
- **Loops below the MLAG pair:** the labs have no access switches connected to each other and no user-made loops, so they cannot show how a network with spanning tree off reacts to a loop. See the campus section.
- **Repeats:** most setups ran only a few times. The results tables give the runs of each setup.

RouterOS 7.26beta7 CHRs in Containerlab, 24 November 2026. Working log: [docs/plans/outage-free-setup-search.md](../docs/plans/outage-free-setup-search.md).

## Looped and reflected frames

The counts are in **Faults across runs** below. This section explains what the packet captures show.

- **A unicast request comes back to its sender with RSTP or MSTP (Medium lab).** Client 2 sent the request once. It reached the rebooting MLAG peer over the peer link and left on that peer's client 2 bond member, back to client 2, a few milliseconds after it was sent. This happened while the rebooting peer brought its ports up, before the runner saw the guest boot. It shows with the MLAG pair as root and with the access switch as root of VLAN 110 only, and never with spanning tree off. Client 2's `bond0` capture shows the request only once, because the Linux bond did not take the returned copy. The copy did cross the wire, so this is a reflected copy at the source (M6), not a wrong capture map.
- **Flood frames come back to their sender with spanning tree off (Small lab).** In `member-flap-repeat`, `secondary-reboot` and `secondary-power-loss`, a broadcast or unknown-unicast frame from client 1 was seen a second time at client 1's own bond members. The captures show one path: the frame crossed the peer link and left the other MLAG peer on its member of client 1's MLAG bond, while that bond was up on both peers. In the member flap this came shortly after the member returned, before the returning peer's first LACPDU. In the reboot and power-loss cases it came shortly before the runner saw the guest uptime reset, at the end of the withdrawal phase. [`validation-none-reboot-power/01-secondary-reboot`](2026-11-24-forwarding-checks/validation-none-reboot-power/01-secondary-reboot) returned frames 399 to 408 in a row.
- **Client 2 gets two copies during a Small lab primary reboot.** Client 2 received a client 1 flood frame once from the booting MLAG primary and once from the MLAG secondary over the peer link ([run 01](2026-11-24-forwarding-checks/validation-none-reboot-power/01-primary-reboot) seq 348, [run 02](2026-11-24-forwarding-checks/validation-none-reboot-power/02-primary-reboot) seq 263). Client 2's bond had taken the booting primary's member into its aggregator about 2 s before. Loss stayed within the limit. Why primary power loss behaves differently from the reboot is not checked.
- **The fix "Packets looped back to a dual-connected bond", listed for 7.25.2 and 7.26beta7, does not fully hold on 7.26beta7.** With spanning tree off no unicast request came back to its sender, so there the remaining fault shows only with flood traffic. Only 7.26beta7 was tested.
- **Other checks held in the spanning-tree-off runs.** No unicast frame reached an unrelated host on the Small lab. After recovery every traffic host MAC sat on its MLAG bond on every MLAG peer, and the MAC-move host sat on `ether5` of one peer and the peer port of the other. Both members of every host bond saw one LACP system ID. No spanning-tree frame appeared on any port. Every MLAG warning in syslog was `MLAG: remote heartbeat timeout` during a reboot: no run logged `failed to sync` or `attempting to resync` (P2), and none logged a warning in the baseline phase.

## Two MLAG pairs with spanning tree off

Rebooting the MLAG primary of pair A or pair B stops streams 101 and 201 for about 20 s, against 5 s. The bypass stream lost nothing. Rebooting either MLAG secondary lost nothing, and the inter-pair member flap stayed within its limit. The one-pair Medium lab with spanning tree off passed every reboot, so the outage needs the second pair. The cause is traced in the [fault report](../docs/plans/routeros-failures-report.md#fault-2-two-mlag-pairs-keep-sending-into-a-rebooting-switch).

## Medium lab with spanning tree off

The Medium lab passed every case with spanning tree off. `medium-core-off-*` runs RSTP on the access switch, which the operator's instruction for live runs excluded. Its result is listed but not used for the recommendation.

The spanning-tree-off live runs of 24 November, with the broadcast stream 501, the unknown-unicast stream 502 and checks A to D graded, are in these suites: [stable-none-plink-macmove-flap](2026-11-24-forwarding-checks/stable-none-plink-macmove-flap/README.md), [validation-none-reboot-power](2026-11-24-forwarding-checks/validation-none-reboot-power/README.md), [ext-medium-stp-off](2026-11-24-forwarding-checks/ext-medium-stp-off/README.md), [ext-medium-core-off](2026-11-24-forwarding-checks/ext-medium-core-off/README.md), [debian-two-pair-stp-off-flap-once](2026-11-24-forwarding-checks/debian-two-pair-stp-off-flap-once/README.md) and [debian-two-pair-stp-off-suite](2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/README.md).
