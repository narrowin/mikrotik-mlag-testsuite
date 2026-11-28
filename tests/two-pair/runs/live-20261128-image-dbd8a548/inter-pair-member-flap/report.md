# PASS — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.202643 s | pass |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 2 at one ping every 100 ms | 0.103072 to 0.309124 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 15 at one ping every 100 ms | 1.45541 to 1.66019 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 14 at one ping every 100 ms | 1.35402 to 1.56082 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.359938 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.353298 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.359316 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.352994 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.92496 to 25.2977 s, switch-a2 -2.62667 to 25.3292 s, switch-b1 -2.32553 to 25.361 s, switch-b2 -1.98027 to 25.4024 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.76344 to 11.7959 s | must ether3 link down | pass | 2026-11-28T07:15:17.231450+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.76344 to 11.7959 s | must ether3 link down | pass | 2026-11-28T07:15:17.967218+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.7959 to 19.8189 s | must ether3 link up | pass | 2026-11-28T07:15:25.247905+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.7959 to 19.8189 s | must ether3 link up | pass | 2026-11-28T07:15:25.994227+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.218 | test | inter-pair-member-flap started in lab two-pair |
| -2.925 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.627 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.326 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.980 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.968 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.116 | state | All four switches run with spanning tree off. pass |
| -0.116 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.116 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host2:bond0 |
| -0.060 | capture | started at switch-a1:eth2 |
| -0.060 | capture | started at switch-b1:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.762 | quiet window | clean |
| 3.762 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.763 | step | Inter-pair member down |
| 3.793 | cable | switch-a1:eth2 set down |
| 3.794 | cable | switch-a1:eth2 down at both ends |
| 3.801 | host2-to-host1 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.309 s, request absent at destination |
| 3.851 | switch-b1 log | interface,info inter-pair link down |
| 3.857 | switch-a1 log | interface,info ether3 link down |
| 3.866 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, request absent at destination |
| 3.906 | switch-a1 log | interface,info inter-pair link down |
| 4.593 | switch-b1 log | interface,info ether3 link down |
| 11.796 | step | Inter-pair member back |
| 11.818 | cable | switch-a1:eth2 set up |
| 11.819 | cable | switch-a1:eth2 up at both ends |
| 11.825 | switch-a1 log | interface,info inter-pair link up |
| 11.874 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.881 | switch-b1 log | interface,info inter-pair link up |
| 11.904 | host1-to-host2 | 15 pings lost at one ping every 100 ms, traffic stopped for 1.455 to 1.66 s, request absent at destination |
| 11.934 | host2-to-host1 | 14 pings lost at one ping every 100 ms, traffic stopped for 1.354 to 1.561 s, request absent at destination |
| 12.620 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 19.819 | step | Flap recovery |
| 22.822 | state | bridge host-entry sampling stopped |
| 22.823 | steps | last step ended |
| 24.746 | state | check after the steps: pass |
| 24.746 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.746 | state | All four switches run with spanning tree off. pass |
| 24.746 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 24.746 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.746 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.746 | streams | measurement ended; captures wait for final replies |
| 25.252 | stopped | captures and streams stopped |
| 25.298 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.329 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.361 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.402 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.404 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
