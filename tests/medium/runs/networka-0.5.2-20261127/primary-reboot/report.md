# PASS — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 31 at one ping every 100 ms | 2.50066 to 2.70577 s | pass |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 32 at one ping every 100 ms | 2.60144 to 2.80872 s | pass |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 54 s. The switch reported 17 s at +23.815 s.
- Full lab state was pass at +24.5043 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.923 | test | primary-reboot started in lab medium-mlag |
| -1.612 | access-switch log | script,info networka primary-reboot start |
| -1.311 | switch1 log | script,info networka primary-reboot start |
| -1.007 | switch2 log | script,info networka primary-reboot start |
| -1.003 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.116 | state | All three switches run with spanning tree off. pass |
| -0.116 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.116 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.003 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.760 | quiet window | clean |
| 3.760 | step | Baseline |
| 7.763 | step | Reboot switch1 |
| 7.811 | reboot | dispatching the reboot to switch1 |
| 7.878 | reboot | switch1 command returned: accepted |
| 8.225 | host2-to-host1 | 26 pings lost at one ping every 100 ms, traffic stopped for 2.601 to 2.809 s, request absent at destination |
| 8.247 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.501 to 2.706 s, reply absent at source |
| 24.293 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.715 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.720 | switch2 log | bridge,warning "bridge" peer link down |
| 25.014 | host1-to-host2 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.517 to 0.726 s, request absent at destination |
| 25.064 | host2-to-host1 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.518 to 0.722 s, request absent at destination |
| 32.316 | recovery | full lab state after reboot of switch1: pass |
| 48.317 | step | Reboot recovery |
| 51.322 | steps | last step ended |
| 52.564 | state | check after the steps: pass |
| 52.564 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 52.564 | state | All three switches run with spanning tree off. pass |
| 52.564 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 52.564 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 52.565 | streams | measurement ended; captures wait for final replies |
| 53.069 | stopped | captures and streams stopped |
| 53.127 | access-switch log | script,info networka primary-reboot end |
| 53.178 | switch1 log | script,info networka primary-reboot end |
| 53.233 | switch2 log | script,info networka primary-reboot end |
| 53.235 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
