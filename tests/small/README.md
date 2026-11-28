# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux hosts, `host1` to `host3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5, in five fresh-deploy rounds; each round ran all four tests once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and `image-proof.json` in each run folder records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/small/` and in `test-results/live-20261128-image-dbd8a548-r2/small/` to `-r5/small/`. The [results table](../../README.md#results) shows round 1, because a summary cell takes one run per test.

| Test | Round 1 | Round 2 | Round 3 | Round 4 | Round 5 |
| --- | --- | --- | --- | --- | --- |
| bond-member-loss | [PASS](runs/live-20261128-image-dbd8a548/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/bond-member-loss/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/bond-member-loss/report.md) |
| cable-delay | [PASS](runs/live-20261128-image-dbd8a548/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/cable-delay/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/cable-delay/report.md) |
| cable-packet-loss | [ERROR](runs/live-20261128-image-dbd8a548/cable-packet-loss/report.md) | [ERROR](runs/live-20261128-image-dbd8a548-r2/cable-packet-loss/report.md) | [ERROR](runs/live-20261128-image-dbd8a548-r3/cable-packet-loss/report.md) | [ERROR](runs/live-20261128-image-dbd8a548-r4/cable-packet-loss/report.md) | [ERROR](runs/live-20261128-image-dbd8a548-r5/cable-packet-loss/report.md) |
| switch-reboot | [PASS](runs/live-20261128-image-dbd8a548/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r2/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r3/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r4/switch-reboot/report.md) | [PASS](runs/live-20261128-image-dbd8a548-r5/switch-reboot/report.md) |

bond-member-loss passed in all five rounds. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 it failed.
cable-packet-loss is ERROR in all five rounds; each report gives its reasons. [Small strict](../small-strict/README.md) runs the same tests with `lacp-strict=yes min-links=1` on the host bonds and coupled LACP control off on the hosts.

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml
```

The cable test is `TEST=bond-member-loss` and the reboot of switch1 in its current MLAG role is `TEST=switch-reboot`. The two test files give the per-stream limits and their reasons. [Cable test](tests/bond-member-loss.yaml), [Reboot test](tests/switch-reboot.yaml)

## Additional Small tests

Cable delay and sustained one-way loss use the same topology. The MAC-move lab adds a MAC-move host on an active-backup bond and runs eleven tests.

[Cable delay](tests/cable-delay.yaml), [Sustained cable loss](tests/cable-packet-loss.yaml), [Small with a MAC-move host](../small-mac-move/README.md)
