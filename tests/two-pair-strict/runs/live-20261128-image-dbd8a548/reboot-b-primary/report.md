# FAIL — reboot-b-primary

Reboot switch-b1 in its checked MLAG primary role of pair B and measure both directions between the hosts.

- Step Reboot switch-b1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 181 at one ping every 100 ms | 18.7496 to 18.9601 s | fail |
| Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 180 at one ping every 100 ms | 18.6762 to 18.8794 s | fail |
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

- Uptime before dispatch was 227 s. The switch reported 16 s at +23.7835 s.
- Full lab state was pass at +25.1781 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.231 | test | reboot-b-primary started in lab two-pair-strict |
| -2.895 | switch-a1 log | script,info networka reboot-b-primary start |
| -2.586 | switch-a2 log | script,info networka reboot-b-primary start |
| -2.280 | switch-b1 log | script,info networka reboot-b-primary start |
| -1.950 | switch-b2 log | script,info networka reboot-b-primary start |
| -1.942 | switch log | marker 'networka reboot-b-primary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.112 | state | All four switches run with spanning tree off. pass |
| -0.112 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.112 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.112 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.815 | quiet window | clean |
| 3.815 | step | Baseline |
| 7.815 | step | Reboot switch-b1 |
| 7.875 | reboot | dispatching the reboot to switch-b1 |
| 7.926 | reboot | switch-b1 command returned: accepted |
| 8.264 | host1-to-host2 | 181 pings lost at one ping every 100 ms, traffic stopped for 18.75 to 18.96 s, reply absent at source, request absent at destination |
| 8.305 | host2-to-host1 | 180 pings lost at one ping every 100 ms, traffic stopped for 18.676 to 18.879 s, request absent at destination |
| 24.579 | switch-b2 log | bridge,warning "bridge" peer disconnected |
| 24.587 | switch-b2 log | bridge,warning "bridge" peer link down |
| 33.054 | recovery | full lab state after reboot of switch-b1: pass |
| 49.056 | step | Reboot recovery |
| 52.058 | steps | last step ended |
| 54.040 | state | check after the steps: pass |
| 54.040 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.040 | state | All four switches run with spanning tree off. pass |
| 54.040 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 54.040 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.040 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.040 | streams | measurement ended; captures wait for final replies |
| 54.552 | stopped | captures and streams stopped |
| 54.586 | switch-a1 log | script,info networka reboot-b-primary end |
| 54.631 | switch-a2 log | script,info networka reboot-b-primary end |
| 54.689 | switch-b1 log | script,info networka reboot-b-primary end |
| 54.736 | switch-b2 log | script,info networka reboot-b-primary end |
| 54.747 | switch log | marker 'networka reboot-b-primary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
