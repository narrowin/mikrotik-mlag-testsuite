# FAIL — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

- Step Inter-pair member down is fail.
- Step Inter-pair member back is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 94 at one ping every 100 ms | 9.73696 to 9.9402 s | fail |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 95 at one ping every 100 ms | 9.80149 to 10.0082 s | fail |
| Inter-pair member down | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member down | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 100 at one ping every 100 ms | 9.73696 to 9.9402 s | fail |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 99 at one ping every 100 ms | 9.80149 to 10.0082 s | fail |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353488 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.355095 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.35398 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.354672 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -2.66855 to 26.424 s, switch-a2 -2.63713 to 26.4532 s, switch-b1 -2.59173 to 26.4832 s, switch-b2 -2.55474 to 26.5278 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.86677 to 11.8848 s | must ether3 link down | pass | 2026-11-27T06:16:54.761435+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.86677 to 11.8848 s | must ether3 link down | pass | 2026-11-27T06:16:55.073280+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.8848 to 19.9001 s | must ether3 link up | pass | 2026-11-27T06:17:02.766889+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.8848 to 19.9001 s | must ether3 link up | pass | 2026-11-27T06:17:03.087928+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.702 | test | inter-pair-member-flap started in lab medium-two-pair-rstp |
| -2.669 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -2.637 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -2.592 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -2.555 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -2.552 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -1.301 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.300 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.300 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.300 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.300 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.299 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.299 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.298 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.298 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.298 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.298 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.298 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.298 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.120 | state | All four switches run RSTP. pass |
| -0.120 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.120 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.120 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.120 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.120 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.115 | capture | started at host1:bond0 |
| -0.115 | capture | started at host1:eth3 |
| -0.115 | capture | started at host2:bond0 |
| -0.063 | capture | started at host2:eth3 |
| -0.063 | capture | started at switch-a1:eth2 |
| -0.063 | capture | started at switch-b1:eth2 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.002 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.715 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.717 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.717 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.717 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.717 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.717 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.717 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.718 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.718 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.719 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.720 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.720 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.720 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.724 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.725 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.726 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.726 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.726 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.726 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.726 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.727 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.728 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.728 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.728 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.728 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.728 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.865 | quiet window | clean |
| 3.865 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.867 | step | Inter-pair member down |
| 3.884 | cable | switch-a1:eth2 set down |
| 3.884 | cable | switch-a1:eth2 down at both ends |
| 3.912 | host2-to-host1 | 95 pings lost at one ping every 100 ms, traffic stopped for 9.801 to 10.008 s, request absent at destination |
| 3.954 | switch-a1 log | interface,info inter-pair link down |
| 3.976 | host1-to-host2 | 94 pings lost at one ping every 100 ms, traffic stopped for 9.737 to 9.94 s, request absent at destination |
| 3.983 | switch-b1 log | interface,info inter-pair link down |
| 4.020 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.021 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.022 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.201 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.204 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.204 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.204 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.204 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.204 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.204 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.205 | switch-b2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.207 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.207 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 4.207 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 4.208 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 4.208 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 4.209 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.212 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.212 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.213 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.213 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.213 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.215 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.215 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 4.215 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 4.240 | switch-a1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 40000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.240 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.240 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 4.240 | switch-b1 log | bridge,stp ether2:0  becomes Root |
| 4.240 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.241 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_PROPOSED |
| 4.241 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.241 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 4.244 | switch-a1 log | interface,info ether3 link down |
| 4.246 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.246 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 4.246 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 4.249 | switch-a1 log | bridge,stp,debug ether2:0  rcv info InferiorRootAlternate |
| 4.556 | switch-b1 log | interface,info ether3 link down |
| 5.210 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.213 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.213 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.213 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.214 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.214 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.214 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.214 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 5.215 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.215 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 5.215 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 6.849 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 7.214 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 7.214 | switch-a2 log | bridge,stp,debug inter-pair becomes edge port |
| 7.214 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 7.214 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.216 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.216 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.216 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.216 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.216 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.216 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.217 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.217 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 7.217 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 9.215 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.216 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.216 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.216 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.216 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.217 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.217 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.217 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.217 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 9.217 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 11.215 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.217 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.219 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.219 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 11.219 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 11.220 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.220 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.220 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.220 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.220 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.885 | step | Inter-pair member back |
| 11.898 | cable | switch-a1:eth2 set up |
| 11.899 | cable | switch-a1:eth2 up at both ends |
| 11.905 | switch-a1 log | interface,info inter-pair link up |
| 11.921 | switch-a1 log | bridge,stp inter-pair:0  becomes Designated |
| 11.921 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_PROPOSE |
| 11.921 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_SYNCED |
| 11.921 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.921 | switch-b1 log | interface,info inter-pair link up |
| 11.928 | switch-b1 log | bridge,stp inter-pair:0  becomes Designated |
| 11.931 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_PROPOSE |
| 11.932 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_SYNCED |
| 11.932 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.939 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x39 { TC LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.940 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 11.940 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 11.940 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 11.940 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 12.249 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.570 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 13.117 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.118 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.118 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 13.119 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.120 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 13.749 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.752 | switch-b1 log | bridge,stp ether2:0  becomes Alternate |
| 13.752 | switch-b1 log | bridge,stp inter-pair:0  becomes Root |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.752 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.752 | switch-b1 log | bridge,stp,debug ether2:0  role transition ALTERNATE\_PORT |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_AGREED |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition REROOT |
| 13.752 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_LEARN |
| 13.753 | switch-b1 log | bridge,stp inter-pair:0  learning |
| 13.753 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_RETIRED |
| 13.753 | switch-b1 log | bridge,stp,debug ether2:0  role transition ALTERNATE\_PORT |
| 13.753 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_FORWARD |
| 13.756 | switch-b1 log | bridge,stp inter-pair:0  forwarding |
| 13.757 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition REROOTED |
| 13.757 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.757 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.758 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.758 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 13.758 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_LEARN |
| 13.758 | switch-a1 log | bridge,stp inter-pair:0  learning |
| 13.760 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_FORWARD |
| 13.760 | switch-a1 log | bridge,stp inter-pair:0  forwarding |
| 13.765 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.765 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 13.765 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 13.765 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.771 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.771 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.772 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.772 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.772 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.772 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.772 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.772 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.773 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.773 | switch-b2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 13.776 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.776 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.776 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.776 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 13.776 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 13.779 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 13.780 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.780 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 13.780 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 13.780 | switch-a2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 14.227 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 14.227 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 14.231 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.314 to 0.519 s, request absent at destination |
| 14.321 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.413 s, request absent at destination |
| 15.115 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.117 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.117 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 15.120 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 15.120 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.120 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 15.120 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 15.120 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 15.121 | switch-a1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 15.150 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 15.757 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.758 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.758 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.760 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.761 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.761 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.761 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 15.873 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 15.873 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 16.116 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 16.753 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 16.754 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 17.119 | switch-b1 log | bridge,stp ether2:0  becomes Designated |
| 17.119 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 17.119 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 17.119 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 17.122 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.124 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.124 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 17.124 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 17.124 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 17.124 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 17.126 | switch-b2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 17.126 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.127 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 17.127 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 17.127 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 17.127 | switch-a2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 17.129 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, request absent at destination |
| 17.231 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 17.758 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.765 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.765 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.765 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.765 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.766 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.132 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.134 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.134 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 19.134 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 19.135 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.135 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 19.135 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 19.135 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 19.137 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 19.137 | switch-a1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 19.239 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 19.763 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 19.764 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.765 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.765 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.765 | switch-b1 log | bridge,stp,debug ether2:0  fdb flush |
| 19.767 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.767 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.767 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.767 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 19.767 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 19.769 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 19.795 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 19.876 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 19.900 | step | Flap recovery |
| 20.133 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 20.133 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 21.235 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 21.764 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 21.764 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.766 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.766 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.768 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.768 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.768 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 21.892 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 22.901 | state | bridge host-entry sampling stopped |
| 22.902 | steps | last step ended |
| 23.762 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.763 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.764 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.764 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.765 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.765 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.774 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.774 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.774 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.778 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.778 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.778 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.888 | state | check after the steps: pass |
| 25.888 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 25.888 | state | All four switches run RSTP. pass |
| 25.888 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 25.888 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 25.888 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 25.888 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 25.888 | state | Both cables of every host are eligible in its LACP bond. pass |
| 25.888 | streams | measurement ended; captures wait for final replies |
| 26.398 | stopped | captures and streams stopped |
| 26.424 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 26.453 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 26.483 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 26.528 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 26.532 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
