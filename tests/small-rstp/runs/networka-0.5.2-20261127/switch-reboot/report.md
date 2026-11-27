# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both client streams. Verify that RouterOS restarted, then wait for MLAG and all client bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | client2:bond0 → client3:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 162 s. The switch reported 23 s at +30.7623 s.
- Full lab state was pass at +32.6345 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.206 | test | switch-reboot started in lab small-mlag-rstp |
| -2.915 | switch1 log | script,info networka switch-reboot start |
| -2.625 | switch2 log | script,info networka switch-reboot start |
| -2.617 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run RSTP. pass |
| -0.114 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.114 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.114 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.060 | capture | started at client1:bond0 |
| -0.060 | capture | started at client2:bond0 |
| -0.060 | capture | started at client3:bond0 |
| -0.005 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.914 | quiet window | clean |
| 3.914 | step | Reboot switch1 |
| 3.964 | reboot | dispatching the reboot to switch1 |
| 4.019 | reboot | switch1 command returned: accepted |
| 20.093 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 22.302 | switch2 log | bridge,warning "bridge" peer disconnected |
| 22.314 | switch2 log | bridge,warning "bridge" peer link down |
| 22.407 | switch2 log | bridge,stp ether2:0  learning |
| 22.408 | switch2 log | bridge,stp ether2:0  forwarding |
| 22.499 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 25.129 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 25.190 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 36.599 | recovery | full lab state after reboot of switch1: pass |
| 41.599 | steps | last step ended |
| 44.070 | state | check after the steps: pass |
| 44.070 | state | Both switches show MLAG connected. pass |
| 44.070 | state | Both switches run RSTP. pass |
| 44.070 | state | Both MLAG peers are the RSTP root bridge. pass |
| 44.070 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| 44.070 | state | Both cables of every client are eligible in its LACP bond. pass |
| 44.071 | streams | measurement ended; captures wait for final replies |
| 44.577 | stopped | captures and streams stopped |
| 44.609 | switch1 log | script,info networka switch-reboot end |
| 44.649 | switch2 log | script,info networka switch-reboot end |
| 44.652 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
