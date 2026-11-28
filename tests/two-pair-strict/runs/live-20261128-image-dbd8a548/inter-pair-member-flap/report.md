# PASS — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 2 at one ping every 100 ms | 0.10558 to 0.309641 s | pass |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.202416 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 15 at one ping every 100 ms | 1.15043 to 1.35714 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 15 at one ping every 100 ms | 1.14592 to 1.34826 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353771 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.354382 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.353633 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.353621 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.86812 to 25.345 s, switch-a2 -2.5682 to 25.3805 s, switch-b1 -2.27386 to 25.4286 s, switch-b2 -1.96663 to 25.5273 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.79794 to 11.8379 s | must ether3 link down | pass | 2026-11-28T07:20:17.702428+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.79794 to 11.8379 s | must ether3 link down | pass | 2026-11-28T07:20:17.782795+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.8379 to 19.858 s | must ether3 link up | pass | 2026-11-28T07:20:25.721429+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.8379 to 19.858 s | must ether3 link up | pass | 2026-11-28T07:20:25.834716+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.162 | test | inter-pair-member-flap started in lab two-pair-strict |
| -2.868 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.568 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.274 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.967 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.960 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.148 | state | check before the steps: pass |
| -0.148 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.148 | state | All four switches run with spanning tree off. pass |
| -0.148 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| -0.148 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.148 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.094 | capture | started at host1:bond0 |
| -0.094 | capture | started at host2:bond0 |
| -0.093 | capture | started at switch-a1:eth2 |
| -0.093 | capture | started at switch-b1:eth2 |
| -0.014 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.009 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.796 | quiet window | clean |
| 3.797 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.798 | step | Inter-pair member down |
| 3.837 | cable | switch-a1:eth2 set down |
| 3.837 | cable | switch-a1:eth2 down at both ends |
| 3.841 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.31 s, reply absent at source, request absent at destination |
| 3.866 | switch-b1 log | interface,info inter-pair link down |
| 3.876 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, request absent at destination |
| 3.921 | switch-a1 log | interface,info inter-pair link down |
| 4.097 | switch-a1 log | interface,info ether3 link down |
| 4.177 | switch-b1 log | interface,info ether3 link down |
| 11.838 | step | Inter-pair member back |
| 11.856 | cable | switch-a1:eth2 set up |
| 11.856 | cable | switch-a1:eth2 up at both ends |
| 11.891 | switch-b1 log | interface,info inter-pair link up |
| 11.946 | switch-a1 log | interface,info inter-pair link up |
| 11.995 | host1-to-host2 | 12 pings lost at one ping every 100 ms, traffic stopped for 1.15 to 1.357 s, request absent at destination |
| 12.008 | host2-to-host1 | 12 pings lost at one ping every 100 ms, traffic stopped for 1.146 to 1.348 s, request absent at destination |
| 12.116 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.229 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.376 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.417 s, request absent at destination |
| 14.387 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.42 s, request absent at destination |
| 19.858 | step | Flap recovery |
| 22.859 | state | bridge host-entry sampling stopped |
| 22.859 | steps | last step ended |
| 24.793 | state | check after the steps: pass |
| 24.793 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.793 | state | All four switches run with spanning tree off. pass |
| 24.793 | state | The inter-pair bond runs with lacp-strict=yes on all four switches. pass |
| 24.793 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.793 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.793 | streams | measurement ended; captures wait for final replies |
| 25.298 | stopped | captures and streams stopped |
| 25.345 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.380 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.429 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.527 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.536 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
