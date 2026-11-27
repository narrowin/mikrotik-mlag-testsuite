# PASS — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 23 at one ping every 100 ms | 2.2896 to 2.49447 s | pass |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 23 at one ping every 100 ms | 2.34399 to 2.54681 s | pass |
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

- Uptime before dispatch was 54 s. The switch reported 16 s at +23.8317 s.
- Full lab state was pass at +24.5099 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.885 | test | primary-reboot started in lab medium-mlag |
| -1.585 | access-switch log | script,info networka primary-reboot start |
| -1.285 | switch1 log | script,info networka primary-reboot start |
| -0.987 | switch2 log | script,info networka primary-reboot start |
| -0.982 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.116 | state | All three switches run with spanning tree off. pass |
| -0.116 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.116 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.741 | quiet window | clean |
| 3.741 | step | Baseline |
| 7.743 | step | Reboot switch1 |
| 7.788 | reboot | dispatching the reboot to switch1 |
| 7.837 | reboot | switch1 command returned: accepted |
| 8.159 | host2-to-host1 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.344 to 2.547 s, request absent at destination |
| 8.238 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.29 to 2.494 s, reply absent at source |
| 23.807 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.734 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.741 | switch2 log | bridge,warning "bridge" peer link down |
| 32.298 | recovery | full lab state after reboot of switch1: pass |
| 48.298 | step | Reboot recovery |
| 51.301 | steps | last step ended |
| 52.538 | state | check after the steps: pass |
| 52.538 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 52.538 | state | All three switches run with spanning tree off. pass |
| 52.538 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 52.538 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 52.538 | streams | measurement ended; captures wait for final replies |
| 53.041 | stopped | captures and streams stopped |
| 53.082 | access-switch log | script,info networka primary-reboot end |
| 53.131 | switch1 log | script,info networka primary-reboot end |
| 53.182 | switch2 log | script,info networka primary-reboot end |
| 53.185 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
