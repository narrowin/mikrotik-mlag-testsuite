# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 5 at one ping every 100 ms | 0.403853 to 0.606606 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 4 at one ping every 100 ms | 0.302399 to 0.511239 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 156 s. The switch reported 18 s at +24.91 s.
- Full lab state was pass at +26.42 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.418 | test | switch-reboot started in lab small-mlag |
| -2.102 | switch1 log | script,info networka switch-reboot start |
| -1.800 | switch2 log | script,info networka switch-reboot start |
| -1.796 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run with spanning tree off. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.814 | quiet window | clean |
| 3.814 | step | Reboot switch1 |
| 3.858 | reboot | dispatching the reboot to switch1 |
| 3.912 | reboot | switch1 command returned: accepted |
| 15.199 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 20.196 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 22.054 | switch2 log | bridge,warning "bridge" peer disconnected |
| 22.066 | switch2 log | bridge,warning "bridge" peer link down |
| 22.155 | host1-to-host2 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.404 to 0.607 s, request absent at destination |
| 22.283 | host2-to-host3 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.302 to 0.511 s, request absent at destination |
| 30.278 | recovery | full lab state after reboot of switch1: pass |
| 35.279 | steps | last step ended |
| 36.880 | state | check after the steps: pass |
| 36.880 | state | Both switches show MLAG connected. pass |
| 36.880 | state | Both switches run with spanning tree off. pass |
| 36.880 | state | Both cables of every host are eligible in its LACP bond. pass |
| 36.881 | streams | measurement ended; captures wait for final replies |
| 37.389 | stopped | captures and streams stopped |
| 37.435 | switch1 log | script,info networka switch-reboot end |
| 37.476 | switch2 log | script,info networka switch-reboot end |
| 37.480 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
