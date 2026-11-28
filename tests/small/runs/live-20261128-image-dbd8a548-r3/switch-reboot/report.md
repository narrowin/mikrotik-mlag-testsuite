# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 6 at one ping every 100 ms | 0.510443 to 0.718501 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 9 at one ping every 100 ms | 0.824092 to 1.03248 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 156 s. The switch reported 16 s at +23.8342 s.
- Full lab state was pass at +24.8489 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.353 | test | switch-reboot started in lab small-mlag |
| -2.063 | switch1 log | script,info networka switch-reboot start |
| -1.768 | switch2 log | script,info networka switch-reboot start |
| -1.763 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both switches show MLAG connected. pass |
| -0.113 | state | Both switches run with spanning tree off. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.820 | quiet window | clean |
| 3.821 | step | Reboot switch1 |
| 3.871 | reboot | dispatching the reboot to switch1 |
| 3.944 | reboot | switch1 command returned: accepted |
| 20.832 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.841 | switch2 log | bridge,warning "bridge" peer link down |
| 21.027 | host1-to-host2 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.51 to 0.719 s, request absent at destination |
| 21.145 | host2-to-host3 | 9 pings lost at one ping every 100 ms, traffic stopped for 0.824 to 1.032 s, request absent at destination |
| 28.720 | recovery | full lab state after reboot of switch1: pass |
| 33.722 | steps | last step ended |
| 35.361 | state | check after the steps: pass |
| 35.361 | state | Both switches show MLAG connected. pass |
| 35.361 | state | Both switches run with spanning tree off. pass |
| 35.361 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.361 | streams | measurement ended; captures wait for final replies |
| 35.867 | stopped | captures and streams stopped |
| 35.911 | switch1 log | script,info networka switch-reboot end |
| 35.941 | switch2 log | script,info networka switch-reboot end |
| 35.945 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
