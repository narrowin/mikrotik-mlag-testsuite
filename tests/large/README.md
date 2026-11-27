# Large MLAG lab

The lab spans two sites, `dc1` and `dc2`, and runs with spanning tree off on every bridge.
Each site has a core MLAG pair (`core1`, `core2`), a distribution MLAG pair (`dist1`, `dist2`), a CHR firewall and two Linux hosts, `traffic` and `service`.
Peer 1 of each pair is configured as MLAG primary.
A collector node, `syslog`, receives the log of all ten CHRs.

## Networka 0.5.2 live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links below open the generated reports; full evidence stays in `test-results/networka-0.5.2-20261127/large/`. Earlier measurements below remain historical.

- [PASS — baseline](runs/networka-0.5.2-20261127/baseline/report.md)
- [FAIL — core-reboot](runs/networka-0.5.2-20261127/core-reboot/report.md)
- [PASS — dci-member-loss](runs/networka-0.5.2-20261127/dci-member-loss/report.md)
- [FAIL — distribution-reboot](runs/networka-0.5.2-20261127/distribution-reboot/report.md)
- [PASS — firewall-loss](runs/networka-0.5.2-20261127/firewall-loss/report.md)
- [FAIL — site-power-loss](runs/networka-0.5.2-20261127/site-power-loss/report.md)

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
[Topology](lab/topology.clab.yml) · [RouterOS startup config](lab/routeros.rsc) · [Host setup](lab/host-setup.sh) · [Two-site design](../../docs/findings/two-site-design.md)

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
| `dc1-traffic-to-vrrp`, `dc2-traffic-to-vrrp` | VLAN 390 from each traffic host to the VRRP address 198.18.40.1 on whichever firewall is master; from dc2 it crosses the DCI while dc1 owns the address |

The VRRP streams have no capture at the firewall. Networka judges them at the sender: a ping counts when its reply returns within 500 ms.

Before every test, the [lab file](lab/lab.yaml) checks MLAG and the role on all eight switches, spanning tree off, both members of the DCI, of each distribution-to-core trunk and of each firewall bond, the VRRP owner at dc1 and both cables of every host.
A reboot or power return is healthy only when all these checks pass again.

## Tests and live verdicts

