# PASS — cable-delay

Delay traffic leaving client1 on its cable to switch2 while measuring delivery on both streams.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Delay on client1 cable | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Delay on client1 cable | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Delay on client1 cable** · pass

- client1-to-client2 median ping round trip was 0.633 ms before the delay, 52.012 ms during it, and 0.553 ms after removal.

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
| -2.302 | test | cable-delay started in lab small-mlag |
| -2.020 | switch1 log | script,info networka cable-delay start |
| -1.741 | switch2 log | script,info networka cable-delay start |
| -1.735 | switch log | marker 'networka cable-delay start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both switches show MLAG connected. pass |
| -0.112 | state | Both switches run with spanning tree off. pass |
| -0.112 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.058 | capture | started at client1:bond0 |
| -0.058 | capture | started at client2:bond0 |
| -0.058 | capture | started at client3:bond0 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.789 | quiet window | clean |
| 3.789 | step | Delay on client1 cable |
| 3.791 | fault | applying the rule for client1:eth2 on client1:eth2 |
| 3.793 | fault | read back the rule for client1:eth2 |
| 8.798 | step | Cable delay cleared |
| 8.804 | fault | removed the rule for client1:eth2, 0 packets dropped |
| 9.769 | recovery | full lab state after clearing the rule is pass |
| 12.772 | steps | last step ended |
| 14.353 | state | check after the steps: pass |
| 14.353 | state | Both switches show MLAG connected. pass |
| 14.353 | state | Both switches run with spanning tree off. pass |
| 14.353 | state | Both cables of every client are eligible in its LACP bond. pass |
| 14.353 | streams | measurement ended; captures wait for final replies |
| 14.860 | stopped | captures and streams stopped |
| 14.894 | switch1 log | script,info networka cable-delay end |
| 14.925 | switch2 log | script,info networka cable-delay end |
| 14.928 | switch log | marker 'networka cable-delay end' written on switch1, switch2 |
