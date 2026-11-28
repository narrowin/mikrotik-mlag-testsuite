# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 7 at one ping every 100 ms | 0.606214 to 0.808828 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 166 s. The switch reported 16 s at +22.7817 s.
- Full lab state was pass at +24.2904 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.819 | test | switch-reboot started in lab small-strict |
| -2.531 | switch1 log | script,info networka switch-reboot start |
| -2.248 | switch2 log | script,info networka switch-reboot start |
| -2.245 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both switches show MLAG connected. pass |
| -0.112 | state | Both switches run with spanning tree off. pass |
| -0.112 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.112 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.806 | quiet window | clean |
| 3.807 | step | Reboot switch1 |
| 3.857 | reboot | dispatching the reboot to switch1 |
| 3.902 | reboot | switch1 command returned: accepted |
| 19.723 | switch2 log | bridge,warning "bridge" peer disconnected |
| 19.727 | switch2 log | bridge,warning "bridge" peer link down |
| 19.935 | host1-to-host2 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.606 to 0.809 s, request absent at destination |
| 19.948 | switch2 log | interface,info host1 link down |
| 20.281 | switch2 log | interface,info host1 link up |
| 21.990 | switch1 log | interface,info host2 link up |
| 22.002 | switch1 log | interface,info host1 link up |
| 22.059 | switch1 log | interface,info host3 link up |
| 28.148 | recovery | full lab state after reboot of switch1: pass |
| 33.149 | steps | last step ended |
| 35.219 | state | check after the steps: pass |
| 35.219 | state | Both switches show MLAG connected. pass |
| 35.219 | state | Both switches run with spanning tree off. pass |
| 35.219 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 35.219 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.219 | streams | measurement ended; captures wait for final replies |
| 35.723 | stopped | captures and streams stopped |
| 35.769 | switch1 log | script,info networka switch-reboot end |
| 35.820 | switch2 log | script,info networka switch-reboot end |
| 35.826 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
