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

| Test | Live verdict and measured stops | Old result of the same fault kind |
| --- | --- | --- |
| [Baseline](baseline.yaml) | PASS — baseline, in `run.7FWsWH` and `run.u56VIq`. No ping lost. | None: the Large baseline was only planned. |
| [DCI member loss](dci-member-loss.yaml) | PASS — dci-member-loss, `run.B2IMcg`. Member down: each DCI direction lost 1 ping at one ping every 100 ms, a stop of 0 to 0.21 s. Member back: each lost 4, a stop of 0.21 to 0.41 s. | Two-pair inter-pair member flap with spanning tree off, `streams.tsv` row `debian-two-pair-stp-off-suite 02-two-pair-stp-off-interpair-member-flap Inter-pair member down`, stream 101: 0.316 to 0.527 s. Same order. |
| [Core reboot](core-reboot.yaml) | FAIL — core-reboot, in `run.af0N9Q` and `run.04fCIw`. Both DCI directions stopped from the reboot of the MLAG primary until its peer logged `peer disconnected` about 20 s later. In `run.04fCIw` dc1-core1 cost 200 and 198 pings, stops of 20.64 to 20.85 s and 20.42 to 20.63 s; dc2-core1 cost 190 and 191, stops of 19.40 to 19.60 s and 19.38 to 19.60 s, all at one ping every 100 ms against 5 s. The site streams and the bypass lost nothing. | Faults across runs, Medium lab: "Loss over the limit, Pair A primary down, STP off, Pair A primary reboot, 3 of 3, 19.67–23.34 s" and "Pair B primary down, 2 of 2, 20.66–22.18 s". Large shows the same fault: two MLAG pairs joined by one distributed bond keep sending into the rebooting MLAG primary. |
| [Distribution reboot](distribution-reboot.yaml) | FAIL — distribution-reboot, `run.lwZPSU`. dc1-dist1 in its MLAG primary role: dc2 to dc1 over the DCI lost 212 pings at one ping every 100 ms, a stop of 19.88 to 20.09 s against 5 s; the dc1 site stream lost 10, a stop of 0.92 to 1.12 s, within 5 s. dc1-dist2 in its secondary role: the dc1 site stream lost 31, a stop of 2.92 to 3.13 s, within 5 s; the DCI lost nothing. | The DCI loss is the same two-pair fault as the core reboot. For the site stream, which crosses only one pair, Medium spanning-tree-off rows `ext-medium-stp-off 01-medium-stp-off-reboot-primary Primary down`, stream 101: 2.188 to 2.393 s, and `01-medium-stp-off-reboot-secondary Secondary down`, stream 101: 2.914 to 3.121 s. Same order. |
| [Firewall loss](firewall-loss.yaml) | With VRRP logging on the firewalls: FAIL — firewall-loss in `run.FoEYqc`, PASS — firewall-loss in `run.rWOjK3`. In both runs the collector logged `vrrp390 now MASTER` on dc2-firewall about 3 s after power loss, then `now MASTER` on dc1-firewall and `now BACKUP, got higher priority 150` on dc2-firewall after power returned. In `run.FoEYqc`, 12.6 s after power returned and before dc1 took the address back, replies came late on streams that cross no firewall: 5 and 4 pings in the two DCI directions and 2 on the dc2 site stream, at one ping every 100 ms, stops of 0.43 to 0.65 s, 0.31 to 0.52 s and 0.10 to 0.31 s against 0 s. The bypass lost nothing. The cause is not traced. An earlier run without VRRP logging, `run.znXUHD`, passed. | None: VRRP was never tested before. |

The DCI streams of `run.af0N9Q` are partly marked unverified because the Linux sender did not keep its 100 ms cadence while the far host stopped answering. The verdict stands on the streams that kept it.

## Limits

The planned Large cases set no limit, so each limit comes from the Small test of the same fault kind.
A stream whose path does not cross the fault has limit 0.

| Test | Limit on an affected stream | Source |
| --- | --- | --- |
| Core reboot, distribution reboot | 5 s | [Small primary reboot](../small/mobile/primary-reboot.yaml), [Small secondary reboot](../small/mobile/secondary-reboot.yaml) |
| DCI member loss | 1 s down, 4 s back | [Small cable test](../small/bond-member-loss.yaml) |
| Firewall loss | No stream crosses a firewall. 20 s off and a 180 s recovery deadline. | [Small primary power loss](../small/mobile/primary-power-loss.yaml) |

## Not covered

- Site power loss has no test. Networka 0.5.1 powers off one CHR at a time and refuses a second `power_off` before the first `power_on`, and it cannot power off a Linux host.
- No stream measures delivery to the VRRP address. A stream needs a Linux destination interface, and the address lives on a CHR firewall. The VRRP checks read the master and backup flags only.
