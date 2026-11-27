# ERROR — cable-packet-loss

Check failover when every frame leaving client1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.995 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is fail.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are unverified.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | client1:bond0 → client2:bond0 | 4 s | 375 at one ping every 100 ms | 38.9746 to 39.185 s | fail |
| One-way cable loss | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | client1:bond0 → client2:bond0 | 4 s | Diagnostic only: 375 pings recorded lost, 144 sent in this step (configured interval 100 ms) | 38.9746 to 39.185 s (diagnostic) | unverified. The step stopped before it completed. |
| Cable loss cleared | client2:bond0 → client3:bond0 | 0 s | Diagnostic only: 0 pings recorded lost, 144 sent in this step (configured interval 100 ms) | unverified | unverified. The step stopped before it completed. |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.335 | test | cable-packet-loss started in lab small-mlag |
| -2.018 | switch1 log | script,info networka cable-packet-loss start |
| -1.727 | switch2 log | script,info networka cable-packet-loss start |
| -1.722 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run with spanning tree off. pass |
| -0.114 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.059 | capture | started at client1:bond0 |
| -0.059 | capture | started at client2:bond0 |
| -0.059 | capture | started at client3:bond0 |
| -0.005 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.803 | quiet window | clean |
| 3.804 | step | One-way cable loss |
| 3.806 | fault | applying the rule for client1:eth2 on client1:eth2 |
| 3.808 | fault | read back the rule for client1:eth2 |
| 3.860 | client1-to-client2 | Diagnostic only: 375 pings recorded lost (configured interval 100 ms), observed stop bounds 38.9746 to 39.185 s, reply absent at destination, reply absent at source, request absent at destination |
| 28.810 | step | Cable loss cleared |
| 28.816 | fault | removed the rule for client1:eth2, 101 packets dropped |
| 29.799 | recovery | full lab state after clearing the rule is fail |
| 35.809 | recovery | full lab state after clearing the rule is fail |
| 41.781 | recovery | full lab state after clearing the rule is fail |
| 43.812 | streams | measurement ended; captures wait for final replies |
| 44.317 | stopped | captures and streams stopped |
| 44.318 | run error | Fault recovery exceeded 14.995 s. |
| 44.346 | switch1 log | script,info networka cable-packet-loss end |
| 44.379 | switch2 log | script,info networka cable-packet-loss end |
| 44.387 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
