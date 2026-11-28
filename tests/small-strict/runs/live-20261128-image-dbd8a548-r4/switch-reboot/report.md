# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 7 at one ping every 100 ms | 0.610107 to 0.816326 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 160 s. The switch reported 16 s at +22.7105 s.
- Full lab state was pass at +24.2015 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.886 | test | switch-reboot started in lab small-strict |
| -2.596 | switch1 log | script,info networka switch-reboot start |
| -2.313 | switch2 log | script,info networka switch-reboot start |
| -2.307 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both switches show MLAG connected. pass |
| -0.115 | state | Both switches run with spanning tree off. pass |
| -0.115 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.796 | quiet window | clean |
| 3.797 | step | Reboot switch1 |
| 3.840 | reboot | dispatching the reboot to switch1 |
| 3.900 | reboot | switch1 command returned: accepted |
| 19.765 | switch2 log | bridge,warning "bridge" peer disconnected |
| 19.774 | switch2 log | bridge,warning "bridge" peer link down |
| 19.887 | host1-to-host2 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.61 to 0.816 s, request absent at destination |
| 19.933 | switch2 log | interface,info host1 link down |
| 20.263 | switch2 log | interface,info host1 link up |
| 20.526 | switch1 log | interface,info host1 link up |
| 20.698 | switch1 log | interface,info host2 link up |
| 20.852 | switch1 log | interface,info host3 link up |
| 28.042 | recovery | full lab state after reboot of switch1: pass |
| 33.042 | steps | last step ended |
| 35.100 | state | check after the steps: pass |
| 35.100 | state | Both switches show MLAG connected. pass |
| 35.100 | state | Both switches run with spanning tree off. pass |
| 35.100 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 35.100 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.100 | streams | measurement ended; captures wait for final replies |
| 35.609 | stopped | captures and streams stopped |
| 35.648 | switch1 log | script,info networka switch-reboot end |
| 35.687 | switch2 log | script,info networka switch-reboot end |
| 35.694 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
