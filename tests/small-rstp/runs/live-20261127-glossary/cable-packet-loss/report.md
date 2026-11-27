# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.9926 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is error.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are unverified.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 109 pings recorded lost, 109 sent in this step (configured interval 100 ms) | 11.2411 to 39.3205 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 0 pings recorded lost, 8 sent in this step (configured interval 100 ms) | unverified | unverified. Sender cadence was invalid in this step. |
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
| -3.212 | test | cable-packet-loss started in lab small-mlag-rstp |
| -2.916 | switch1 log | script,info networka cable-packet-loss start |
| -2.619 | switch2 log | script,info networka cable-packet-loss start |
| -2.612 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both switches show MLAG connected. pass |
| -0.113 | state | Both switches run RSTP. pass |
| -0.113 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.113 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.808 | quiet window | clean |
| 3.808 | step | One-way cable loss |
| 3.810 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.814 | fault | read back the rule for host1:eth2 |
| 3.845 | host1-to-host2 | Diagnostic only: 109 pings recorded lost (configured interval 100 ms), observed stop bounds 11.2411 to 39.3205 s, reply absent at source, request absent at destination |
| 28.816 | step | Cable loss cleared |
| 28.823 | fault | removed the rule for host1:eth2, 92 packets dropped |
| 30.715 | recovery | full lab state after clearing the rule is fail |
| 37.564 | recovery | full lab state after clearing the rule is fail |
| 43.817 | streams | measurement ended; captures wait for final replies |
| 44.320 | stopped | captures and streams stopped |
| 44.321 | run error | Fault recovery exceeded 14.9926 s. |
| 44.356 | switch1 log | script,info networka cable-packet-loss end |
| 44.390 | switch2 log | script,info networka cable-packet-loss end |
| 44.398 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
