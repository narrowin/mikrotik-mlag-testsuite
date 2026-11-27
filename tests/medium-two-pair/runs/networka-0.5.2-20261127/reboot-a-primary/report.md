# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 183 at one ping every 100 ms | 18.9537 to 19.1575 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 183 at one ping every 100 ms | 18.9428 to 19.1573 s | fail |
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

- Uptime before dispatch was 110 s. The switch reported 17 s at +23.8842 s.
- Full lab state was pass at +25.3083 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.162 | test | reboot-a-primary started in lab medium-two-pair |
| -2.863 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.562 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.243 | switch-b1 log | script,info networka reboot-a-primary start |
| -1.949 | switch-b2 log | script,info networka reboot-a-primary start |
| -1.942 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.131 | state | check before the steps: pass |
| -0.131 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.131 | state | All four switches run with spanning tree off. pass |
| -0.131 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.131 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.131 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.075 | capture | started at host1:bond0 |
| -0.075 | capture | started at host2:bond0 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.754 | quiet window | clean |
| 3.754 | step | Baseline |
| 7.754 | step | Reboot switch-a1 |
| 7.797 | reboot | dispatching the reboot to switch-a1 |
| 7.845 | reboot | switch-a1 command returned: accepted |
| 8.191 | host1-to-host2 | 183 pings lost at one ping every 100 ms, traffic stopped for 18.954 to 19.157 s, request absent at destination |
| 8.209 | host2-to-host1 | 183 pings lost at one ping every 100 ms, traffic stopped for 18.943 to 19.157 s, reply absent at source, request absent at destination |
| 24.686 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 24.690 | switch-a2 log | bridge,warning "bridge" peer link down |
| 33.105 | recovery | full lab state after reboot of switch-a1: pass |
| 49.107 | step | Reboot recovery |
| 52.110 | steps | last step ended |
| 54.074 | state | check after the steps: pass |
| 54.074 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.074 | state | All four switches run with spanning tree off. pass |
| 54.074 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 54.074 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.074 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.074 | streams | measurement ended; captures wait for final replies |
| 54.579 | stopped | captures and streams stopped |
| 54.612 | switch-a1 log | script,info networka reboot-a-primary end |
| 54.644 | switch-a2 log | script,info networka reboot-a-primary end |
| 54.680 | switch-b1 log | script,info networka reboot-a-primary end |
| 54.725 | switch-b2 log | script,info networka reboot-a-primary end |
| 54.729 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
