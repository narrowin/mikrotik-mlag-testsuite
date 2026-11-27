# FAIL — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

- Step switch1 power lost is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 111 at one ping every 100 ms | 11.4579 to 11.6637 s | fail |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 77 at one ping every 100 ms | 7.81332 to 12.1141 s | fail |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 15 at one ping every 100 ms | 1.04478 to 1.24912 s | pass |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 14 at one ping every 100 ms | 1.0431 to 1.24812 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.003 s.
- The new boot was detected at +29.037 s, with all lab checks passing at +30.492 s.

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.738 | test | primary-power-loss started in lab medium-mlag-rstp |
| -2.442 | access-switch log | script,info networka primary-power-loss start |
| -2.145 | switch1 log | script,info networka primary-power-loss start |
| -1.853 | switch2 log | script,info networka primary-power-loss start |
| -1.842 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| -0.773 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.771 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.771 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.116 | state | All three switches run RSTP. pass |
| -0.116 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.116 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.116 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.116 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host2:bond0 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.245 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.246 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.246 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.251 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.254 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.254 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.741 | quiet window | clean |
| 3.741 | step | Baseline |
| 5.248 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.249 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.249 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.251 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.253 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.253 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.741 | step | switch1 power lost |
| 7.862 | power | withdrawing the data cables of switch1 and stopping its guest |
| 7.873 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 8.000 | access-switch log | interface,info ether2 link down |
| 8.032 | power | switch1 guest paused and all data cables down |
| 8.055 | switch2 log | interface,info ether2 link down |
| 8.077 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.080 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.080 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 8.084 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 8.087 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_AGREE |
| 8.089 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.093 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.093 | switch2 log | bridge,warning "bridge" peer link down |
| 8.093 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 8.093 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 8.093 | access-switch log | bridge,stp uplink:0  discarding |
| 8.153 | host1-to-host2 | 111 pings lost at one ping every 100 ms, traffic stopped for 11.458 to 11.664 s, request absent at destination |
| 8.181 | host2-to-host1 | 76 pings lost at one ping every 100 ms, traffic stopped for 7.813 to 12.114 s, request absent at destination |
| 9.647 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.648 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.648 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 9.648 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 11.651 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.651 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.651 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 11.651 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 13.656 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.658 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.658 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 13.658 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 13.951 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 13.951 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 13.951 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_PROPOSE |
| 13.951 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_SYNCED |
| 13.951 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.953 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.953 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 15.662 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.662 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.662 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 15.663 | access-switch log | bridge,stp uplink:0  becomes Root |
| 15.663 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 15.663 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 15.663 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210102 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.663 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210102 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.664 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 15.664 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_SYNCED |
| 17.665 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.668 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.668 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 19.673 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.676 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.676 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 19.676 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_LEARN |
| 19.676 | access-switch log | bridge,stp uplink:0  learning |
| 19.676 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_RETIRED |
| 19.676 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_FORWARD |
| 19.677 | access-switch log | bridge,stp uplink:0  forwarding |
| 19.677 | access-switch log | bridge,stp,debug uplink:0  role transition REROOTED |
| 21.676 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.678 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.678 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 23.672 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.673 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.673 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 25.678 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.679 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.679 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 27.684 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.686 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.686 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 28.033 | step | switch1 power restored |
| 28.035 | power | resetting and resuming the guest of switch1 |
| 28.241 | power | switch1 guest running and all data cables up |
| 29.062 | access-switch log | interface,info ether2 link up (speed 10G, full duplex) |
| 29.096 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 29.685 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.687 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.687 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 31.695 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.696 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.696 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 33.695 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.698 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.698 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 34.120 | switch2 log | bridge,warning "bridge" peer link down |
| 35.702 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.704 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.704 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 37.712 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.712 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.712 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 39.136 | switch2 log | bridge,warning "bridge" peer link down |
| 39.711 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.713 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.713 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 41.721 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.722 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.723 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 43.721 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.722 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.722 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 43.765 | switch2 log | bridge,stp ether2:0  learning |
| 43.765 | switch2 log | bridge,stp ether2:0  forwarding |
| 43.766 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 43.767 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 43.767 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 43.767 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 43.767 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 43.769 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.771 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.771 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 43.771 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 43.835 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.840 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 43.840 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.840 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 44.243 | host1-to-host2 | 4 pings lost at one ping every 100 ms, traffic stopped for 0.31 to 0.517 s, request absent at destination |
| 44.319 | host2-to-host1 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.205 to 0.413 s, request absent at destination |
| 45.355 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.215 | host1-to-host2 | 11 pings lost at one ping every 100 ms, traffic stopped for 1.045 to 1.249 s, reply absent at source |
| 46.279 | host2-to-host1 | 11 pings lost at one ping every 100 ms, traffic stopped for 1.043 to 1.248 s, request absent at destination |
| 46.354 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 46.721 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 46.722 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 47.350 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.351 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.352 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 47.352 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 47.352 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.353 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.353 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 47.355 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.356 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 47.357 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 47.358 | switch1 log | bridge,stp access-switch:0  learning |
| 47.359 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 47.360 | switch1 log | bridge,stp access-switch:0  forwarding |
| 47.362 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.362 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 47.362 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 47.362 | switch1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 47.362 | switch1 log | bridge,stp,debug ether2:0  fdb flush |
| 47.362 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.382 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 47.382 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 49.348 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.351 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.351 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 49.730 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 50.351 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 50.351 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 51.351 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.353 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.353 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 53.355 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.356 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.356 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 55.355 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.356 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.356 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 57.366 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 57.366 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 57.366 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 58.527 | recovery | full lab state after power restoration of switch1: pass |
| 59.385 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 59.386 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 59.386 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 61.386 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 61.386 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 61.389 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 63.384 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 63.385 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 63.385 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 65.386 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 65.388 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 65.388 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 67.405 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 67.407 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 67.407 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 69.399 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 69.400 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 69.400 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 71.401 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 71.402 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 71.402 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 73.401 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 73.401 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 73.401 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 74.528 | step | Power recovery |
| 75.398 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 75.399 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 75.399 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 77.401 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 77.402 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 77.402 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 77.528 | steps | last step ended |
| 79.418 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 79.421 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 79.421 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 79.560 | state | check after the steps: pass |
| 79.560 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 79.560 | state | All three switches run RSTP. pass |
| 79.560 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 79.560 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 79.560 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 79.560 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 79.561 | streams | measurement ended; captures wait for final replies |
| 80.064 | stopped | captures and streams stopped |
| 80.096 | access-switch log | script,info networka primary-power-loss end |
| 80.150 | switch1 log | script,info networka primary-power-loss end |
| 80.183 | switch2 log | script,info networka primary-power-loss end |
| 80.185 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
