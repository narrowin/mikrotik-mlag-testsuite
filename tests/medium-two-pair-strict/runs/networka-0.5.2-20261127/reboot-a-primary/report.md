# FAIL — reboot-a-primary

Reboot switch-a1 in its checked MLAG primary role of pair A and measure both directions between the hosts.

- Step Reboot switch-a1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 188 at one ping every 100 ms | 19.4467 to 19.6514 s | fail |
| Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 188 at one ping every 100 ms | 19.4565 to 19.6618 s | fail |
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

- Uptime before dispatch was 110 s. The switch reported 17 s at +24.1671 s.
- Full lab state was pass at +25.6395 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.445 | test | reboot-a-primary started in lab medium-two-pair-strict |
| -3.112 | switch-a1 log | script,info networka reboot-a-primary start |
| -2.772 | switch-a2 log | script,info networka reboot-a-primary start |
| -2.455 | switch-b1 log | script,info networka reboot-a-primary start |
| -2.140 | switch-b2 log | script,info networka reboot-a-primary start |
| -2.133 | switch log | marker 'networka reboot-a-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.113 | state | All four switches run with spanning tree off. pass |
| -0.113 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.113 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.741 | quiet window | clean |
| 3.742 | step | Baseline |
| 7.742 | step | Reboot switch-a1 |
| 7.811 | reboot | dispatching the reboot to switch-a1 |
| 7.865 | reboot | switch-a1 command returned: accepted |
| 8.264 | host1-to-host2 | 188 pings lost at one ping every 100 ms, traffic stopped for 19.447 to 19.651 s, request absent at destination |
| 8.328 | host2-to-host1 | 188 pings lost at one ping every 100 ms, traffic stopped for 19.457 to 19.662 s, reply absent at source, request absent at destination |
| 25.331 | switch-a2 log | bridge,warning "bridge" peer disconnected |
| 25.339 | switch-a2 log | bridge,warning "bridge" peer link down |
| 33.451 | recovery | full lab state after reboot of switch-a1: pass |
| 49.452 | step | Reboot recovery |
| 52.454 | steps | last step ended |
| 54.681 | state | check after the steps: pass |
| 54.681 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.681 | state | All four switches run with spanning tree off. pass |
| 54.681 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 54.681 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.681 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.682 | streams | measurement ended; captures wait for final replies |
| 55.190 | stopped | captures and streams stopped |
| 55.230 | switch-a1 log | script,info networka reboot-a-primary end |
| 55.272 | switch-a2 log | script,info networka reboot-a-primary end |
| 55.306 | switch-b1 log | script,info networka reboot-a-primary end |
| 55.356 | switch-b2 log | script,info networka reboot-a-primary end |
| 55.361 | switch log | marker 'networka reboot-a-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
