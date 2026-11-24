# Findings and recommendation

## Recommendation

**For outage-free MLAG failover, run the MLAG pair and the bridges directly attached to it with spanning tree off** (`protocol-mode=none`, `forward-reserved-addresses=no`). It is the only setup that passed every case in both labs: MLAG peer reboots cost 2.0–2.9 s of traffic, a returning bond member 2.3–2.9 s, a peer link cut or MAC move nothing.

**This is outside MikroTik's documented design.** The MLAG manual describes MLAG with STP, RSTP or MSTP and never with spanning tree off. Cisco, Arista, Aruba and Juniper all keep spanning tree on for MLAG pairs and turn it off only on the peer link. With spanning tree off, RouterOS ignores `bpdu-guard` and `edge`, so loop protection has to come from `loop-protect` on the access ports, storm control on CRS hardware, or spanning tree on the access switches. Use it where every device below the pair attaches over an MLAG bond, as in a data centre, and see the campus section otherwise. [MikroTik MLAG](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) · [Bridging: forward-reserved-addresses, bpdu-guard](https://manual.mikrotik.com/docs/bridging-and-switching/) · [Loop Protect](https://help.mikrotik.com/docs/spaces/ROS/pages/23396469/Loop+Protect) · [Cisco vPC design guide](https://www.cisco.com/c/dam/en/us/td/docs/switches/datacenter/sw/design/vpc_design/vpc_best_practices_design_guide.pdf)

With spanning tree on, the result depends on which bridge is root for the service VLAN:

- **MLAG pair is root (RSTP or MSTP):** an MLAG primary reboot stops traffic for 10.9–13.1 s, in every variant tried (`mlag-lacp-fallback=no`, named MSTP region, MSTI per VLAN, `lacp-strict`). The bridge ID does not change. The saved captures show the cause: only the MLAG primary sends BPDUs, and while it reboots the secondary still reports itself as connected secondary and sends none. The next bridge's root information then expires and it elects a new root. In `rstp-pair-root-run2` the access switch made itself root 6 s after the last BPDU. In the two-pair lab, pair B did the same, with equal priorities and with per-pair priorities alike.
- **Access switch is root of everything:** VLAN 110 did not forward at all with default settings.
- **MSTP split root passes:** MLAG pair as root of the default instance, the access switch as root of the MSTI that carries the service VLAN, and `mlag-lacp-fallback=no`. It passed three times. It is a workaround, not a design: the service VLAN's root sits on a switch outside the pair, and if that switch is lost the root moves back to the pair.

## Campus: where spanning tree goes

In a campus, users can create loops below the MLAG pair, so the pair cannot simply drop loop protection. Spanning tree cannot be carried through an STP-off pair safely: `forward-reserved-addresses=yes` would relay BPDUs, but it also relays LACP, 802.1X and the address MikroTik uses for MLAG and LLDP, and MikroTik advises it only for transparent bridging and analysis.

| Option | Where spanning tree runs | Loop protection | Status |
| --- | --- | --- | --- |
| **1. Boundary at the access uplinks** | Off on the MLAG pair; RSTP on each access switch, with its uplink bond as edge | `bpdu-guard` and `loop-protect` on user ports, storm control on CRS hardware | **Passed in the Medium lab**, 2 runs: MLAG peer reboots 1.9–2.9 s while down, power loss at most 0.42 s. The access uplink forwarded. A user loop was not tested: the access switch has no spare port pair. |
| **2. RSTP on the pair, edge toward access** | RSTP on the pair and the access switches; `edge=yes` on the pair's MLAG bonds toward the access switches | Spanning tree everywhere except across those edge bonds, where the access switch's BPDUs are ignored | Untested in the Medium lab. MikroTik suggests `edge=yes` on MLAG bonds only toward devices that do not run RSTP or MSTP, such as servers; the Small lab already uses it that way. Using it toward a spanning-tree access switch goes against that guidance. |
| **3. Standard design** | RSTP or MSTP everywhere, MLAG pair as root | Full spanning tree | Tested: 10.9–13.1 s outage on an MLAG primary reboot. Safe, but slow. |
| 4. Transparent pair | Off on the pair with `forward-reserved-addresses=yes` | One spanning tree through the pair | Not recommended: undocumented for MLAG and relays LACP and MLAG frames. |

**What option 1 showed:**

- **Why the earlier layout failed:** an access switch uplink that is not an edge port waits for an RSTP agreement from the switch above. With spanning tree off on the MLAG pair, none arrives, so the uplink stayed discarding. With `edge=yes` on the uplink it forwarded at once in every run.
- **The MLAG pair does not relay BPDUs** with `protocol-mode=none` and `forward-reserved-addresses=no`: BPDUs from the access switch reached the pair's ports and went no further.
- **Edge ports send no BPDUs.** `bpdu-guard` therefore only catches another switch plugged in below that sends its own BPDUs. A cable looped between two ports of the same access switch would be caught only by `loop-protect`, which is untested.

**Next tests:** a user loop on the access switch (a patch between two ports, which needs a topology change) to check that `bpdu-guard` or `loop-protect` disables the loop port and not the uplink, and option 2. The lab cannot test loops between two access switches, storm control (CHR has no switch chip) or hardware-offloaded MLAG.

## What these results do not cover

- **Power loss:** tested virtually with spanning tree off: every data link of one CHR drops carrier, the guest stops for 20 s, then boots. All cases passed in both labs. Power off itself cost no loss; the only loss, 0.33–0.79 s in the Small lab, came when the MLAG primary returned. That is less than a reboot, likely because carrier loss removes the bond member at once (inferred, not measured). One run each. A physical bench test with real switches still needs hardware.
- **Large lab and real hardware:** not run yet.
- **Loops below the MLAG pair:** the labs have no access switches connected to each other and no user-made loops, so they cannot show how a network with spanning tree off reacts to a loop. See the campus section.
- **Repeats:** most setups ran one to three times.

RouterOS 7.26beta7 CHRs in Containerlab, 24 November 2026. Working log: [docs/plans/outage-free-setup-search.md](../docs/plans/outage-free-setup-search.md).
