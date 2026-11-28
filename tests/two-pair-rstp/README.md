# Medium lab with two MLAG pairs and RSTP

This is the [two-pair lab](../two-pair/README.md) with RSTP on every bridge and the MLAG pair as root bridge. Pair A has priority `0x2000` and is the root, pair B `0x4000`. The host ports stay edge ports, and the peer links and the inter-pair bond keep `edge=auto`, as in the old field setup.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `two-pair-rstp`, and management subnet, `172.30.114.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on all four bridges, root ID `0x2000.02:00:00:21:00:11` (switch-a1) on all four, pair A as root bridge, pair B reaching it through `inter-pair`, and every bridge port forwarding with the host ports as edge ports.
Each test in `tests/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/two-pair/lab](../two-pair/lab).

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and [image-proof.json](runs/live-20261128-image-dbd8a548/image-proof.json) records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/two-pair-rstp/`.

- [PASS — baseline](runs/live-20261128-image-dbd8a548/baseline/report.md)
- [FAIL — inter-pair-member-flap](runs/live-20261128-image-dbd8a548/inter-pair-member-flap/report.md)
- [FAIL — reboot-a-primary](runs/live-20261128-image-dbd8a548/reboot-a-primary/report.md)
- [PASS — reboot-a-secondary](runs/live-20261128-image-dbd8a548/reboot-a-secondary/report.md)
- [FAIL — reboot-b-primary](runs/live-20261128-image-dbd8a548/reboot-b-primary/report.md)
- [PASS — reboot-b-secondary](runs/live-20261128-image-dbd8a548/reboot-b-secondary/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/two-pair-rstp NAME=two-pair-rstp CONFIG=tests/two-pair/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the two-pair README](../two-pair/README.md).
