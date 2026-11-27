# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked MLAG secondary role and pause the guest before a cold reset. Measure both directions between host1 and host2 and on the independent bypass.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:eth1 → host2:bond0 | 5 s | 1 at one ping every 100 ms | 0 to 0.207847 s | pass |
| switch2 power lost | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power lost | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch2 power restored | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch2** · pass

- Data cables lost carrier and the guest was paused for 20.003 s.
- The new boot was detected at +21.959 s, with all lab checks passing at +22.589 s.

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
| -1.919 | test | secondary-power-loss started in lab medium-mlag |
| -1.631 | access-switch log | script,info networka secondary-power-loss start |
| -1.343 | switch1 log | script,info networka secondary-power-loss start |
| -1.051 | switch2 log | script,info networka secondary-power-loss start |
| -1.040 | switch log | marker 'networka secondary-power-loss start' written on access-switch, switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.116 | state | All three switches run with spanning tree off. pass |
| -0.116 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.116 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.863 | quiet window | clean |
| 3.863 | step | Baseline |
| 7.864 | step | switch2 power lost |
| 7.987 | power | withdrawing the data cables of switch2 and stopping its guest |
| 7.991 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 8.055 | access-switch log | interface,info ether3 link down |
| 8.131 | power | switch2 guest paused and all data cables down |
| 8.719 | switch1 log | interface,info ether2 link down |
| 8.746 | switch1 log | bridge,warning "bridge" peer link down |
| 28.132 | step | switch2 power restored |
| 28.133 | power | resetting and resuming the guest of switch2 |
| 28.350 | power | switch2 guest running and all data cables up |
| 28.803 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 29.142 | access-switch log | interface,info ether3 link up (speed 10G, full duplex) |
| 33.822 | switch1 log | bridge,warning "bridge" peer link down |
| 38.837 | switch1 log | bridge,warning "bridge" peer link down |
| 50.722 | recovery | full lab state after power restoration of switch2: pass |
| 66.725 | step | Power recovery |
| 69.729 | steps | last step ended |
| 70.951 | state | check after the steps: pass |
| 70.951 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 70.951 | state | All three switches run with spanning tree off. pass |
| 70.951 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 70.951 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 70.951 | streams | measurement ended; captures wait for final replies |
| 71.456 | stopped | captures and streams stopped |
| 71.493 | access-switch log | script,info networka secondary-power-loss end |
| 71.535 | switch1 log | script,info networka secondary-power-loss end |
| 71.592 | switch2 log | script,info networka secondary-power-loss end |
| 71.598 | switch log | marker 'networka secondary-power-loss end' written on access-switch, switch1, switch2 |
