# ERROR — cable-packet-loss

Check failover when every frame leaving client1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.9945 s.
- Not valid: client1-to-client2 sent a ping at least every 450 ms.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is error.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are unverified.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | client1:bond0 → client2:bond0 | 4 s | Diagnostic only: 220 pings recorded lost, 220 sent in this step (configured interval 100 ms) | at least 22.8157 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| One-way cable loss | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | client1:bond0 → client2:bond0 | 4 s | Diagnostic only: 0 pings recorded lost, 0 sent in this step (configured interval 100 ms) | unverified | unverified. No sender pings were captured in this step. |
| Cable loss cleared | client2:bond0 → client3:bond0 | 0 s | Diagnostic only: 0 pings recorded lost, 143 sent in this step (configured interval 100 ms) | unverified | unverified. The step stopped before it completed. |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.945 | test | cable-packet-loss started in lab small-mlag-rstp |
| -1.910 | switch1 log | script,info networka cable-packet-loss start |
| -1.880 | switch2 log | script,info networka cable-packet-loss start |
| -1.873 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | Both switches show MLAG connected. pass |
| -0.110 | state | Both switches run RSTP. pass |
| -0.110 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.110 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.110 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.056 | capture | started at client1:bond0 |
| -0.056 | capture | started at client2:bond0 |
| -0.056 | capture | started at client3:bond0 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.807 | quiet window | clean |
| 3.807 | step | One-way cable loss |
| 3.810 | fault | applying the rule for client1:eth2 on client1:eth2 |
| 3.814 | fault | read back the rule for client1:eth2 |
| 3.869 | client1-to-client2 | Diagnostic only: 220 pings recorded lost (configured interval 100 ms), observed stop bounds at least 22.8157 s, reply absent at source, request absent at destination |
| 28.814 | step | Cable loss cleared |
| 28.820 | fault | removed the rule for client1:eth2, 104 packets dropped |
| 30.656 | recovery | full lab state after clearing the rule is fail |
| 37.505 | recovery | full lab state after clearing the rule is fail |
| 43.817 | streams | measurement ended; captures wait for final replies |
| 44.429 | stopped | captures and streams stopped |
| 44.429 | run error | Fault recovery exceeded 14.9945 s. |
| 44.478 | switch1 log | script,info networka cable-packet-loss end |
| 44.521 | switch2 log | script,info networka cable-packet-loss end |
| 44.526 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
