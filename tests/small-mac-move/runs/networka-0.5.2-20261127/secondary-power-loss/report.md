# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked secondary role and pause the guest before a cold reset. Measure both directions on the client bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | client1:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | client2:bond0 → client1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | client1:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | client2:bond0 → client1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.003 s.
- The new boot was detected at +22.016 s, with all lab checks passing at +22.852 s.

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
| -1.974 | test | secondary-power-loss started in lab small-mlag-mobile |
| -1.676 | switch1 log | script,info networka secondary-power-loss start |
| -1.386 | switch2 log | script,info networka secondary-power-loss start |
| -1.383 | switch log | marker 'networka secondary-power-loss start' written on switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.110 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.057 | capture | started at client1:bond0 |
| -0.057 | capture | started at client2:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client2-to-client1 | started from client2:bond0 to client1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.764 | quiet window | clean |
| 3.764 | step | Baseline |
| 7.765 | step | switch2 power lost |
| 7.864 | power | withdrawing the data cables of switch2 and stopping its guest |
| 7.982 | power | switch2 guest paused and all data cables down |
| 8.820 | switch1 log | interface,info ether2 link down |
| 8.856 | switch1 log | bridge,warning "bridge" peer link down |
| 27.983 | step | switch2 power restored |
| 27.984 | power | resetting and resuming the guest of switch2 |
| 28.136 | power | switch2 guest running and all data cables up |
| 28.841 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.865 | switch1 log | bridge,warning "bridge" peer link down |
| 38.875 | switch1 log | bridge,warning "bridge" peer link down |
| 50.836 | recovery | full lab state after power restoration of switch2: pass |
| 66.838 | step | Power recovery |
| 69.840 | steps | last step ended |
| 71.282 | state | check after the steps: pass |
| 71.282 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 71.282 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 71.283 | streams | measurement ended; captures wait for final replies |
| 71.790 | stopped | captures and streams stopped |
| 71.835 | switch1 log | script,info networka secondary-power-loss end |
| 71.892 | switch2 log | script,info networka secondary-power-loss end |
| 71.895 | switch log | marker 'networka secondary-power-loss end' written on switch1, switch2 |
