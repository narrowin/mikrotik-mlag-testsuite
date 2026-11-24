# Labs

Each folder holds one lab: its Containerlab topology, the RouterOS startup config each CHR imports, and an inventory. Containerlab resolves every path relative to the topology file, so a lab folder is self-contained apart from `shared/`. Deploy from the repository root.

| Lab | Question it answers | Topology | Deployment | Management subnet |
| --- | --- | --- | --- | --- |
| [Small](small/README.md) | Does one MLAG pair keep directly bonded hosts forwarding through link, LACP, MAC and reboot faults? | `small/small.clab.yml` | `mlag-small` | `172.30.215.0/27` |
| [Medium](medium/README.md) | Does a downstream access switch change the outcome with STP off or RSTP on? | `medium/medium.clab.yml` | `mlag-medium` | `172.30.218.0/27` |
| [Medium, pair-root variant](medium/README.md#pair-root-variant) | What happens when the MLAG pair itself is the RSTP root? | `medium/medium-pair-root.clab.yml` | `mlag-medium` | `172.30.216.0/27` |
| [Large](large/README.md) | Do two sites with core and access pairs and a VRRP firewall recover from site faults? Planned. | Pending | `mlag-large` | Pending |

Both Medium topologies use the deployment name `mlag-medium`, so deploy only one at a time. Local campaign runs use the `mlag-external` OrbStack VM. For a browser-based first run, see the [quickstart](../README.md#quick-start).

## Deploy and remove a lab

Build the traffic-host image once, then deploy with the pinned CHR image:

```sh
sudo docker build -f labs/shared/client.Dockerfile -t mlag-lab-endpoint:local labs/shared
sudo env MLAG_CHR_IMAGE="$(cat labs/campaign-image.txt)" containerlab deploy -t labs/small/small.clab.yml
sudo containerlab destroy -t labs/small/small.clab.yml --cleanup
```

Each lab README lists the extra steps for that lab. Containerlab writes its lab directory (`clab-<name>/`) next to the topology, and the syslog collector writes `routeros.jsonl` to the lab's `logs/` folder. Git ignores both.

## Shared files

| File | Used by | Job |
| --- | --- | --- |
| [campaign-image.txt](campaign-image.txt) | Every CHR, the runner | The RouterOS CHR image pinned by digest for the whole campaign |
| [shared/client.Dockerfile](shared/client.Dockerfile) | Traffic hosts | Alpine image with iproute2 and iputils, tagged `mlag-lab-endpoint:local` |
| [shared/client-network.sh](shared/client-network.sh) | Traffic hosts | Builds the LACP or active-backup bond, VLAN 110 address and bypass link |
| [shared/root-client.sh](shared/root-client.sh) | Medium traffic hosts | Host 1 gets a single VLAN 110 port behind the access switch; Host 2 uses `client-network.sh`. Both pin the other host's MAC. |
| [shared/forward-control.sh](shared/forward-control.sh) | Every CHR | Makes each veth-to-TAP bridge pass STP, LACP and LLDP; `--wire` also turns off MAC learning so it acts as a plain cable |
| [shared/qemu-data-link.sh](shared/qemu-data-link.sh) | Every CHR | QEMU wrapper that advertises 10G full duplex on the data NICs |
| [shared/rsyslog.conf](shared/rsyslog.conf) | Syslog collector | Writes RouterOS syslog from each lab subnet to `logs/routeros.jsonl` |
| [networka/](networka/) | Operator | Networka checkpoint profiles: `small.yml`, `medium.yml` and the RouterOS command sequence |

The runner copies these files into each run's `inputs/` folder and records their SHA-256. [Syslog notes](../docs/syslog/README.md) · [Networka checkpoints](../docs/operator-guide.md#collect-a-networka-checkpoint)
