# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.9934 s.
- One-way cable loss: No full recovery state check completed before the run stopped.
- Step One-way cable loss is error.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 28 at one ping every 100 ms | 2.82827 to 3.04047 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 3 pings recorded lost, 146 sent in this step (configured interval 100 ms) | 0.206523 to 0.411556 s (diagnostic) | error. The step stopped before it completed. |
| Cable loss cleared | host2:bond0 → host3:bond0 | 0 s | Diagnostic only: 0 pings recorded lost, 145 sent in this step (configured interval 100 ms) | error | error. The step stopped before it completed. |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.881 | test | cable-packet-loss started in lab small-strict |
| -2.587 | switch1 log | script,info networka cable-packet-loss start |
| -2.294 | switch2 log | script,info networka cable-packet-loss start |
| -2.287 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Both switches show MLAG connected. pass |
| -0.114 | state | Both switches run with spanning tree off. pass |
| -0.114 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.114 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.811 | quiet window | clean |
| 3.811 | step | One-way cable loss |
| 3.813 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.816 | fault | read back the rule for host1:eth2 |
| 3.884 | host1-to-host2 | 28 pings lost at one ping every 100 ms, traffic stopped for 2.828 to 3.04 s, request absent at destination |
| 6.772 | switch2 log | interface,info host1 link down |
| 28.818 | step | Cable loss cleared |
| 28.826 | fault | removed the rule for host1:eth2, 44 packets dropped |
| 43.179 | switch2 log | interface,info host1 link up |
| 43.243 | host1-to-host2 | Diagnostic only: 3 pings recorded lost (configured interval 100 ms), observed outage bounds 0.206523 to 0.411556 s, reply absent at source |
| 43.908 | streams | measurement ended; captures wait for final replies |
| 44.413 | stopped | captures and streams stopped |
| 44.413 | run error | Fault recovery exceeded 14.9934 s. |
| 44.699 | switch1 log | script,info networka cable-packet-loss end |
| 45.020 | switch2 log | script,info networka cable-packet-loss end |
| 45.026 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
