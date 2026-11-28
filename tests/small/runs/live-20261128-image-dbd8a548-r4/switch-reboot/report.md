# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 3 at one ping every 100 ms | 0.204344 to 0.4101 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 7 at one ping every 100 ms | 0.62777 to 0.831846 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 158 s. The switch reported 16 s at +22.9741 s.
- Full lab state was pass at +23.9281 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.372 | test | switch-reboot started in lab small-mlag |
| -2.091 | switch1 log | script,info networka switch-reboot start |
| -1.773 | switch2 log | script,info networka switch-reboot start |
| -1.766 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both switches show MLAG connected. pass |
| -0.111 | state | Both switches run with spanning tree off. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.806 | quiet window | clean |
| 3.806 | step | Reboot switch1 |
| 3.847 | reboot | dispatching the reboot to switch1 |
| 3.896 | reboot | switch1 command returned: accepted |
| 20.158 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.165 | switch2 log | bridge,warning "bridge" peer link down |
| 20.305 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.204 to 0.41 s, request absent at destination |
| 20.371 | host2-to-host3 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.628 to 0.832 s, request absent at destination |
| 27.775 | recovery | full lab state after reboot of switch1: pass |
| 32.776 | steps | last step ended |
| 34.400 | state | check after the steps: pass |
| 34.400 | state | Both switches show MLAG connected. pass |
| 34.400 | state | Both switches run with spanning tree off. pass |
| 34.400 | state | Both cables of every host are eligible in its LACP bond. pass |
| 34.400 | streams | measurement ended; captures wait for final replies |
| 34.906 | stopped | captures and streams stopped |
| 34.952 | switch1 log | script,info networka switch-reboot end |
| 34.987 | switch2 log | script,info networka switch-reboot end |
| 34.991 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
