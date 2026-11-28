# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- Step One-way cable loss is error.
- Step Cable loss cleared is error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 218 pings recorded lost, 218 sent in this step (configured interval 100 ms) | 22.6356 to 39.3302 s (diagnostic) | error. Sender cadence was invalid in this step. |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 0 pings recorded lost, 53 sent in this step (configured interval 100 ms) | error | error. Sender cadence was invalid in this step. |
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
| -2.313 | test | cable-packet-loss started in lab small-mlag |
| -2.026 | switch1 log | script,info networka cable-packet-loss start |
| -1.748 | switch2 log | script,info networka cable-packet-loss start |
| -1.739 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | Both switches show MLAG connected. pass |
| -0.110 | state | Both switches run with spanning tree off. pass |
| -0.110 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.056 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.813 | quiet window | clean |
| 3.813 | step | One-way cable loss |
| 3.815 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.818 | fault | read back the rule for host1:eth2 |
| 3.861 | host1-to-host2 | Diagnostic only: 218 pings recorded lost (configured interval 100 ms), observed outage bounds 22.6356 to 39.3302 s, reply absent at source, request absent at destination |
| 28.821 | step | Cable loss cleared |
| 28.831 | fault | removed the rule for host1:eth2, 95 packets dropped |
| 43.181 | recovery | full lab state after clearing the rule is pass |
| 48.186 | steps | last step ended |
| 49.775 | state | check after the steps: pass |
| 49.775 | state | Both switches show MLAG connected. pass |
| 49.775 | state | Both switches run with spanning tree off. pass |
| 49.775 | state | Both cables of every host are eligible in its LACP bond. pass |
| 49.776 | streams | measurement ended; captures wait for final replies |
| 50.283 | stopped | captures and streams stopped |
| 50.315 | switch1 log | script,info networka cable-packet-loss end |
| 50.363 | switch2 log | script,info networka cable-packet-loss end |
| 50.367 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
