# PASS — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 17 at one ping every 100 ms | 1.67191 to 1.87803 s | pass |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 17 at one ping every 100 ms | 1.66572 to 1.87091 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 4 at one ping every 100 ms | 0.206003 to 0.414096 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 4 at one ping every 100 ms | 0.208039 to 0.410612 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353524 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.353082 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.352658 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.353149 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.91092 to 25.4534 s, switch-a2 -2.61064 to 25.4893 s, switch-b1 -2.31996 to 25.5187 s, switch-b2 -2.02702 to 25.5713 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.79962 to 11.8385 s | must ether3 link down | pass | 2026-11-27T07:54:31.470897+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.79962 to 11.8385 s | must ether3 link down | pass | 2026-11-27T07:54:31.712491+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.8385 to 19.8613 s | must ether3 link up | pass | 2026-11-27T07:54:39.504997+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.8385 to 19.8613 s | must ether3 link up | pass | 2026-11-27T07:54:39.730114+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.209 | test | inter-pair-member-flap started in lab medium-two-pair |
| -2.911 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.611 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.320 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -2.027 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -2.022 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.115 | state | All four switches run with spanning tree off. pass |
| -0.115 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.115 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.115 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.110 | capture | started at host1:bond0 |
| -0.110 | capture | started at host2:bond0 |
| -0.057 | capture | started at switch-a1:eth2 |
| -0.057 | capture | started at switch-b1:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.797 | quiet window | clean |
| 3.798 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.800 | step | Inter-pair member down |
| 3.837 | cable | switch-a1:eth2 set down |
| 3.838 | cable | switch-a1:eth2 down at both ends |
| 3.853 | switch-b1 log | interface,info inter-pair link down |
| 3.866 | host1-to-host2 | 17 pings lost at one ping every 100 ms, traffic stopped for 1.672 to 1.878 s, reply absent at source, request absent at destination |
| 3.880 | host2-to-host1 | 17 pings lost at one ping every 100 ms, traffic stopped for 1.666 to 1.871 s, request absent at destination |
| 3.912 | switch-a1 log | interface,info inter-pair link down |
| 4.451 | switch-a1 log | interface,info ether3 link down |
| 4.692 | switch-b1 log | interface,info ether3 link down |
| 11.838 | step | Inter-pair member back |
| 11.860 | cable | switch-a1:eth2 set up |
| 11.860 | cable | switch-a1:eth2 up at both ends |
| 11.899 | switch-b1 log | interface,info inter-pair link up |
| 11.950 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 11.951 | switch-a1 log | interface,info inter-pair link up |
| 11.958 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 12.485 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.710 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.395 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.206 to 0.414 s, request absent at destination |
| 14.404 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.411 s, request absent at destination |
| 19.861 | step | Flap recovery |
| 22.864 | state | bridge host-entry sampling stopped |
| 22.865 | steps | last step ended |
| 24.919 | state | check after the steps: pass |
| 24.919 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.919 | state | All four switches run with spanning tree off. pass |
| 24.919 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 24.919 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.919 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.919 | streams | measurement ended; captures wait for final replies |
| 25.425 | stopped | captures and streams stopped |
| 25.453 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.489 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.519 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.571 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.578 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
