# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 4 at one ping every 100 ms | 0.314988 to 0.519995 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 10 at one ping every 100 ms | 0.929253 to 1.13601 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 161 s. The switch reported 16 s at +22.8453 s.
- Full lab state was pass at +24.422 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.901 | test | switch-reboot started in lab small-strict |
| -2.606 | switch1 log | script,info networka switch-reboot start |
| -2.312 | switch2 log | script,info networka switch-reboot start |
| -2.303 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both switches show MLAG connected. pass |
| -0.115 | state | Both switches run with spanning tree off. pass |
| -0.115 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.827 | quiet window | clean |
| 3.828 | step | Reboot switch1 |
| 3.879 | reboot | dispatching the reboot to switch1 |
| 3.916 | reboot | switch1 command returned: accepted |
| 19.683 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 20.152 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.158 | switch2 log | bridge,warning "bridge" peer link down |
| 20.246 | host2-to-host3 | 10 pings lost at one ping every 100 ms, traffic stopped for 0.929 to 1.136 s, reply absent at source, request absent at destination |
| 20.491 | switch2 log | interface,info host2 link down |
| 20.534 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.315 to 0.52 s, reply absent at source, request absent at destination |
| 20.543 | switch2 log | interface,info host3 link down |
| 20.821 | switch2 log | interface,info host2 link up |
| 21.200 | switch2 log | interface,info host3 link up |
| 22.324 | switch1 log | interface,info host1 link up |
| 22.370 | switch1 log | interface,info host3 link up |
| 22.432 | switch1 log | interface,info host2 link up |
| 28.301 | recovery | full lab state after reboot of switch1: pass |
| 33.301 | steps | last step ended |
| 35.390 | state | check after the steps: pass |
| 35.390 | state | Both switches show MLAG connected. pass |
| 35.390 | state | Both switches run with spanning tree off. pass |
| 35.390 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 35.390 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.390 | streams | measurement ended; captures wait for final replies |
| 35.893 | stopped | captures and streams stopped |
| 35.926 | switch1 log | script,info networka switch-reboot end |
| 35.979 | switch2 log | script,info networka switch-reboot end |
| 35.982 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
