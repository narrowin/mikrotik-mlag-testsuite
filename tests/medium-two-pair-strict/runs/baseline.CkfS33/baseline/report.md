# PASS — baseline

Check forwarding in both directions between the hosts across both MLAG pairs, and on the independent bypass. Both host streams cross the inter-pair bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Every host bond member on the switches is synchronized, collecting and distributing. · pass
- The inter-pair bond and the host bond are forwarding bridge ports on all four switches. · pass

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

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -4.136 | test | baseline started in lab medium-two-pair-strict |
| -3.571 | switch-a1 log | script,info networka baseline start |
| -3.024 | switch-a2 log | script,info networka baseline start |
| -2.460 | switch-b1 log | script,info networka baseline start |
| -1.913 | switch-b2 log | script,info networka baseline start |
| -1.910 | switch log | marker 'networka baseline start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.126 | state | check before the steps: pass |
| -0.126 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.126 | state | All four switches run with spanning tree off. pass |
| -0.126 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.126 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.126 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.071 | capture | started at host1:bond0 |
| -0.071 | capture | started at host1:eth3 |
| -0.071 | capture | started at host2:bond0 |
| -0.071 | capture | started at host2:eth3 |
| -0.012 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.009 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.006 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.878 | quiet window | clean |
| 3.878 | step | Steady traffic |
| 8.776 | state | Steady traffic pass |
| 8.776 | steps | last step ended |
| 10.695 | state | check after the steps: pass |
| 10.695 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 10.695 | state | All four switches run with spanning tree off. pass |
| 10.695 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 10.695 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 10.695 | state | Both cables of every host are eligible in its LACP bond. pass |
| 10.695 | streams | measurement ended; captures wait for final replies |
| 11.201 | stopped | captures and streams stopped |
| 11.232 | switch-a1 log | script,info networka baseline end |
| 11.270 | switch-a2 log | script,info networka baseline end |
| 11.313 | switch-b1 log | script,info networka baseline end |
| 11.363 | switch-b2 log | script,info networka baseline end |
| 11.368 | switch log | marker 'networka baseline end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
