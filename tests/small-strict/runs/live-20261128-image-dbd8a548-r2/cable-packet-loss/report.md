# PASS — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 24 at one ping every 100 ms | 2.40249 to 2.60664 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | 4 at one ping every 100 ms | 0.311595 to 0.516466 s | pass |
| Cable loss cleared | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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
| -2.838 | test | cable-packet-loss started in lab small-strict |
| -2.552 | switch1 log | script,info networka cable-packet-loss start |
| -2.272 | switch2 log | script,info networka cable-packet-loss start |
| -2.267 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.109 | state | check before the steps: pass |
| -0.109 | state | Both switches show MLAG connected. pass |
| -0.109 | state | Both switches run with spanning tree off. pass |
| -0.109 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.109 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.056 | capture | started at host2:bond0 |
| -0.056 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.803 | quiet window | clean |
| 3.803 | step | One-way cable loss |
| 3.805 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.807 | fault | read back the rule for host1:eth2 |
| 3.842 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.402 to 2.607 s, request absent at destination |
| 6.108 | switch2 log | interface,info host1 link down |
| 28.808 | step | Cable loss cleared |
| 28.816 | fault | removed the rule for host1:eth2, 40 packets dropped |
| 42.631 | switch2 log | interface,info host1 link up |
| 42.716 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.312 to 0.516 s, reply absent at source |
| 43.660 | recovery | full lab state after clearing the rule is pass |
| 48.664 | steps | last step ended |
| 50.724 | state | check after the steps: pass |
| 50.724 | state | Both switches show MLAG connected. pass |
| 50.724 | state | Both switches run with spanning tree off. pass |
| 50.724 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 50.724 | state | Both cables of every host are eligible in its LACP bond. pass |
| 50.724 | streams | measurement ended; captures wait for final replies |
| 51.229 | stopped | captures and streams stopped |
| 51.261 | switch1 log | script,info networka cable-packet-loss end |
| 51.314 | switch2 log | script,info networka cable-packet-loss end |
| 51.316 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
