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

- Uptime before dispatch was 169 s. The switch reported 17 s at +23.8365 s.
- Full lab state was pass at +25.2196 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.119 | test | reboot-a-secondary started in lab two-pair-strict |
| -2.810 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.499 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.203 | switch-b1 log | script,info networka reboot-a-secondary start |
| -1.908 | switch-b2 log | script,info networka reboot-a-secondary start |
| -1.896 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.115 | state | All four switches run with spanning tree off. pass |
| -0.115 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.115 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.756 | quiet window | clean |
| 3.757 | step | Baseline |
| 7.757 | step | Reboot switch-a2 |
| 7.805 | reboot | dispatching the reboot to switch-a2 |
| 7.851 | reboot | switch-a2 command returned: accepted |
| 21.395 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.399 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 24.403 | switch-a1 log | bridge,warning "bridge" peer link down |
| 33.025 | recovery | full lab state after reboot of switch-a2: pass |
| 49.025 | step | Reboot recovery |
| 52.027 | steps | last step ended |
| 53.977 | state | check after the steps: pass |
| 53.977 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.977 | state | All four switches run with spanning tree off. pass |
| 53.977 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 53.977 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.977 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.977 | streams | measurement ended; captures wait for final replies |
| 54.484 | stopped | captures and streams stopped |
| 54.513 | switch-a1 log | script,info networka reboot-a-secondary end |
| 54.560 | switch-a2 log | script,info networka reboot-a-secondary end |
| 54.593 | switch-b1 log | script,info networka reboot-a-secondary end |
| 54.633 | switch-b2 log | script,info networka reboot-a-secondary end |
| 54.638 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
