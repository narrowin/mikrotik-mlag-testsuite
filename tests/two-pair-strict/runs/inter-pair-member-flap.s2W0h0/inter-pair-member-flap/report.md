# FAIL — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

- Step Inter-pair member down is fail.
- Step Inter-pair member back is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 78 at one ping every 100 ms | 8.05368 to 8.26084 s | fail |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 79 at one ping every 100 ms | 8.12048 to 8.33055 s | fail |
| Inter-pair member down | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member down | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 82 at one ping every 100 ms | 8.05368 to 8.26084 s | fail |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 83 at one ping every 100 ms | 8.12048 to 8.33055 s | fail |
| Inter-pair member back | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member back | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Bridge host entries

**pass**
- switch-a1 · 54 samples across 3 steps, longest interval 0.353649 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.354638 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.353856 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.353571 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.76627 to 25.4512 s, switch-a2 -2.48293 to 25.4869 s, switch-b1 -2.20084 to 25.5232 s, switch-b2 -1.92382 to 25.5734 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.87933 to 11.9018 s | must ether3 link down | pass | 2026-11-27T05:25:22.409057+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.87933 to 11.9018 s | must ether3 link down | pass | 2026-11-27T05:25:22.584506+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.9018 to 19.9224 s | must ether3 link up | pass | 2026-11-27T05:25:30.447163+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.9018 to 19.9224 s | must ether3 link up | pass | 2026-11-27T05:25:30.618181+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.047 | test | inter-pair-member-flap started in lab medium-two-pair-strict |
| -2.766 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.483 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.201 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.924 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.911 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.127 | state | check before the steps: pass |
| -0.127 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.127 | state | All four switches run with spanning tree off. pass |
| -0.127 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.127 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.127 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.068 | capture | started at host1:bond0 |
| -0.068 | capture | started at host1:eth3 |
| -0.067 | capture | started at host2:bond0 |
| -0.067 | capture | started at host2:eth3 |
| -0.067 | capture | started at switch-a1:eth2 |
| -0.067 | capture | started at switch-b1:eth2 |
| -0.011 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.007 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.877 | quiet window | clean |
| 3.878 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.879 | step | Inter-pair member down |
| 3.897 | cable | switch-a1:eth2 set down |
| 3.897 | cable | switch-a1:eth2 down at both ends |
| 3.905 | switch-b1 log | interface,info inter-pair link down |
| 3.976 | host2-to-host1 | 79 pings lost at one ping every 100 ms, traffic stopped for 8.12 to 8.331 s, request absent at destination |
| 3.994 | host1-to-host2 | 78 pings lost at one ping every 100 ms, traffic stopped for 8.054 to 8.261 s, request absent at destination |
| 3.995 | switch-a1 log | interface,info inter-pair link down |
| 4.323 | switch-a1 log | interface,info ether3 link down |
| 4.498 | switch-b1 log | interface,info ether3 link down |
| 11.902 | step | Inter-pair member back |
| 11.920 | cable | switch-a1:eth2 set up |
| 11.921 | cable | switch-a1:eth2 up at both ends |
| 11.958 | switch-b1 log | interface,info inter-pair link up |
| 12.021 | switch-a1 log | interface,info inter-pair link up |
| 12.361 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.532 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.323 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.309 to 0.518 s, request absent at destination |
| 14.355 | host2-to-host1 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.31 to 0.513 s, request absent at destination |
| 19.922 | step | Flap recovery |
| 22.926 | state | bridge host-entry sampling stopped |
| 22.926 | steps | last step ended |
| 24.908 | state | check after the steps: pass |
| 24.908 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.908 | state | All four switches run with spanning tree off. pass |
| 24.908 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 24.908 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.908 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.908 | streams | measurement ended; captures wait for final replies |
| 25.416 | stopped | captures and streams stopped |
| 25.451 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.487 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.523 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.573 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.576 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
