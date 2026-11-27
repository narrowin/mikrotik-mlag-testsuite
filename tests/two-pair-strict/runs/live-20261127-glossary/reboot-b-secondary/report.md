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

- Uptime before dispatch was 296 s. The switch reported 23 s at +30.8265 s.
- Full lab state was pass at +32.289 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.463 | test | reboot-b-secondary started in lab two-pair-strict |
| -3.103 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.750 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.361 | switch-b1 log | script,info networka reboot-b-secondary start |
| -2.061 | switch-b2 log | script,info networka reboot-b-secondary start |
| -2.054 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.121 | state | check before the steps: pass |
| -0.121 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.121 | state | All four switches run with spanning tree off. pass |
| -0.121 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.121 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.121 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.067 | capture | started at host1:bond0 |
| -0.067 | capture | started at host2:bond0 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.003 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.746 | quiet window | clean |
| 3.746 | step | Baseline |
| 7.748 | step | Reboot switch-b2 |
| 7.845 | reboot | dispatching the reboot to switch-b2 |
| 7.912 | reboot | switch-b2 command returned: accepted |
| 22.563 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 27.004 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 27.014 | switch-b1 log | bridge,warning "bridge" peer link down |
| 40.134 | recovery | full lab state after reboot of switch-b2: pass |
| 56.136 | step | Reboot recovery |
| 59.137 | steps | last step ended |
| 62.923 | state | check after the steps: pass |
| 62.923 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 62.923 | state | All four switches run with spanning tree off. pass |
| 62.923 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 62.923 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 62.923 | state | Both cables of every host are eligible in its LACP bond. pass |
| 62.923 | streams | measurement ended; captures wait for final replies |
| 63.431 | stopped | captures and streams stopped |
| 63.459 | switch-a1 log | script,info networka reboot-b-secondary end |
| 63.506 | switch-a2 log | script,info networka reboot-b-secondary end |
| 63.552 | switch-b1 log | script,info networka reboot-b-secondary end |
| 63.618 | switch-b2 log | script,info networka reboot-b-secondary end |
| 63.636 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
