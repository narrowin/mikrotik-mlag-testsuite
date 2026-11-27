# PASS — primary-reboot

Reboot switch1 in its checked primary role and measure both directions on the client bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | client1:bond0 → client2:bond0 | 5 s | 37 at one ping every 100 ms | 2.8076 to 3.01408 s | pass |
| Reboot switch1 | client2:bond0 → client1:bond0 | 5 s | 35 at one ping every 100 ms | 2.81939 to 3.03084 s | pass |
| Reboot recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 48 s. The switch reported 16 s at +22.8039 s.
- Full lab state was pass at +23.6273 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.009 | test | primary-reboot started in lab small-mlag-mobile |
| -1.698 | switch1 log | script,info networka primary-reboot start |
| -1.401 | switch2 log | script,info networka primary-reboot start |
| -1.391 | switch log | marker 'networka primary-reboot start' written on switch1, switch2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.113 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.060 | capture | started at client1:bond0 |
| -0.060 | capture | started at client2:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client2-to-client1 | started from client2:bond0 to client1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.750 | quiet window | clean |
| 3.750 | step | Baseline |
| 7.752 | step | Reboot switch1 |
| 7.806 | reboot | dispatching the reboot to switch1 |
| 7.859 | reboot | switch1 command returned: accepted |
| 8.226 | client1-to-client2 | 28 pings lost at one ping every 100 ms, traffic stopped for 2.808 to 3.014 s, reply absent at source, request absent at destination |
| 8.246 | client2-to-client1 | 28 pings lost at one ping every 100 ms, traffic stopped for 2.819 to 3.031 s, request absent at destination |
| 23.475 | switch2 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.489 | switch2 log | bridge,warning "bridge" peer disconnected |
| 23.496 | switch2 log | bridge,warning "bridge" peer link down |
| 23.737 | client1-to-client2 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.619 to 0.824 s, request absent at destination |
| 23.777 | client2-to-client1 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.52 to 0.728 s, request absent at destination |
| 25.810 | client1-to-client2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.312 s, request absent at destination |
| 25.858 | client2-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 31.434 | recovery | full lab state after reboot of switch1: pass |
| 47.435 | step | Reboot recovery |
| 50.436 | steps | last step ended |
| 51.874 | state | check after the steps: pass |
| 51.874 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 51.874 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 51.874 | streams | measurement ended; captures wait for final replies |
| 52.381 | stopped | captures and streams stopped |
| 52.413 | switch1 log | script,info networka primary-reboot end |
| 52.464 | switch2 log | script,info networka primary-reboot end |
| 52.468 | switch log | marker 'networka primary-reboot end' written on switch1, switch2 |
