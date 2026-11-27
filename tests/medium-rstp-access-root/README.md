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

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/medium-rstp-access-root/`.

- [FAIL — baseline](runs/live-20261127-glossary/baseline/report.md)
- [FAIL — primary-power-loss](runs/live-20261127-glossary/primary-power-loss/report.md)
- [FAIL — primary-reboot](runs/live-20261127-glossary/primary-reboot/report.md)
- [FAIL — secondary-power-loss](runs/live-20261127-glossary/secondary-power-loss/report.md)
- [FAIL — secondary-reboot](runs/live-20261127-glossary/secondary-reboot/report.md)

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
Whether RouterOS or the lab causes it is not proven yet.
