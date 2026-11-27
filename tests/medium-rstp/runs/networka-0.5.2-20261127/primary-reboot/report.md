# FAIL — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

- Step Reboot switch1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 176 at one ping every 100 ms | 16.0731 to 16.279 s | fail |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 176 at one ping every 100 ms | 16.0193 to 16.2238 s | fail |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 57 s. The switch reported 16 s at +22.8221 s.
- Full lab state was pass at +24.2882 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.630 | test | primary-reboot started in lab medium-mlag-rstp |
| -2.423 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.422 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.421 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -2.338 | access-switch log | script,info networka primary-reboot start |
| -2.047 | switch1 log | script,info networka primary-reboot start |
| -1.756 | switch2 log | script,info networka primary-reboot start |
| -1.751 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.421 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.420 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.420 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.111 | state | check before the steps: pass |
| -0.111 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.111 | state | All three switches run RSTP. pass |
| -0.111 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.111 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.111 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.111 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:eth1 |
| -0.057 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.587 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.589 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.589 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.595 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.596 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.596 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.738 | quiet window | clean |
| 3.739 | step | Baseline |
| 5.598 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.600 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.600 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.597 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.598 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.598 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.740 | step | Reboot switch1 |
| 7.783 | reboot | dispatching the reboot to switch1 |
| 7.843 | reboot | switch1 command returned: accepted |
| 8.144 | host1-to-host2 | 21 pings lost at one ping every 100 ms, traffic stopped for 2.085 to 2.289 s, reply absent at source |
| 8.165 | host2-to-host1 | 21 pings lost at one ping every 100 ms, traffic stopped for 2.079 to 2.284 s, request absent at destination |
| 13.281 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 13.281 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 13.281 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.283 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.283 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 13.284 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 13.286 | switch2 log | bridge,stp access-switch:0  discarding |
| 13.286 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 13.332 | host1-to-host2 | 155 pings lost at one ping every 100 ms, traffic stopped for 16.073 to 16.279 s, reply absent at source, request absent at destination |
| 13.338 | host2-to-host1 | 155 pings lost at one ping every 100 ms, traffic stopped for 16.019 to 16.224 s, request absent at destination |
| 14.282 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.287 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.289 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 14.986 | switch2 log | bridge,stp access-switch:0  learning |
| 16.288 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.290 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.291 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 16.291 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 16.291 | switch2 log | bridge,stp access-switch:0  discarding |
| 17.992 | switch2 log | bridge,stp access-switch:0  learning |
| 18.297 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.299 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.299 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 18.299 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 18.300 | switch2 log | bridge,stp access-switch:0  discarding |
| 19.988 | switch2 log | bridge,stp access-switch:0  learning |
| 20.301 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.303 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.305 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 20.305 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 20.305 | switch2 log | bridge,stp access-switch:0  discarding |
| 21.995 | switch2 log | bridge,stp access-switch:0  learning |
| 22.306 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.309 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.309 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 22.309 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 22.309 | switch2 log | bridge,stp access-switch:0  discarding |
| 24.004 | switch2 log | bridge,stp access-switch:0  learning |
| 24.010 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.013 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.015 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 24.015 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.015 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 24.015 | access-switch log | bridge,stp uplink:0  becomes Root |
| 24.015 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 24.015 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_PROPOSED |
| 24.015 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 24.015 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 24.015 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_SYNCED |
| 24.015 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.018 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 24.018 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.018 | switch2 log | bridge,warning "bridge" peer link down |
| 24.022 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.022 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 24.022 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 24.022 | access-switch log | bridge,stp uplink:0  discarding |
| 24.045 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.047 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 24.048 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_SYNCED |
| 24.048 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 24.050 | switch2 log | bridge,stp access-switch:0  forwarding |
| 24.200 | switch2 log | bridge,stp ether2:0  learning |
| 24.201 | switch2 log | bridge,stp ether2:0  forwarding |
| 24.201 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 24.202 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 24.202 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.202 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 24.203 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 24.204 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.209 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.209 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 24.209 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 24.253 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 24.498 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 25.445 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.452 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 26.996 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 26.996 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 27.457 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.458 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.458 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 27.458 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 27.458 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.459 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.459 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 27.461 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.462 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 27.463 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 27.466 | switch1 log | bridge,stp access-switch:0  learning |
| 27.467 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 27.469 | switch1 log | bridge,stp access-switch:0  forwarding |
| 27.471 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 27.473 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.473 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 27.489 | switch1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 27.490 | switch1 log | bridge,stp,debug ether2:0  fdb flush |
| 27.490 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.505 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 27.507 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 29.456 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.458 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.458 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 29.458 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_LEARN |
| 29.462 | access-switch log | bridge,stp uplink:0  learning |
| 29.462 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_RETIRED |
| 29.462 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_FORWARD |
| 29.462 | access-switch log | bridge,stp uplink:0  forwarding |
| 29.462 | access-switch log | bridge,stp,debug uplink:0  role transition REROOTED |
| 30.007 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 30.462 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 30.462 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 31.463 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.465 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.465 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 32.072 | recovery | full lab state after reboot of switch1: pass |
| 33.468 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.470 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.470 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 35.467 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.469 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.469 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 37.471 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.472 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.473 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 39.474 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.476 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.476 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 41.486 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.486 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.487 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 43.490 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.491 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.491 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 45.482 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.484 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.484 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 47.484 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.485 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.485 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 48.073 | step | Reboot recovery |
| 49.499 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.501 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.501 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 51.077 | steps | last step ended |
| 51.502 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.503 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.503 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 53.210 | state | check after the steps: pass |
| 53.210 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 53.210 | state | All three switches run RSTP. pass |
| 53.210 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 53.210 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 53.210 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 53.210 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 53.210 | streams | measurement ended; captures wait for final replies |
| 53.505 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.507 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.507 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 53.718 | stopped | captures and streams stopped |
| 53.761 | access-switch log | script,info networka primary-reboot end |
| 53.807 | switch1 log | script,info networka primary-reboot end |
| 53.850 | switch2 log | script,info networka primary-reboot end |
| 53.854 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
