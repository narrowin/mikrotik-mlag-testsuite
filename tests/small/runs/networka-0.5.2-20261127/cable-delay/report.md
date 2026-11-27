# FAIL — cable-delay

Delay traffic leaving client1 on its cable to switch2 while measuring delivery on both streams.

- Step Delay on client1 cable is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Delay on client1 cable | client1:bond0 → client2:bond0 | 0 s | 1 at one ping every 100 ms | 0 to 0.204889 s | fail |
| Delay on client1 cable | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Delay on client1 cable** · pass

- client1-to-client2 median ping round trip was 0.641 ms before the delay, 51.757 ms during it, and 0.645 ms after removal.

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
| -2.407 | test | cable-delay started in lab small-mlag |
| -2.110 | switch1 log | script,info networka cable-delay start |
| -1.812 | switch2 log | script,info networka cable-delay start |
| -1.801 | switch log | marker 'networka cable-delay start' written on switch1, switch2 |
| -0.123 | state | check before the steps: pass |
| -0.123 | state | Both switches show MLAG connected. pass |
| -0.123 | state | Both switches run with spanning tree off. pass |
| -0.123 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.066 | capture | started at client1:bond0 |
| -0.065 | capture | started at client2:bond0 |
| -0.065 | capture | started at client3:bond0 |
| -0.006 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.920 | quiet window | clean |
| 3.921 | step | Delay on client1 cable |
| 3.925 | fault | applying the rule for client1:eth2 on client1:eth2 |
| 3.930 | fault | read back the rule for client1:eth2 |
| 8.927 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 8.930 | step | Cable delay cleared |
| 8.937 | fault | removed the rule for client1:eth2, 0 packets dropped |
| 9.921 | recovery | full lab state after clearing the rule is pass |
| 12.921 | steps | last step ended |
| 14.540 | state | check after the steps: pass |
| 14.540 | state | Both switches show MLAG connected. pass |
| 14.540 | state | Both switches run with spanning tree off. pass |
| 14.540 | state | Both cables of every client are eligible in its LACP bond. pass |
| 14.540 | streams | measurement ended; captures wait for final replies |
| 15.044 | stopped | captures and streams stopped |
| 15.073 | switch1 log | script,info networka cable-delay end |
| 15.120 | switch2 log | script,info networka cable-delay end |
| 15.123 | switch log | marker 'networka cable-delay end' written on switch1, switch2 |
