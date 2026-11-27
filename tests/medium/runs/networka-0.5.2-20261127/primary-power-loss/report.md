# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 1 at one ping every 100 ms | 0 to 0.201935 s | pass |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.214919 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.003 s.
- The new boot was detected at +28.150 s, with all lab checks passing at +28.909 s.

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.029 | test | primary-power-loss started in lab medium-mlag |
| -1.665 | access-switch log | script,info networka primary-power-loss start |
| -1.283 | switch1 log | script,info networka primary-power-loss start |
| -0.970 | switch2 log | script,info networka primary-power-loss start |
| -0.967 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.111 | state | All three switches run with spanning tree off. pass |
| -0.111 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.111 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:eth1 |
| -0.057 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.800 | quiet window | clean |
| 3.800 | step | Baseline |
| 7.800 | step | switch1 power lost |
| 7.967 | power | withdrawing the data cables of switch1 and stopping its guest |
| 8.131 | switch2 log | interface,info ether2 link down |
| 8.143 | power | switch1 guest paused and all data cables down |
| 8.168 | switch2 log | bridge,warning "bridge" peer link down |
| 8.220 | access-switch log | interface,info ether2 link down |
| 28.144 | step | switch1 power restored |
| 28.146 | power | resetting and resuming the guest of switch1 |
| 28.274 | access-switch log | interface,info ether2 link up (speed 10G, full duplex) |
| 28.366 | power | switch1 guest running and all data cables up |
| 29.152 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 34.169 | switch2 log | bridge,warning "bridge" peer link down |
| 39.187 | switch2 log | bridge,warning "bridge" peer link down |
| 44.214 | switch2 log | bridge,warning "bridge" peer link down |
| 46.272 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, reply absent at source |
| 46.278 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.215 s, request absent at destination |
| 57.055 | recovery | full lab state after power restoration of switch1: pass |
| 73.056 | step | Power recovery |
| 76.059 | steps | last step ended |
| 77.317 | state | check after the steps: pass |
| 77.317 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 77.317 | state | All three switches run with spanning tree off. pass |
| 77.317 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 77.317 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 77.317 | streams | measurement ended; captures wait for final replies |
| 77.822 | stopped | captures and streams stopped |
| 77.865 | access-switch log | script,info networka primary-power-loss end |
| 77.926 | switch1 log | script,info networka primary-power-loss end |
| 77.977 | switch2 log | script,info networka primary-power-loss end |
| 77.980 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
