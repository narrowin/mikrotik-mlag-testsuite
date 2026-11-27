# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts. Both bypass streams must continue while it restarts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 159 at one ping every 100 ms | 16.4552 to 16.6658 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 158 at one ping every 100 ms | 16.3528 to 16.5577 s | fail |
| Reboot switch-a1 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-a1

Reboot switch-a1 · pass

- Uptime before dispatch was 242 s. The switch reported 16 s at +22.6848 s.
- Full lab state was pass at +24.0717 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.079 | test | reboot-a-primary started in lab medium-two-pair |
| -2.790 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.506 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.217 | switch-b1 log | script,info networka reboot-a-primary start |
| -1.932 | switch-b2 log | script,info networka reboot-a-primary start |
| -1.930 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.116 | state | All four switches run with spanning tree off. pass |
| -0.116 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.116 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.062 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.006 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.878 | quiet window | clean |
| 3.878 | step | Baseline |
| 7.879 | step | Reboot switch-a1 |
| 7.931 | reboot | dispatching the reboot to switch-a1 |
| 7.996 | reboot | switch-a1 command returned: accepted |
| 8.320 | host1-to-host2 | 159 pings lost at one ping every 100 ms, traffic stopped for 16.455 to 16.666 s, request absent at destination |
| 8.336 | host2-to-host1 | 158 pings lost at one ping every 100 ms, traffic stopped for 16.353 to 16.558 s, reply absent at source, request absent at destination |
| 19.822 | switch-a2 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.846 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 23.849 | switch-a2 log | bridge,warning "bridge" peer link down |
| 32.003 | recovery | full lab state after reboot of switch-a1: pass |
| 48.006 | step | Reboot recovery |
| 51.007 | steps | last step ended |
| 52.937 | state | check after the steps: pass |
| 52.937 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 52.937 | state | All four switches run with spanning tree off. pass |
| 52.937 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 52.937 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 52.937 | state | Both cables of every host are eligible in its LACP bond. pass |
| 52.937 | streams | measurement ended; captures wait for final replies |
| 53.443 | stopped | captures and streams stopped |
| 53.494 | switch-a1 log | script,info networka reboot-a-primary end |
| 53.530 | switch-a2 log | script,info networka reboot-a-primary end |
| 53.580 | switch-b1 log | script,info networka reboot-a-primary end |
| 53.613 | switch-b2 log | script,info networka reboot-a-primary end |
| 53.619 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
