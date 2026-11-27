# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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

- Uptime before dispatch was 165 s. The switch reported 17 s at +24.828 s.
- Full lab state was pass at +26.7202 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.226 | test | switch-reboot started in lab small-mlag-rstp |
| -2.933 | switch1 log | script,info networka switch-reboot start |
| -2.621 | switch2 log | script,info networka switch-reboot start |
| -2.613 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both switches show MLAG connected. pass |
| -0.115 | state | Both switches run RSTP. pass |
| -0.115 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.115 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.818 | quiet window | clean |
| 3.818 | step | Reboot switch1 |
| 3.865 | reboot | dispatching the reboot to switch1 |
| 3.919 | reboot | switch1 command returned: accepted |
| 21.379 | switch2 log | bridge,warning "bridge" peer disconnected |
| 21.389 | switch2 log | bridge,warning "bridge" peer link down |
| 21.470 | switch2 log | bridge,stp ether2:0  learning |
| 21.472 | switch2 log | bridge,stp ether2:0  forwarding |
| 22.132 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.133 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 24.425 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 30.586 | recovery | full lab state after reboot of switch1: pass |
| 35.587 | steps | last step ended |
| 38.095 | state | check after the steps: pass |
| 38.095 | state | Both switches show MLAG connected. pass |
| 38.095 | state | Both switches run RSTP. pass |
| 38.095 | state | Both MLAG peers are the RSTP root bridge. pass |
| 38.095 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| 38.095 | state | Both cables of every host are eligible in its LACP bond. pass |
| 38.095 | streams | measurement ended; captures wait for final replies |
| 38.600 | stopped | captures and streams stopped |
| 38.642 | switch1 log | script,info networka switch-reboot end |
| 38.677 | switch2 log | script,info networka switch-reboot end |
| 38.682 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
