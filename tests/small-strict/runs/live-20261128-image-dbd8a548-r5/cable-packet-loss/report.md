# PASS — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 25 at one ping every 100 ms | 2.50362 to 2.71645 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | 3 at one ping every 100 ms | 0.207355 to 0.415415 s | pass |
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
| -2.775 | test | cable-packet-loss started in lab small-strict |
| -2.495 | switch1 log | script,info networka cable-packet-loss start |
| -2.214 | switch2 log | script,info networka cable-packet-loss start |
| -2.211 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both switches show MLAG connected. pass |
| -0.111 | state | Both switches run with spanning tree off. pass |
| -0.111 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.801 | quiet window | clean |
| 3.801 | step | One-way cable loss |
| 3.803 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.806 | fault | read back the rule for host1:eth2 |
| 3.854 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.504 to 2.716 s, request absent at destination |
| 6.284 | switch2 log | interface,info host1 link down |
| 28.808 | step | Cable loss cleared |
| 28.815 | fault | removed the rule for host1:eth2, 41 packets dropped |
| 42.692 | switch2 log | interface,info host1 link up |
| 42.741 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.415 s, reply absent at source |
| 43.573 | recovery | full lab state after clearing the rule is pass |
| 48.574 | steps | last step ended |
| 50.647 | state | check after the steps: pass |
| 50.647 | state | Both switches show MLAG connected. pass |
| 50.647 | state | Both switches run with spanning tree off. pass |
| 50.647 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 50.647 | state | Both cables of every host are eligible in its LACP bond. pass |
| 50.647 | streams | measurement ended; captures wait for final replies |
| 51.151 | stopped | captures and streams stopped |
| 51.190 | switch1 log | script,info networka cable-packet-loss end |
| 51.229 | switch2 log | script,info networka cable-packet-loss end |
| 51.232 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
