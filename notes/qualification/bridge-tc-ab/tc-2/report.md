# FAIL — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- Step One-way cable loss is fail.
- Step Cable loss cleared is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 361 at one ping every 100 ms | 39.2003 to 39.4108 s | fail |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | 361 at one ping every 100 ms | 39.2003 to 39.4108 s | fail |
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
| -2.899 | test | cable-packet-loss started in lab forwarding-ab-small |
| -2.433 | switch1 log | script,info networka cable-packet-loss start |
| -1.898 | switch2 log | script,info networka cable-packet-loss start |
| -1.891 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both switches show MLAG connected. pass |
| -0.119 | state | Both switches run with spanning tree off. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.998 | quiet window | clean |
| 3.998 | step | One-way cable loss |
| 4.003 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 4.007 | fault | read back the rule for host1:eth2 |
| 4.042 | host1-to-host2 | 361 pings lost at one ping every 100 ms, traffic stopped for 39.2 to 39.411 s, late reply, reply absent at destination, reply absent at source, request absent at destination |
| 29.010 | step | Cable loss cleared |
| 29.019 | fault | removed the rule for host1:eth2, 83 packets dropped |
| 30.084 | recovery | full lab state after clearing the rule is fail |
| 31.382 | recovery | full lab state after clearing the rule is fail |
| 32.651 | recovery | full lab state after clearing the rule is fail |
| 33.919 | recovery | full lab state after clearing the rule is fail |
| 35.168 | recovery | full lab state after clearing the rule is fail |
| 36.413 | recovery | full lab state after clearing the rule is fail |
| 37.685 | recovery | full lab state after clearing the rule is fail |
| 38.922 | recovery | full lab state after clearing the rule is fail |
| 40.215 | recovery | full lab state after clearing the rule is fail |
| 41.470 | recovery | full lab state after clearing the rule is fail |
| 42.725 | recovery | full lab state after clearing the rule is fail |
| 44.004 | recovery | full lab state after clearing the rule is pass |
| 49.006 | steps | last step ended |
| 50.644 | state | check after the steps: pass |
| 50.644 | state | Both switches show MLAG connected. pass |
| 50.644 | state | Both switches run with spanning tree off. pass |
| 50.644 | state | Both cables of every host are eligible in its LACP bond. pass |
| 50.644 | streams | measurement ended; captures wait for final replies |
| 51.155 | stopped | captures and streams stopped |
| 51.186 | switch1 log | script,info networka cable-packet-loss end |
| 51.232 | switch2 log | script,info networka cable-packet-loss end |
| 51.238 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
