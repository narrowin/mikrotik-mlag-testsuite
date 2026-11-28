# Medium MLAG lab with RSTP and the access switch as root

This is the [Medium lab](../medium/README.md) with RSTP on every bridge and the access switch, a switch outside the MLAG pair, as root bridge. The access switch has priority `0x1000` and switch1 and switch2 `0x8000`; host ports are edge ports, and the peer link and the uplinks are not.
It is the second root placement of [ADR 0006](../../docs/adr/0006-spanning-tree-off-is-the-reference-and-rstp-is-tested-with-the-root-on-and-outside-the-mlag-pair.md), next to [Medium RSTP](../medium-rstp/README.md), where the MLAG pair is root.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `medium-mlag-rstp-access-root`, and management subnet, `172.30.115.0/24`, so it can run next to the other Medium labs.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml) sets `STP_MODE: rstp`, `STP_ROOT: access-switch` and the collector address for the shared startup config.
[lab.yaml](lab/lab.yaml) checks the following before and after every test:

- RSTP on all three bridges.
- The access switch as root bridge with root ID `0x1000.02:00:00:21:01:03`.
- Both MLAG peers on that root through their MLAG bond `access-switch`.
- Every bridge port forwarding, with the host ports as edge ports.

Each test in `tests/` is a symbolic link to the base test of the same name. Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so the test runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/medium/lab](../medium/lab).

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and [image-proof.json](runs/live-20261128-image-dbd8a548/image-proof.json) records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/medium-rstp-access-root/`.

- [ERROR — baseline](runs/live-20261128-image-dbd8a548/baseline/report.md)
- [ERROR — primary-power-loss](runs/live-20261128-image-dbd8a548/primary-power-loss/report.md)
- [ERROR — primary-reboot](runs/live-20261128-image-dbd8a548/primary-reboot/report.md)
- [ERROR — secondary-power-loss](runs/live-20261128-image-dbd8a548/secondary-power-loss/report.md)
- [ERROR — secondary-reboot](runs/live-20261128-image-dbd8a548/secondary-reboot/report.md)

Every test is ERROR, because the state check before the test failed and its steps did not run. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 every test failed on the same state check.

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium-rstp-access-root NAME=medium-mlag-rstp-access-root CONFIG=tests/medium/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged, as in Medium RSTP: see [the Medium README](../medium/README.md).

## What the runs show

Every test stopped before its first step: the state check before the test failed, so no fault was injected and no outage was measured.
The access switch is root and both MLAG peers reach it through their MLAG bond, but the `uplink` port of the access switch never forwards.
The switch logs show both MLAG peers putting their bond port `access-switch` back into the proposed root role every 2 s, and their peer link `ether2` back into the designated discarding state each time.
The old suite saw VLAN 110 not forward with this root placement on 2026-11-24 ([ADR 0006](../../docs/adr/0006-spanning-tree-off-is-the-reference-and-rstp-is-tested-with-the-root-on-and-outside-the-mlag-pair.md)).
The investigation below attributes the blocker to RouterOS RSTP/MLAG agreement handling on this CHR build; it found no lab correction that preserves the intended non-edge, rapid RSTP behaviour.

## RSTP agreement investigation, 27 November 2026

The investigation used RouterOS 7.26beta7, the pinned CHR image and qualified containerlab build from [Run a lab](../../docs/tests/README.md#run-a-lab), and Networka at `03f61c33145a51cd714774e5d92bd4735d6196f0`.
It started its own lab, left other deployed labs untouched, and used the existing `baseline` test without changing its state checks, streams, flood check or limits.
The generated reports distinguish an ERROR before traffic starts from a measured FAIL.

| Lab settings | Baseline report | What it establishes |
| --- | --- | --- |
| Original startup config, fresh deployment | [ERROR](runs/rstp-agreement-original-20261127/baseline/report.md) | The access switch is root, MLAG is connected and LACP members are distributing, but the access uplink does not forward. |
| Default `edge=auto` on both MLAG peer ports, fresh deployment | [ERROR](runs/rstp-agreement-peer-default-20261127/baseline/report.md) | Restoring the default peer-port setting does not correct startup. |
| Original settings except `point-to-point=no` on the access uplink | [PASS](runs/rstp-agreement-timer-control-20261127/baseline/report.md) | With timer-based forwarding, both streams and the flood check pass. VLAN membership, the cables and the existing state checks can work unchanged. |
| Original rapid RSTP settings restored after the timer control | [ERROR](runs/rstp-agreement-restored-20261127/baseline/report.md) | The passing control did not repair the original RSTP behaviour. |
| Medium RSTP with the MLAG pair as root, fresh deployment | [PASS](../medium-rstp/runs/rstp-agreement-control-20261127/baseline/report.md) | The same shared startup config and baseline work with the other root placement. |

Full evidence, diagnostic bridge and bond state, and BPDU captures stay in `test-results/rstp-access-root-20261127/`, outside git.
The `original`, `clean-original`, `peer-edge-no-restored`, `peer-default-cold`, `timer-control` and `original-final` folders record the controls; `peer-edge-auto` records a passing live change that did not survive a fresh deployment.
The `pair-root-control` folder holds the Medium RSTP control. Replaying the investigation evidence reproduced `result.json` and `report.md` byte for byte, checked with SHA-256 before and after replay.

### What isolated the cause

- Disabling the host-facing bridge ports leaves the access uplink blocked. The symptom does not require ping traffic or Networka's judge.
- A single access-uplink bond member still blocks with MLAG enabled. Temporarily disabling MLAG on both peers lets ordinary RSTP forward on that same single-member path.
- Admitting untagged frames on the peer ports does not clear the blocker.
- The blocked access switch repeatedly sends RSTP proposals. A capture at the CHR tap of the receiving MLAG peer sees those proposals, but no agreement reply during the capture. This places the missing reply inside RouterOS rather than in containerlab's virtual cable.
- Both MLAG peers report the correct access-switch root ID and forwarding root ports while their STP logs repeatedly return those ports to the proposed-root role. The access-switch designated uplink remains non-forwarding.

This configuration follows the [MikroTik MLAG requirements](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/): matching priorities and STP settings on both MLAG peers, matching MLAG bond IDs and VLAN 110 tagged on the peer link.
The [bridge-port reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/port/) distinguishes a non-edge port from default edge discovery and timer-based forwarding.
The evidence isolates a RouterOS RSTP/MLAG agreement problem; it does not identify an internal RouterOS code defect, and it does not establish the behaviour of CRS switch hardware or another RouterOS build.

### Controls that are not a lab fix

Changing peer-port settings on a live lab can clear the blocked state temporarily. Removing the peer-port override from the startup config did not pass after a fresh deployment, so that proposed correction was reverted.
Default discovery on the access uplink makes it report `edge-port: yes` even though it connects to the MLAG pair and receives no agreement. That conceals the missing agreement by treating the uplink as an edge port.
Setting `point-to-point=no` keeps it non-edge and allows timer-based forwarding, but changes the rapid RSTP behaviour this lab is meant to measure.
The startup config and state checks are therefore retained, and this root placement remains blocked pending a RouterOS correction.
