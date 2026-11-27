# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 3 at one ping every 100 ms | 0.205965 to 0.410999 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 6 at one ping every 100 ms | 0.522427 to 0.727389 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 2053 s. The switch reported 23 s at +31.0127 s.
- Full lab state was pass at +32.0847 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.498 | test | switch-reboot started in lab small-mlag |
| -2.153 | switch1 log | script,info networka switch-reboot start |
| -1.823 | switch2 log | script,info networka switch-reboot start |
| -1.819 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both switches show MLAG connected. pass |
| -0.116 | state | Both switches run with spanning tree off. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.883 | quiet window | clean |
| 3.884 | step | Reboot switch1 |
| 3.931 | reboot | dispatching the reboot to switch1 |
| 3.986 | reboot | switch1 command returned: accepted |
| 18.594 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.590 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.454 | switch2 log | bridge,warning "bridge" peer disconnected |
| 25.465 | switch2 log | bridge,warning "bridge" peer link down |
| 25.600 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.206 to 0.411 s, request absent at destination |
| 25.669 | host2-to-host3 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.522 to 0.727 s, reply absent at source, request absent at destination |
| 25.821 | switch2 log | interface,info host3 link down |
| 26.149 | switch2 log | interface,info host3 link up |
| 27.495 | switch1 log | interface,info host2 link up |
| 27.530 | switch1 log | interface,info host1 link up |
| 27.573 | switch1 log | interface,info host3 link up |
| 36.016 | recovery | full lab state after reboot of switch1: pass |
| 41.017 | steps | last step ended |
| 42.661 | state | check after the steps: pass |
| 42.661 | state | Both switches show MLAG connected. pass |
| 42.661 | state | Both switches run with spanning tree off. pass |
| 42.661 | state | Both cables of every host are eligible in its LACP bond. pass |
| 42.661 | streams | measurement ended; captures wait for final replies |
| 43.170 | stopped | captures and streams stopped |
| 43.223 | switch1 log | script,info networka switch-reboot end |
| 43.262 | switch2 log | script,info networka switch-reboot end |
| 43.268 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
