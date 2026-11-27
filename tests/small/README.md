# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux hosts, `host1` to `host3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/small/`.

- [FAIL — bond-member-loss](runs/live-20261127-glossary/bond-member-loss/report.md)
- [PASS — cable-delay](runs/live-20261127-glossary/cable-delay/report.md)
- [ERROR — cable-packet-loss](runs/live-20261127-glossary/cable-packet-loss/report.md)
- [PASS — switch-reboot](runs/live-20261127-glossary/switch-reboot/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml
```

The cable test is `TEST=bond-member-loss` and the reboot of switch1 in its current MLAG role is `TEST=switch-reboot`. The two test files give the per-stream limits and their reasons. [Cable test](tests/bond-member-loss.yaml), [Reboot test](tests/switch-reboot.yaml)

## Additional Small tests

Cable delay and sustained one-way loss use the same topology. The MAC-move lab adds a MAC-move host on an active-backup bond and runs eleven tests.

[Cable delay](tests/cable-delay.yaml), [Sustained cable loss](tests/cable-packet-loss.yaml), [Small with a MAC-move host](../small-mac-move/README.md)
