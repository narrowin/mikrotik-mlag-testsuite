# Lab and device names

## Labs

| Name | Containerlab deployment | Scope |
| --- | --- | --- |
| Small lab | `mlag-small` | Two RouterOS MLAG switches plus Linux traffic and logging containers |
| Medium lab | `mlag-medium` | One MLAG pair, one dual-attached access switch and traffic hosts |
| Large lab | `mlag-large`, planned | Two sites with core and access MLAG pairs |

STP mode and root placement are variants within a lab. The OrbStack host VM retains its existing name `mlag-external`.

## Devices

Use **site-role-number**. `dc1` is the first site, Site A in the Large lab. `dc2` is the second site, Site B. Containerlab adds the lab prefix to each container name.

| Device name | Meaning |
| --- | --- |
| `dc1-core-mlag1`, `dc1-core-mlag2` | Core MLAG switches at site 1 |
| `dc1-access-switch1` | Medium lab’s ordinary access switch |
| `dc1-access-mlag1`, `dc1-access-mlag2` | Large lab’s access MLAG pair |
| `dc1-traffic-host1`, `dc1-traffic-host2` | Linux traffic endpoints |
| `dc1-mac-move-host` | Linux endpoint for MAC-move tests |
| `dc1-firewall1` | Large lab’s CHR firewall and VRRP peer at Site A |
| `dc1-service-host1` | Large lab’s local service endpoint |
| `dc1-syslog-collector` | Management log receiver |

The second site uses the same roles with `dc2-`. Example container name, `clab-mlag-medium-dc1-core-mlag1`.

[Small inventory](../labs/small/README.md) · [Medium inventory](../labs/medium/README.md) · [Large inventory](../labs/large/README.md) · [Drawings](diagrams/mlag-scenarios.drawio)

## Cases and evidence

Case IDs use the lab size and sequence, such as `SMALL-03` or `MEDIUM-04`. Record **lab, case ID, STP mode, root placement, repeat** for each attempt. [Ordered cases](cases/README.md)

Archived captures retain their recorded node IDs, deployment names and CLI selectors. Inventories and the case index map these to current names. The earlier three-CHR pair-root control is a Medium lab topology variant.
