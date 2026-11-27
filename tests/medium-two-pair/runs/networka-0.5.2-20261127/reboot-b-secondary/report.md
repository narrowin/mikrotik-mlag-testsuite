# PASS — reboot-b-secondary

Reboot switch-b2 in its checked MLAG secondary role of pair B and measure both directions between the hosts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-b2

Reboot switch-b2 · pass

- Uptime before dispatch was 296 s. The switch reported 17 s at +23.8438 s.
- Full lab state was pass at +25.2447 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.263 | test | reboot-b-secondary started in lab medium-two-pair |
| -2.950 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.636 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.238 | switch-b1 log | script,info networka reboot-b-secondary start |
| -1.928 | switch-b2 log | script,info networka reboot-b-secondary start |
| -1.922 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.113 | state | All four switches run with spanning tree off. pass |
| -0.113 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.113 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.739 | quiet window | clean |
| 3.739 | step | Baseline |
| 7.741 | step | Reboot switch-b2 |
| 7.787 | reboot | dispatching the reboot to switch-b2 |
| 7.836 | reboot | switch-b2 command returned: accepted |
| 20.251 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.488 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 24.490 | switch-b1 log | bridge,warning "bridge" peer link down |
| 33.031 | recovery | full lab state after reboot of switch-b2: pass |
| 49.032 | step | Reboot recovery |
| 52.032 | steps | last step ended |
| 54.157 | state | check after the steps: pass |
| 54.157 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.157 | state | All four switches run with spanning tree off. pass |
| 54.157 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 54.157 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.157 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.157 | streams | measurement ended; captures wait for final replies |
| 54.661 | stopped | captures and streams stopped |
| 54.704 | switch-a1 log | script,info networka reboot-b-secondary end |
| 54.751 | switch-a2 log | script,info networka reboot-b-secondary end |
| 54.792 | switch-b1 log | script,info networka reboot-b-secondary end |
| 54.839 | switch-b2 log | script,info networka reboot-b-secondary end |
| 54.844 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
