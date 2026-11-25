# Labs

Each folder holds one lab: its Containerlab topology, the RouterOS startup config each CHR imports, and an inventory. Containerlab resolves every path relative to the topology file, so a lab folder is self-contained apart from `shared/`. Deploy instance 0 by hand from the repository root; `campaign.sh` deploys every instance from its own copy.

| Lab | Question it answers | Topology | Deployment | Management subnet |
| --- | --- | --- | --- | --- |
| [Small](small/README.md) | Does one MLAG pair keep directly bonded hosts forwarding through link, LACP, MAC and reboot faults? | `small/small.clab.yml` | `mlag-small` | `172.30.215.0/27` |
| [Medium](medium/README.md) | Does a downstream access switch change the outcome with STP off or RSTP on? | `medium/medium.clab.yml` | `mlag-medium` | `172.30.218.0/27` |
| [Medium, pair-root variant](medium/README.md#pair-root-variant) | What happens when the MLAG pair itself is the RSTP root? | `medium/medium-pair-root.clab.yml` | `mlag-medium-pair-root` | `172.30.216.0/27` |
| [Medium, two-pair variant](medium/README.md#two-pair-variant) | Does STP root stay on the core pair when a second MLAG pair replaces the access switch? | `medium/medium-two-pair.clab.yml` | `mlag-medium-two-pair` | `172.30.219.0/27` |
| [Large](large/README.md) | Do two sites with core and access pairs and a VRRP firewall recover from site faults? Not yet deployed; the runner has no Large cases yet. | `large/large.clab.yml` | `mlag-large` | `172.30.220.0/27` |

Each topology has its own deployment name and subnet, so different labs can run side by side. Local campaign runs use the `mlag-external` OrbStack VM. For a browser-based first run, see the [quickstart](../README.md#quick-start).

## Deploy and remove a lab

Build the traffic-host image once, then deploy with the pinned CHR image:

```sh
sudo docker build -f labs/shared/client.Dockerfile -t mlag-lab-endpoint:local labs/shared
sudo env MLAG_CHR_IMAGE="$(cat labs/campaign-image.txt)" containerlab deploy -t labs/small/small.clab.yml
sudo containerlab destroy -t labs/small/small.clab.yml --cleanup
```

Each lab README lists the extra steps for that lab. Containerlab writes its lab directory (`clab-<name>/`) next to the topology, and the syslog collector writes `routeros.jsonl` to the lab's `logs/` folder. Git ignores both.

## Lab instances

`MLAG_INSTANCE` (0 to 3, default 0) runs up to three more copies of a lab in the same VM. Instance 0 is the lab in the table above. Instance N is named `<deployment>-i<N>` and adds 10·N to the third octet of the management subnet: Small instance 2 is `mlag-small-i2` on `172.30.235.0/27`. The topology files read `MLAG_LAB_NAME` and `MLAG_MGMT_NET` and default to instance 0; the runner reads `MLAG_INSTANCE` and records it in each `attempt.json`.

[campaign.sh](campaign.sh) derives the variables from `MLAG_INSTANCE` and deploys instance N from its own copy, `<MLAG_LABS_COPY>-i<N>`, by default `/var/tmp/mlag-labs-i<N>`. In that copy the startup configs send syslog to that instance's collector. The copy is synced from the checkout only while no lab is deployed from it. Different labs at the same instance share the copy and deploy one after the other. `campaign.sh` takes `small`, `medium`, `medium-pair-root` and `medium-two-pair`; the Large lab has no instances yet. [parallel.sh](parallel.sh) starts several campaigns at once inside the VM, one per lab instance, and prints one PASS or FAIL line per campaign:

```sh
labs/parallel.sh --destroy \
  1 small /var/tmp/c-small-1 "baseline:--bridge-mode none --case baseline" -- \
  2 small /var/tmp/c-small-2 "baseline:--bridge-mode none --case baseline"
```

Each campaign writes its console output to `<campaign dir>/console.log` and each suite to `<campaign dir>/<sub-folder>/`. `parallel.sh` exits 0 when every campaign passed, 1 when any failed and 2 on a usage error. `--destroy` removes only the labs that the campaigns deployed. [Run suites in parallel](../docs/operator-guide.md#run-suites-in-parallel)

Deploy instances through `campaign.sh` or `parallel.sh`. A deploy of instance N straight from this folder keeps the instance 0 syslog target in the startup configs, so its RouterOS logs reach the wrong collector.

Remove an instance with the same variables it was deployed with, never with `containerlab destroy --name`:

```sh
sudo env MLAG_LAB_NAME=mlag-small-i2 MLAG_MGMT_NET=235 containerlab destroy -t /var/tmp/mlag-labs-i2/small/small.clab.yml --cleanup
```

## Shared files

| File | Used by | Job |
| --- | --- | --- |
| [campaign-image.txt](campaign-image.txt) | Every CHR, the runner | The RouterOS CHR image pinned by digest for the whole campaign |
| [shared/client.Dockerfile](shared/client.Dockerfile) | Traffic hosts | Alpine image with iproute2 and iputils, tagged `mlag-lab-endpoint:local` |
| [shared/client-network.sh](shared/client-network.sh) | Traffic hosts | Builds the LACP or active-backup bond, VLAN 110 address and bypass link |
| [shared/root-client.sh](shared/root-client.sh) | Medium traffic hosts | Host 1 gets a single VLAN 110 port behind the access switch; Host 2 uses `client-network.sh`. Both pin the other host's MAC. |
| [shared/forward-control.sh](shared/forward-control.sh) | Every CHR | Makes each veth-to-TAP bridge pass STP, LACP and LLDP; `--wire` also turns off MAC learning so it acts as a plain cable |
| [shared/qemu-data-link.sh](shared/qemu-data-link.sh) | Every CHR | QEMU wrapper that advertises 10G full duplex on the data NICs |
| [shared/rsyslog.conf](shared/rsyslog.conf) | Syslog collector | Writes RouterOS syslog from each lab and instance subnet to `logs/routeros.jsonl` |
| [networka/](networka/) | Operator | Networka checkpoint profiles for each lab and the read-only RouterOS sequences |

The runner copies these files into each run's `inputs/` folder and records their SHA-256. [Syslog notes](../docs/syslog/README.md) · [Networka checkpoints](../docs/operator-guide.md#collect-a-networka-checkpoint)
