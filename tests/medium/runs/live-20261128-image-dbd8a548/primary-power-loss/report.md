# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 1 at one ping every 100 ms | 0 to 0.208934 s | pass |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.004 s.
- The new boot was detected at +29.132 s, with all lab checks passing at +29.809 s after power-on dispatch, against a 180 s recovery deadline.

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
| -2.063 | test | primary-power-loss started in lab medium-mlag |
| -1.721 | access-switch log | script,info networka primary-power-loss start |
| -1.399 | switch1 log | script,info networka primary-power-loss start |
| -1.071 | switch2 log | script,info networka primary-power-loss start |
| -1.068 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.118 | state | All three switches run with spanning tree off. pass |
| -0.118 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.118 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.065 | capture | started at host1:eth1 |
| -0.065 | capture | started at host2:bond0 |
| -0.010 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.006 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.753 | quiet window | clean |
| 3.753 | step | Baseline |
| 7.755 | step | switch1 power lost |
| 7.883 | power | taking down the data cables of switch1 and stopping its guest |
| 7.928 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 8.050 | power | switch1 guest paused and all data cables down |
| 8.796 | access-switch log | interface,info ether2 link down |
| 8.891 | switch2 log | interface,info ether2 link down |
| 8.920 | switch2 log | bridge,warning "bridge" peer link down |
| 28.052 | step | switch1 power restored |
| 28.054 | power | resetting and resuming the guest of switch1 |
| 28.262 | power | switch1 guest running and all data cables up |
| 28.853 | access-switch log | interface,info ether2 link up (speed 10G, full duplex) |
| 28.928 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.961 | switch2 log | bridge,warning "bridge" peer link down |
| 38.991 | switch2 log | bridge,warning "bridge" peer link down |
| 44.012 | switch2 log | bridge,warning "bridge" peer link down |
| 57.863 | recovery | full lab state after the power loss of switch1: pass |
| 73.866 | step | Power recovery |
| 76.870 | steps | last step ended |
| 78.572 | state | check after the steps: pass |
| 78.572 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 78.572 | state | All three switches run with spanning tree off. pass |
| 78.572 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 78.572 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 78.573 | streams | measurement ended; captures wait for final replies |
| 79.080 | stopped | captures and streams stopped |
| 79.119 | access-switch log | script,info networka primary-power-loss end |
| 79.243 | switch1 log | script,info networka primary-power-loss end |
| 79.266 | switch2 log | script,info networka primary-power-loss end |
| 79.276 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
