# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked MLAG secondary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:eth1 → host2:bond0 | 5 s | 1 at one ping every 100 ms | 0 to 0.205139 s | pass |
| switch2 power lost | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.206172 s | pass |
| switch2 power restored | host1:eth1 → host2:bond0 | 5 s | 1 at one ping every 100 ms | 0 to 0.204441 s | pass |
| switch2 power restored | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.207367 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.002 s.
- The new boot was detected at +28.089 s, with all lab checks passing at +28.751 s.

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
| -1.857 | test | secondary-power-loss started in lab medium-mlag |
| -1.556 | access-switch log | script,info networka secondary-power-loss start |
| -1.249 | switch1 log | script,info networka secondary-power-loss start |
| -0.959 | switch2 log | script,info networka secondary-power-loss start |
| -0.956 | switch log | marker 'networka secondary-power-loss start' written on access-switch, switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.112 | state | All three switches run with spanning tree off. pass |
| -0.112 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.112 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.059 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.766 | quiet window | clean |
| 3.766 | step | Baseline |
| 7.766 | step | switch2 power lost |
| 7.927 | power | withdrawing the data cables of switch2 and stopping its guest |
| 7.938 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 7.972 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 8.076 | power | switch2 guest paused and all data cables down |
| 8.348 | access-switch log | interface,info ether3 link down |
| 8.365 | switch1 log | interface,info ether2 link down |
| 8.397 | switch1 log | bridge,warning "bridge" peer link down |
| 28.077 | step | switch2 power restored |
| 28.078 | power | resetting and resuming the guest of switch2 |
| 28.274 | power | switch2 guest running and all data cables up |
| 28.397 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 28.413 | access-switch log | interface,info ether3 link up (speed 10G, full duplex) |
| 33.410 | switch1 log | bridge,warning "bridge" peer link down |
| 38.423 | switch1 log | bridge,warning "bridge" peer link down |
| 43.439 | switch1 log | bridge,warning "bridge" peer link down |
| 45.571 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 45.591 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, request absent at destination |
| 56.829 | recovery | full lab state after power restoration of switch2: pass |
| 72.831 | step | Power recovery |
| 75.832 | steps | last step ended |
| 77.043 | state | check after the steps: pass |
| 77.043 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 77.043 | state | All three switches run with spanning tree off. pass |
| 77.043 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 77.043 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 77.043 | streams | measurement ended; captures wait for final replies |
| 77.547 | stopped | captures and streams stopped |
| 77.594 | access-switch log | script,info networka secondary-power-loss end |
| 77.631 | switch1 log | script,info networka secondary-power-loss end |
| 77.681 | switch2 log | script,info networka secondary-power-loss end |
| 77.691 | switch log | marker 'networka secondary-power-loss end' written on access-switch, switch1, switch2 |
