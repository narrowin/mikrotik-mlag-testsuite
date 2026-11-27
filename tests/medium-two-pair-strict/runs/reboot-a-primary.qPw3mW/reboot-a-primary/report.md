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
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 175 at one ping every 100 ms | 18.1305 to 18.337 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 175 at one ping every 100 ms | 18.1369 to 18.345 s | fail |
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

- Uptime before dispatch was 126 s. The switch reported 16 s at +22.894 s.
- Full lab state was pass at +24.2505 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.051 | test | reboot-a-primary started in lab medium-two-pair-strict |
| -2.762 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.474 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.192 | switch-b1 log | script,info networka reboot-a-primary start |
| -1.916 | switch-b2 log | script,info networka reboot-a-primary start |
| -1.910 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run with spanning tree off. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.061 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.002 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.861 | quiet window | clean |
| 3.861 | step | Baseline |
| 7.865 | step | Reboot switch-a1 |
| 7.908 | reboot | dispatching the reboot to switch-a1 |
| 7.959 | reboot | switch-a1 command returned: accepted |
| 8.305 | host2-to-host1 | 175 pings lost at one ping every 100 ms, traffic stopped for 18.137 to 18.345 s, reply absent at source, request absent at destination |
| 8.329 | host1-to-host2 | 175 pings lost at one ping every 100 ms, traffic stopped for 18.131 to 18.337 s, request absent at destination |
| 24.035 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 24.045 | switch-a2 log | bridge,warning "bridge" peer link down |
| 32.158 | recovery | full lab state after reboot of switch-a1: pass |
| 48.163 | step | Reboot recovery |
| 51.167 | steps | last step ended |
| 53.155 | state | check after the steps: pass |
| 53.155 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.155 | state | All four switches run with spanning tree off. pass |
| 53.155 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 53.155 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.155 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.155 | streams | measurement ended; captures wait for final replies |
| 53.662 | stopped | captures and streams stopped |
| 53.698 | switch-a1 log | script,info networka reboot-a-primary end |
| 53.744 | switch-a2 log | script,info networka reboot-a-primary end |
| 53.790 | switch-b1 log | script,info networka reboot-a-primary end |
| 53.822 | switch-b2 log | script,info networka reboot-a-primary end |
| 53.826 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
