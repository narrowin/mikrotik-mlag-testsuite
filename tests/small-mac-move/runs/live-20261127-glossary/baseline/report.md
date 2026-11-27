# PASS — baseline

Check forwarding in both directions on the host bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both switch host bonds contain their wired member and use it for LACP forwarding. · pass
- Both switch host bridge ports are forwarding and both peer ports have carrier. · pass

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
| -2.625 | test | baseline started in lab small-mlag-mac-move |
| -2.018 | switch1 log | script,info networka baseline start |
| -1.434 | switch2 log | script,info networka baseline start |
| -1.429 | switch log | marker 'networka baseline start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.114 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.762 | quiet window | clean |
| 3.762 | step | Steady traffic |
| 8.536 | state | Steady traffic pass |
| 8.536 | steps | last step ended |
| 9.946 | state | check after the steps: pass |
| 9.946 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 9.946 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 9.947 | streams | measurement ended; captures wait for final replies |
| 10.450 | stopped | captures and streams stopped |
| 10.485 | switch1 log | script,info networka baseline end |
| 10.532 | switch2 log | script,info networka baseline end |
| 10.537 | switch log | marker 'networka baseline end' written on switch1, switch2 |
