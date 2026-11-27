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
[Topology](lab/topology.clab.yml) · [RouterOS startup config](lab/routeros.rsc) · [Host setup](lab/host-setup.sh) · [Two-site design](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/plans/two-site-design.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/large NAME=large-mlag CONFIG=tests/large/lab/devices.yml
```

The lab runs ten CHRs. On the lab VM each used about 360 MiB of memory, so plan for 4 GiB free. Start takes about a minute.

## Streams

Every stream sends one ping every 100 ms.

| Stream | Path |
| --- | --- |
| `dc1-traffic-to-dc1-service`, `dc2-traffic-to-dc2-service` | Site VLAN through the local distribution pair |
| `dc1-to-dc2-over-dci`, `dc2-to-dc1-over-dci` | VLAN 390 through both distribution pairs, both core pairs and the DCI |

Before every test, the [lab file](lab/lab.yaml) checks MLAG and the role on all eight switches, spanning tree off, both members of the DCI, of each distribution-to-core trunk and of each firewall bond, the VRRP owner at dc1 and both cables of every host.
A reboot or power return is healthy only when all these checks pass again.

## Tests and live verdicts

The old suite ran no Large case: the `large-*` cases were only planned, so there are no old Large results to match.
Where a test repeats a fault kind measured on Small or Medium, its row names the old measured range from [results/README.md](../../results/README.md#faults-across-runs) or [results/index/streams.tsv](../../results/index/streams.tsv) at commit `3af4cd8`.

Each verdict is the first line of the generated `report.md` of one live run, `20261127T065530Z` on 27 November 2026, with Networka 0.5.1 at commit `f7916dd`, RouterOS 7.26beta7 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`). Every replay matched the saved `result.json`. The run's verdict files are in [runs/20261127T065530Z](runs/20261127T065530Z/); the captures and the full switch log `switches.log` stay under `test-results/large.20261127T065530Z/`, outside git. Lost pings count at one ping every 100 ms, and an outage is the lower to upper bound the report gives.

| Test | Live verdict and measured outages | Old result of the same fault kind |
| --- | --- | --- |
| [Baseline](cases/baseline.yaml) | [PASS — baseline](runs/20261127T065530Z/baseline/report.md). No ping lost. | None: the Large baseline was only planned. |
| [DCI member loss](cases/dci-member-loss.yaml) | [PASS — dci-member-loss](runs/20261127T065530Z/dci-member-loss/report.md). Member down: dc1 to dc2 over the DCI lost 2 pings, an outage of 0.11 to 0.31 s, and dc2 to dc1 lost 2, 0.11 to 0.31 s, against 1 s. Member back: dc1 to dc2 lost 4, 0.21 to 0.41 s, and dc2 to dc1 lost 5, 0.21 to 0.42 s, against 4 s. The site streams lost nothing. | Two-pair inter-pair member flap with spanning tree off, `streams.tsv` row `debian-two-pair-stp-off-suite 02-two-pair-stp-off-interpair-member-flap Inter-pair member down`, stream 101: 0.316 to 0.527 s. Same order. |
| [Core reboot](cases/core-reboot.yaml) | [FAIL — core-reboot](runs/20261127T065530Z/core-reboot/report.md). Both DCI directions stopped from the reboot of the MLAG primary until its peer logged `peer disconnected`, 16.0 s later at dc1 and 16.2 s later at dc2. Reboot dc1-core1: dc2 to dc1 lost 142 pings, an outage of 14.47 to 16.76 s against 5 s. Reboot dc2-core1: dc2 to dc1 lost 154, 15.77 to 15.97 s. In both steps dc1 to dc2 is unverified because the sender did not keep its 100 ms cadence; the report records 74 and 79 pings lost as diagnostic only. The site streams lost nothing. | Faults across runs, Medium lab: "Loss over the limit, Pair A primary down, STP off, Pair A primary reboot, 3 of 3, 19.67–23.34 s" and "Pair B primary down, 2 of 2, 20.66–22.18 s". Large shows the same fault: two MLAG pairs joined by one inter-pair bond keep sending into the rebooting MLAG primary. |
| [Distribution reboot](cases/distribution-reboot.yaml) | [FAIL — distribution-reboot](runs/20261127T065530Z/distribution-reboot/report.md). Reboot dc1-dist1 in its MLAG primary role: both DCI directions lost 162 pings, outages of 16.80 to 17.00 s from dc1 to dc2 and 16.78 to 16.98 s from dc2 to dc1, against 5 s, until dc1-dist2 logged `peer disconnected` 16.2 s after the reboot; the dc1 site stream lost nothing. Reboot dc1-dist2 in its secondary role: the dc1 site stream lost 29, 2.92 to 3.13 s, within 5 s; the DCI lost nothing. | The DCI loss is the same two-pair fault as the core reboot. For the site stream, which crosses only one pair, Medium spanning-tree-off rows `ext-medium-stp-off 01-medium-stp-off-reboot-primary Primary down`, stream 101: 2.188 to 2.393 s, and `01-medium-stp-off-reboot-secondary Secondary down`, stream 101: 2.914 to 3.121 s. Same order. |
| [Firewall loss](cases/firewall-loss.yaml) | [PASS — firewall-loss](runs/20261127T065530Z/firewall-loss/report.md). No ping lost. The collector logged `vrrp390 now MASTER` on dc2-firewall 2.8 s after power loss, then `now MASTER` on dc1-firewall and `now BACKUP, got higher priority 150` on dc2-firewall 31.9 s after power returned. The result is intermittent: earlier runs passed in `run.rWOjK3`, `run.Kw5bjL` and `run.znXUHD` but failed in `run.FoEYqc`, with late replies on streams that cross no firewall; the cause is not traced. | None: VRRP was never tested before. |

## Limits

The planned Large cases set no limit, so each limit comes from a Small lab test of the same fault kind.
A stream whose path does not cross the fault has limit 0.

| Test | Limit on an affected stream | Source |
| --- | --- | --- |
| Core reboot, distribution reboot | 5 s | [Small with a mobile host, primary reboot](../small-mobile/cases/primary-reboot.yaml) and [secondary reboot](../small-mobile/cases/secondary-reboot.yaml) |
| DCI member loss | 1 s down, 4 s back | [Small cable test](../small/cases/bond-member-loss.yaml) |
| Firewall loss | No stream crosses a firewall. 20 s off and a 180 s recovery deadline. | [Small with a mobile host, primary power loss](../small-mobile/cases/primary-power-loss.yaml) |

## Not covered

- Site power loss has no test. Networka 0.5.1 powers off one CHR at a time and refuses a second `power_off` before the first `power_on`, and it cannot power off a Linux host.
- No stream measures delivery to the VRRP address. A stream needs a Linux destination interface, and the address lives on a CHR firewall. The VRRP checks read the master and backup flags only.
