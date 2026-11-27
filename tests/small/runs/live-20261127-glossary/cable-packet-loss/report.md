# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.993 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is fail.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are unverified.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 244 at one ping every 100 ms | 25.3013 to 40.0428 s | fail |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 244 pings recorded lost, 9 sent in this step (configured interval 100 ms) | 25.3013 to 40.0428 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Cable loss cleared | host2:bond0 → host3:bond0 | 0 s | Diagnostic only: 0 pings recorded lost, 144 sent in this step (configured interval 100 ms) | unverified | unverified. The step stopped before it completed. |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.396 | test | cable-packet-loss started in lab small-mlag |
| -2.093 | switch1 log | script,info networka cable-packet-loss start |
| -1.801 | switch2 log | script,info networka cable-packet-loss start |
| -1.797 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Both switches show MLAG connected. pass |
| -0.111 | state | Both switches run with spanning tree off. pass |
| -0.111 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.815 | quiet window | clean |
| 3.815 | step | One-way cable loss |
| 3.817 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.820 | fault | read back the rule for host1:eth2 |
| 3.857 | host1-to-host2 | Diagnostic only: 244 pings recorded lost (configured interval 100 ms), observed stop bounds 25.3013 to 40.0428 s, reply absent at destination, reply absent at source, request absent at destination |
| 28.822 | step | Cable loss cleared |
| 28.829 | fault | removed the rule for host1:eth2, 106 packets dropped |
| 29.842 | recovery | full lab state after clearing the rule is fail |
| 35.844 | recovery | full lab state after clearing the rule is fail |
| 41.863 | recovery | full lab state after clearing the rule is fail |
| 43.824 | streams | measurement ended; captures wait for final replies |
| 44.328 | stopped | captures and streams stopped |
| 44.328 | run error | Fault recovery exceeded 14.993 s. |
| 44.355 | switch1 log | script,info networka cable-packet-loss end |
| 44.384 | switch2 log | script,info networka cable-packet-loss end |
| 44.390 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
