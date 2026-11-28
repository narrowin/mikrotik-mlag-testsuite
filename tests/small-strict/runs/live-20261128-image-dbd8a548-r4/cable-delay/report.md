# PASS — cable-delay

Delay traffic leaving host1 on its cable to switch2 while measuring delivery on both streams.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Delay on host1 cable | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Delay on host1 cable | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable delay cleared | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Delay on host1 cable** · pass

- host1-to-host2 median ping round trip was 0.685 ms before the delay, 51.852 ms during it, and 0.608 ms after removal.

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.885 | test | cable-delay started in lab small-strict |
| -2.596 | switch1 log | script,info networka cable-delay start |
| -2.308 | switch2 log | script,info networka cable-delay start |
| -2.306 | switch log | marker 'networka cable-delay start' written on switch1, switch2 |
| -0.112 | state | check before the steps: pass |
| -0.112 | state | Both switches show MLAG connected. pass |
| -0.112 | state | Both switches run with spanning tree off. pass |
| -0.112 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.112 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.809 | quiet window | clean |
| 3.810 | step | Delay on host1 cable |
| 3.811 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.814 | fault | read back the rule for host1:eth2 |
| 8.815 | step | Cable delay cleared |
| 8.826 | fault | removed the rule for host1:eth2, 0 packets dropped |
| 9.357 | recovery | full lab state after clearing the rule is pass |
| 12.358 | steps | last step ended |
| 14.521 | state | check after the steps: pass |
| 14.521 | state | Both switches show MLAG connected. pass |
| 14.521 | state | Both switches run with spanning tree off. pass |
| 14.521 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 14.521 | state | Both cables of every host are eligible in its LACP bond. pass |
| 14.521 | streams | measurement ended; captures wait for final replies |
| 15.025 | stopped | captures and streams stopped |
| 15.060 | switch1 log | script,info networka cable-delay end |
| 15.098 | switch2 log | script,info networka cable-delay end |
| 15.103 | switch log | marker 'networka cable-delay end' written on switch1, switch2 |
