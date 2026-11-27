# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 173 at one ping every 100 ms | 17.8962 to 18.1021 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 172 at one ping every 100 ms | 17.796 to 18.0029 s | fail |
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

- Uptime before dispatch was 110 s. The switch reported 17 s at +23.8055 s.
- Full lab state was pass at +25.2735 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.141 | test | reboot-a-primary started in lab two-pair-strict |
| -2.839 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.529 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.235 | switch-b1 log | script,info networka reboot-a-primary start |
| -1.949 | switch-b2 log | script,info networka reboot-a-primary start |
| -1.937 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.112 | state | All four switches run with spanning tree off. pass |
| -0.112 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.112 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.112 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.737 | quiet window | clean |
| 3.738 | step | Baseline |
| 7.739 | step | Reboot switch-a1 |
| 7.785 | reboot | dispatching the reboot to switch-a1 |
| 7.835 | reboot | switch-a1 command returned: accepted |
| 8.150 | host1-to-host2 | 173 pings lost at one ping every 100 ms, traffic stopped for 17.896 to 18.102 s, request absent at destination |
| 8.194 | host2-to-host1 | 172 pings lost at one ping every 100 ms, traffic stopped for 17.796 to 18.003 s, reply absent at source, request absent at destination |
| 25.056 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 25.062 | switch-a2 log | bridge,warning "bridge" peer link down |
| 33.058 | recovery | full lab state after reboot of switch-a1: pass |
| 49.059 | step | Reboot recovery |
| 52.062 | steps | last step ended |
| 53.984 | state | check after the steps: pass |
| 53.984 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.984 | state | All four switches run with spanning tree off. pass |
| 53.984 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 53.984 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.984 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.984 | streams | measurement ended; captures wait for final replies |
| 54.488 | stopped | captures and streams stopped |
| 54.531 | switch-a1 log | script,info networka reboot-a-primary end |
| 54.568 | switch-a2 log | script,info networka reboot-a-primary end |
| 54.605 | switch-b1 log | script,info networka reboot-a-primary end |
| 54.646 | switch-b2 log | script,info networka reboot-a-primary end |
| 54.651 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
