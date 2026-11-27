# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2 and on the independent bypass.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 5 at one ping every 100 ms | 0.314335 to 0.518716 s | pass |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 3 at one ping every 100 ms | 0.208425 to 0.416858 s | pass |
| switch1 power lost | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 6 at one ping every 100 ms | 0.519087 to 0.733542 s | pass |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 7 at one ping every 100 ms | 0.611747 to 0.81489 s | pass |
| switch1 power restored | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power restored | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.002 s.
- The new boot was detected at +27.974 s, with all lab checks passing at +29.634 s.

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.886 | test | primary-power-loss started in lab medium-mlag |
| -1.592 | access-switch log | script,info networka primary-power-loss start |
| -1.282 | switch1 log | script,info networka primary-power-loss start |
| -0.998 | switch2 log | script,info networka primary-power-loss start |
| -0.995 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.114 | state | All three switches run with spanning tree off. pass |
| -0.114 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.114 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth3 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.981 | quiet window | clean |
| 3.981 | step | Baseline |
| 7.983 | step | switch1 power lost |
| 8.108 | power | withdrawing the data cables of switch1 and stopping its guest |
| 8.145 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 8.263 | access-switch log | interface,info ether2 link down |
| 8.282 | power | switch1 guest paused and all data cables down |
| 8.955 | switch2 log | interface,info ether2 link down |
| 8.984 | switch2 log | bridge,warning "bridge" peer link down |
| 9.074 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.314 to 0.519 s, request absent at destination |
| 9.100 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.417 s, request absent at destination |
| 28.283 | step | switch1 power restored |
| 28.284 | power | resetting and resuming the guest of switch1 |
| 28.474 | power | switch1 guest running and all data cables up |
| 29.009 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 29.316 | access-switch log | interface,info ether2 link up (speed 10G, full duplex) |
| 34.027 | switch2 log | bridge,warning "bridge" peer link down |
| 39.041 | switch2 log | bridge,warning "bridge" peer link down |
| 44.045 | switch2 log | bridge,warning "bridge" peer link down |
| 44.524 | host2-to-host1 | 7 pings lost at one ping every 100 ms, traffic stopped for 0.612 to 0.815 s, request absent at destination |
| 44.541 | host1-to-host2 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.519 to 0.734 s, request absent at destination |
| 57.919 | recovery | full lab state after power restoration of switch1: pass |
| 73.921 | step | Power recovery |
| 76.924 | steps | last step ended |
| 78.169 | state | check after the steps: pass |
| 78.169 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 78.169 | state | All three switches run with spanning tree off. pass |
| 78.169 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 78.169 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 78.169 | streams | measurement ended; captures wait for final replies |
| 78.674 | stopped | captures and streams stopped |
| 78.701 | access-switch log | script,info networka primary-power-loss end |
| 78.755 | switch1 log | script,info networka primary-power-loss end |
| 78.797 | switch2 log | script,info networka primary-power-loss end |
| 78.809 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
