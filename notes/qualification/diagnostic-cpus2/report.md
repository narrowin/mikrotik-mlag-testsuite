# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.99 s.
- One-way cable loss: The lab did not recover within the deadline
- Step One-way cable loss is error.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 29 at one ping every 100 ms | 2.91202 to 3.11843 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 0 pings recorded lost, 147 sent in this step (configured interval 100 ms) | error | error. The step stopped before it completed. |
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
| -4.289 | test | cable-packet-loss started in lab failover-candidate |
| -2.727 | switch1 log | script,info networka cable-packet-loss start |
| -1.854 | switch2 log | script,info networka cable-packet-loss start |
| -1.847 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both switches show MLAG connected. pass |
| -0.116 | state | Both switches run with spanning tree off. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.881 | quiet window | clean |
| 3.881 | step | One-way cable loss |
| 3.884 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.888 | fault | read back the rule for host1:eth2 |
| 3.960 | host1-to-host2 | 29 pings lost at one ping every 100 ms, traffic stopped for 2.912 to 3.118 s, request absent at destination |
| 6.790 | switch2 log | interface,info host1 link down |
| 28.889 | step | Cable loss cleared |
| 28.899 | fault | removed the rule for host1:eth2, 49 packets dropped |
| 29.924 | recovery | full lab state after clearing the rule is fail |
| 31.191 | recovery | full lab state after clearing the rule is fail |
| 32.424 | recovery | full lab state after clearing the rule is fail |
| 33.702 | recovery | full lab state after clearing the rule is fail |
| 35.012 | recovery | full lab state after clearing the rule is fail |
| 36.279 | recovery | full lab state after clearing the rule is fail |
| 37.485 | recovery | full lab state after clearing the rule is fail |
| 38.785 | recovery | full lab state after clearing the rule is fail |
| 40.098 | recovery | full lab state after clearing the rule is fail |
| 41.374 | recovery | full lab state after clearing the rule is fail |
| 42.631 | recovery | full lab state after clearing the rule is fail |
| 43.891 | streams | measurement ended; captures wait for final replies |
| 44.019 | switch2 log | interface,info host1 link up |
| 44.403 | stopped | captures and streams stopped |
| 44.403 | run error | Fault recovery exceeded 14.99 s. |
| 44.448 | switch1 log | script,info networka cable-packet-loss end |
| 44.492 | switch2 log | script,info networka cable-packet-loss end |
| 44.496 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
