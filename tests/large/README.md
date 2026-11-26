# Large MLAG lab

The lab spans two sites, `dc1` and `dc2`, and runs with spanning tree off on every bridge.
Each site has a core MLAG pair (`core1`, `core2`), a distribution MLAG pair (`dist1`, `dist2`), a CHR firewall and two Linux hosts, `traffic` and `service`.
Peer 1 of each pair is configured as MLAG primary.
A collector node, `syslog`, receives the log of all ten CHRs.

## Wiring

Each pair has a single-member peer link. Every other connection is one LACP bond, and both peers of a pair give their side the same `mlag-id`.

| Bond | Members | `mlag-id` | VLANs |
| --- | --- | --- | --- |
| DCI | `dc1-core1` to `dc2-core1`, `dc1-core2` to `dc2-core2` | 33 at both sites | 390 |
| Distribution to core | `dist1` to `core1`, `dist2` to `core2` | 31 on the cores, 21 on distribution | 390 |
| Firewall | one cable to each local core | 32 on the cores | 390 |
| Traffic host | one cable to each distribution switch | 22 | site VLAN, 390 tagged |
| Service host | one cable to each distribution switch | 23 | site VLAN |

The site VLAN is 110 at `dc1` and 120 at `dc2`. It stays on the distribution pair.
VLAN 390 reaches both firewalls and both traffic hosts across the DCI.
The firewalls share VRRP address 198.18.40.1. The dc1 firewall has priority 150 and owns it; the dc2 firewall has priority 100.
The bypass is a cable between the two traffic hosts that crosses no switch.
[Topology](topology.clab.yml) · [RouterOS startup config](routeros.rsc) · [Host setup](host-setup.sh) · [Two-site design](../../docs/plans/two-site-design.md)

## Commands

Run from the repository root with the host tools, Containerlab build and `lab_nw` function of the [Small lab](../small/README.md#commands).
The lab runs ten CHRs. On the lab VM each used about 360 MiB of memory, so plan for 4 GiB free. Start takes about a minute.

```sh
sudo env "CLAB=$CLAB" tests/large/start.sh
```

Run this block for each attempt.

```sh
CASE=baseline
mkdir -p test-results/large
RUN=$(mktemp -d test-results/large/run.XXXXXX)
lab_nw test run "tests/large/$CASE.yaml" \
  --lab tests/large/clab-large-mlag --config tests/large/devices.yml --save "$RUN"
lab_nw test replay "$RUN/$CASE"
```

Remove the lab when finished.

```sh
sudo "$CLAB" destroy -t tests/large/topology.clab.yml --cleanup
```

## Streams

Every stream sends one ping every 100 ms.

| Stream | Path |
| --- | --- |
| `dc1-traffic-to-dc1-service`, `dc2-traffic-to-dc2-service` | Site VLAN through the local distribution pair |
| `dc1-to-dc2-over-dci`, `dc2-to-dc1-over-dci` | VLAN 390 through both distribution pairs, both core pairs and the DCI |
| `bypass-dc1-to-dc2`, `bypass-dc2-to-dc1` | The bypass cable |

Before every test, the [lab file](lab.yaml) checks MLAG and the role on all eight switches, spanning tree off, both members of the DCI, of each distribution-to-core trunk and of each firewall bond, the VRRP owner at dc1 and both cables of every host.
A reboot or power return is healthy only when all these checks pass again.

## Tests and live verdicts

The old suite ran no Large case: the `large-*` cases were only planned, so there are no old Large results to match.
Where a test repeats a fault kind measured on Small or Medium, its row names the old measured range from [results/README.md](../../results/README.md#faults-across-runs) or [results/index/streams.tsv](../../results/index/streams.tsv) at commit `3af4cd8`.

Each verdict is the first line of the generated `report.md` of a live run on 26 November 2026. Each saved run replayed with identical `result.json` and `report.md`. The evidence stays under `test-results/large/`, outside git.

| Test | Live verdict | Old result of the same fault kind |
| --- | --- | --- |
| [Baseline](baseline.yaml) | PASS — baseline, in two runs | None: the old Large baseline was only planned. |

