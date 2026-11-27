# Medium MLAG lab with RSTP

This is the [Medium lab](../medium/README.md) with RSTP on every bridge and the MLAG pair as root bridge. [Medium RSTP with the access switch as root](../medium-rstp-access-root/README.md) is the same lab with a switch outside the pair as root. Switch1 and switch2 have priority `0x1000` and the access switch `0x8000`; host ports are edge ports, and the peer link and the uplinks are not.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `medium-mlag-rstp`, and management subnet, `172.30.113.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on all three bridges, both peers as root bridge with root ID `0x1000.02:00:00:21:01:01` (switch1), the access switch on the same root through `uplink`, and every bridge port forwarding with the host ports as edge ports.
Each test in `tests/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/medium/lab](../medium/lab).

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/medium-rstp/`.

- [PASS — baseline](runs/live-20261127-glossary/baseline/report.md)
- [FAIL — primary-power-loss](runs/live-20261127-glossary/primary-power-loss/report.md)
- [FAIL — primary-reboot](runs/live-20261127-glossary/primary-reboot/report.md)
- [PASS — secondary-power-loss](runs/live-20261127-glossary/secondary-power-loss/report.md)
- [FAIL — secondary-reboot](runs/live-20261127-glossary/secondary-reboot/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium-rstp NAME=medium-mlag-rstp CONFIG=tests/medium/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the Medium README](../medium/README.md).
