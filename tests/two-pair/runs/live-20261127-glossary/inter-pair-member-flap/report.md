# PASS — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 26 at one ping every 100 ms | 2.60961 to 2.81365 s | pass |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 25 at one ping every 100 ms | 2.51186 to 2.71573 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 2 at one ping every 100 ms | 0.107042 to 0.312346 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 2 at one ping every 100 ms | 0 to 0.210702 s | pass |
| Flap recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Bridge host entries

**pass**
- switch-a1 · 54 samples across 3 steps, longest interval 0.353494 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.35335 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.354446 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.354196 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.79986 to 25.3133 s, switch-a2 -2.47458 to 25.3493 s, switch-b1 -2.18385 to 25.4048 s, switch-b2 -1.89623 to 25.4537 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.76957 to 11.7973 s | must ether3 link down | pass | 2026-11-27T09:31:35.469671+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.76957 to 11.7973 s | must ether3 link down | pass | 2026-11-27T09:31:35.789432+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.7973 to 19.8146 s | must ether3 link up | pass | 2026-11-27T09:31:43.488118+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.7973 to 19.8146 s | must ether3 link up | pass | 2026-11-27T09:31:43.799115+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.112 | test | inter-pair-member-flap started in lab two-pair |
| -2.800 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.475 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.184 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.896 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.885 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run with spanning tree off. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at switch-a1:eth2 |
| -0.061 | capture | started at switch-b1:eth2 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.767 | quiet window | clean |
| 3.768 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.770 | step | Inter-pair member down |
| 3.793 | host1-to-host2 | 26 pings lost at one ping every 100 ms, traffic stopped for 2.61 to 2.814 s, reply absent at source, request absent at destination |
| 3.797 | cable | switch-a1:eth2 set down |
| 3.797 | cable | switch-a1:eth2 down at both ends |
| 3.816 | switch-b1 log | interface,info inter-pair link down |
| 3.869 | host2-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.512 to 2.716 s, request absent at destination |
| 3.877 | switch-a1 log | interface,info inter-pair link down |
| 4.282 | switch-a1 log | interface,info ether3 link down |
| 4.602 | switch-b1 log | interface,info ether3 link down |
| 11.797 | step | Inter-pair member back |
| 11.812 | cable | switch-a1:eth2 set up |
| 11.813 | cable | switch-a1:eth2 up at both ends |
| 11.827 | switch-a1 log | interface,info inter-pair link up |
| 11.873 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 11.875 | switch-b1 log | interface,info inter-pair link up |
| 12.301 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.612 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.147 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.312 s, request absent at destination |
| 14.217 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 19.815 | step | Flap recovery |
| 22.815 | state | bridge host-entry sampling stopped |
| 22.816 | steps | last step ended |
| 24.779 | state | check after the steps: pass |
| 24.779 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.779 | state | All four switches run with spanning tree off. pass |
| 24.779 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 24.779 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.779 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.779 | streams | measurement ended; captures wait for final replies |
| 25.283 | stopped | captures and streams stopped |
| 25.313 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.349 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.405 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.454 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.458 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
