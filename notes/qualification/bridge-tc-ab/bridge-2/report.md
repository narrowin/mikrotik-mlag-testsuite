# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.9922 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is fail.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 290 at one ping every 100 ms | at least 31.7841 s | fail |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 290 pings recorded lost, 66 sent in this step (configured interval 100 ms) | at least 31.7841 s (diagnostic) | error. Sender cadence was invalid in this step. |
| Cable loss cleared | host2:bond0 → host3:bond0 | 0 s | Diagnostic only: 0 pings recorded lost, 144 sent in this step (configured interval 100 ms) | error | error. The step stopped before it completed. |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.571 | test | cable-packet-loss started in lab forwarding-ab-small |
| -2.201 | switch1 log | script,info networka cable-packet-loss start |
| -1.834 | switch2 log | script,info networka cable-packet-loss start |
| -1.825 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both switches show MLAG connected. pass |
| -0.118 | state | Both switches run with spanning tree off. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.823 | quiet window | clean |
| 3.823 | step | One-way cable loss |
| 3.826 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.829 | fault | read back the rule for host1:eth2 |
| 3.880 | host1-to-host2 | Diagnostic only: 290 pings recorded lost (configured interval 100 ms), observed outage bounds at least 31.7841 s, reply absent at destination, reply absent at source, request absent at destination |
| 28.831 | step | Cable loss cleared |
| 28.839 | fault | removed the rule for host1:eth2, 89 packets dropped |
| 29.848 | recovery | full lab state after clearing the rule is fail |
| 31.079 | recovery | full lab state after clearing the rule is fail |
| 32.325 | recovery | full lab state after clearing the rule is fail |
| 33.549 | recovery | full lab state after clearing the rule is fail |
| 34.805 | recovery | full lab state after clearing the rule is fail |
| 36.067 | recovery | full lab state after clearing the rule is fail |
| 37.302 | recovery | full lab state after clearing the rule is fail |
| 38.526 | recovery | full lab state after clearing the rule is fail |
| 39.784 | recovery | full lab state after clearing the rule is fail |
| 41.026 | recovery | full lab state after clearing the rule is fail |
| 42.231 | recovery | full lab state after clearing the rule is fail |
| 43.496 | recovery | full lab state after clearing the rule is fail |
| 43.832 | streams | measurement ended; captures wait for final replies |
| 44.356 | stopped | captures and streams stopped |
| 44.357 | run error | Fault recovery exceeded 14.9922 s. |
| 44.402 | switch1 log | script,info networka cable-packet-loss end |
| 44.443 | switch2 log | script,info networka cable-packet-loss end |
| 44.449 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
