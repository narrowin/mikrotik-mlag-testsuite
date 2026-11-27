# PASS — inter-pair-member-flap

Take the inter-pair bond member between switch-a1 and switch-b1 down and back. Measure both host streams, which cross the inter-pair bond, and sample the host entries of both hosts on all four switches.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 19 at one ping every 100 ms | 1.87293 to 2.07842 s | pass |
| Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 20 at one ping every 100 ms | 1.97367 to 2.17936 s | pass |
| Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 20 at one ping every 100 ms | 1.67265 to 1.87709 s | pass |
| Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 22 at one ping every 100 ms | 1.78117 to 1.98609 s | pass |
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
- switch-a1 · 54 samples across 3 steps, longest interval 0.353858 s.
- switch-a2 · 54 samples across 3 steps, longest interval 0.353437 s.
- switch-b1 · 54 samples across 3 steps, longest interval 0.353623 s.
- switch-b2 · 54 samples across 3 steps, longest interval 0.354896 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch-a1 -4.04433 to 26.4216 s, switch-a2 -3.73687 to 26.4546 s, switch-b1 -3.42205 to 26.4967 s, switch-b2 -3.1164 to 26.5517 s | must\_not heartbeat timeout | pass | not logged |
| Inter-pair member down | switch-a1 3.76335 to 11.7878 s | must ether3 link down | pass | 2026-11-27T08:06:12.662029+00:00 switch-a1 interface,info ether3 link down |
| Inter-pair member down | switch-b1 3.76335 to 11.7878 s | must ether3 link down | pass | 2026-11-27T08:06:13.209643+00:00 switch-b1 interface,info ether3 link down |
| Inter-pair member back | switch-a1 11.7878 to 19.8024 s | must ether3 link up | pass | 2026-11-27T08:06:20.676272+00:00 switch-a1 interface,info ether3 link up (speed 10G, full duplex) |
| Inter-pair member back | switch-b1 11.7878 to 19.8024 s | must ether3 link up | pass | 2026-11-27T08:06:21.238911+00:00 switch-b1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -4.359 | test | inter-pair-member-flap started in lab medium-two-pair-rstp |
| -4.044 | switch-a1 log | script,info networka inter-pair-member-flap start |
| -3.737 | switch-a2 log | script,info networka inter-pair-member-flap start |
| -3.422 | switch-b1 log | script,info networka inter-pair-member-flap start |
| -3.116 | switch-b2 log | script,info networka inter-pair-member-flap start |
| -3.096 | switch log | marker 'networka inter-pair-member-flap start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -2.410 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.409 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.409 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -2.408 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.408 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.408 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -2.408 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -2.408 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -2.408 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.408 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.407 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -2.407 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -2.407 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.404 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.403 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.401 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.401 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.401 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.401 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.401 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.398 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.398 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.398 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.398 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.398 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.398 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.117 | state | check before the steps: pass |
| -0.117 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.117 | state | All four switches run RSTP. pass |
| -0.117 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.117 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.117 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.117 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.117 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.059 | capture | started at switch-a1:eth2 |
| -0.059 | capture | started at switch-b1:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.606 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.606 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.608 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.608 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.608 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.608 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.608 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.609 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.609 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.609 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.610 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.611 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.611 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.614 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.616 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.616 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.616 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.616 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.616 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.616 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.619 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.619 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.619 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.619 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.619 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.620 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.761 | quiet window | clean |
| 3.762 | state | watching bridge host entries on switch-a1, switch-a2, switch-b1, switch-b2 |
| 3.763 | step | Inter-pair member down |
| 3.786 | cable | switch-a1:eth2 set down |
| 3.786 | cable | switch-a1:eth2 down at both ends |
| 3.790 | host2-to-host1 | 20 pings lost at one ping every 100 ms, traffic stopped for 1.974 to 2.179 s, reply absent at source, request absent at destination |
| 3.849 | switch-b1 log | interface,info inter-pair link down |
| 3.873 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.875 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.875 | host1-to-host2 | 19 pings lost at one ping every 100 ms, traffic stopped for 1.873 to 2.078 s, request absent at destination |
| 3.878 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.896 | switch-a1 log | interface,info inter-pair link down |
| 3.980 | switch-a1 log | interface,info ether3 link down |
| 4.062 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.064 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.064 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.065 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.066 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.066 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.066 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.066 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.067 | switch-b2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.067 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 4.067 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 4.067 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.068 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 4.068 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 4.069 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.071 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.071 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.071 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.071 | switch-a1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 40000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.071 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 4.072 | switch-a1 log | bridge,stp,debug ether2:0  rcv info InferiorRootAlternate |
| 4.072 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.073 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.073 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.073 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 4.073 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 4.073 | switch-b1 log | bridge,stp ether2:0  becomes Root |
| 4.074 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.075 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_PROPOSED |
| 4.076 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.076 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 4.078 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.080 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 4.080 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 4.527 | switch-b1 log | interface,info ether3 link down |
| 5.062 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.063 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.063 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.063 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.063 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.063 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.063 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.063 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 5.065 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3f { TC PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.065 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 5.066 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 7.067 | switch-a2 log | bridge,stp,debug inter-pair becomes edge port |
| 7.067 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 7.067 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 7.067 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.068 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.068 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.068 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.069 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.069 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.069 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.069 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.069 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 7.069 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 7.069 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 9.070 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.072 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.072 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.072 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.072 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.072 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.072 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.074 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.074 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 9.074 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 11.085 | switch-a2 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.086 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.087 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.087 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.087 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.088 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.088 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.089 | switch-b1 log | bridge,stp,debug ether2 rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.089 | switch-b1 log | bridge,stp,debug ether2:0  rcv info SuperiorDesignated |
| 11.089 | switch-b1 log | bridge,stp,debug ether2:0  role transition ROOT\_AGREED |
| 11.788 | step | Inter-pair member back |
| 11.802 | cable | switch-a1:eth2 set up |
| 11.802 | cable | switch-a1:eth2 up at both ends |
| 11.835 | switch-a1 log | interface,info inter-pair link up |
| 11.850 | switch-a1 log | bridge,stp inter-pair:0  becomes Designated |
| 11.851 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_PROPOSE |
| 11.851 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_SYNCED |
| 11.852 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.863 | host2-to-host1 | 18 pings lost at one ping every 100 ms, traffic stopped for 1.781 to 1.986 s, request absent at destination |
| 11.865 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x38 { LEARN FWD ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.866 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 11.866 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 11.866 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 11.866 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 11.880 | switch-b1 log | interface,info inter-pair link up |
| 11.896 | switch-b1 log | bridge,stp inter-pair:0  becomes Designated |
| 11.898 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_PROPOSE |
| 11.898 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_SYNCED |
| 11.898 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.900 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.900 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 11.901 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.902 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 11.949 | host1-to-host2 | 17 pings lost at one ping every 100 ms, traffic stopped for 1.673 to 1.877 s, request absent at destination |
| 11.994 | switch-a1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.556 | switch-b1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.958 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.959 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.959 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 12.961 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.961 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 13.630 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.630 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.630 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.630 | switch-b1 log | bridge,stp ether2:0  becomes Alternate |
| 13.631 | switch-b1 log | bridge,stp inter-pair:0  becomes Root |
| 13.631 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.631 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.631 | switch-b1 log | bridge,stp,debug ether2:0  role transition ALTERNATE\_PORT |
| 13.631 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_AGREED |
| 13.631 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition REROOT |
| 13.631 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_LEARN |
| 13.639 | switch-b1 log | bridge,stp inter-pair:0  learning |
| 13.640 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_RETIRED |
| 13.640 | switch-b1 log | bridge,stp,debug ether2:0  role transition ALTERNATE\_PORT |
| 13.640 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_FORWARD |
| 13.651 | switch-b1 log | bridge,stp inter-pair:0  forwarding |
| 13.651 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition REROOTED |
| 13.651 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.651 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.654 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.654 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 13.654 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_LEARN |
| 13.656 | switch-a1 log | bridge,stp inter-pair:0  learning |
| 13.656 | switch-a1 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_FORWARD |
| 13.661 | switch-a1 log | bridge,stp inter-pair:0  forwarding |
| 13.662 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.662 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 13.662 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 13.662 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.675 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.678 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.678 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.678 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.678 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.679 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.679 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.679 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.679 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 13.679 | switch-b2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 13.681 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.682 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.682 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 13.682 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.683 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.684 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 13.684 | switch-a2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 13.684 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 13.685 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 13.685 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 14.085 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 14.086 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 14.161 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.417 s, request absent at destination |
| 14.233 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.314 s, request absent at destination |
| 14.959 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.961 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.961 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 14.961 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 14.962 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.962 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 14.962 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 14.963 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 14.965 | switch-a1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 14.980 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 15.632 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.634 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.634 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.636 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.636 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.636 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.636 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 15.955 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 16.081 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 16.081 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 16.630 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 16.630 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 16.966 | switch-b1 log | bridge,stp ether2:0  becomes Designated |
| 16.966 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 16.966 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 16.966 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 16.966 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.967 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.967 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 16.967 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 16.967 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 16.967 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 16.967 | switch-b2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 16.970 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.970 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 16.970 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 16.970 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 16.970 | switch-a2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 17.085 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 17.635 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.637 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.637 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.639 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.639 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.639 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 18.978 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.981 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.981 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 18.981 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 18.983 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.983 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 18.983 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 18.984 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 18.985 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 18.986 | switch-a1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 19.081 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 19.090 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 19.634 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 19.634 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.636 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.636 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.636 | switch-b1 log | bridge,stp,debug ether2:0  fdb flush |
| 19.638 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.638 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.638 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 19.638 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.638 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 19.638 | switch-b2 log | bridge,stp,debug ether2:0  fdb flush |
| 19.645 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 19.802 | step | Flap recovery |
| 19.977 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 19.977 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 21.084 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 21.648 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 21.648 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.650 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.650 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.652 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.652 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.652 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 22.092 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 22.806 | state | bridge host-entry sampling stopped |
| 22.806 | steps | last step ended |
| 23.648 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.649 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.649 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.652 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.652 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.652 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.660 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.663 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.663 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.664 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.665 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.666 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.885 | state | check after the steps: pass |
| 25.885 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 25.885 | state | All four switches run RSTP. pass |
| 25.885 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 25.885 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 25.885 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 25.885 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 25.885 | state | Both cables of every host are eligible in its LACP bond. pass |
| 25.885 | streams | measurement ended; captures wait for final replies |
| 26.393 | stopped | captures and streams stopped |
| 26.422 | switch-a1 log | script,info networka inter-pair-member-flap end |
| 26.455 | switch-a2 log | script,info networka inter-pair-member-flap end |
| 26.497 | switch-b1 log | script,info networka inter-pair-member-flap end |
| 26.552 | switch-b2 log | script,info networka inter-pair-member-flap end |
| 26.562 | switch log | marker 'networka inter-pair-member-flap end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
