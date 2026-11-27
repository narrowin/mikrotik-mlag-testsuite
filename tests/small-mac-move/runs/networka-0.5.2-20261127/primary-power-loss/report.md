# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked primary role and pause the guest before a cold reset. Measure both directions on the client bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | client1:bond0 → client2:bond0 | 5 s | 3 at one ping every 100 ms | 0.213308 to 0.415597 s | pass |
| switch1 power lost | client2:bond0 → client1:bond0 | 5 s | 3 at one ping every 100 ms | 0.211903 to 0.416805 s | pass |
| switch1 power restored | client1:bond0 → client2:bond0 | 5 s | 6 at one ping every 100 ms | 0.414876 to 0.624033 s | pass |
| switch1 power restored | client2:bond0 → client1:bond0 | 5 s | 6 at one ping every 100 ms | 0.51283 to 0.721392 s | pass |
| Power recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.004 s.
- The new boot was detected at +22.127 s, with all lab checks passing at +22.975 s.

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.944 | test | primary-power-loss started in lab small-mlag-mobile |
| -1.660 | switch1 log | script,info networka primary-power-loss start |
| -1.376 | switch2 log | script,info networka primary-power-loss start |
| -1.370 | switch log | marker 'networka primary-power-loss start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.114 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.058 | capture | started at client1:bond0 |
| -0.058 | capture | started at client2:bond0 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client2-to-client1 | started from client2:bond0 to client1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.747 | quiet window | clean |
| 3.747 | step | Baseline |
| 7.749 | step | switch1 power lost |
| 7.856 | power | withdrawing the data cables of switch1 and stopping its guest |
| 7.951 | power | switch1 guest paused and all data cables down |
| 8.193 | switch2 log | interface,info ether2 link down |
| 8.222 | switch2 log | bridge,warning "bridge" peer link down |
| 8.333 | client1-to-client2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.416 s, request absent at destination |
| 8.365 | client2-to-client1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.417 s, request absent at destination |
| 27.953 | step | switch1 power restored |
| 27.955 | power | resetting and resuming the guest of switch1 |
| 28.120 | power | switch1 guest running and all data cables up |
| 28.280 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.294 | switch2 log | bridge,warning "bridge" peer link down |
| 38.309 | switch2 log | bridge,warning "bridge" peer link down |
| 43.317 | switch2 log | bridge,warning "bridge" peer link down |
| 43.858 | client2-to-client1 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.513 to 0.721 s, request absent at destination |
| 43.905 | client1-to-client2 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.415 to 0.624 s, request absent at destination |
| 45.890 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 50.931 | recovery | full lab state after power restoration of switch1: pass |
| 66.932 | step | Power recovery |
| 69.938 | steps | last step ended |
| 71.380 | state | check after the steps: pass |
| 71.380 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 71.380 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 71.380 | streams | measurement ended; captures wait for final replies |
| 71.890 | stopped | captures and streams stopped |
| 71.930 | switch1 log | script,info networka primary-power-loss end |
| 71.970 | switch2 log | script,info networka primary-power-loss end |
| 71.973 | switch log | marker 'networka primary-power-loss end' written on switch1, switch2 |
