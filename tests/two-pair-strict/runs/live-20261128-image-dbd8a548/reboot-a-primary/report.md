# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 185 at one ping every 100 ms | 19.1532 to 19.3626 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 185 at one ping every 100 ms | 19.1539 to 19.3598 s | fail |
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

- Uptime before dispatch was 108 s. The switch reported 17 s at +23.9306 s.
- Full lab state was pass at +25.3456 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.317 | test | reboot-a-primary started in lab two-pair-strict |
| -3.010 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.704 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.397 | switch-b1 log | script,info networka reboot-a-primary start |
| -2.087 | switch-b2 log | script,info networka reboot-a-primary start |
| -2.082 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
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
| 3.829 | quiet window | clean |
| 3.829 | step | Baseline |
| 7.832 | step | Reboot switch-a1 |
| 7.906 | reboot | dispatching the reboot to switch-a1 |
| 7.961 | reboot | switch-a1 command returned: accepted |
| 8.296 | host2-to-host1 | 185 pings lost at one ping every 100 ms, traffic stopped for 19.154 to 19.36 s, reply absent at source, request absent at destination |
| 8.345 | host1-to-host2 | 185 pings lost at one ping every 100 ms, traffic stopped for 19.153 to 19.363 s, request absent at destination |
| 25.092 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 25.103 | switch-a2 log | bridge,warning "bridge" peer link down |
| 33.252 | recovery | full lab state after reboot of switch-a1: pass |
| 49.252 | step | Reboot recovery |
| 52.254 | steps | last step ended |
| 54.230 | state | check after the steps: pass |
| 54.230 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.230 | state | All four switches run with spanning tree off. pass |
| 54.230 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 54.230 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.230 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.230 | streams | measurement ended; captures wait for final replies |
| 54.735 | stopped | captures and streams stopped |
| 54.767 | switch-a1 log | script,info networka reboot-a-primary end |
| 54.796 | switch-a2 log | script,info networka reboot-a-primary end |
| 54.828 | switch-b1 log | script,info networka reboot-a-primary end |
| 54.862 | switch-b2 log | script,info networka reboot-a-primary end |
| 54.867 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
