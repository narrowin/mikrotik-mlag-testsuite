# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked MLAG secondary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.207113 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.004 s.
- The new boot was detected at +28.516 s, with all lab checks passing at +29.192 s.

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
| -1.892 | test | secondary-power-loss started in lab medium-mlag |
| -1.573 | access-switch log | script,info networka secondary-power-loss start |
| -1.281 | switch1 log | script,info networka secondary-power-loss start |
| -0.974 | switch2 log | script,info networka secondary-power-loss start |
| -0.967 | switch log | marker 'networka secondary-power-loss start' written on access-switch, switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.114 | state | All three switches run with spanning tree off. pass |
| -0.114 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.114 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.735 | quiet window | clean |
| 3.735 | step | Baseline |
| 7.736 | step | switch2 power lost |
| 7.858 | power | withdrawing the data cables of switch2 and stopping its guest |
| 8.003 | power | switch2 guest paused and all data cables down |
| 8.573 | access-switch log | interface,info ether3 link down |
| 8.579 | switch1 log | interface,info ether2 link down |
| 8.606 | switch1 log | bridge,warning "bridge" peer link down |
| 28.005 | step | switch2 power restored |
| 28.007 | power | resetting and resuming the guest of switch2 |
| 28.218 | power | switch2 guest running and all data cables up |
| 28.627 | access-switch log | interface,info ether3 link up (speed 10G, full duplex) |
| 28.665 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.692 | switch1 log | bridge,warning "bridge" peer link down |
| 38.710 | switch1 log | bridge,warning "bridge" peer link down |
| 43.722 | switch1 log | bridge,warning "bridge" peer link down |
| 46.408 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 57.199 | recovery | full lab state after power restoration of switch2: pass |
| 73.200 | step | Power recovery |
| 76.202 | steps | last step ended |
| 77.451 | state | check after the steps: pass |
| 77.451 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 77.451 | state | All three switches run with spanning tree off. pass |
| 77.451 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 77.451 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 77.451 | streams | measurement ended; captures wait for final replies |
| 77.957 | stopped | captures and streams stopped |
| 77.994 | access-switch log | script,info networka secondary-power-loss end |
| 78.035 | switch1 log | script,info networka secondary-power-loss end |
| 78.080 | switch2 log | script,info networka secondary-power-loss end |
| 78.084 | switch log | marker 'networka secondary-power-loss end' written on access-switch, switch1, switch2 |
