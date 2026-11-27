# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 233 at one ping every 100 ms | 24.0736 to 24.2805 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 234 at one ping every 100 ms | 24.1094 to 24.3146 s | fail |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-b1

Reboot switch-b1 · pass

- Uptime before dispatch was 229 s. The switch reported 22 s at +30.8747 s.
- Full lab state was pass at +32.5484 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.209 | test | reboot-b-primary started in lab two-pair |
| -2.913 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.485 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.193 | switch-b1 log | script,info networka reboot-b-primary start |
| -1.899 | switch-b2 log | script,info networka reboot-b-primary start |
| -1.895 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.115 | state | All four switches run with spanning tree off. pass |
| -0.115 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.115 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.754 | quiet window | clean |
| 3.755 | step | Baseline |
| 7.755 | step | Reboot switch-b1 |
| 7.809 | reboot | dispatching the reboot to switch-b1 |
| 7.859 | reboot | switch-b1 command returned: accepted |
| 8.316 | host2-to-host1 | 232 pings lost at one ping every 100 ms, traffic stopped for 24.109 to 24.315 s, request absent at destination |
| 8.368 | host1-to-host2 | 232 pings lost at one ping every 100 ms, traffic stopped for 24.074 to 24.281 s, reply absent at source, request absent at destination |
| 24.900 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 29.896 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 31.552 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 31.613 | switch-b2 log | bridge,warning "bridge" peer link down |
| 32.630 | host2-to-host1 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.313 s, request absent at destination |
| 32.648 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 40.357 | recovery | full lab state after reboot of switch-b1: pass |
| 56.361 | step | Reboot recovery |
| 59.362 | steps | last step ended |
| 61.639 | state | check after the steps: pass |
| 61.639 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 61.639 | state | All four switches run with spanning tree off. pass |
| 61.639 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 61.639 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 61.639 | state | Both cables of every host are eligible in its LACP bond. pass |
| 61.639 | streams | measurement ended; captures wait for final replies |
| 62.155 | stopped | captures and streams stopped |
| 62.210 | switch-a1 log | script,info networka reboot-b-primary end |
| 62.281 | switch-a2 log | script,info networka reboot-b-primary end |
| 62.380 | switch-b1 log | script,info networka reboot-b-primary end |
| 62.432 | switch-b2 log | script,info networka reboot-b-primary end |
| 62.439 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
