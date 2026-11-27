# PASS — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 26 at one ping every 100 ms | 2.29315 to 2.50014 s | pass |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 25 at one ping every 100 ms | 2.2906 to 2.49546 s | pass |
| Reboot switch1 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 177 s. The switch reported 16 s at +22.8486 s.
- Full lab state was pass at +23.4918 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.981 | test | primary-reboot started in lab medium-mlag |
| -1.690 | access-switch log | script,info networka primary-reboot start |
| -1.381 | switch1 log | script,info networka primary-reboot start |
| -0.994 | switch2 log | script,info networka primary-reboot start |
| -0.989 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.115 | state | All three switches run with spanning tree off. pass |
| -0.115 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.115 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth3 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.901 | quiet window | clean |
| 3.901 | step | Baseline |
| 7.904 | step | Reboot switch1 |
| 7.947 | reboot | dispatching the reboot to switch1 |
| 7.999 | reboot | switch1 command returned: accepted |
| 8.350 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.293 to 2.5 s, reply absent at source |
| 8.361 | host2-to-host1 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.291 to 2.495 s, request absent at destination |
| 23.839 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.257 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.264 | switch2 log | bridge,warning "bridge" peer link down |
| 24.451 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.416 s, request absent at destination |
| 24.491 | host2-to-host1 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.308 s, request absent at destination |
| 31.439 | recovery | full lab state after reboot of switch1: pass |
| 47.441 | step | Reboot recovery |
| 50.443 | steps | last step ended |
| 51.656 | state | check after the steps: pass |
| 51.656 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 51.656 | state | All three switches run with spanning tree off. pass |
| 51.656 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 51.656 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 51.656 | streams | measurement ended; captures wait for final replies |
| 52.160 | stopped | captures and streams stopped |
| 52.204 | access-switch log | script,info networka primary-reboot end |
| 52.247 | switch1 log | script,info networka primary-reboot end |
| 52.294 | switch2 log | script,info networka primary-reboot end |
| 52.296 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
