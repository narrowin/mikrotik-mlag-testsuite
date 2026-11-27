# PASS — baseline

Check forwarding in both directions on the client bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both switch client bonds contain their wired member and use it for LACP forwarding. · pass
- Both switch client bridge ports are forwarding and both peer ports have carrier. · pass

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.659 | test | baseline started in lab small-mlag-mobile |
| -2.067 | switch1 log | script,info networka baseline start |
| -1.487 | switch2 log | script,info networka baseline start |
| -1.481 | switch log | marker 'networka baseline start' written on switch1, switch2 |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.120 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.060 | capture | started at client1:bond0 |
| -0.059 | capture | started at client2:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client2-to-client1 | started from client2:bond0 to client1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.740 | quiet window | clean |
| 3.740 | step | Steady traffic |
| 8.598 | state | Steady traffic pass |
| 8.598 | steps | last step ended |
| 10.042 | state | check after the steps: pass |
| 10.042 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 10.042 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 10.042 | streams | measurement ended; captures wait for final replies |
| 10.548 | stopped | captures and streams stopped |
| 10.599 | switch1 log | script,info networka baseline end |
| 10.641 | switch2 log | script,info networka baseline end |
| 10.643 | switch log | marker 'networka baseline end' written on switch1, switch2 |
