# PASS — primary-reboot

Reboot switch1 in its checked primary role and measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:bond0 → host2:bond0 | 5 s | 30 at one ping every 100 ms | 2.18583 to 2.39114 s | pass |
| Reboot switch1 | host2:bond0 → host1:bond0 | 5 s | 30 at one ping every 100 ms | 2.18355 to 2.39097 s | pass |
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

- Uptime before dispatch was 54 s. The switch reported 16 s at +22.7928 s.
- Full lab state was pass at +23.6221 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.910 | test | primary-reboot started in lab small-mlag-mac-move |
| -1.623 | switch1 log | script,info networka primary-reboot start |
| -1.336 | switch2 log | script,info networka primary-reboot start |
| -1.328 | switch log | marker 'networka primary-reboot start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.114 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.056 | capture | started at host1:bond0 |
| -0.055 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.742 | quiet window | clean |
| 3.743 | step | Baseline |
| 7.747 | step | Reboot switch1 |
| 7.800 | reboot | dispatching the reboot to switch1 |
| 7.852 | reboot | switch1 command returned: accepted |
| 8.264 | host1-to-host2 | 22 pings lost at one ping every 100 ms, traffic stopped for 2.186 to 2.391 s, reply absent at source, request absent at destination |
| 8.265 | host2-to-host1 | 22 pings lost at one ping every 100 ms, traffic stopped for 2.184 to 2.391 s, request absent at destination |
| 24.134 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.139 | switch2 log | bridge,warning "bridge" peer link down |
| 24.184 | host1-to-host2 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.619 to 0.825 s, request absent at destination |
| 24.200 | host2-to-host1 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.616 to 0.828 s, request absent at destination |
| 26.467 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 26.497 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 31.422 | recovery | full lab state after reboot of switch1: pass |
| 47.422 | step | Reboot recovery |
| 50.425 | steps | last step ended |
| 51.884 | state | check after the steps: pass |
| 51.884 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 51.884 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 51.884 | streams | measurement ended; captures wait for final replies |
| 52.389 | stopped | captures and streams stopped |
| 52.423 | switch1 log | script,info networka primary-reboot end |
| 52.471 | switch2 log | script,info networka primary-reboot end |
| 52.475 | switch log | marker 'networka primary-reboot end' written on switch1, switch2 |
