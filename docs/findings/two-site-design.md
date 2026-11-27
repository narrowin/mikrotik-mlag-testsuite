# Two-site design: two straight DCI links leave no path when opposite cores fail

With two straight DCI links, the sites lose their connection when one core fails at each site on opposite sides.
A full mesh of four DCI links keeps one link whenever at least one core per site survives.
MikroTik documents neither design for two MLAG pairs joined to each other.

[ADR 0017](../adr/0017-the-large-lab-joins-its-sites-with-two-straight-dci-links-and-has-one-vrrp-firewall-per-site.md) records why the [Large lab](../../tests/large/README.md) uses two straight DCI links and one VRRP firewall per site.
This page records the design facts behind it, from the two-site design of the old suite at commit `95c7482`.
The link counts below follow from the wiring; they are not measurements.

## DCI links that survive a fault

The DCI joins the core pair of `dc1` with the core pair of `dc2` as one inter-pair bond.
The straight design has `dc1-core1` to `dc2-core1` and `dc1-core2` to `dc2-core2`.
The full mesh adds `dc1-core1` to `dc2-core2` and `dc1-core2` to `dc2-core1` to the same bond.

| Fault | Two straight links | Four links, full mesh |
| --- | --- | --- |
| No fault | 2 | 4 |
| One DCI cable | 1 | 3 |
| One core at either site | 1 | 2 |
| Same-index cores, such as `dc1-core1` and `dc2-core1` | 1 | 1 |
| Opposite-index cores, such as `dc1-core1` and `dc2-core2` | 0 | 1 |
| Both cores at one site, or every DCI cable | 0 | 0 |

- Two straight links are enough if the requirement is any single core or DCI cable fault and one link can carry the load.
- Four links are needed if any one core at each site may fail at the same time, or if two links of capacity must survive one core fault.
- Two links in the same conduit can fail together, so count physical routes, not cables.
- A RouterOS ingress switch hashes traffic only over its own active local bond members, so traffic entering one core can use only that core's DCI links.

## Distribution-to-core links

The same count applies between a distribution pair and its core pair inside one site. The straight design has `dc1-dist1` to `dc1-core1` and `dc1-dist2` to `dc1-core2`; the crossed design has the other two.

| Fault | Two straight | Two crossed | Four, full mesh |
| --- | --- | --- | --- |
| One cable | 1 | 1 | 3 |
| One switch | 1 | 1 | 2 |
| `dc1-dist1` and `dc1-core1` | 1 | 0 | 1 |
| `dc1-dist1` and `dc1-core2` | 0 | 1 | 1 |
| Both switches of one tier | 0 | 0 | 0 |

- Two crossed links cover the same single faults as two straight links, but a different pair of double faults.

## What MikroTik documents

- The [MLAG manual](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) shows one link from each MLAG peer to a common LACP partner, and two local bond members per MLAG peer in a four-member MLAG bond.
- The peer ports must be directly connected, and MikroTik recommends a bond of several physical links as the peer link.
- ICCP uses untagged link-local Ethernet frames on the peer link, so a carrier service between the peer ports of one MLAG pair needs MikroTik's confirmation.
- Every extended VLAN must be tagged on both peer ports, and spanning-tree settings must match within a pair.
- Known unicast for an MLAG bond crosses the peer link only when the ingress MLAG peer has no active local bond member of that bond.
- The manual and the public MikroTik replies reviewed on 24 November 2026 give no approval or recommendation for two straight links between two MLAG pairs.

## Configuration rules from the design

- Both MLAG peers of a pair give their bond toward the other pair the same `mlag-id`, and each pair uses its own ID, such as `21` on the distribution pair and `31` on the core pair.
- Unrelated bonds on the same pair get distinct IDs.
- A bond used as the peer link is a plain LACP bond with no `mlag-id`.
- Bond members are equal-speed and full duplex, with MII link monitoring and `lacp-rate=1sec`.
- Every bond between switches is `edge=no` on all four switches of the two pairs.

## Field reports

- A November 2026 report of two interconnected CRS326 pairs saw instability after bond member changes on 7.25.1, and ran stable with one interconnect cable disconnected: [forum thread](https://forum.mikrotik.com/t/two-interconnected-mlag-pairs-on-crs326-which-routeros-versions-are-stable/274258).
- Other operators reported a working four-member MLAG bond and shorter failover with a full mesh: [four-member MLAG bond](https://forum.mikrotik.com/t/mlag-vlan-filtering-rstp-breaks-everything/269081/2), [full-mesh reboot comparison](https://forum.mikrotik.com/t/connect-mlag-to-another-mlag/184077/5).
- The report of an outage on rejoin with exactly the straight two-link wiring is cited in ADR 0017.
- The 7.26beta7 announcement lists further MLAG fixes for BPDUs sent to the wrong bond and for path cost with an external root: [7.26beta announcement](https://forum.mikrotik.com/t/7-26beta-development-is-released/273582).

## Not built

- The full mesh, the crossed distribution links and a core pair stretched between the sites are not built as labs.
- A stretched core pair would need its peer link carried between the sites, which MikroTik would have to confirm.
