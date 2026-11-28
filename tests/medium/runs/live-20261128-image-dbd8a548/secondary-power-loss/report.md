# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked MLAG secondary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.210114 s | pass |
| switch2 power restored | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.009 s.
- The new boot was detected at +39.455 s, with all lab checks passing at +40.651 s after power-on dispatch, against a 180 s recovery deadline.

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
| -2.006 | test | secondary-power-loss started in lab medium-mlag |
| -1.677 | access-switch log | script,info networka secondary-power-loss start |
| -1.358 | switch1 log | script,info networka secondary-power-loss start |
| -1.040 | switch2 log | script,info networka secondary-power-loss start |
| -1.034 | switch log | marker 'networka secondary-power-loss start' written on access-switch, switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.110 | state | All three switches run with spanning tree off. pass |
| -0.110 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.110 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:eth1 |
| -0.056 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.821 | quiet window | clean |
| 3.822 | step | Baseline |
| 7.823 | step | switch2 power lost |
| 8.020 | power | taking down the data cables of switch2 and stopping its guest |
| 8.031 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 8.191 | power | switch2 guest paused and all data cables down |
| 8.417 | access-switch log | interface,info ether3 link down |
| 8.461 | switch1 log | interface,info ether2 link down |
| 8.494 | switch1 log | bridge,warning "bridge" peer link down |
| 28.191 | step | switch2 power restored |
| 28.199 | power | resetting and resuming the guest of switch2 |
| 28.456 | power | switch2 guest running and all data cables up |
| 28.477 | access-switch log | interface,info ether3 link up (speed 10G, full duplex) |
| 28.533 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.568 | switch1 log | bridge,warning "bridge" peer link down |
| 38.591 | switch1 log | bridge,warning "bridge" peer link down |
| 43.635 | switch1 log | bridge,warning "bridge" peer link down |
| 48.670 | switch1 log | bridge,warning "bridge" peer link down |
| 68.850 | recovery | full lab state after the power loss of switch2: pass |
| 84.853 | step | Power recovery |
| 87.854 | steps | last step ended |
| 89.106 | state | check after the steps: pass |
| 89.106 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 89.106 | state | All three switches run with spanning tree off. pass |
| 89.106 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 89.106 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 89.106 | streams | measurement ended; captures wait for final replies |
| 89.613 | stopped | captures and streams stopped |
| 89.658 | access-switch log | script,info networka secondary-power-loss end |
| 89.699 | switch1 log | script,info networka secondary-power-loss end |
| 89.760 | switch2 log | script,info networka secondary-power-loss end |
| 89.766 | switch log | marker 'networka secondary-power-loss end' written on access-switch, switch1, switch2 |
