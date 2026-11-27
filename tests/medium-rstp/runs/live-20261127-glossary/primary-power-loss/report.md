# FAIL — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

- Step switch1 power lost is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 111 at one ping every 100 ms | 11.3802 to 11.5856 s | fail |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 111 at one ping every 100 ms | 11.4689 to 11.676 s | fail |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 6 at one ping every 100 ms | 0.521257 to 0.729197 s | pass |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 6 at one ping every 100 ms | 0.519602 to 0.728475 s | pass |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Power loss of switch1** · pass

- Data cables lost carrier and the guest was paused for 20.007 s.
- The new boot was detected at +28.829 s, with all lab checks passing at +30.298 s.

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
| -3.390 | test | primary-power-loss started in lab medium-mlag-rstp |
| -3.089 | access-switch log | script,info networka primary-power-loss start |
| -2.795 | switch1 log | script,info networka primary-power-loss start |
| -2.496 | switch2 log | script,info networka primary-power-loss start |
| -2.487 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| -2.007 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.006 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.005 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.302 | state | check before the steps: pass |
| -0.302 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.302 | state | All three switches run RSTP. pass |
| -0.302 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.302 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.302 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.302 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.246 | capture | started at host1:eth1 |
| -0.245 | capture | started at host2:bond0 |
| -0.006 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.003 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.009 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.011 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.011 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 2.014 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.015 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.015 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.767 | quiet window | clean |
| 3.767 | step | Baseline |
| 4.012 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.013 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.013 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 6.013 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.015 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.015 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.770 | step | switch1 power lost |
| 7.895 | power | withdrawing the data cables of switch1 and stopping its guest |
| 7.940 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 8.049 | power | switch1 guest paused and all data cables down |
| 8.524 | switch2 log | interface,info ether2 link down |
| 8.562 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.565 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.565 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 8.569 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 8.571 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_AGREE |
| 8.572 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.574 | host2-to-host1 | 111 pings lost at one ping every 100 ms, traffic stopped for 11.469 to 11.676 s, request absent at destination |
| 8.576 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.576 | switch2 log | bridge,warning "bridge" peer link down |
| 8.576 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 8.576 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 8.577 | access-switch log | bridge,stp uplink:0  discarding |
| 8.646 | access-switch log | interface,info ether2 link down |
| 8.655 | host1-to-host2 | 110 pings lost at one ping every 100 ms, traffic stopped for 11.38 to 11.586 s, request absent at destination |
| 10.015 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.015 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.015 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 10.016 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 12.020 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.021 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.021 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 12.021 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 14.025 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.026 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.026 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 14.026 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 14.560 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 14.560 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 14.560 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_PROPOSE |
| 14.560 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_SYNCED |
| 14.560 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.561 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.561 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 16.027 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.029 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.029 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 16.029 | access-switch log | bridge,stp uplink:0  becomes Root |
| 16.029 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210102 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.029 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 16.029 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 16.029 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210102 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.029 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 16.029 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_SYNCED |
| 18.037 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.038 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.038 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 20.043 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.047 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.047 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 20.047 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_LEARN |
| 20.048 | access-switch log | bridge,stp uplink:0  learning |
| 20.050 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_RETIRED |
| 20.052 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_FORWARD |
| 20.053 | access-switch log | bridge,stp uplink:0  forwarding |
| 20.058 | access-switch log | bridge,stp,debug uplink:0  role transition REROOTED |
| 22.052 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.053 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.054 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 24.061 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.062 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.062 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 26.066 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.066 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.067 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 28.053 | step | switch1 power restored |
| 28.056 | power | resetting and resuming the guest of switch1 |
| 28.072 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.073 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.073 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 28.261 | power | switch1 guest running and all data cables up |
| 28.612 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 28.678 | access-switch log | interface,info ether2 link up (speed 10G, full duplex) |
| 30.074 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.074 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.074 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 32.074 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.074 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.074 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 33.653 | switch2 log | bridge,warning "bridge" peer link down |
| 34.074 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.074 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.074 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 36.079 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.081 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.082 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 38.083 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.083 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.083 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 38.666 | switch2 log | bridge,warning "bridge" peer link down |
| 40.085 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.087 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.087 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 42.092 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.094 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.094 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 43.680 | switch2 log | bridge,warning "bridge" peer link down |
| 44.029 | switch2 log | bridge,stp ether2:0  learning |
| 44.030 | switch2 log | bridge,stp ether2:0  forwarding |
| 44.031 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 44.031 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 44.031 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 44.032 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 44.032 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 44.033 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.035 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.036 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 44.036 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 44.083 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 44.084 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.087 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.087 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 44.116 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.118 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 44.119 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.121 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 45.161 | host1-to-host2 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.521 to 0.729 s, reply absent at source |
| 45.235 | host2-to-host1 | 6 pings lost at one ping every 100 ms, traffic stopped for 0.52 to 0.728 s, request absent at destination |
| 45.754 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.754 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 45.754 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 45.754 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.754 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.757 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.757 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 45.760 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.760 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 45.761 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 45.763 | switch1 log | bridge,stp access-switch:0  learning |
| 45.764 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 45.766 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.766 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 45.777 | switch1 log | bridge,stp access-switch:0  forwarding |
| 45.777 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 45.780 | switch1 log | bridge,stp,debug ether2:0  fdb flush |
| 45.780 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.780 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 46.102 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 46.103 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 46.751 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 47.751 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.752 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.752 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 48.755 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 49.752 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.754 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.754 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 51.763 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.763 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 51.764 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.762 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.763 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.763 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 55.770 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.771 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.771 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 57.770 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 57.772 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 57.773 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 58.353 | recovery | full lab state after power restoration of switch1: pass |
| 59.776 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 59.777 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 59.777 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 61.777 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 61.778 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 61.778 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 63.774 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 63.774 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 63.774 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 65.772 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 65.772 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 65.773 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 67.775 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 67.775 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 67.775 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 69.778 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 69.778 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 69.779 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 71.785 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 71.787 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 71.787 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 73.791 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 73.791 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 73.791 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 74.354 | step | Power recovery |
| 75.800 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 75.800 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 75.800 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 77.358 | steps | last step ended |
| 77.803 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 77.804 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 77.805 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 79.393 | state | check after the steps: pass |
| 79.393 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 79.393 | state | All three switches run RSTP. pass |
| 79.393 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 79.393 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 79.393 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 79.393 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 79.394 | streams | measurement ended; captures wait for final replies |
| 79.800 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 79.800 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 79.800 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 79.898 | stopped | captures and streams stopped |
| 79.932 | access-switch log | script,info networka primary-power-loss end |
| 79.986 | switch1 log | script,info networka primary-power-loss end |
| 80.014 | switch2 log | script,info networka primary-power-loss end |
| 80.019 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
