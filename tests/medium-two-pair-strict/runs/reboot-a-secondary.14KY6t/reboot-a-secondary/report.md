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

- Uptime before dispatch was 183 s. The switch reported 16 s at +22.8721 s.
- Full lab state was pass at +24.2302 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.024 | test | reboot-a-secondary started in lab medium-two-pair-strict |
| -2.730 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.444 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.170 | switch-b1 log | script,info networka reboot-a-secondary start |
| -1.890 | switch-b2 log | script,info networka reboot-a-secondary start |
| -1.878 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run with spanning tree off. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.062 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.881 | quiet window | clean |
| 3.881 | step | Baseline |
| 7.882 | step | Reboot switch-a2 |
| 7.927 | reboot | dispatching the reboot to switch-a2 |
| 7.969 | reboot | switch-a2 command returned: accepted |
| 21.048 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.060 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 24.064 | switch-a1 log | bridge,warning "bridge" peer link down |
| 32.157 | recovery | full lab state after reboot of switch-a2: pass |
| 48.159 | step | Reboot recovery |
| 51.163 | steps | last step ended |
| 53.087 | state | check after the steps: pass |
| 53.087 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 53.087 | state | All four switches run with spanning tree off. pass |
| 53.087 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 53.087 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 53.087 | state | Both cables of every host are eligible in its LACP bond. pass |
| 53.088 | streams | measurement ended; captures wait for final replies |
| 53.592 | stopped | captures and streams stopped |
| 53.629 | switch-a1 log | script,info networka reboot-a-secondary end |
| 53.666 | switch-a2 log | script,info networka reboot-a-secondary end |
| 53.716 | switch-b1 log | script,info networka reboot-a-secondary end |
| 53.767 | switch-b2 log | script,info networka reboot-a-secondary end |
| 53.772 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
