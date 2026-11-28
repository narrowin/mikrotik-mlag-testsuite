# Small MLAG lab with lacp-strict

This is the [Small lab](../small/README.md) with `lacp-strict=yes min-links=1` on the host bonds of both switches and coupled LACP control off (`coupled_control off`) on the Linux host bonds.
With `lacp-strict=yes` and `min-links=1` a switch withdraws a host bond whose bond member has no LACP partner, and MLAG forwards through the peer link. With `coupled_control off` a Linux bond stops sending on a bond member whose partner stops collecting. These settings address failover under sustained one-way packet loss; the tests and their limits are unchanged.
The lab has its own name, `small-strict`, and management subnet, `172.30.103.0/24`, so it can run next to the Small lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `LACP_STRICT: "yes"` for the shared startup config and `COUPLED_CONTROL: "off"` for the shared host setup, and [lab.yaml](lab/lab.yaml), which checks `lacp-strict=yes` and `min-links=1` on every host bond of both switches before and after every test.
No state check reads `coupled_control` on the Linux hosts, because Networka has none for it.
Each test in `tests/` is a symbolic link to the Small test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the Small lab's files in [tests/small/lab](../small/lab).

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5, in five fresh-deploy rounds; each round ran all four tests once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and `image-proof.json` in each run folder records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/small-strict/` and in `test-results/live-20261128-image-dbd8a548-r2/small-strict/` to `-r5/small-strict/`. The [results table](../../README.md#results) shows round 1, because a summary cell takes one run per test.

| Test | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
| --- | --- | --- | --- | --- | --- |
| bond-member-loss | [PASS](runs/live-20261128-image-dbd8a548/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/bond-member-loss/report.md) |
| cable-delay | [PASS](runs/live-20261128-image-dbd8a548/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/cable-delay/report.md) |
| cable-packet-loss | [ERROR](runs/live-20261128-image-dbd8a548/cable-packet-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/cable-packet-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/cable-packet-loss/report.md) | [ERROR](runs/live-20261128-image-dbd8a548-r4/cable-packet-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/cable-packet-loss/report.md) |
| switch-reboot | [PASS](runs/live-20261128-image-dbd8a548/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/switch-reboot/report.md) |

cable-packet-loss missed the 15 s recovery deadline in 2 of 5 rounds, [round 1](runs/live-20261128-image-dbd8a548/cable-packet-loss/report.md) and [round 4](runs/live-20261128-image-dbd8a548-r4/cable-packet-loss/report.md): both reports say the run stopped when fault recovery passed the test's `recovery_deadline_s: 15` with no full recovery state check completed, while the outage of the one-way cable loss step passed its 4 s limit. It passed in rounds 2, 3 and 5.

## Earlier qualification

On 27 November 2026 all four tests passed once each with these settings, which were then part of the Small lab, before Small strict became its own lab. [The qualification](../../notes/final-qualification.md) and [its generated reports](../../notes/qualification/small-arm64/README.md).

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small-strict NAME=small-strict CONFIG=tests/small/lab/devices.yml
```

The tests and their limits are the Small lab's, unchanged: see [the Small README](../small/README.md).
