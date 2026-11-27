# PASS — reboot-a-secondary

Reboot switch-a2 in its checked MLAG secondary role of pair A and measure both directions between the hosts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-a2

Reboot switch-a2 · pass

- Uptime before dispatch was 170 s. The switch reported 17 s at +24.9962 s.
- Full lab state was pass at +26.4131 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.603 | test | reboot-a-secondary started in lab medium-two-pair-strict |
| -3.281 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.805 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.388 | switch-b1 log | script,info networka reboot-a-secondary start |
| -2.061 | switch-b2 log | script,info networka reboot-a-secondary start |
| -2.057 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.111 | state | All four switches run with spanning tree off. pass |
| -0.111 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.111 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.790 | quiet window | clean |
| 3.791 | step | Baseline |
| 7.794 | step | Reboot switch-a2 |
| 7.931 | reboot | dispatching the reboot to switch-a2 |
| 7.998 | reboot | switch-a2 command returned: accepted |
| 20.155 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.165 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.778 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 25.785 | switch-a1 log | bridge,warning "bridge" peer link down |
| 34.344 | recovery | full lab state after reboot of switch-a2: pass |
| 50.345 | step | Reboot recovery |
| 53.347 | steps | last step ended |
| 55.357 | state | check after the steps: pass |
| 55.357 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 55.357 | state | All four switches run with spanning tree off. pass |
| 55.357 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 55.357 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 55.357 | state | Both cables of every host are eligible in its LACP bond. pass |
| 55.357 | streams | measurement ended; captures wait for final replies |
| 55.862 | stopped | captures and streams stopped |
| 55.916 | switch-a1 log | script,info networka reboot-a-secondary end |
| 55.955 | switch-a2 log | script,info networka reboot-a-secondary end |
| 55.999 | switch-b1 log | script,info networka reboot-a-secondary end |
| 56.050 | switch-b2 log | script,info networka reboot-a-secondary end |
| 56.055 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
