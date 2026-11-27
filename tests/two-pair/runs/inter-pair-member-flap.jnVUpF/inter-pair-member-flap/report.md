# FAIL — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

- Step Inter-pair member down is fail.
- Step Inter-pair member back is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 78 at one ping every 100 ms | 8.02404 to 8.23448 s | fail |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 78 at one ping every 100 ms | 8.01614 to 8.21984 s | fail |
| Inter-pair member down | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member down | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 79 at one ping every 100 ms | 8.02404 to 8.23448 s | fail |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 79 at one ping every 100 ms | 8.01614 to 8.21984 s | fail |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353741 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.354421 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.354252 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.355098 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.72101 to 25.3625 s, switch-a2 -2.42545 to 25.406 s, switch-b1 -2.14239 to 25.4575 s, switch-b2 -1.87051 to 25.4914 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.87414 to 11.8916 s | must ether3 link down | pass | 2026-11-27T05:19:13.711721+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.87414 to 11.8916 s | must ether3 link down | pass | 2026-11-27T05:19:14.303248+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.8916 to 19.9063 s | must ether3 link up | pass | 2026-11-27T05:19:21.712406+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.8916 to 19.9063 s | must ether3 link up | pass | 2026-11-27T05:19:22.315684+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.009 | test | inter-pair-member-flap started in lab medium-two-pair |
| -2.721 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.425 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.142 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -1.871 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -1.868 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.127 | state | check before the steps: pass |
| -0.127 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.127 | state | All four switches run with spanning tree off. pass |
| -0.127 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.127 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.127 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.121 | capture | started at host1:bond0 |
| -0.121 | capture | started at host1:eth3 |
| -0.121 | capture | started at host2:bond0 |
| -0.121 | capture | started at host2:eth3 |
| -0.067 | capture | started at switch-a1:eth2 |
| -0.067 | capture | started at switch-b1:eth2 |
| -0.012 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.007 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.872 | quiet window | clean |
| 3.873 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.874 | step | Inter-pair member down |
| 3.887 | host1-to-host2 | 78 pings lost at one ping every 100 ms, traffic stopped for 8.024 to 8.234 s, request absent at destination |
| 3.888 | host2-to-host1 | 78 pings lost at one ping every 100 ms, traffic stopped for 8.016 to 8.22 s, request absent at destination |
| 3.890 | cable | switch-a1:eth2 set down |
| 3.890 | cable | switch-a1:eth2 down at both ends |
| 3.918 | switch-b1 log | interface,info inter-pair link down |
| 3.926 | switch-a1 log | interface,info inter-pair link down |
| 4.177 | switch-a1 log | interface,info ether3 link down |
| 4.769 | switch-b1 log | interface,info ether3 link down |
| 11.892 | step | Inter-pair member back |
| 11.906 | cable | switch-a1:eth2 set up |
| 11.906 | cable | switch-a1:eth2 up at both ends |
| 11.946 | switch-b1 log | interface,info inter-pair link up |
| 11.957 | switch-a1 log | interface,info inter-pair link up |
| 12.178 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.781 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 14.278 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 14.349 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 19.906 | step | Flap recovery |
| 22.909 | state | bridge host-entry sampling stopped |
| 22.909 | steps | last step ended |
| 24.807 | state | check after the steps: pass |
| 24.807 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 24.807 | state | All four switches run with spanning tree off. pass |
| 24.807 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 24.807 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 24.807 | state | Both cables of every host are eligible in its LACP bond. pass |
| 24.807 | streams | measurement ended; captures wait for final replies |
| 25.313 | stopped | captures and streams stopped |
| 25.363 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 25.406 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 25.457 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 25.491 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 25.501 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
