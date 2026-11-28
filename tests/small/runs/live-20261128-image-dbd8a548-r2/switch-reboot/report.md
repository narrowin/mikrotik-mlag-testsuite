# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 5 at one ping every 100 ms | 0.40739 to 0.614557 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 5 at one ping every 100 ms | 0.411587 to 0.614581 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 159 s. The switch reported 17 s at +23.8225 s.
- Full lab state was pass at +24.8233 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.365 | test | switch-reboot started in lab small-mlag |
| -2.057 | switch1 log | script,info networka switch-reboot start |
| -1.768 | switch2 log | script,info networka switch-reboot start |
| -1.762 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both switches show MLAG connected. pass |
| -0.113 | state | Both switches run with spanning tree off. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.853 | quiet window | clean |
| 3.853 | step | Reboot switch1 |
| 3.901 | reboot | dispatching the reboot to switch1 |
| 3.958 | reboot | switch1 command returned: accepted |
| 20.525 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.535 | switch2 log | bridge,warning "bridge" peer link down |
| 20.781 | host1-to-host2 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.407 to 0.615 s, request absent at destination |
| 20.781 | host2-to-host3 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.412 to 0.615 s, request absent at destination |
| 28.724 | recovery | full lab state after reboot of switch1: pass |
| 33.725 | steps | last step ended |
| 35.314 | state | check after the steps: pass |
| 35.314 | state | Both switches show MLAG connected. pass |
| 35.314 | state | Both switches run with spanning tree off. pass |
| 35.314 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.314 | streams | measurement ended; captures wait for final replies |
| 35.821 | stopped | captures and streams stopped |
| 35.868 | switch1 log | script,info networka switch-reboot end |
| 35.905 | switch2 log | script,info networka switch-reboot end |
| 35.908 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
