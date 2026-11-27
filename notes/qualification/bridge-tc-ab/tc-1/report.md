# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.992 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is fail.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 380 at one ping every 100 ms | 39.56 to 39.7683 s | fail |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 380 pings recorded lost, 144 sent in this step (configured interval 100 ms) | 39.56 to 39.7683 s (diagnostic) | error. The step stopped before it completed. |
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
| -3.424 | test | cable-packet-loss started in lab forwarding-ab-small |
| -2.618 | switch1 log | script,info networka cable-packet-loss start |
| -1.852 | switch2 log | script,info networka cable-packet-loss start |
| -1.847 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run with spanning tree off. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.003 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.919 | quiet window | clean |
| 3.919 | step | One-way cable loss |
| 3.921 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.924 | host1-to-host2 | Diagnostic only: 380 pings recorded lost (configured interval 100 ms), observed outage bounds 39.56 to 39.7683 s, late reply, reply absent at destination, request absent at destination |
| 3.925 | fault | read back the rule for host1:eth2 |
| 28.928 | step | Cable loss cleared |
| 28.939 | fault | removed the rule for host1:eth2, 83 packets dropped |
| 30.002 | recovery | full lab state after clearing the rule is fail |
| 31.275 | recovery | full lab state after clearing the rule is fail |
| 32.523 | recovery | full lab state after clearing the rule is fail |
| 33.769 | recovery | full lab state after clearing the rule is fail |
| 35.014 | recovery | full lab state after clearing the rule is fail |
| 36.245 | recovery | full lab state after clearing the rule is fail |
| 37.490 | recovery | full lab state after clearing the rule is fail |
| 38.708 | recovery | full lab state after clearing the rule is fail |
| 39.945 | recovery | full lab state after clearing the rule is fail |
| 41.239 | recovery | full lab state after clearing the rule is fail |
| 42.473 | recovery | full lab state after clearing the rule is fail |
| 43.684 | recovery | full lab state after clearing the rule is fail |
| 43.933 | streams | measurement ended; captures wait for final replies |
| 44.444 | stopped | captures and streams stopped |
| 44.444 | run error | Fault recovery exceeded 14.992 s. |
| 44.478 | switch1 log | script,info networka cable-packet-loss end |
| 44.527 | switch2 log | script,info networka cable-packet-loss end |
| 44.530 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
