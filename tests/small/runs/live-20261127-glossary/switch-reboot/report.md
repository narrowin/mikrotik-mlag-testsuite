# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 4 at one ping every 100 ms | 0.311698 to 0.519048 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 7 at one ping every 100 ms | 0.616669 to 0.827075 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 160 s. The switch reported 17 s at +24.0568 s.
- Full lab state was pass at +25.1312 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.427 | test | switch-reboot started in lab small-mlag |
| -2.120 | switch1 log | script,info networka switch-reboot start |
| -1.816 | switch2 log | script,info networka switch-reboot start |
| -1.812 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run with spanning tree off. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.819 | quiet window | clean |
| 3.819 | step | Reboot switch1 |
| 3.864 | reboot | dispatching the reboot to switch1 |
| 3.906 | reboot | switch1 command returned: accepted |
| 20.884 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.893 | switch2 log | bridge,warning "bridge" peer link down |
| 21.071 | host2-to-host3 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.617 to 0.827 s, request absent at destination |
| 21.263 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.312 to 0.519 s, request absent at destination |
| 28.995 | recovery | full lab state after reboot of switch1: pass |
| 33.996 | steps | last step ended |
| 35.606 | state | check after the steps: pass |
| 35.606 | state | Both switches show MLAG connected. pass |
| 35.606 | state | Both switches run with spanning tree off. pass |
| 35.606 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.606 | streams | measurement ended; captures wait for final replies |
| 36.114 | stopped | captures and streams stopped |
| 36.163 | switch1 log | script,info networka switch-reboot end |
| 36.206 | switch2 log | script,info networka switch-reboot end |
| 36.213 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
