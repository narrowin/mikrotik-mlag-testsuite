# PASS — switch-reboot

Reboot switch1 in its current MLAG role while measuring both client streams. Verify that RouterOS restarted, then wait for MLAG and all client bonds to recover.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Reboot switch1 | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | client2:bond0 → client3:bond0 | 4 s | 7 at one ping every 100 ms | 0.63011 to 0.836066 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 57 s. The switch reported 16 s at +22.6922 s.
- Full lab state was pass at +23.6802 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.382 | test | switch-reboot started in lab small-mlag |
| -2.094 | switch1 log | script,info networka switch-reboot start |
| -1.806 | switch2 log | script,info networka switch-reboot start |
| -1.801 | switch log | marker 'networka switch-reboot start' written on switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | Both switches show MLAG connected. pass |
| -0.110 | state | Both switches run with spanning tree off. pass |
| -0.110 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.056 | capture | started at client1:bond0 |
| -0.056 | capture | started at client2:bond0 |
| -0.056 | capture | started at client3:bond0 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.809 | quiet window | clean |
| 3.809 | step | Reboot switch1 |
| 3.851 | reboot | dispatching the reboot to switch1 |
| 3.904 | reboot | switch1 command returned: accepted |
| 19.197 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 19.377 | switch2 log | bridge,warning "bridge" peer disconnected |
| 19.387 | switch2 log | bridge,warning "bridge" peer link down |
| 19.621 | client2-to-client3 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.63 to 0.836 s, request absent at destination |
| 27.531 | recovery | full lab state after reboot of switch1: pass |
| 32.532 | steps | last step ended |
| 34.095 | state | check after the steps: pass |
| 34.095 | state | Both switches show MLAG connected. pass |
| 34.095 | state | Both switches run with spanning tree off. pass |
| 34.095 | state | Both cables of every client are eligible in its LACP bond. pass |
| 34.095 | streams | measurement ended; captures wait for final replies |
| 34.599 | stopped | captures and streams stopped |
| 34.644 | switch1 log | script,info networka switch-reboot end |
| 34.684 | switch2 log | script,info networka switch-reboot end |
| 34.695 | switch log | marker 'networka switch-reboot end' written on switch1, switch2 |
