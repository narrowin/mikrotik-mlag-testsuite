# PASS — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 30 at one ping every 100 ms | 3.03015 to 3.23539 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | 3 at one ping every 100 ms | 0.209338 to 0.415435 s | pass |
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
| -2.516 | test | cable-packet-loss started in lab small-mlag |
| -2.182 | switch1 log | script,info networka cable-packet-loss start |
| -1.834 | switch2 log | script,info networka cable-packet-loss start |
| -1.831 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.117 | state | check before the steps: pass |
| -0.117 | state | Both switches show MLAG connected. pass |
| -0.117 | state | Both switches run with spanning tree off. pass |
| -0.117 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.909 | quiet window | clean |
| 3.910 | step | One-way cable loss |
| 3.912 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.916 | fault | read back the rule for host1:eth2 |
| 3.956 | host1-to-host2 | 30 pings lost at one ping every 100 ms, traffic stopped for 3.03 to 3.235 s, request absent at destination |
| 6.734 | switch2 log | interface,info host1 link down |
| 28.917 | step | Cable loss cleared |
| 28.924 | fault | removed the rule for host1:eth2, 48 packets dropped |
| 43.035 | switch2 log | interface,info host1 link up |
| 43.105 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.415 s, reply absent at source |
| 43.826 | recovery | full lab state after clearing the rule is pass |
| 48.829 | steps | last step ended |
| 50.473 | state | check after the steps: pass |
| 50.473 | state | Both switches show MLAG connected. pass |
| 50.473 | state | Both switches run with spanning tree off. pass |
| 50.473 | state | Both cables of every host are eligible in its LACP bond. pass |
| 50.473 | streams | measurement ended; captures wait for final replies |
| 50.976 | stopped | captures and streams stopped |
| 51.017 | switch1 log | script,info networka cable-packet-loss end |
| 51.068 | switch2 log | script,info networka cable-packet-loss end |
| 51.071 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
