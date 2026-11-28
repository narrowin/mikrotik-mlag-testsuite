# PASS — primary-reboot

Reboot switch1 in its checked primary role and measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:bond0 → host2:bond0 | 5 s | 37 at one ping every 100 ms | 2.91466 to 3.12178 s | pass |
| Reboot switch1 | host2:bond0 → host1:bond0 | 5 s | 38 at one ping every 100 ms | 2.9198 to 3.12764 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 55 s. The switch reported 23 s at +30.9181 s.
- Full lab state was pass at +31.8051 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.796 | test | primary-reboot started in lab small-mlag-mac-move |
| -1.984 | switch1 log | script,info networka primary-reboot start |
| -1.540 | switch2 log | script,info networka primary-reboot start |
| -1.526 | switch log | marker 'networka primary-reboot start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.118 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.813 | quiet window | clean |
| 3.813 | step | Baseline |
| 7.820 | step | Reboot switch1 |
| 7.899 | reboot | dispatching the reboot to switch1 |
| 7.965 | reboot | switch1 command returned: accepted |
| 8.422 | host2-to-host1 | 29 pings lost at one ping every 100 ms, traffic stopped for 2.92 to 3.128 s, reply absent at source, request absent at destination |
| 8.468 | host1-to-host2 | 29 pings lost at one ping every 100 ms, traffic stopped for 2.915 to 3.122 s, request absent at destination |
| 23.658 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 26.483 | switch2 log | bridge,warning "bridge" peer disconnected |
| 26.492 | switch2 log | bridge,warning "bridge" peer link down |
| 26.766 | host2-to-host1 | 8 pings lost at one ping every 100 ms, traffic stopped for 0.728 to 0.935 s, request absent at destination |
| 26.818 | host1-to-host2 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.62 to 0.824 s, request absent at destination |
| 28.852 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 28.891 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 39.704 | recovery | full lab state after reboot of switch1: pass |
| 55.705 | step | Reboot recovery |
| 58.737 | steps | last step ended |
| 60.508 | state | check after the steps: pass |
| 60.508 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 60.508 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 60.510 | streams | measurement ended; captures wait for final replies |
| 61.030 | stopped | captures and streams stopped |
| 61.065 | switch1 log | script,info networka primary-reboot end |
| 61.106 | switch2 log | script,info networka primary-reboot end |
| 61.126 | switch log | marker 'networka primary-reboot end' written on switch1, switch2 |
