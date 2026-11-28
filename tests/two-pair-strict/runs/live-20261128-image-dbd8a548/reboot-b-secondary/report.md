# PASS — reboot-b-secondary

Reboot switch-b2 in its checked MLAG secondary role of pair B and measure both directions between the hosts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
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

- Uptime before dispatch was 286 s. The switch reported 16 s at +23.7509 s.
- Full lab state was pass at +25.2457 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.236 | test | reboot-b-secondary started in lab two-pair-strict |
| -2.920 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.610 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.309 | switch-b1 log | script,info networka reboot-b-secondary start |
| -2.004 | switch-b2 log | script,info networka reboot-b-secondary start |
| -1.954 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.114 | state | All four switches run with spanning tree off. pass |
| -0.114 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.114 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.769 | quiet window | clean |
| 3.770 | step | Baseline |
| 7.771 | step | Reboot switch-b2 |
| 7.825 | reboot | dispatching the reboot to switch-b2 |
| 7.911 | reboot | switch-b2 command returned: accepted |
| 20.493 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.927 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 24.931 | switch-b1 log | bridge,warning "bridge" peer link down |
| 33.070 | recovery | full lab state after reboot of switch-b2: pass |
| 49.073 | step | Reboot recovery |
| 52.076 | steps | last step ended |
| 54.027 | state | check after the steps: pass |
| 54.027 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.027 | state | All four switches run with spanning tree off. pass |
| 54.027 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 54.027 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.027 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.027 | streams | measurement ended; captures wait for final replies |
| 54.532 | stopped | captures and streams stopped |
| 54.562 | switch-a1 log | script,info networka reboot-b-secondary end |
| 54.603 | switch-a2 log | script,info networka reboot-b-secondary end |
| 54.634 | switch-b1 log | script,info networka reboot-b-secondary end |
| 54.671 | switch-b2 log | script,info networka reboot-b-secondary end |
| 54.675 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
