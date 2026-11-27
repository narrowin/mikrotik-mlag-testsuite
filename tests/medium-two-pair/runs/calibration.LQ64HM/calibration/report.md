# PASS — calibration

Verify that measurement isolates a two-second one-way bypass cut, outside both MLAG pairs, while the host streams across both pairs continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way bypass cut | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host1:eth3 → host2:eth3 | 2.3 s | 19 at one ping every 100 ms | 1.87313 to 2.08089 s | pass |
| One-way bypass cut | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:eth3 → host2:eth3 | 2.3 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.027 | test | calibration started in lab medium-two-pair |
| -2.740 | switch-a1 log | script,info networka calibration start |
| -2.450 | switch-a2 log | script,info networka calibration start |
| -2.166 | switch-b1 log | script,info networka calibration start |
| -1.881 | switch-b2 log | script,info networka calibration start |
| -1.874 | switch log | marker 'networka calibration start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run with spanning tree off. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.002 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.861 | quiet window | clean |
| 3.862 | step | One-way bypass cut |
| 3.867 | fault | applying the rule for bypass-host1-to-host2 on host2:eth3 |
| 3.871 | fault | read back the rule for bypass-host1-to-host2 |
| 3.954 | bypass-host1-to-host2 | 19 pings lost at one ping every 100 ms, traffic stopped for 1.873 to 2.081 s, reply absent at destination |
| 5.871 | step | Bypass restored |
| 5.882 | fault | removed the rule for bypass-host1-to-host2, 19 packets dropped |
| 8.887 | step | After calibration |
| 11.890 | steps | last step ended |
| 13.784 | state | check after the steps: pass |
| 13.784 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 13.784 | state | All four switches run with spanning tree off. pass |
| 13.784 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 13.784 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 13.784 | state | Both cables of every host are eligible in its LACP bond. pass |
| 13.784 | streams | measurement ended; captures wait for final replies |
| 14.287 | stopped | captures and streams stopped |
| 14.331 | switch-a1 log | script,info networka calibration end |
| 14.366 | switch-a2 log | script,info networka calibration end |
| 14.404 | switch-b1 log | script,info networka calibration end |
| 14.440 | switch-b2 log | script,info networka calibration end |
| 14.443 | switch log | marker 'networka calibration end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
