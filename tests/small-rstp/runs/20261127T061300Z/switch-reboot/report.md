# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both client streams. Verify that RouterOS restarted, then wait for MLAG and all client bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | client1:bond0 → client2:bond0 | 4 s | 4 at one ping every 100 ms | 0.31733 to 0.523343 s | pass |
| Reboot switch1 | client2:bond0 → client3:bond0 | 4 s | 5 at one ping every 100 ms | 0.40252 to 0.610744 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 287 s. The switch reported 17 s at +23.7472 s.
- Full lab state was pass at +25.4763 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.952 | test | switch-reboot started in lab small-mlag-rstp |
| -1.922 | switch1 log | script,info networka switch-reboot start |
| -1.885 | switch2 log | script,info networka switch-reboot start |
| -1.881 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both switches show MLAG connected. pass |
| -0.113 | state | Both switches run RSTP. pass |
| -0.113 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.113 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.113 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.058 | capture | started at client1:bond0 |
| -0.058 | capture | started at client2:bond0 |
| -0.057 | capture | started at client3:bond0 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.803 | quiet window | clean |
| 3.804 | step | Reboot switch1 |
| 3.854 | reboot | dispatching the reboot to switch1 |
| 3.907 | reboot | switch1 command returned: accepted |
| 20.542 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.553 | switch2 log | bridge,stp,debug client3:0  role transition DESIGNATED\_SYNCED |
| 20.553 | switch2 log | bridge,stp,debug client2:0  role transition DESIGNATED\_SYNCED |
| 20.553 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 20.553 | switch2 log | bridge,warning "bridge" peer link down |
| 20.651 | switch2 log | bridge,stp ether2:0  learning |
| 20.651 | switch2 log | bridge,stp ether2:0  forwarding |
| 20.652 | switch2 log | bridge,stp,debug client3:0  role transition DESIGNATED\_SYNCED |
| 20.652 | switch2 log | bridge,stp,debug client2:0  role transition DESIGNATED\_SYNCED |
| 20.653 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 20.653 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 20.653 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 20.712 | client2-to-client3 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.403 to 0.611 s, request absent at destination |
| 20.717 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 20.719 | switch2 log | bridge,stp,debug client2:0  role transition DESIGNATED\_SYNCED |
| 20.720 | switch2 log | bridge,stp,debug client3:0  role transition DESIGNATED\_SYNCED |
| 20.751 | client1-to-client2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.317 to 0.523 s, request absent at destination |
| 23.054 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 23.406 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 29.330 | recovery | full lab state after reboot of switch1: pass |
| 34.331 | steps | last step ended |
| 36.796 | state | check after the steps: pass |
| 36.796 | state | Both switches show MLAG connected. pass |
| 36.796 | state | Both switches run RSTP. pass |
| 36.796 | state | Both MLAG peers are the RSTP root bridge. pass |
| 36.796 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| 36.796 | state | Both cables of every client are eligible in its LACP bond. pass |
| 36.796 | streams | measurement ended; captures wait for final replies |
| 37.300 | stopped | captures and streams stopped |
| 37.329 | switch1 log | script,info networka switch-reboot end |
| 37.358 | switch2 log | script,info networka switch-reboot end |
| 37.364 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
