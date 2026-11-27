# PASS — calibration

Verify that measurement can bound a two-second one-way loss without loss on the other three streams.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host1:eth3 → host2:eth3 | 2.3 s | 19 at one ping every 100 ms | 1.88187 to 2.08819 s | pass |
| One-way bypass cut | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:eth3 → host2:eth3 | 2.3 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.791 | test | calibration started in lab medium-mlag |
| -1.514 | access-switch log | script,info networka calibration start |
| -1.230 | switch1 log | script,info networka calibration start |
| -0.945 | switch2 log | script,info networka calibration start |
| -0.939 | switch log | marker 'networka calibration start' written on access-switch, switch1, switch2 |
| -0.117 | state | check before the steps: pass |
| -0.117 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.117 | state | All three switches run with spanning tree off. pass |
| -0.117 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.117 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host1:eth3 |
| -0.062 | capture | started at host2:bond0 |
| -0.062 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.852 | quiet window | clean |
| 3.852 | step | Baseline |
| 7.854 | step | One-way bypass cut |
| 7.859 | fault | applying the rule for bypass-host1-to-host2 on host2:eth3 |
| 7.863 | fault | read back the rule for bypass-host1-to-host2 |
| 7.914 | bypass-host1-to-host2 | 19 pings lost at one ping every 100 ms, traffic stopped for 1.882 to 2.088 s, reply absent at destination |
| 9.865 | step | Bypass restored |
| 9.871 | fault | removed the rule for bypass-host1-to-host2, 19 packets dropped |
| 12.873 | step | After calibration |
| 15.873 | steps | last step ended |
| 17.089 | state | check after the steps: pass |
| 17.089 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 17.089 | state | All three switches run with spanning tree off. pass |
| 17.089 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 17.089 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 17.089 | streams | measurement ended; captures wait for final replies |
| 17.594 | stopped | captures and streams stopped |
| 17.642 | access-switch log | script,info networka calibration end |
| 17.690 | switch1 log | script,info networka calibration end |
| 17.722 | switch2 log | script,info networka calibration end |
| 17.729 | switch log | marker 'networka calibration end' written on access-switch, switch1, switch2 |
