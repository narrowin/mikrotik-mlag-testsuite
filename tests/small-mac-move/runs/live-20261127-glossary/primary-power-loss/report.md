# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked primary role and pause the guest before a cold reset. Measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:bond0 → host2:bond0 | 5 s | 4 at one ping every 100 ms | 0.207434 to 0.417342 s | pass |
| switch1 power lost | host2:bond0 → host1:bond0 | 5 s | 4 at one ping every 100 ms | 0.204723 to 0.415967 s | pass |
| switch1 power restored | host1:bond0 → host2:bond0 | 5 s | 5 at one ping every 100 ms | 0.314859 to 0.520042 s | pass |
| switch1 power restored | host2:bond0 → host1:bond0 | 5 s | 5 at one ping every 100 ms | 0.307044 to 0.511581 s | pass |
| Power recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.002 s.
- The new boot was detected at +28.325 s, with all lab checks passing at +29.183 s.

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
| -2.173 | test | primary-power-loss started in lab small-mlag-mac-move |
| -1.754 | switch1 log | script,info networka primary-power-loss start |
| -1.412 | switch2 log | script,info networka primary-power-loss start |
| -1.409 | switch log | marker 'networka primary-power-loss start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.112 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.783 | quiet window | clean |
| 3.784 | step | Baseline |
| 7.786 | step | switch1 power lost |
| 7.885 | power | withdrawing the data cables of switch1 and stopping its guest |
| 7.930 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 7.932 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 7.990 | power | switch1 guest paused and all data cables down |
| 8.421 | switch2 log | interface,info ether2 link down |
| 8.453 | switch2 log | bridge,warning "bridge" peer link down |
| 8.660 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.417 s, request absent at destination |
| 8.662 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.205 to 0.416 s, request absent at destination |
| 27.991 | step | switch1 power restored |
| 27.992 | power | resetting and resuming the guest of switch1 |
| 28.159 | power | switch1 guest running and all data cables up |
| 28.483 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.503 | switch2 log | bridge,warning "bridge" peer link down |
| 38.526 | switch2 log | bridge,warning "bridge" peer link down |
| 43.546 | switch2 log | bridge,warning "bridge" peer link down |
| 44.082 | host2-to-host1 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.307 to 0.512 s, request absent at destination |
| 44.130 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.315 to 0.52 s, request absent at destination |
| 46.061 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 46.107 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 57.175 | recovery | full lab state after power restoration of switch1: pass |
| 73.177 | step | Power recovery |
| 76.181 | steps | last step ended |
| 77.638 | state | check after the steps: pass |
| 77.638 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 77.638 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 77.638 | streams | measurement ended; captures wait for final replies |
| 78.142 | stopped | captures and streams stopped |
| 78.185 | switch1 log | script,info networka primary-power-loss end |
| 78.224 | switch2 log | script,info networka primary-power-loss end |
| 78.228 | switch log | marker 'networka primary-power-loss end' written on switch1, switch2 |
