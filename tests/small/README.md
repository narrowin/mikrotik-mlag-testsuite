# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux clients, `client1` to `client3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml
```

The cable test is `CASE=bond-member-loss` and the reboot of switch1 in its current MLAG role is `CASE=switch-reboot`. The two test files give the per-stream limits and their reasons. [Cable test](cases/bond-member-loss.yaml), [Reboot test](cases/switch-reboot.yaml)

## Additional Small cases

Cable delay and sustained one-way loss use the same topology. The mobile setup adds an active-backup host for the eleven historical cases.

[Cable delay](cases/cable-delay.yaml), [Sustained cable loss](cases/cable-packet-loss.yaml), [Mobile Small guide](../small-mobile/README.md)

## Measured cable return

On 26 November 2026, in the first committed native CHR cable run, client1 to client2 lost 24 pings at one ping every 100 ms when the cable to switch2 came back. The measured stop was 2.399 to 2.610 s, within its 4 s limit. [Walkthrough](../../docs/walkthrough-networka-tests.md)
