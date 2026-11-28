# ERROR — cable-packet-loss

Check failover when every frame leaving host1 on its cable to switch2 is lost. The link keeps carrier and frames in the reverse direction are left unfiltered.

- The run stopped: Fault recovery exceeded 14.9924 s.
- One-way cable loss: No full recovery state check completed before the run stopped.
- Step One-way cable loss is error.
- Step Cable loss cleared is error.

Traffic is shown through the sender cutoff after the run stopped. The final lab state and closing window are error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way cable loss | host1:bond0 → host2:bond0 | 4 s | 32 at one ping every 100 ms | 3.2305 to 3.44109 s | pass |
| One-way cable loss | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable loss cleared | host1:bond0 → host2:bond0 | 4 s | Diagnostic only: 4 pings recorded lost, 145 sent in this step (configured interval 100 ms) | 0.314189 to 0.519099 s (diagnostic) | error. The step stopped before it completed. |
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
| -2.929 | test | cable-packet-loss started in lab small-strict |
| -2.642 | switch1 log | script,info networka cable-packet-loss start |
| -2.358 | switch2 log | script,info networka cable-packet-loss start |
| -2.347 | switch log | marker 'networka cable-packet-loss start' written on switch1, switch2 |
| -0.110 | state | check before the steps: pass |
| -0.110 | state | Both switches show MLAG connected. pass |
| -0.110 | state | Both switches run with spanning tree off. pass |
| -0.110 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.110 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.057 | capture | started at host1:bond0 |
| -0.057 | capture | started at host2:bond0 |
| -0.057 | capture | started at host3:bond0 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.826 | quiet window | clean |
| 3.826 | step | One-way cable loss |
| 3.828 | fault | applying the rule for host1:eth2 on host1:eth2 |
| 3.831 | fault | read back the rule for host1:eth2 |
| 3.847 | host1-to-host2 | 32 pings lost at one ping every 100 ms, traffic stopped for 3.23 to 3.441 s, request absent at destination |
| 6.822 | switch2 log | interface,info host1 link down |
| 28.832 | step | Cable loss cleared |
| 28.840 | fault | removed the rule for host1:eth2, 49 packets dropped |
| 43.124 | switch2 log | interface,info host1 link up |
| 43.212 | host1-to-host2 | Diagnostic only: 4 pings recorded lost (configured interval 100 ms), observed outage bounds 0.314189 to 0.519099 s, reply absent at source |
| 43.918 | streams | measurement ended; captures wait for final replies |
| 44.424 | stopped | captures and streams stopped |
| 44.424 | run error | Fault recovery exceeded 14.9924 s. |
| 44.710 | switch1 log | script,info networka cable-packet-loss end |
| 44.985 | switch2 log | script,info networka cable-packet-loss end |
| 44.992 | switch log | marker 'networka cable-packet-loss end' written on switch1, switch2 |