The old suite ran no Large case: the `large-*` cases were only planned, so there are no old Large results to match.
Where a test repeats a fault kind measured on Small or Medium, its row names the old measured range from [results/README.md](../../results/README.md#faults-across-runs) or [results/index/streams.tsv](../../results/index/streams.tsv) at commit `3af4cd8`.

Each verdict is the first line of the generated `report.md` of one live run, `20261127T070754Z` on 27 November 2026, with all six tests. Firewall loss and site power loss ran a second time in `20261127T071526Z`. Both runs used Networka from source at commit `a61d3cf`, RouterOS 7.26beta7 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`). Every replay matched the saved `result.json` and `report.md`. The verdict files are in [runs/20261127T070754Z](runs/20261127T070754Z/) and [runs/20261127T071526Z](runs/20261127T071526Z/); the captures and the full switch log `switches.log` stay under `test-results/large.<run>/`, outside git. Lost pings count at one ping every 100 ms, and an outage is the lower to upper bound the report gives.

| Test | Live verdict and measured outages | Old result of the same fault kind |
| --- | --- | --- |
| [Baseline](tests/baseline.yaml) | [PASS — baseline](runs/20261127T070754Z/baseline/report.md). No ping lost. | None: the Large baseline was only planned. |
| [DCI member loss](tests/dci-member-loss.yaml) | [PASS — dci-member-loss](runs/20261127T070754Z/dci-member-loss/report.md). Member down: each DCI direction lost 1 ping, an outage of 0 to 0.21 s, against 1 s. Member back: each lost 2, 0 to 0.21 s, against 4 s. The site streams and both VRRP streams lost nothing. | Two-pair inter-pair member flap with spanning tree off, `streams.tsv` row `debian-two-pair-stp-off-suite 02-two-pair-stp-off-interpair-member-flap Inter-pair member down`, stream 101: 0.316 to 0.527 s. Same order. |
| [Core reboot](tests/core-reboot.yaml) | [FAIL — core-reboot](runs/20261127T070754Z/core-reboot/report.md). Both DCI directions stopped from the reboot of the MLAG primary until its peer logged `peer disconnected`, 16.0 s later at dc1 and 17.9 s later at dc2. Reboot dc1-core1: dc1 to dc2 lost 159 pings, an outage of 16.47 to 16.68 s, and dc2 to dc1 lost 143, 14.81 to 17.05 s, against 5 s; dc1 to the VRRP address lost 6, 0.52 to 0.73 s, within 5 s. Reboot dc2-core1: dc2 to dc1 lost 171, 17.49 to 17.71 s; dc1 to dc2 is unverified because the sender did not keep its 100 ms cadence, and the report records 66 pings lost as diagnostic only. The site streams lost nothing, and dc2 to the VRRP address lost nothing in either reboot. | Faults across runs, Medium lab: "Loss over the limit, Pair A primary down, STP off, Pair A primary reboot, 3 of 3, 19.67–23.34 s" and "Pair B primary down, 2 of 2, 20.66–22.18 s". Large shows the same fault: two MLAG pairs joined by one inter-pair bond keep sending into the rebooting MLAG primary. |
| [Distribution reboot](tests/distribution-reboot.yaml) | [FAIL — distribution-reboot](runs/20261127T070754Z/distribution-reboot/report.md). Reboot dc1-dist1 in its MLAG primary role: dc1 to dc2 lost 174 pings, an outage of 16.37 to 16.58 s, and dc2 to dc1 lost 175, 18.15 to 18.35 s, against 5 s, until dc1-dist2 logged `peer disconnected` 16.3 s after the reboot; the dc1 site stream lost 4, 0.31 to 0.52 s, and dc1 to the VRRP address lost 3, 0.21 to 0.41 s, within 5 s. Reboot dc1-dist2 in its secondary role: the dc1 site stream lost 26, 2.60 to 2.81 s, within 5 s; dc1 to the VRRP address is unverified because the sender did not keep its cadence, and the report records 113 pings lost as diagnostic only; the DCI lost nothing. | The DCI loss is the same two-pair fault as the core reboot. For the site stream, which crosses only one pair, Medium spanning-tree-off rows `ext-medium-stp-off 01-medium-stp-off-reboot-primary Primary down`, stream 101: 2.188 to 2.393 s, and `01-medium-stp-off-reboot-secondary Secondary down`, stream 101: 2.914 to 3.121 s. Same order. |
| [Firewall loss](tests/firewall-loss.yaml) | [PASS — firewall-loss](runs/20261127T070754Z/firewall-loss/report.md) and [PASS — firewall-loss](runs/20261127T071526Z/firewall-loss/report.md). The streams between hosts lost nothing. Power lost: dc1 to the VRRP address lost 26 pings, an outage of 2.61 to 2.82 s in both runs, and dc2 to it lost 26, 2.64 to 2.85 s and 2.64 to 2.84 s, against 4 s, while the collector logged `vrrp390 now MASTER` on dc2-firewall 2.8 s after power loss. Power back: dc1 to the address lost 1, 0 to 0.20 s, in the first run and nothing in the second; dc1-firewall logged `now MASTER` 25.1 s and 31.9 s after power returned. Earlier runs before the VRRP streams passed in `run.rWOjK3`, `run.Kw5bjL` and `run.znXUHD` but failed in `run.FoEYqc`, with late replies on streams that cross no firewall; the cause is not traced. | None: VRRP was never tested before. |
| [Site power loss](tests/site-power-loss.yaml) | [PASS — site-power-loss](runs/20261127T070754Z/site-power-loss/report.md) and [PASS — site-power-loss](runs/20261127T071526Z/site-power-loss/report.md). The dc2 site stream lost nothing. dc2 to the VRRP address lost 31 pings, an outage of 3.12 to 3.33 s, and 28, 2.81 to 3.02 s, against 4 s, while dc2-firewall logged `vrrp390 now MASTER` 3.5 s and 3.2 s after power loss; it lost nothing when dc1 took the address back. The streams with a dc1 end stopped for up to 39.9 s and 47.8 s, within 216 s; their lower bounds are near 0 because the powered-off sender could not send. Every dc1 CHR showed a new boot within 48.5 s of power return, and all lab checks passed 51.1 s and 38.1 s after it. | None: no lab lost a whole site before. |

## Limits

The planned Large cases set no limit, so each limit comes from a Small lab test of the same fault kind, from a protocol timer where no lab measured the fault kind, or from the test's own holds.
A stream whose path does not cross the fault has limit 0.

| Test | Limit on an affected stream | Source |
| --- | --- | --- |
| Core reboot, distribution reboot | 5 s | [Small with a MAC-move host, primary reboot](../small-mac-move/tests/primary-reboot.yaml) and [secondary reboot](../small-mac-move/tests/secondary-reboot.yaml) |
| DCI member loss | 1 s down, 4 s back | [Small cable test](../small/tests/bond-member-loss.yaml) |
| Firewall loss | No stream between hosts crosses a firewall. 20 s off and a 180 s recovery deadline. | [Small with a MAC-move host, primary power loss](../small-mac-move/tests/primary-power-loss.yaml) |
| Firewall loss and site power loss, VRRP streams | 4 s while the address moves to dc2 and back | RFC 5798 Master_Down_Interval of the dc2 firewall: 3 × 1 s advertisements + (256 − 100) / 256 s = 3.61 s, rounded up for one ping interval and the host-table move. No other lab tests VRRP, so no measured limit exists. |
| Site power loss, streams with a dc1 end | 216 s: the 20 s off hold, the 180 s power return deadline and the 16 s hold after it | The test's own holds and the deadline from [Small with a MAC-move host, primary power loss](../small-mac-move/tests/primary-power-loss.yaml). The limit only requires that dc1 traffic returns within the test. |
| Site power loss, dc2 site stream | 0 s | Its path stays on the dc2 distribution pair, which keeps power. |
| Other tests, VRRP streams | The limit of the test's DCI or reboot streams when the path crosses the fault, otherwise 0 s | The same sources as the rows above. |

## Not covered

- A powered-off Linux host keeps running with all its cables down, so its bond and neighbour entries survive the site power loss; a real host would boot with them empty.
- The VRRP streams cannot tell a lost request from a lost reply, because the firewall has no capture point.
- Site power loss at dc2, and a complete DCI cut with one VRRP master at each site, have no test.
