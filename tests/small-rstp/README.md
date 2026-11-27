# Small MLAG lab with RSTP

This is the [Small lab](../small/README.md) with RSTP on every bridge and the MLAG pair as root bridge. Switch1 and switch2 have priority `0x1000`, and the host bond ports are edge ports.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `small-mlag-rstp`, and management subnet, `172.30.102.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on both bridges, both peers as root bridge, and every bridge port forwarding with the host ports as edge ports.
Each test in `tests/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/small/lab](../small/lab).

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/small-rstp/`.

- [FAIL — bond-member-loss](runs/live-20261127-glossary/bond-member-loss/report.md)
- [PASS — cable-delay](runs/live-20261127-glossary/cable-delay/report.md)
- [ERROR — cable-packet-loss](runs/live-20261127-glossary/cable-packet-loss/report.md)
- [PASS — switch-reboot](runs/live-20261127-glossary/switch-reboot/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small-rstp NAME=small-mlag-rstp CONFIG=tests/small/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the Small README](../small/README.md).
