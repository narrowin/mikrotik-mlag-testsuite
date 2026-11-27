# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked secondary role and pause the guest before a cold reset. Measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.004 s.
- The new boot was detected at +22.914 s, with all lab checks passing at +23.765 s.

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.952 | test | secondary-power-loss started in lab small-mlag-mac-move |
| -1.658 | switch1 log | script,info networka secondary-power-loss start |
| -1.368 | switch2 log | script,info networka secondary-power-loss start |
| -1.364 | switch log | marker 'networka secondary-power-loss start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.112 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.750 | quiet window | clean |
| 3.750 | step | Baseline |
| 7.752 | step | switch2 power lost |
| 7.844 | power | withdrawing the data cables of switch2 and stopping its guest |
| 7.944 | power | switch2 guest paused and all data cables down |
| 8.460 | switch1 log | interface,info ether2 link down |
| 8.485 | switch1 log | bridge,warning "bridge" peer link down |
| 27.946 | step | switch2 power restored |
| 27.948 | power | resetting and resuming the guest of switch2 |
| 28.112 | power | switch2 guest running and all data cables up |
| 28.503 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.522 | switch1 log | bridge,warning "bridge" peer link down |
| 38.538 | switch1 log | bridge,warning "bridge" peer link down |
| 43.555 | switch1 log | bridge,warning "bridge" peer link down |
| 51.713 | recovery | full lab state after power restoration of switch2: pass |
| 67.713 | step | Power recovery |
| 70.717 | steps | last step ended |
| 72.167 | state | check after the steps: pass |
| 72.167 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 72.167 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 72.167 | streams | measurement ended; captures wait for final replies |
| 72.672 | stopped | captures and streams stopped |
| 72.699 | switch1 log | script,info networka secondary-power-loss end |
| 72.755 | switch2 log | script,info networka secondary-power-loss end |
| 72.758 | switch log | marker 'networka secondary-power-loss end' written on switch1, switch2 |
