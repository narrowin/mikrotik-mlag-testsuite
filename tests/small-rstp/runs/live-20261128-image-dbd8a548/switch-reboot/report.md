# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both host streams. Verify that RouterOS restarted, then wait for MLAG and all host bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | host1:bond0 → host2:bond0 | 4 s | 4 at one ping every 100 ms | 0.303939 to 0.516308 s | pass |
| Reboot switch1 | host2:bond0 → host3:bond0 | 4 s | 5 at one ping every 100 ms | 0.409425 to 0.619975 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 162 s. The switch reported 16 s at +23.7485 s.
- Full lab state was pass at +25.5845 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.054 | test | switch-reboot started in lab small-mlag-rstp |
| -2.751 | switch1 log | script,info networka switch-reboot start |
| -2.465 | switch2 log | script,info networka switch-reboot start |
| -2.463 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both switches show MLAG connected. pass |
| -0.111 | state | Both switches run RSTP. pass |
| -0.111 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.111 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.828 | quiet window | clean |
| 3.828 | step | Reboot switch1 |
| 3.876 | reboot | dispatching the reboot to switch1 |
| 3.913 | reboot | switch1 command returned: accepted |
| 19.151 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 20.287 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.292 | switch2 log | bridge,stp,debug host3:0  role transition DESIGNATED\_SYNCED |
| 20.292 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 20.292 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 20.292 | switch2 log | bridge,warning "bridge" peer link down |
| 20.355 | switch2 log | bridge,stp ether2:0  learning |
| 20.357 | switch2 log | bridge,stp ether2:0  forwarding |
| 20.358 | switch2 log | bridge,stp,debug host3:0  role transition DESIGNATED\_SYNCED |
| 20.358 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 20.358 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 20.358 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 20.358 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 20.422 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 20.425 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 20.426 | switch2 log | bridge,stp,debug host3:0  role transition DESIGNATED\_SYNCED |
| 20.437 | host2-to-host3 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.409 to 0.62 s, request absent at destination |
| 20.438 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.304 to 0.516 s, request absent at destination |
| 23.075 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 23.083 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 29.461 | recovery | full lab state after reboot of switch1: pass |
| 34.462 | steps | last step ended |
| 38.182 | state | check after the steps: pass |
| 38.182 | state | Both switches show MLAG connected. pass |
| 38.182 | state | Both switches run RSTP. pass |
| 38.182 | state | Both MLAG peers are the RSTP root bridge. pass |
| 38.182 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| 38.182 | state | Both cables of every host are eligible in its LACP bond. pass |
| 38.182 | streams | measurement ended; captures wait for final replies |
| 38.707 | stopped | captures and streams stopped |
| 38.748 | switch1 log | script,info networka switch-reboot end |
| 38.788 | switch2 log | script,info networka switch-reboot end |
| 38.793 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
