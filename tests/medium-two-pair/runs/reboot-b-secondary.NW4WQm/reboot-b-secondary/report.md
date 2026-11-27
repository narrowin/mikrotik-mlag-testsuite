# PASS — reboot-b-secondary

Reboot switch-b2 in its checked MLAG secondary role of pair B and measure both directions between the hosts. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
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

## Reboot of switch-b2

Reboot switch-b2 · pass

- Uptime before dispatch was 419 s. The switch reported 15 s at +22.8859 s.
- Full lab state was pass at +24.2296 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -4.253 | test | reboot-b-secondary started in lab medium-two-pair |
| -3.386 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.831 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.413 | switch-b1 log | script,info networka reboot-b-secondary start |
| -2.116 | switch-b2 log | script,info networka reboot-b-secondary start |
| -2.112 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.174 | state | check before the steps: pass |
| -0.174 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.174 | state | All four switches run with spanning tree off. pass |
| -0.174 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.174 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.174 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.073 | capture | started at host1:bond0 |
| -0.064 | capture | started at host1:eth3 |
| -0.064 | capture | started at host2:bond0 |
| -0.063 | capture | started at host2:eth3 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.006 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.908 | quiet window | clean |
| 3.909 | step | Baseline |
| 7.912 | step | Reboot switch-b2 |
| 7.959 | reboot | dispatching the reboot to switch-b2 |
| 8.018 | reboot | switch-b2 command returned: accepted |
| 18.498 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.495 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.502 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 24.509 | switch-b1 log | bridge,warning "bridge" peer link down |
| 32.188 | recovery | full lab state after reboot of switch-b2: pass |
| 48.191 | step | Reboot recovery |
| 51.193 | steps | last step ended |
| 53.142 | state | check after the steps: pass |
| 53.142 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.142 | state | All four switches run with spanning tree off. pass |
| 53.142 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 53.142 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.142 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.142 | streams | measurement ended; captures wait for final replies |
| 53.652 | stopped | captures and streams stopped |
| 53.700 | switch-a1 log | script,info networka reboot-b-secondary end |
| 53.747 | switch-a2 log | script,info networka reboot-b-secondary end |
| 53.801 | switch-b1 log | script,info networka reboot-b-secondary end |
| 53.858 | switch-b2 log | script,info networka reboot-b-secondary end |
| 53.861 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
