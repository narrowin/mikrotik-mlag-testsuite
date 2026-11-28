# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 181 at one ping every 100 ms | 16.5939 to 16.8001 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 181 at one ping every 100 ms | 16.5525 to 16.7606 s | fail |
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

- Uptime before dispatch was 226 s. The switch reported 17 s at +23.9123 s.
- Full lab state was pass at +25.3826 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.177 | test | reboot-b-primary started in lab two-pair |
| -2.878 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.580 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.280 | switch-b1 log | script,info networka reboot-b-primary start |
| -1.953 | switch-b2 log | script,info networka reboot-b-primary start |
| -1.934 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.117 | state | check before the steps: pass |
| -0.117 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.117 | state | All four switches run with spanning tree off. pass |
| -0.117 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.117 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.117 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.749 | quiet window | clean |
| 3.749 | step | Baseline |
| 7.752 | step | Reboot switch-b1 |
| 7.796 | reboot | dispatching the reboot to switch-b1 |
| 7.839 | reboot | switch-b1 command returned: accepted |
| 8.214 | host1-to-host2 | 160 pings lost at one ping every 100 ms, traffic stopped for 16.594 to 16.8 s, reply absent at source, request absent at destination |
| 8.273 | host2-to-host1 | 160 pings lost at one ping every 100 ms, traffic stopped for 16.553 to 16.761 s, request absent at destination |
| 24.796 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 24.802 | switch-b2 log | bridge,warning "bridge" peer link down |
| 25.219 | host1-to-host2 | 21 pings lost at one ping every 100 ms, traffic stopped for 2.069 to 2.276 s, reply absent at source, request absent at destination |
| 25.235 | host2-to-host1 | 21 pings lost at one ping every 100 ms, traffic stopped for 2.084 to 2.291 s, request absent at destination |
| 33.178 | recovery | full lab state after reboot of switch-b1: pass |
| 49.178 | step | Reboot recovery |
| 52.179 | steps | last step ended |
| 54.117 | state | check after the steps: pass |
| 54.117 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.117 | state | All four switches run with spanning tree off. pass |
| 54.117 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 54.117 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.117 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.117 | streams | measurement ended; captures wait for final replies |
| 54.624 | stopped | captures and streams stopped |
| 54.651 | switch-a1 log | script,info networka reboot-b-primary end |
| 54.690 | switch-a2 log | script,info networka reboot-b-primary end |
| 54.735 | switch-b1 log | script,info networka reboot-b-primary end |
| 54.788 | switch-b2 log | script,info networka reboot-b-primary end |
| 54.792 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
