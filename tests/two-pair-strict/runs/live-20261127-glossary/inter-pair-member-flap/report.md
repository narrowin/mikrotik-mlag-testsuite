# FAIL — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

- Step Inter-pair member down is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 53 at one ping every 100 ms | 5.40884 to 5.61424 s | fail |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 53 at one ping every 100 ms | 5.41469 to 5.62633 s | fail |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 5 at one ping every 100 ms | 0.318171 to 0.523095 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 6 at one ping every 100 ms | 0.419289 to 0.621454 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.35295 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.354596 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.353701 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.353456 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.79831 to 25.3637 s, switch-a2 -2.4945 to 25.3975 s, switch-b1 -2.19752 to 25.4506 s, switch-b2 -1.88309 to 25.4831 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.79815 to 11.8375 s | must ether3 link down | pass | 2026-11-27T09:31:34.214036+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.79815 to 11.8375 s | must ether3 link down | pass | 2026-11-27T09:31:34.621327+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.8375 to 19.8551 s | must ether3 link up | pass | 2026-11-27T09:31:42.262148+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.8375 to 19.8551 s | must ether3 link up | pass | 2026-11-27T09:31:42.631259+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.106 | test | inter-pair-member-flap started in lab two-pair-strict |
| -2.798 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.495 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.198 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.883 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.873 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.119 | state | All four switches run with spanning tree off. pass |
| -0.119 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.119 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.060 | capture | started at switch-a1:eth2 |
| -0.060 | capture | started at switch-b1:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.796 | quiet window | clean |
| 3.797 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.798 | step | Inter-pair member down |
| 3.835 | cable | switch-a1:eth2 set down |
| 3.835 | cable | switch-a1:eth2 down at both ends |
| 3.867 | switch-a1 log | interface,info inter-pair link down |
| 3.875 | host1-to-host2 | 53 pings lost at one ping every 100 ms, traffic stopped for 5.409 to 5.614 s, reply absent at source, request absent at destination |
| 3.882 | host2-to-host1 | 53 pings lost at one ping every 100 ms, traffic stopped for 5.415 to 5.626 s, request absent at destination |
| 3.909 | switch-a1 log | interface,info ether3 link down |
| 3.931 | switch-b1 log | interface,info inter-pair link down |
| 4.316 | switch-b1 log | interface,info ether3 link down |
| 11.838 | step | Inter-pair member back |
| 11.854 | cable | switch-a1:eth2 set up |
| 11.854 | cable | switch-a1:eth2 up at both ends |
| 11.872 | switch-b1 log | interface,info inter-pair link up |
| 11.894 | switch-a1 log | interface,info inter-pair link up |
| 11.930 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 11.943 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, reply absent at source |
| 11.957 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.326 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.195 | host2-to-host1 | 5 pings lost at one ping every 100 ms, traffic stopped for 0.419 to 0.621 s, request absent at destination |
| 14.272 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.318 to 0.523 s, request absent at destination |
| 19.855 | step | Flap recovery |
| 22.859 | state | bridge host-entry sampling stopped |
| 22.859 | steps | last step ended |
| 24.817 | state | check after the steps: pass |
| 24.817 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.817 | state | All four switches run with spanning tree off. pass |
| 24.817 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 24.817 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.817 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.818 | streams | measurement ended; captures wait for final replies |
| 25.323 | stopped | captures and streams stopped |
| 25.364 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.397 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.451 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.483 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.486 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
