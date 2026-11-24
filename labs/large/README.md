# Large lab

![Two-site lab with a CHR firewall at each site sharing a VRRP address](../../docs/diagrams/large-lab.png)

The planned Large lab spans Site A and Site B. Each site has a core MLAG pair, a distribution MLAG pair and one RouterOS CHR firewall.

| Site | Core switches | Distribution switches |
| --- | --- | --- |
| Site A | `dc1-core-mlag1`, `dc1-core-mlag2` | `dc1-access-mlag1`, `dc1-access-mlag2` |
| Site B | `dc2-core-mlag1`, `dc2-core-mlag2` | `dc2-access-mlag1`, `dc2-access-mlag2` |

Each pair has its own peer link. Distributed LACP trunks connect distribution to core within each site. The DCI connects the two core pairs. Two-member and four-member interconnects are separate wiring variants.

| Site | RouterOS CHR firewall | Traffic and service hosts |
| --- | --- | --- |
| Site A | `dc1-firewall1` | `dc1-traffic-host1`, `dc1-service-host1` |
| Site B | `dc2-firewall1` | `dc2-traffic-host1`, `dc2-service-host1` |

Deployment and management addresses remain pending.

## Firewall attachments

Each firewall uses the pinned CHR image and an ordinary two-member LACP bond. Match `mlag-id` on the two local cores for the firewall attachment. The core-side port numbers are pending.

| Firewall | CHR `ether2` to | CHR `ether3` to | VLAN 390 address | VRRP priority |
| --- | --- | --- | --- | --- |
| `dc1-firewall1` | `dc1-core-mlag1` | `dc1-core-mlag2` | `198.18.40.2/24` | 150 |
| `dc2-firewall1` | `dc2-core-mlag1` | `dc2-core-mlag2` | `198.18.40.3/24` | 100 |

In the planned Containerlab topology, use `kind: mikrotik_chr` and [large-firewall.rsc](large-firewall.rsc) as the `startup-config` for both firewalls. It selects the settings by CHR identity and enables VRRPv3 with VRID 39, VIP `198.18.40.1`, one-second advertisements and preemption. Leave CHR `ether1` for management. CHR `ether2` and `ether3` correspond to Containerlab data interfaces `eth1` and `eth2`. Carry VLAN 390 tagged on both firewall bonds, the DCI and the peer ports and core-to-distribution trunks that carry the test path. Keep this VLAN isolated to the test lab. [Pinned image](../campaign-image.txt) · [Firewall VRRP test plan](../../docs/plans/two-site-design.md#target--local-distribution-and-firewall-vrrp)

Each local service host keeps its own two-member LACP bond to distribution, with one cable to each peer. Match its switch-side `mlag-id` within that pair and use a distinct ID from the client bond.

[Editable draw.io · Large lab](../../docs/diagrams/mlag-scenarios.drawio) · [Drawing](../../docs/diagrams/large-lab.png) · [Wiring and test stages](../../docs/plans/two-site-design.md) · [Test plan](../../docs/validation-plan.md#large-lab-bridge-mode-comparison)

## Files

| File | Job |
| --- | --- |
| [large-firewall.rsc](large-firewall.rsc) | Planned RouterOS config for the VRRP CHR firewalls |

The topology is not written yet. [Design](../../docs/plans/two-site-design.md) · [Test plan](../../docs/validation-plan.md#large-lab-bridge-mode-comparison)
