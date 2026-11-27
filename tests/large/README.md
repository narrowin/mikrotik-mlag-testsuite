# Large MLAG lab

The lab spans two sites, `dc1` and `dc2`, and runs with spanning tree off on every bridge.
Each site has a core MLAG pair (`core1`, `core2`), a distribution MLAG pair (`dist1`, `dist2`), a CHR firewall and two Linux hosts, `traffic` and `service`.
Peer 1 of each pair is configured as MLAG primary.
A collector node, `syslog`, receives the log of all ten CHRs.

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/large/`.

- [PASS — baseline](runs/live-20261127-glossary/baseline/report.md)
- [FAIL — core-reboot](runs/live-20261127-glossary/core-reboot/report.md)
- [PASS — dci-member-loss](runs/live-20261127-glossary/dci-member-loss/report.md)
- [FAIL — distribution-reboot](runs/live-20261127-glossary/distribution-reboot/report.md)
- [PASS — firewall-loss](runs/live-20261127-glossary/firewall-loss/report.md)
- [PASS — site-power-loss](runs/live-20261127-glossary/site-power-loss/report.md)

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

The Linux hosts keep permanent neighbour entries for the measured destinations, so an unanswered ARP request cannot prevent a ping from being transmitted during an outage. Host destinations use their fixed bond MAC addresses. The VRRP address uses `00:00:5e:00:01:27`, the shared virtual MAC for VRID 39 in [routeros.rsc](lab/routeros.rsc), as specified by [RFC 5798 section 7.3](https://www.rfc-editor.org/rfc/rfc5798.html#section-7.3). That MAC follows whichever firewall owns the address.

Before every test, the [lab file](lab/lab.yaml) checks MLAG and the role on all eight switches, spanning tree off, both members of the DCI, of each distribution-to-core trunk and of each firewall bond, the VRRP owner at dc1 and both cables of every host.
A reboot or power return is healthy only when all these checks pass again.

## Tests and live verdicts

The old suite ran no Large case: the `large-*` cases were only planned, so there are no old Large results to match.
Where a test repeats a fault kind measured on Small or Medium, its row names the old measured range from [results/README.md](../../results/README.md#faults-across-runs) or [results/index/streams.tsv](../../results/index/streams.tsv) at commit `3af4cd8`.

Each verdict is the first line of the generated `report.md` of one live run in [runs/live-20261127-glossary](runs/live-20261127-glossary/) on 27 November 2026, with RouterOS 7.26beta7 and Networka 0.5.2. Every replay matched the saved `result.json` and `report.md`. The captures and the full switch log stay under `test-results/live-20261127-glossary/large/`, outside git. Lost pings count at one ping every 100 ms, and an outage is the lower to upper bound the report gives.

| Test | Live verdict and measured outages | Old result of the same fault kind |
| --- | --- | --- |
| [Baseline](tests/baseline.yaml) | [PASS — baseline](runs/live-20261127-glossary/baseline/report.md). No ping lost. | None: the Large baseline was only planned. |
| [DCI member loss](tests/dci-member-loss.yaml) | [PASS — dci-member-loss](runs/live-20261127-glossary/dci-member-loss/report.md). Member down: each DCI direction lost 1 ping, an outage of 0 to 0.21 s, against 1 s. Member back: each lost 4, 0.20 to 0.42 s, against 4 s. | Two-pair inter-pair member flap with spanning tree off, `streams.tsv` row `debian-two-pair-stp-off-suite 02-two-pair-stp-off-interpair-member-flap Inter-pair member down`, stream 101: 0.316 to 0.527 s. Same order. |
| [Core reboot](tests/core-reboot.yaml) | [FAIL — core-reboot](runs/live-20261127-glossary/core-reboot/report.md). Reboot dc1-core1: dc2 to dc1 lost 211 pings, an outage of 21.77 to 21.98 s, against 5 s; dc1 to dc2 is ERROR, 166 lost at 17.13 to 22.43 s; each VRRP stream lost 10, 0.94 to 1.15 s, within 5 s. Reboot dc2-core1: dc1 to dc2 lost 167, 17.10 to 17.31 s, and dc2 to dc1 lost 169, 17.09 to 17.29 s; dc2 to the VRRP address lost 3, 0.21 to 0.41 s. | Faults across runs, Medium lab: "Loss over the limit, Pair A primary down, STP off, Pair A primary reboot, 3 of 3, 19.67–23.34 s" and "Pair B primary down, 2 of 2, 20.66–22.18 s". Large shows the same fault: two MLAG pairs joined by one inter-pair bond keep sending into the rebooting MLAG primary. |
| [Distribution reboot](tests/distribution-reboot.yaml) | [FAIL — distribution-reboot](runs/live-20261127-glossary/distribution-reboot/report.md). Reboot dc1-dist1 in its MLAG primary role: each DCI direction lost 181 pings, 18.58 to 18.79 s, against 5 s; the dc1 site stream lost 5, 0.41 to 0.61 s, and dc1 to the VRRP address lost 3, 0.20 to 0.41 s. Reboot dc1-dist2 in its secondary role: the dc1 site stream lost 23, 2.29 to 2.50 s, within 5 s; dc1 to the VRRP address is ERROR, 89 lost at 9.17 to 19.82 s; the DCI lost nothing. | The DCI loss is the same two-pair fault as the core reboot. For the site stream, which crosses only one pair, Medium spanning-tree-off rows `ext-medium-stp-off 01-medium-stp-off-reboot-primary Primary down`, stream 101: 2.188 to 2.393 s, and `01-medium-stp-off-reboot-secondary Secondary down`, stream 101: 2.914 to 3.121 s. Same order. |
| [Firewall loss](tests/firewall-loss.yaml) | [PASS — firewall-loss](runs/live-20261127-glossary/firewall-loss/report.md). The streams between hosts lost nothing. Power lost: each VRRP stream lost 34 pings, 3.44 to 3.66 s, against 4 s. Power back: no ping lost. | None: VRRP was never tested before. |
| [Site power loss](tests/site-power-loss.yaml) | [PASS — site-power-loss](runs/live-20261127-glossary/site-power-loss/report.md). Local dc2 traffic lost no pings, against 0 s. dc2 to the VRRP address lost 30 pings, 3.03 to 3.23 s, against 4 s. Separately, dc1's restart and rejoin completed with all lab state checks passing 50.623 s after power-on dispatch, against the 180 s recovery deadline. dc1 host interruptions retain their 216 s combined allowance. | None: no lab lost a whole site before. |

## Sender cadence correction, 27 November 2026

The earlier runs above used dynamic neighbour entries on the Linux hosts. During an outage, unanswered ARP requests could make an entry fail and queue pings inside Linux instead of transmitting them. The sender log then reported local `Destination Host Unreachable` and `sendmsg: No route to host` errors. Networka correctly gave the affected stream ERROR because its captured sending pace could not measure the outage.

The investigation reproduced this in a fresh Large lab using pinned Networka `03f61c33145a51cd714774e5d92bd4735d6196f0`. In the [before-correction distribution-reboot report](runs/sender-cadence-before-20261127/distribution-reboot/report.md), the dc1 DCI stream during the MLAG primary reboot and the dc1 VRRP stream during the MLAG secondary reboot are ERRORs shown only as diagnostics. A live neighbour-state log recorded those destinations becoming FAILED, while other streams from the same host kept sending normally.

[host-setup.sh](lab/host-setup.sh) now installs permanent neighbours for the measured host addresses and the shared VRRP virtual MAC. This follows the existing two-pair lab's approach and makes ping transmission independent of ARP recovery. RouterOS forwarding interruptions still lose pings and are judged against the original limits.

After a fresh deployment, every measured destination on every Linux host had the expected permanent MAC entry. The unchanged [baseline](runs/sender-cadence-fixed-20261127/baseline/report.md) passed, and the corrected [distribution-reboot report](runs/sender-cadence-fixed-20261127/distribution-reboot/report.md) has valid sender cadence and no stream measurement ERRORs. Its overall verdict remains FAIL because forwarding interruptions exceed their limits.

| Existing test after the correction | Generated report | Sender cadence and measurement validity |
| --- | --- | --- |
| Baseline | [PASS](runs/sender-cadence-fixed-20261127/baseline/report.md) | Pass on every stream |
| Distribution reboot | [FAIL](runs/sender-cadence-fixed-20261127/distribution-reboot/report.md) | Pass on every stream; forwarding outages exceed their limits |
| Core reboot | [FAIL](runs/sender-cadence-fixed-20261127/core-reboot/report.md) | Pass on every stream; forwarding outages exceed their limits |
| Firewall power loss and VRRP return | [PASS](runs/sender-cadence-fixed-20261127/firewall-loss/report.md) | Pass on every stream; the shared MAC works when the VRRP address moves to dc2 and back |

All before- and after-correction results and reports replayed byte for byte with the pinned Networka commit, checked with SHA-256 before and after replay. The unchanged DCI member loss and site power loss tests were not repeated in this investigation.

Full captures, sender logs, neighbour-state logs and copies of the startup config stay in `test-results/large-cadence-20261127/`, outside git. The checked-in reports are generated by Networka and are not edited by hand. Only the investigation's own Large lab was deployed and removed; other deployed labs were left untouched.

## Limits

The planned Large cases set no limit, so each limit comes from a Small lab test of the same fault kind, from a protocol timer where no lab measured the fault kind, or from the test's own holds.
A stream whose path does not cross the fault has limit 0.

| Test | Limit on an affected stream | Source |
| --- | --- | --- |
| Core reboot, distribution reboot | 5 s | [Small with a MAC-move host, primary reboot](../small-mac-move/tests/primary-reboot.yaml) and [secondary reboot](../small-mac-move/tests/secondary-reboot.yaml) |
| DCI member loss | 1 s down, 4 s back | [Small cable test](../small/tests/bond-member-loss.yaml) |
| Firewall loss | No stream between hosts crosses a firewall. 20 s off and a 180 s recovery deadline. | [Small with a MAC-move host, primary power loss](../small-mac-move/tests/primary-power-loss.yaml) |
| Firewall loss and site power loss, VRRP streams | 4 s while the address moves to dc2 and back | [RFC 9568, section 6.1](https://www.rfc-editor.org/rfc/rfc9568.html#section-6.1): the dc2 firewall's down interval is 3 × 1 s advertisements + (256 − 100) / 256 s = 3.609375 s, rounded up with a local margin. The retained 4 s return limit is a separate acceptance criterion; the failover calculation does not establish an outage bound for preemption. |
| Site power loss, streams with a dc1 host | 216 s combined interruption allowance: the 20 s off hold, the 180 s power return deadline and the 16 s hold after it | The test's own holds and the deadline from [Small with a MAC-move host, primary power loss](../small-mac-move/tests/primary-power-loss.yaml). This allowance includes intentional downtime, rather than specifying failover performance. |
| Site power loss, dc2 site stream | 0 s | Its path stays on the dc2 distribution pair, which keeps power. |
| Other tests, VRRP streams | The limit of the test's DCI or reboot streams when the path crosses the fault, otherwise 0 s | The same sources as the rows above. |

The 5 s reboot limits are local availability requirements copied from the Small lab, not documented IEEE or RouterOS maxima. Three fast LACP intervals plus two seconds for forwarding was their original rationale; it does not account for every MLAG detection and rejoin mechanism. See [the corrected limit rationale](../../docs/adr/0003-a-test-is-a-yaml-file-and-every-limit-carries-its-reason-next-to-it.md).

The site-power report opens with dc2's forwarding and the measured interruption reaching the VRRP address while dc1 is down. dc1's restart and rejoin appear in a separate section, with the time from power-on dispatch until all lab state checks pass against the existing 180 s recovery deadline. Intentional interruptions at dc1 hosts retain their 216 s combined allowance in the detailed table. The later recovery step still requires 0 s on every stream. The dc2 site stream's 0 s and surviving VRRP stream's 4 s limits remain ordinary availability checks. Missing pings at a sender with its data cables down cannot establish service continuity, and the report does not subtract 20 s from an outage bound to claim a recovery time.

The linked site-power report has been regenerated from the unchanged saved `result.json` with the reporting change now included in pinned Networka `30e706a`. No new live run or verdict is implied. The results summary excludes intentional host interruptions within their combined limits from its worst-outage comparison; confirmed breaches remain eligible.

## Not covered

- ARP resolution and recovery on the Linux hosts: the measured destinations have permanent neighbour entries so the streams keep sending throughout an outage.
- A powered-off Linux host keeps running with all its cables down, so its bond and neighbour entries survive the site power loss; a real host would boot with them empty.
- The VRRP streams cannot tell a lost request from a lost reply, because the firewall has no capture point.
- Site power loss at dc2, and a complete DCI cut with one VRRP master at each site, have no test.
