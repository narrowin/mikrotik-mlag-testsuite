# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 165 at one ping every 100 ms | 17.0958 to 17.2994 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 165 at one ping every 100 ms | 17.0611 to 17.2665 s | fail |
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

- Uptime before dispatch was 230 s. The switch reported 16 s at +23.7075 s.
- Full lab state was pass at +25.0876 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.189 | test | reboot-b-primary started in lab medium-two-pair-strict |
| -2.882 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.581 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.278 | switch-b1 log | script,info networka reboot-b-primary start |
| -1.955 | switch-b2 log | script,info networka reboot-b-primary start |
| -1.950 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.116 | state | All four switches run with spanning tree off. pass |
| -0.116 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.116 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.736 | quiet window | clean |
| 3.736 | step | Baseline |
| 7.739 | step | Reboot switch-b1 |
| 7.801 | reboot | dispatching the reboot to switch-b1 |
| 7.854 | reboot | switch-b1 command returned: accepted |
| 8.276 | host2-to-host1 | 165 pings lost at one ping every 100 ms, traffic stopped for 17.061 to 17.266 s, request absent at destination |
| 8.291 | host1-to-host2 | 165 pings lost at one ping every 100 ms, traffic stopped for 17.096 to 17.299 s, reply absent at source, request absent at destination |
| 21.022 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.498 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 24.503 | switch-b2 log | bridge,warning "bridge" peer link down |
| 32.889 | recovery | full lab state after reboot of switch-b1: pass |
| 48.890 | step | Reboot recovery |
| 51.891 | steps | last step ended |
| 53.882 | state | check after the steps: pass |
| 53.882 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.882 | state | All four switches run with spanning tree off. pass |
| 53.882 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 53.882 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.882 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.882 | streams | measurement ended; captures wait for final replies |
| 54.387 | stopped | captures and streams stopped |
| 54.426 | switch-a1 log | script,info networka reboot-b-primary end |
| 54.458 | switch-a2 log | script,info networka reboot-b-primary end |
| 54.515 | switch-b1 log | script,info networka reboot-b-primary end |
| 54.563 | switch-b2 log | script,info networka reboot-b-primary end |
| 54.570 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
