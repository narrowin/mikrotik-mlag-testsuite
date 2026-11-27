# FAIL — cable-delay

Delay traffic leaving client1 on its cable to switch2 while measuring delivery on both streams.

- Step Delay on client1 cable is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Delay on client1 cable | client1:bond0 → client2:bond0 | 0 s | 1 at one ping every 100 ms | 0 to 0.209204 s | fail |
| Delay on client1 cable | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Delay on client1 cable** · pass

- client1-to-client2 median ping round trip was 0.625 ms before the delay, 51.342 ms during it, and 0.599 ms after removal.

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.263 | test | cable-delay started in lab small-mlag-rstp |
| -2.958 | switch1 log | script,info networka cable-delay start |
| -2.661 | switch2 log | script,info networka cable-delay start |
| -2.657 | switch log | marker 'networka cable-delay start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both switches show MLAG connected. pass |
| -0.112 | state | Both switches run RSTP. pass |
| -0.112 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.112 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.112 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.059 | capture | started at client1:bond0 |
| -0.059 | capture | started at client2:bond0 |
| -0.059 | capture | started at client3:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.002 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.835 | quiet window | clean |
| 3.836 | step | Delay on client1 cable |
| 3.840 | fault | applying the rule for client1:eth2 on client1:eth2 |
| 3.844 | fault | read back the rule for client1:eth2 |
| 8.832 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 8.846 | step | Cable delay cleared |
| 8.854 | fault | removed the rule for client1:eth2, 0 packets dropped |
| 10.699 | recovery | full lab state after clearing the rule is pass |
| 13.700 | steps | last step ended |
| 16.148 | state | check after the steps: pass |
| 16.148 | state | Both switches show MLAG connected. pass |
| 16.148 | state | Both switches run RSTP. pass |
| 16.148 | state | Both MLAG peers are the RSTP root bridge. pass |
| 16.148 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| 16.148 | state | Both cables of every client are eligible in its LACP bond. pass |
| 16.148 | streams | measurement ended; captures wait for final replies |
| 16.662 | stopped | captures and streams stopped |
| 16.713 | switch1 log | script,info networka cable-delay end |
| 16.747 | switch2 log | script,info networka cable-delay end |
| 16.753 | switch log | marker 'networka cable-delay end' written on switch1, switch2 |
