# PASS — reboot-a-secondary

Reboot switch-a2 in its checked MLAG secondary role of pair A and measure both directions between the hosts. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
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

## Reboot of switch-a2

Reboot switch-a2 · pass

- Uptime before dispatch was 300 s. The switch reported 16 s at +22.8369 s.
- Full lab state was pass at +24.1587 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.083 | test | reboot-a-secondary started in lab medium-two-pair |
| -2.709 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.424 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.128 | switch-b1 log | script,info networka reboot-a-secondary start |
| -1.846 | switch-b2 log | script,info networka reboot-a-secondary start |
| -1.841 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.119 | state | All four switches run with spanning tree off. pass |
| -0.119 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.119 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.063 | capture | started at host1:bond0 |
| -0.062 | capture | started at host1:eth3 |
| -0.062 | capture | started at host2:bond0 |
| -0.062 | capture | started at host2:eth3 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.006 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.860 | quiet window | clean |
| 3.860 | step | Baseline |
| 7.862 | step | Reboot switch-a2 |
| 7.910 | reboot | dispatching the reboot to switch-a2 |
| 7.955 | reboot | switch-a2 command returned: accepted |
| 24.018 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 24.026 | switch-a1 log | bridge,warning "bridge" peer link down |
| 32.069 | recovery | full lab state after reboot of switch-a2: pass |
| 48.069 | step | Reboot recovery |
| 51.071 | steps | last step ended |
| 53.012 | state | check after the steps: pass |
| 53.012 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.012 | state | All four switches run with spanning tree off. pass |
| 53.012 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 53.012 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.012 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.012 | streams | measurement ended; captures wait for final replies |
| 53.517 | stopped | captures and streams stopped |
| 53.544 | switch-a1 log | script,info networka reboot-a-secondary end |
| 53.592 | switch-a2 log | script,info networka reboot-a-secondary end |
| 53.634 | switch-b1 log | script,info networka reboot-a-secondary end |
| 53.670 | switch-b2 log | script,info networka reboot-a-secondary end |
| 53.674 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
