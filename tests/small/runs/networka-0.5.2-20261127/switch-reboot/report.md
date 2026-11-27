# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both client streams. Verify that RouterOS restarted, then wait for MLAG and all client bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | client2:bond0 → client3:bond0 | 4 s | 3 at one ping every 100 ms | 0.213276 to 0.425425 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 161 s. The switch reported 16 s at +23.7534 s.
- Full lab state was pass at +24.769 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.356 | test | switch-reboot started in lab small-mlag |
| -2.043 | switch1 log | script,info networka switch-reboot start |
| -1.745 | switch2 log | script,info networka switch-reboot start |
| -1.740 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both switches show MLAG connected. pass |
| -0.112 | state | Both switches run with spanning tree off. pass |
| -0.112 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.059 | capture | started at client1:bond0 |
| -0.058 | capture | started at client2:bond0 |
| -0.058 | capture | started at client3:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.844 | quiet window | clean |
| 3.844 | step | Reboot switch1 |
| 3.890 | reboot | dispatching the reboot to switch1 |
| 3.948 | reboot | switch1 command returned: accepted |
| 17.414 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 20.907 | switch2 log | bridge,warning "bridge" peer disconnected |
| 20.917 | switch2 log | bridge,warning "bridge" peer link down |
| 21.212 | client2-to-client3 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.425 s, request absent at destination |
| 28.659 | recovery | full lab state after reboot of switch1: pass |
| 33.659 | steps | last step ended |
| 35.248 | state | check after the steps: pass |
| 35.248 | state | Both switches show MLAG connected. pass |
| 35.248 | state | Both switches run with spanning tree off. pass |
| 35.248 | state | Both cables of every client are eligible in its LACP bond. pass |
| 35.248 | streams | measurement ended; captures wait for final replies |
| 35.753 | stopped | captures and streams stopped |
| 35.791 | switch1 log | script,info networka switch-reboot end |
| 35.846 | switch2 log | script,info networka switch-reboot end |
| 35.849 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
