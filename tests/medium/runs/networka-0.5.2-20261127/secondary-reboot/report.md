# FAIL — secondary-reboot

Reboot switch2 in its checked MLAG secondary role and measure both directions between host1 and host2.

- Flood probes: 10.110.0.255 A probe was seen more than once across the sender's bond members.
- After the steps, host1-to-host2: 246 pings lost in total at one ping every 100 ms, longest measured stop at least 25.5247 s, 0 duplicated.
- After the steps, host2-to-host1: 246 pings lost in total at one ping every 100 ms, longest measured stop at least 25.5189 s, 0 duplicated.
- Step Reboot switch2 is fail.
- Step Reboot recovery is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host1:eth1 → host2:bond0 | 5 s | 267 at one ping every 100 ms | at least 25.5247 s | fail |
| Reboot switch2 | host2:bond0 → host1:eth1 | 5 s | 268 at one ping every 100 ms | at least 25.5189 s | fail |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 246 at one ping every 100 ms | at least 25.5247 s | fail |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 246 at one ping every 100 ms | at least 25.5189 s | fail |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · fail

- host1:eth1 → host2:bond0 · 246 pings lost in total at one ping every 100 ms, longest measured stop at least 25.5247 s · 0 duplicates
- host2:bond0 → host1:eth1 · 246 pings lost in total at one ping every 100 ms, longest measured stop at least 25.5189 s · 0 duplicates

## Reboot of switch2

Reboot switch2 · pass

- Uptime before dispatch was 54 s. The switch reported 18 s at +24.773 s.
- Full lab state was pass at +25.4141 s, against a 60 s limit.

## Flood probes

**fail**
- host2:bond0 → 10.110.0.255 · 517 probes at one every 100 ms, 2 returned to the sender, 39 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 517 probes at one every 100 ms, 0 returned to the sender, 39 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.863 | test | secondary-reboot started in lab medium-mlag |
| -1.561 | access-switch log | script,info networka secondary-reboot start |
| -1.270 | switch1 log | script,info networka secondary-reboot start |
| -0.981 | switch2 log | script,info networka secondary-reboot start |
| -0.976 | switch log | marker 'networka secondary-reboot start' written on access-switch, switch1, switch2 |
| -0.124 | state | check before the steps: pass |
| -0.124 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.124 | state | All three switches run with spanning tree off. pass |
| -0.124 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.124 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:eth1 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth1 |
| -0.061 | capture | started at host2:eth2 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.001 | flood probe | started from host2:bond0 to 10.110.0.255 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 4.005 | quiet window | clean |
| 4.005 | step | Baseline |
| 8.006 | step | Reboot switch2 |
| 8.056 | reboot | dispatching the reboot to switch2 |
| 8.097 | reboot | switch2 command returned: accepted |
| 8.479 | host2-to-host1 | 22 pings lost at one ping every 100 ms, traffic stopped for 2.196 to 2.4 s, reply absent at source |
| 8.553 | host1-to-host2 | 21 pings lost at one ping every 100 ms, traffic stopped for 2.1 to 2.303 s, request absent at destination |
| 24.148 | switch1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.718 | switch1 log | bridge,warning "bridge" peer disconnected |
| 25.727 | switch1 log | bridge,warning "bridge" peer link down |
| 28.205 | host2-to-host1 | 246 pings lost at one ping every 100 ms, traffic stopped for at least 25.519 s, reply absent at source |
| 28.280 | host1-to-host2 | 246 pings lost at one ping every 100 ms, traffic stopped for at least 25.525 s, request absent at destination |
| 33.470 | recovery | full lab state after reboot of switch2: pass |
| 49.473 | step | Reboot recovery |
| 52.476 | steps | last step ended |
| 53.804 | state | check after the steps: pass |
| 53.804 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 53.804 | state | All three switches run with spanning tree off. pass |
| 53.804 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 53.804 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 53.805 | streams | measurement ended; captures wait for final replies |
| 54.310 | stopped | captures and streams stopped |
| 54.348 | access-switch log | script,info networka secondary-reboot end |
| 54.382 | switch1 log | script,info networka secondary-reboot end |
| 54.436 | switch2 log | script,info networka secondary-reboot end |
| 54.440 | switch log | marker 'networka secondary-reboot end' written on access-switch, switch1, switch2 |
