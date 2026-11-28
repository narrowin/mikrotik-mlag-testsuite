# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 166 s. The switch reported 16 s at +22.6658 s.
- Full lab state was pass at +24.1394 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.808 | test | switch-reboot started in lab small-strict |
| -2.536 | switch1 log | script,info networka switch-reboot start |
| -2.257 | switch2 log | script,info networka switch-reboot start |
| -2.255 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both switches show MLAG connected. pass |
| -0.115 | state | Both switches run with spanning tree off. pass |
| -0.115 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.824 | quiet window | clean |
| 3.825 | step | Reboot switch1 |
| 3.866 | reboot | dispatching the reboot to switch1 |
| 3.920 | reboot | switch1 command returned: accepted |
| 19.707 | switch2 log | bridge,warning "bridge" peer disconnected |
| 19.714 | switch2 log | bridge,warning "bridge" peer link down |
| 20.410 | switch1 log | interface,info host2 link up |
| 20.471 | switch1 log | interface,info host1 link up |
| 20.482 | switch1 log | interface,info host3 link up |
| 28.006 | recovery | full lab state after reboot of switch1: pass |
| 33.006 | steps | last step ended |
| 35.073 | state | check after the steps: pass |
| 35.073 | state | Both switches show MLAG connected. pass |
| 35.073 | state | Both switches run with spanning tree off. pass |
| 35.073 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 35.073 | state | Both cables of every host are eligible in its LACP bond. pass |
| 35.074 | streams | measurement ended; captures wait for final replies |
| 35.577 | stopped | captures and streams stopped |
| 35.604 | switch1 log | script,info networka switch-reboot end |
| 35.646 | switch2 log | script,info networka switch-reboot end |
| 35.650 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
