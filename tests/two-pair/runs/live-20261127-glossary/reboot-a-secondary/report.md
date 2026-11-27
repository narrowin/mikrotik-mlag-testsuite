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

- Uptime before dispatch was 170 s. The switch reported 17 s at +23.8024 s.
- Full lab state was pass at +25.261 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.085 | test | reboot-a-secondary started in lab two-pair |
| -2.745 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.444 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.158 | switch-b1 log | script,info networka reboot-a-secondary start |
| -1.860 | switch-b2 log | script,info networka reboot-a-secondary start |
| -1.853 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.114 | state | All four switches run with spanning tree off. pass |
| -0.114 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.114 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.779 | quiet window | clean |
| 3.779 | step | Baseline |
| 7.782 | step | Reboot switch-a2 |
| 7.823 | reboot | dispatching the reboot to switch-a2 |
| 7.882 | reboot | switch-a2 command returned: accepted |
| 21.261 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.970 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 24.977 | switch-a1 log | bridge,warning "bridge" peer link down |
| 33.084 | recovery | full lab state after reboot of switch-a2: pass |
| 49.088 | step | Reboot recovery |
| 52.090 | steps | last step ended |
| 54.049 | state | check after the steps: pass |
| 54.049 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 54.049 | state | All four switches run with spanning tree off. pass |
| 54.049 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 54.049 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 54.049 | state | Both cables of every host are eligible in its LACP bond. pass |
| 54.049 | streams | measurement ended; captures wait for final replies |
| 54.556 | stopped | captures and streams stopped |
| 54.589 | switch-a1 log | script,info networka reboot-a-secondary end |
| 54.636 | switch-a2 log | script,info networka reboot-a-secondary end |
| 54.681 | switch-b1 log | script,info networka reboot-a-secondary end |
| 54.722 | switch-b2 log | script,info networka reboot-a-secondary end |
| 54.726 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
