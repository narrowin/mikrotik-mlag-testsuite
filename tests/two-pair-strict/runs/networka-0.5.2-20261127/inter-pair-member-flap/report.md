# FAIL — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

- Step Inter-pair member down is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 49 at one ping every 100 ms | 5.00628 to 5.21384 s | fail |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 49 at one ping every 100 ms | 4.9934 to 5.20179 s | fail |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 6 at one ping every 100 ms | 0.322501 to 0.526544 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 5 at one ping every 100 ms | 0.20775 to 0.410632 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353791 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.353282 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.353241 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.353193 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.86484 to 25.3205 s, switch-a2 -2.56126 to 25.3755 s, switch-b1 -2.25262 to 25.4195 s, switch-b2 -1.95254 to 25.4681 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.74568 to 11.7736 s | must ether3 link down | pass | 2026-11-27T08:00:27.138950+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.74568 to 11.7736 s | must ether3 link down | pass | 2026-11-27T08:00:27.655076+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.7736 to 19.7965 s | must ether3 link up | pass | 2026-11-27T08:00:35.170271+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.7736 to 19.7965 s | must ether3 link up | pass | 2026-11-27T08:00:35.651837+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.165 | test | inter-pair-member-flap started in lab medium-two-pair-strict |
| -2.865 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.561 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.253 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.953 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.946 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.123 | state | check before the steps: pass |
| -0.123 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.123 | state | All four switches run with spanning tree off. pass |
| -0.123 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.123 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.123 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.068 | capture | started at host1:bond0 |
| -0.068 | capture | started at host2:bond0 |
| -0.067 | capture | started at switch-a1:eth2 |
| -0.067 | capture | started at switch-b1:eth2 |
| -0.010 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.003 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.744 | quiet window | clean |
| 3.744 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.746 | step | Inter-pair member down |
| 3.773 | cable | switch-a1:eth2 set down |
| 3.773 | cable | switch-a1:eth2 down at both ends |
| 3.777 | host2-to-host1 | 49 pings lost at one ping every 100 ms, traffic stopped for 4.993 to 5.202 s, request absent at destination |
| 3.788 | host1-to-host2 | 49 pings lost at one ping every 100 ms, traffic stopped for 5.006 to 5.214 s, reply absent at source, request absent at destination |
| 3.844 | switch-a1 log | interface,info inter-pair link down |
| 3.870 | switch-b1 log | interface,info inter-pair link down |
| 3.968 | switch-a1 log | interface,info ether3 link down |
| 4.484 | switch-b1 log | interface,info ether3 link down |
| 11.774 | step | Inter-pair member back |
| 11.795 | cable | switch-a1:eth2 set up |
| 11.796 | cable | switch-a1:eth2 up at both ends |
| 11.801 | switch-b1 log | interface,info inter-pair link up |
| 11.820 | host2-to-host1 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.309 s, reply absent at source, request absent at destination |
| 11.851 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.311 s, request absent at destination |
| 11.891 | switch-a1 log | interface,info inter-pair link up |
| 12.000 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.481 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.105 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.323 to 0.527 s, request absent at destination |
| 14.156 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.411 s, request absent at destination |
| 19.796 | step | Flap recovery |
| 22.798 | state | bridge host-entry sampling stopped |
| 22.799 | steps | last step ended |
| 24.770 | state | check after the steps: pass |
| 24.770 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.770 | state | All four switches run with spanning tree off. pass |
| 24.770 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 24.770 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.770 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.770 | streams | measurement ended; captures wait for final replies |
| 25.274 | stopped | captures and streams stopped |
| 25.321 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.375 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.419 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.468 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.472 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
