# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 174 at one ping every 100 ms | 18.0634 to 18.2708 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 173 at one ping every 100 ms | 17.9443 to 18.1518 s | fail |
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

- Uptime before dispatch was 237 s. The switch reported 17 s at +24.5336 s.
- Full lab state was pass at +26.1551 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.538 | test | reboot-b-primary started in lab medium-two-pair |
| -3.194 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.863 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.556 | switch-b1 log | script,info networka reboot-b-primary start |
| -2.229 | switch-b2 log | script,info networka reboot-b-primary start |
| -2.219 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.120 | state | All four switches run with spanning tree off. pass |
| -0.120 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.120 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.120 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.063 | capture | started at host1:bond0 |
| -0.063 | capture | started at host2:bond0 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.756 | quiet window | clean |
| 3.757 | step | Baseline |
| 7.759 | step | Reboot switch-b1 |
| 7.812 | reboot | dispatching the reboot to switch-b1 |
| 7.871 | reboot | switch-b1 command returned: accepted |
| 8.218 | host1-to-host2 | 174 pings lost at one ping every 100 ms, traffic stopped for 18.063 to 18.271 s, reply absent at source, request absent at destination |
| 8.298 | host2-to-host1 | 173 pings lost at one ping every 100 ms, traffic stopped for 17.944 to 18.152 s, request absent at destination |
| 18.862 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.867 | switch-b2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.281 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 25.284 | switch-b2 log | bridge,warning "bridge" peer link down |
| 33.967 | recovery | full lab state after reboot of switch-b1: pass |
| 49.968 | step | Reboot recovery |
| 52.971 | steps | last step ended |
| 55.026 | state | check after the steps: pass |
| 55.026 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 55.026 | state | All four switches run with spanning tree off. pass |
| 55.026 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 55.026 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 55.026 | state | Both cables of every host are eligible in its LACP bond. pass |
| 55.026 | streams | measurement ended; captures wait for final replies |
| 55.533 | stopped | captures and streams stopped |
| 55.575 | switch-a1 log | script,info networka reboot-b-primary end |
| 55.612 | switch-a2 log | script,info networka reboot-b-primary end |
| 55.648 | switch-b1 log | script,info networka reboot-b-primary end |
| 55.697 | switch-b2 log | script,info networka reboot-b-primary end |
| 55.698 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
