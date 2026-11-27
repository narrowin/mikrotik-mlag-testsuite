# PASS — baseline

Check forwarding in both directions between the hosts across both MLAG pairs, and on the independent bypass. Both host streams cross the inter-pair bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Every host bond member on the switches is synchronized, collecting and distributing. · pass
- The inter-pair bond and the host bond are forwarding bridge ports on all four switches. · pass

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

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -5.768 | test | baseline started in lab medium-two-pair-rstp |
| -5.362 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -5.361 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -5.361 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -5.361 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -5.361 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -5.361 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -5.361 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -5.358 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -5.357 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -5.356 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -5.356 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -5.356 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -5.355 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -5.131 | switch-a1 log | script,info networka baseline start |
| -4.490 | switch-a2 log | script,info networka baseline start |
| -3.861 | switch-b1 log | script,info networka baseline start |
| -3.349 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.347 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.347 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -3.347 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -3.347 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -3.347 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -3.347 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -3.317 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.316 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -3.316 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -3.316 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -3.315 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -3.315 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -3.222 | switch-b2 log | script,info networka baseline start |
| -3.212 | switch log | marker 'networka baseline start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -1.343 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.341 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.341 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.341 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.341 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.340 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.340 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.340 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.340 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.339 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.339 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.339 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.339 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.120 | state | All four switches run RSTP. pass |
| -0.120 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.120 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.120 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.120 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.120 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.063 | capture | started at host1:bond0 |
| -0.063 | capture | started at host1:eth3 |
| -0.063 | capture | started at host2:bond0 |
| -0.063 | capture | started at host2:eth3 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.007 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.661 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.662 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.663 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.663 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.664 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.664 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.665 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.665 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.666 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.666 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.667 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.667 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.667 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.658 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.661 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.661 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.661 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.661 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.661 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.661 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.661 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.662 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.662 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.662 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.663 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.663 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.855 | quiet window | clean |
| 3.855 | step | Steady traffic |
| 4.659 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.661 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.661 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.661 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.661 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.661 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.661 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.662 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.663 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.663 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.663 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.663 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.663 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.660 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.662 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.662 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 6.662 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.662 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 6.662 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 6.662 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.663 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.663 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 6.663 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.663 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 6.663 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 6.663 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.657 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.658 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.658 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 8.658 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.658 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 8.658 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 8.658 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.659 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.659 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 8.659 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.659 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 8.659 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 8.659 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.748 | state | Steady traffic pass |
| 8.748 | steps | last step ended |
| 10.664 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.666 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.666 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 10.666 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 10.666 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 10.666 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 10.666 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 10.667 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.668 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 10.668 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 10.668 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 10.668 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 10.669 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.803 | state | check after the steps: pass |
| 11.803 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 11.803 | state | All four switches run RSTP. pass |
| 11.803 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 11.803 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 11.803 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 11.803 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 11.803 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.803 | streams | measurement ended; captures wait for final replies |
| 12.306 | stopped | captures and streams stopped |
| 12.331 | switch-a1 log | script,info networka baseline end |
| 12.360 | switch-a2 log | script,info networka baseline end |
| 12.390 | switch-b1 log | script,info networka baseline end |
| 12.435 | switch-b2 log | script,info networka baseline end |
| 12.438 | switch log | marker 'networka baseline end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
