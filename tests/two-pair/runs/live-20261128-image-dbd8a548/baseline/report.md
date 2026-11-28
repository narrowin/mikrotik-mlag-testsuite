# PASS — baseline

Check forwarding in both directions between the hosts across both MLAG pairs. Both host streams cross the inter-pair bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Every host bond member on the switches is synchronized, collecting and distributing. · pass
- The inter-pair bond and the host bond are forwarding bridge ports on all four switches. · pass

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -4.664 | test | baseline started in lab two-pair |
| -3.995 | switch-a1 log | script,info networka baseline start |
| -3.371 | switch-a2 log | script,info networka baseline start |
| -2.778 | switch-b1 log | script,info networka baseline start |
| -2.162 | switch-b2 log | script,info networka baseline start |
| -2.160 | switch log | marker 'networka baseline start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.112 | state | All four switches run with spanning tree off. pass |
| -0.112 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.112 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.112 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.759 | quiet window | clean |
| 3.760 | step | Steady traffic |
| 8.735 | state | Steady traffic pass |
| 8.735 | steps | last step ended |
| 10.687 | state | check after the steps: pass |
| 10.687 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 10.687 | state | All four switches run with spanning tree off. pass |
| 10.687 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 10.687 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 10.687 | state | Both cables of every host are eligible in its LACP bond. pass |
| 10.687 | streams | measurement ended; captures wait for final replies |
| 11.191 | stopped | captures and streams stopped |
| 11.227 | switch-a1 log | script,info networka baseline end |
| 11.274 | switch-a2 log | script,info networka baseline end |
| 11.314 | switch-b1 log | script,info networka baseline end |
| 11.358 | switch-b2 log | script,info networka baseline end |
| 11.361 | switch log | marker 'networka baseline end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
