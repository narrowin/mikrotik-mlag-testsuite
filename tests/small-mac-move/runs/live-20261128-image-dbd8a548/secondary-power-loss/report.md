# PASS — secondary-power-loss

Withdraw all data links of switch2 in its checked secondary role and pause the guest before a cold reset. Measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
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

- Data cables lost carrier and the guest was paused for 20.003 s.
- The new boot was detected at +28.138 s, with all lab checks passing at +29.016 s after power-on dispatch, against a 180 s recovery deadline.

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
| -3.504 | test | secondary-power-loss started in lab small-mlag-mac-move |
| -2.932 | switch1 log | script,info networka secondary-power-loss start |
| -2.501 | switch2 log | script,info networka secondary-power-loss start |
| -2.483 | switch log | marker 'networka secondary-power-loss start' written on switch1, switch2 |
| -0.221 | state | check before the steps: pass |
| -0.221 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.221 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.066 | capture | started at host1:bond0 |
| -0.065 | capture | started at host2:bond0 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.918 | quiet window | clean |
| 3.919 | step | Baseline |
| 7.921 | step | switch2 power lost |
| 8.121 | power | taking down the data cables of switch2 and stopping its guest |
| 8.232 | power | switch2 guest paused and all data cables down |
| 8.873 | switch1 log | interface,info ether2 link down |
| 8.910 | switch1 log | bridge,warning "bridge" peer link down |
| 28.233 | step | switch2 power restored |
| 28.235 | power | resetting and resuming the guest of switch2 |
| 28.415 | power | switch2 guest running and all data cables up |
| 28.961 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 33.992 | switch1 log | bridge,warning "bridge" peer link down |
| 39.009 | switch1 log | bridge,warning "bridge" peer link down |
| 44.024 | switch1 log | bridge,warning "bridge" peer link down |
| 57.252 | recovery | full lab state after the power loss of switch2: pass |
| 73.254 | step | Power recovery |
| 76.258 | steps | last step ended |
| 77.717 | state | check after the steps: pass |
| 77.717 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 77.717 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 77.717 | streams | measurement ended; captures wait for final replies |
| 78.223 | stopped | captures and streams stopped |
| 78.255 | switch1 log | script,info networka secondary-power-loss end |
| 78.318 | switch2 log | script,info networka secondary-power-loss end |
| 78.326 | switch log | marker 'networka secondary-power-loss end' written on switch1, switch2 |
