# PASS — primary-power-loss

Withdraw all data links of switch1 in its checked primary role and pause the guest before a cold reset. Measure both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:bond0 → host2:bond0 | 5 s | 4 at one ping every 100 ms | 0.310737 to 0.515276 s | pass |
| switch1 power lost | host2:bond0 → host1:bond0 | 5 s | 4 at one ping every 100 ms | 0.311284 to 0.515679 s | pass |
| switch1 power restored | host1:bond0 → host2:bond0 | 5 s | 6 at one ping every 100 ms | 0.413241 to 0.621193 s | pass |
| switch1 power restored | host2:bond0 → host1:bond0 | 5 s | 5 at one ping every 100 ms | 0.304038 to 0.514137 s | pass |
| Power recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.013 s.
- The new boot was detected at +26.981 s, with all lab checks passing at +27.974 s after power-on dispatch, against a 180 s recovery deadline.

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
| -2.017 | test | primary-power-loss started in lab small-mlag-mac-move |
| -1.712 | switch1 log | script,info networka primary-power-loss start |
| -1.401 | switch2 log | script,info networka primary-power-loss start |
| -1.394 | switch log | marker 'networka primary-power-loss start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.112 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.841 | quiet window | clean |
| 3.841 | step | Baseline |
| 7.842 | step | switch1 power lost |
| 8.681 | power | taking down the data cables of switch1 and stopping its guest |
| 8.743 | host2-to-host1 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.311 to 0.516 s, request absent at destination |
| 8.751 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.311 to 0.515 s, request absent at destination |
| 9.171 | power | switch1 guest paused and all data cables down |
| 9.633 | switch2 log | interface,info ether2 link down |
| 10.091 | switch2 log | bridge,warning "bridge" peer link down |
| 29.173 | step | switch1 power restored |
| 29.184 | power | resetting and resuming the guest of switch1 |
| 29.420 | power | switch1 guest running and all data cables up |
| 29.717 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 34.748 | switch2 log | bridge,warning "bridge" peer link down |
| 39.779 | switch2 log | bridge,warning "bridge" peer link down |
| 44.795 | switch2 log | bridge,warning "bridge" peer link down |
| 47.489 | host1-to-host2 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.413 to 0.621 s, request absent at destination |
| 47.518 | host2-to-host1 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.304 to 0.514 s, request absent at destination |
| 49.558 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 49.583 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 57.158 | recovery | full lab state after the power loss of switch1: pass |
| 73.160 | step | Power recovery |
| 76.163 | steps | last step ended |
| 78.297 | state | check after the steps: pass |
| 78.297 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 78.297 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 78.298 | streams | measurement ended; captures wait for final replies |
| 78.807 | stopped | captures and streams stopped |
| 78.873 | switch1 log | script,info networka primary-power-loss end |
| 78.958 | switch2 log | script,info networka primary-power-loss end |
| 78.966 | switch log | marker 'networka primary-power-loss end' written on switch1, switch2 |
