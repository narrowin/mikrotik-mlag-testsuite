# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts. Both bypass streams must continue while it restarts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 173 at one ping every 100 ms | 17.9267 to 18.133 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 173 at one ping every 100 ms | 17.8922 to 18.1011 s | fail |
| Reboot switch-b1 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
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

## Reboot of switch-b1

Reboot switch-b1 · pass

- Uptime before dispatch was 358 s. The switch reported 16 s at +22.8013 s.
- Full lab state was pass at +24.161 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.257 | test | reboot-b-primary started in lab medium-two-pair |
| -2.969 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.683 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.328 | switch-b1 log | script,info networka reboot-b-primary start |
| -1.996 | switch-b2 log | script,info networka reboot-b-primary start |
| -1.989 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.130 | state | check before the steps: pass |
| -0.130 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.130 | state | All four switches run with spanning tree off. pass |
| -0.130 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.130 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.130 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.075 | capture | started at host1:bond0 |
| -0.075 | capture | started at host1:eth3 |
| -0.074 | capture | started at host2:bond0 |
| -0.074 | capture | started at host2:eth3 |
| -0.012 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.007 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.872 | quiet window | clean |
| 3.872 | step | Baseline |
| 7.873 | step | Reboot switch-b1 |
| 7.937 | reboot | dispatching the reboot to switch-b1 |
| 8.006 | reboot | switch-b1 command returned: accepted |
| 8.364 | host1-to-host2 | 173 pings lost at one ping every 100 ms, traffic stopped for 17.927 to 18.133 s, reply absent at source, request absent at destination |
| 8.398 | host2-to-host1 | 173 pings lost at one ping every 100 ms, traffic stopped for 17.892 to 18.101 s, request absent at destination |
| 22.572 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.966 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 23.974 | switch-b2 log | bridge,warning "bridge" peer link down |
| 32.098 | recovery | full lab state after reboot of switch-b1: pass |
| 48.100 | step | Reboot recovery |
| 51.104 | steps | last step ended |
| 53.041 | state | check after the steps: pass |
| 53.041 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.041 | state | All four switches run with spanning tree off. pass |
| 53.041 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 53.041 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.041 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.042 | streams | measurement ended; captures wait for final replies |
| 53.547 | stopped | captures and streams stopped |
| 53.596 | switch-a1 log | script,info networka reboot-b-primary end |
| 53.649 | switch-a2 log | script,info networka reboot-b-primary end |
| 53.708 | switch-b1 log | script,info networka reboot-b-primary end |
| 53.737 | switch-b2 log | script,info networka reboot-b-primary end |
| 53.743 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
