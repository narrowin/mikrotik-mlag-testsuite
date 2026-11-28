# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 4 at one ping every 100 ms | 0.304815 to 0.513514 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 9 at one ping every 100 ms | 0.832456 to 1.04008 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 158 s. The switch reported 18 s at +24.9039 s.
- Full lab state was pass at +25.9664 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.393 | test | switch-reboot started in lab small-mlag |
| -2.093 | switch1 log | script,info networka switch-reboot start |
| -1.795 | switch2 log | script,info networka switch-reboot start |
| -1.791 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both switches show MLAG connected. pass |
| -0.111 | state | Both switches run with spanning tree off. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.823 | quiet window | clean |
| 3.823 | step | Reboot switch1 |
| 3.890 | reboot | dispatching the reboot to switch1 |
| 3.945 | reboot | switch1 command returned: accepted |
| 18.121 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 21.592 | switch2 log | bridge,warning "bridge" peer disconnected |
| 21.598 | switch2 log | bridge,warning "bridge" peer link down |
| 21.780 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.305 to 0.514 s, request absent at destination |
| 21.852 | host2-to-host3 | 9 pings lost at one ping every 100 ms, traffic stopped for 0.832 to 1.04 s, request absent at destination |
| 29.857 | recovery | full lab state after reboot of switch1: pass |
| 34.859 | steps | last step ended |
| 36.475 | state | check after the steps: pass |
| 36.475 | state | Both switches show MLAG connected. pass |
| 36.475 | state | Both switches run with spanning tree off. pass |
| 36.475 | state | Both cables of every host are eligible in its LACP bond. pass |
| 36.475 | streams | measurement ended; captures wait for final replies |
| 36.984 | stopped | captures and streams stopped |
| 37.031 | switch1 log | script,info networka switch-reboot end |
| 37.076 | switch2 log | script,info networka switch-reboot end |
| 37.083 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
