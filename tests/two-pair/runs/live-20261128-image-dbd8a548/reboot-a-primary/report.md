# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 175 at one ping every 100 ms | 16.2435 to 16.4548 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 175 at one ping every 100 ms | 16.2516 to 16.4562 s | fail |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-a1

Reboot switch-a1 · pass

- Uptime before dispatch was 109 s. The switch reported 16 s at +23.0077 s.
- Full lab state was pass at +24.3279 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.177 | test | reboot-a-primary started in lab two-pair |
| -2.871 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.576 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.277 | switch-b1 log | script,info networka reboot-a-primary start |
| -1.943 | switch-b2 log | script,info networka reboot-a-primary start |
| -1.942 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.109 | state | check before the steps: pass |
| -0.109 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.109 | state | All four switches run with spanning tree off. pass |
| -0.109 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.109 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.109 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.056 | capture | started at host1:bond0 |
| -0.056 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.773 | quiet window | clean |
| 3.773 | step | Baseline |
| 7.775 | step | Reboot switch-a1 |
| 7.834 | reboot | dispatching the reboot to switch-a1 |
| 7.888 | reboot | switch-a1 command returned: accepted |
| 8.224 | host1-to-host2 | 157 pings lost at one ping every 100 ms, traffic stopped for 16.243 to 16.455 s, request absent at destination |
| 8.260 | host2-to-host1 | 157 pings lost at one ping every 100 ms, traffic stopped for 16.252 to 16.456 s, reply absent at source, request absent at destination |
| 24.244 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 24.252 | switch-a2 log | bridge,warning "bridge" peer link down |
| 24.677 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 24.716 | host2-to-host1 | 18 pings lost at one ping every 100 ms, traffic stopped for 1.771 to 1.977 s, reply absent at source |
| 24.887 | host1-to-host2 | 17 pings lost at one ping every 100 ms, traffic stopped for 1.666 to 1.87 s, request absent at destination |
| 32.162 | recovery | full lab state after reboot of switch-a1: pass |
| 48.165 | step | Reboot recovery |
| 51.167 | steps | last step ended |
| 53.157 | state | check after the steps: pass |
| 53.157 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.157 | state | All four switches run with spanning tree off. pass |
| 53.157 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 53.157 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.157 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.157 | streams | measurement ended; captures wait for final replies |
| 53.662 | stopped | captures and streams stopped |
| 53.708 | switch-a1 log | script,info networka reboot-a-primary end |
| 53.749 | switch-a2 log | script,info networka reboot-a-primary end |
| 53.790 | switch-b1 log | script,info networka reboot-a-primary end |
| 53.829 | switch-b2 log | script,info networka reboot-a-primary end |
| 53.842 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
