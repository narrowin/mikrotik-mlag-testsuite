# FAIL — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

- Step Reboot switch1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 194 at one ping every 100 ms | 18.022 to 18.227 s | fail |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 194 at one ping every 100 ms | 18.0127 to 18.2206 s | fail |
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

- Uptime before dispatch was 57 s. The switch reported 17 s at +23.7926 s.
- Full lab state was pass at +25.3436 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.714 | test | primary-reboot started in lab medium-mlag-rstp |
| -2.418 | access-switch log | script,info networka primary-reboot start |
| -2.124 | switch1 log | script,info networka primary-reboot start |
| -1.953 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.952 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.952 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -1.819 | switch2 log | script,info networka primary-reboot start |
| -1.814 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.115 | state | All three switches run RSTP. pass |
| -0.115 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.115 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.115 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.115 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.047 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.048 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.048 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 2.046 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.046 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.046 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.748 | quiet window | clean |
| 3.748 | step | Baseline |
| 4.045 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.046 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.047 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 6.049 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.050 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.050 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.750 | step | Reboot switch1 |
| 7.802 | reboot | dispatching the reboot to switch1 |
| 7.870 | reboot | switch1 command returned: accepted |
| 8.239 | host1-to-host2 | 20 pings lost at one ping every 100 ms, traffic stopped for 1.981 to 2.185 s, reply absent at source |
| 8.257 | host2-to-host1 | 20 pings lost at one ping every 100 ms, traffic stopped for 1.979 to 2.183 s, request absent at destination |
| 12.036 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 12.036 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 12.036 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.038 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.038 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 12.038 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 12.042 | switch2 log | bridge,stp access-switch:0  discarding |
| 12.042 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 12.070 | host2-to-host1 | 174 pings lost at one ping every 100 ms, traffic stopped for 18.013 to 18.221 s, request absent at destination |
| 12.078 | host1-to-host2 | 174 pings lost at one ping every 100 ms, traffic stopped for 18.022 to 18.227 s, reply absent at source, request absent at destination |
| 13.036 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.039 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.039 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 13.496 | switch2 log | bridge,stp access-switch:0  learning |
| 15.042 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.044 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.044 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 15.044 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 15.047 | switch2 log | bridge,stp access-switch:0  discarding |
| 16.501 | switch2 log | bridge,stp access-switch:0  learning |
| 17.046 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.049 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.049 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 17.049 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 17.052 | switch2 log | bridge,stp access-switch:0  discarding |
| 18.509 | switch2 log | bridge,stp access-switch:0  learning |
| 19.052 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.055 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.055 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 19.056 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 19.057 | switch2 log | bridge,stp access-switch:0  discarding |
| 20.516 | switch2 log | bridge,stp access-switch:0  learning |
| 21.057 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.059 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.060 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 21.060 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 21.062 | switch2 log | bridge,stp access-switch:0  discarding |
| 22.517 | switch2 log | bridge,stp access-switch:0  learning |
| 23.062 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.065 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.065 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 23.065 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 23.065 | switch2 log | bridge,stp access-switch:0  discarding |
| 24.524 | switch2 log | bridge,stp access-switch:0  learning |
| 24.588 | switch2 log | bridge,warning "bridge" peer disconnected |
| 24.591 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.593 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 24.593 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 24.594 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.594 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 24.594 | access-switch log | bridge,stp uplink:0  becomes Root |
| 24.594 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 24.594 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_PROPOSED |
| 24.594 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 24.594 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 24.594 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_SYNCED |
| 24.594 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.594 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.594 | switch2 log | bridge,warning "bridge" peer link down |
| 24.597 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x5e { PROP LEARN AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.597 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 24.597 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 24.597 | access-switch log | bridge,stp uplink:0  discarding |
| 24.628 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.631 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 24.631 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_SYNCED |
| 24.632 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 24.634 | switch2 log | bridge,stp access-switch:0  forwarding |
| 24.706 | switch2 log | bridge,stp ether2:0  learning |
| 24.708 | switch2 log | bridge,stp ether2:0  forwarding |
| 24.709 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 24.709 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 24.710 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.710 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 24.711 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 24.712 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.713 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d2 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.714 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 24.715 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 24.780 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 26.182 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.180 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.525 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.525 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 28.177 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.178 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.178 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 28.178 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 28.178 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.179 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.179 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 28.180 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x48 { AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.181 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 28.183 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 28.185 | switch1 log | bridge,stp access-switch:0  learning |
| 28.187 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 28.190 | switch1 log | bridge,stp access-switch:0  forwarding |
| 28.193 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.193 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 28.197 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 28.197 | switch1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 28.209 | switch1 log | bridge,stp,debug ether2:0  fdb flush |
| 28.210 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.213 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 28.214 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 30.174 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.177 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.178 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 30.178 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_LEARN |
| 30.178 | access-switch log | bridge,stp uplink:0  learning |
| 30.178 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_RETIRED |
| 30.179 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_FORWARD |
| 30.180 | access-switch log | bridge,stp uplink:0  forwarding |
| 30.180 | access-switch log | bridge,stp,debug uplink:0  role transition REROOTED |
| 30.535 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 31.179 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 31.179 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 32.186 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.187 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.187 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 33.145 | recovery | full lab state after reboot of switch1: pass |
| 34.189 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.190 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.191 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 36.192 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.193 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.194 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 38.196 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.197 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.197 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 40.208 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.208 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.209 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 42.213 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.214 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.214 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 44.230 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.231 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.231 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 46.231 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.232 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.232 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 48.231 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.232 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.232 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 49.146 | step | Reboot recovery |
| 50.231 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.232 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.232 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 52.148 | steps | last step ended |
| 52.224 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.225 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.225 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 54.202 | state | check after the steps: pass |
| 54.202 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 54.202 | state | All three switches run RSTP. pass |
| 54.202 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 54.202 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 54.202 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 54.202 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 54.202 | streams | measurement ended; captures wait for final replies |
| 54.242 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.244 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.244 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 54.707 | stopped | captures and streams stopped |
| 54.753 | access-switch log | script,info networka primary-reboot end |
| 54.795 | switch1 log | script,info networka primary-reboot end |
| 54.835 | switch2 log | script,info networka primary-reboot end |
| 54.839 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
