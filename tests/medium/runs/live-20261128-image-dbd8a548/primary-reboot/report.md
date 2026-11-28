# PASS — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 33 at one ping every 100 ms | 2.50827 to 2.71444 s | pass |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 32 at one ping every 100 ms | 2.51727 to 2.72257 s | pass |
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

- Uptime before dispatch was 57 s. The switch reported 24 s at +31.356 s.
- Full lab state was pass at +32.0965 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.536 | test | primary-reboot started in lab medium-mlag |
| -2.024 | access-switch log | script,info networka primary-reboot start |
| -1.604 | switch1 log | script,info networka primary-reboot start |
| -1.160 | switch2 log | script,info networka primary-reboot start |
| -1.151 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.119 | state | All three switches run with spanning tree off. pass |
| -0.119 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.119 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.063 | capture | started at host1:eth1 |
| -0.062 | capture | started at host2:bond0 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.778 | quiet window | clean |
| 3.778 | step | Baseline |
| 7.778 | step | Reboot switch1 |
| 7.831 | reboot | dispatching the reboot to switch1 |
| 7.891 | reboot | switch1 command returned: accepted |
| 8.318 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.508 to 2.714 s, reply absent at source |
| 8.324 | host2-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.517 to 2.723 s, request absent at destination |
| 26.352 | switch2 log | bridge,warning "bridge" peer disconnected |
| 26.362 | switch2 log | bridge,warning "bridge" peer link down |
| 26.424 | host1-to-host2 | 8 pings lost at one ping every 100 ms, traffic stopped for 0.728 to 0.934 s, request absent at destination |
| 26.441 | host2-to-host1 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.623 to 0.831 s, request absent at destination |
| 39.928 | recovery | full lab state after reboot of switch1: pass |
| 55.929 | step | Reboot recovery |
| 58.932 | steps | last step ended |
| 60.609 | state | check after the steps: pass |
| 60.609 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 60.609 | state | All three switches run with spanning tree off. pass |
| 60.609 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 60.609 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 60.610 | streams | measurement ended; captures wait for final replies |
| 61.122 | stopped | captures and streams stopped |
| 61.179 | access-switch log | script,info networka primary-reboot end |
| 61.265 | switch1 log | script,info networka primary-reboot end |
| 61.323 | switch2 log | script,info networka primary-reboot end |
| 61.330 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
