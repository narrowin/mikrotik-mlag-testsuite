# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux hosts, `host1` to `host3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Networka 0.5.2 live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links below open the generated reports; full evidence stays in `test-results/networka-0.5.2-20261127/small/`. Earlier measurements below remain historical.

- [FAIL — bond-member-loss](runs/networka-0.5.2-20261127/bond-member-loss/report.md)
- [FAIL — cable-delay](runs/networka-0.5.2-20261127/cable-delay/report.md)
- [ERROR — cable-packet-loss](runs/networka-0.5.2-20261127/cable-packet-loss/report.md)
- [PASS — switch-reboot](runs/networka-0.5.2-20261127/switch-reboot/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml
```

The cable test is `TEST=bond-member-loss` and the reboot of switch1 in its current MLAG role is `TEST=switch-reboot`. The two test files give the per-stream limits and their reasons. [Cable test](tests/bond-member-loss.yaml), [Reboot test](tests/switch-reboot.yaml)

## Additional Small tests

Cable delay and sustained one-way loss use the same topology. The MAC-move lab adds a MAC-move host on an active-backup bond and runs eleven tests.

[Cable delay](tests/cable-delay.yaml), [Sustained cable loss](tests/cable-packet-loss.yaml), [Small with a MAC-move host](../small-mac-move/README.md)

## Measured cable return

On 26 November 2026, in the first committed native CHR cable run, host1 to host2 lost 24 pings at one ping every 100 ms when the cable to switch2 came back. The measured stop was 2.399 to 2.610 s, within its 4 s limit. [Walkthrough](../../docs/walkthrough-networka-tests.md)
