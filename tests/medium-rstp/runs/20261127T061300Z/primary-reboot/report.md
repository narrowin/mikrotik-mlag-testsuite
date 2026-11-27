# ERROR — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2. Both bypass streams must continue while it restarts.

- Not valid: host1-to-host2 sent a ping at least every 450 ms.
- Not valid: host2-to-host1 sent a ping at least every 450 ms.
- Step Reboot switch1 is error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | Diagnostic only: 112 pings recorded lost, 274 sent in this step (configured interval 100 ms) | 8.53613 to 28.678 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | Diagnostic only: 243 pings recorded lost, 406 sent in this step (configured interval 100 ms) | 28.1015 to 28.3147 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot switch1 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch1 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch1

Reboot switch1 · pass

- Uptime before dispatch was 55 s. The switch reported 17 s at +23.811 s.
- Full lab state was pass at +31.7402 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.678 | test | primary-reboot started in lab medium-mlag-rstp |
| -1.647 | access-switch log | script,info networka primary-reboot start |
| -1.603 | switch1 log | script,info networka primary-reboot start |
| -1.563 | switch2 log | script,info networka primary-reboot start |
| -1.560 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| -0.551 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.550 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.550 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.114 | state | check before the steps: pass |
| -0.114 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.114 | state | All three switches run RSTP. pass |
| -0.114 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.114 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.114 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.114 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth3 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.457 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.457 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 1.457 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.474 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.475 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.475 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.878 | quiet window | clean |
| 3.878 | step | Baseline |
| 5.480 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.482 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.482 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.494 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.495 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.495 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.879 | step | Reboot switch1 |
| 7.926 | reboot | dispatching the reboot to switch1 |
| 7.967 | reboot | switch1 command returned: accepted |
| 8.325 | host1-to-host2 | Diagnostic only: 29 pings recorded lost (configured interval 100 ms), observed stop bounds 2.91135 to 3.11353 s, reply absent at source |
| 8.355 | host2-to-host1 | Diagnostic only: 28 pings recorded lost (configured interval 100 ms), observed stop bounds 2.83205 to 3.03801 s, request absent at destination |
| 12.809 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 12.809 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 12.809 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.811 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.811 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 12.811 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 12.812 | switch2 log | bridge,stp access-switch:0  discarding |
| 12.812 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 12.836 | host2-to-host1 | Diagnostic only: 215 pings recorded lost (configured interval 100 ms), observed stop bounds 28.1015 to 28.3147 s, late reply, reply absent at destination, request absent at destination |
| 12.882 | host1-to-host2 | Diagnostic only: 83 pings recorded lost (configured interval 100 ms), observed stop bounds 8.53613 to 28.678 s, reply absent at source, request absent at destination |
| 14.194 | switch2 log | bridge,stp access-switch:0  learning |
| 14.820 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.820 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.820 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 14.820 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 14.820 | switch2 log | bridge,stp access-switch:0  discarding |
| 16.201 | switch2 log | bridge,stp access-switch:0  learning |
| 16.823 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.827 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.827 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 16.827 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 16.827 | switch2 log | bridge,stp access-switch:0  discarding |
| 18.201 | switch2 log | bridge,stp access-switch:0  learning |
| 18.825 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.830 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.830 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 18.830 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 18.831 | switch2 log | bridge,stp access-switch:0  discarding |
| 20.214 | switch2 log | bridge,stp access-switch:0  learning |
| 20.828 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.831 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.831 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 20.831 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 20.834 | switch2 log | bridge,stp access-switch:0  discarding |
| 22.223 | switch2 log | bridge,stp access-switch:0  learning |
| 22.831 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.835 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.843 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 22.843 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 22.843 | switch2 log | bridge,stp access-switch:0  discarding |
| 24.231 | switch2 log | bridge,stp access-switch:0  learning |
| 24.836 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.838 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7c { LEARN FWD AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.838 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 24.838 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_DISCARD |
| 24.839 | switch2 log | bridge,stp access-switch:0  discarding |
| 25.065 | switch2 log | bridge,warning "bridge" peer disconnected |
| 25.068 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.071 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.071 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 25.071 | access-switch log | bridge,stp uplink:0  becomes Root |
| 25.071 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 25.072 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_PROPOSE |
| 25.072 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_PROPOSED |
| 25.072 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 25.072 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 25.072 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_SYNCED |
| 25.072 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.072 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_SYNCED |
| 25.072 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 25.073 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.073 | switch2 log | bridge,warning "bridge" peer link down |
| 25.074 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x1000:020000210102 cistEpc: 0 cistRegionalRootId: 0x1000:020000210102 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.074 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 25.109 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.111 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 25.112 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 25.115 | switch2 log | bridge,stp access-switch:0  learning |
| 25.117 | switch2 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 25.120 | switch2 log | bridge,stp access-switch:0  forwarding |
| 25.137 | switch2 log | bridge,stp ether2:0  learning |
| 25.141 | switch2 log | bridge,stp ether2:0  forwarding |
| 25.142 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 25.143 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_AGREE |
| 25.144 | switch2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 25.145 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 25.146 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 25.148 | switch2 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d1 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.152 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x7d { TC LEARN FWD AGREE DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x87d1 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.152 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 25.152 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_DISCARD |
| 25.166 | access-switch log | bridge,stp uplink:0  discarding |
| 25.183 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 26.515 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.515 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 27.238 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 27.238 | switch2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.521 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 28.518 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.518 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.518 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 30.522 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.524 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.524 | access-switch log | bridge,stp,debug uplink:0  rcv info InferiorDesignated |
| 30.855 | access-switch log | bridge,stp uplink:0  becomes Designated |
| 30.855 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 30.855 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_PROPOSE |
| 30.855 | access-switch log | bridge,stp,debug uplink:0  role transition DESIGNATED\_SYNCED |
| 30.855 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.856 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.856 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 30.859 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x4e { PROP AGREE DSGN } cistRootId: 0x8000:020000210103 cistEpc: 0 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.860 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorDesignated |
| 32.530 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.532 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.534 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 32.534 | access-switch log | bridge,stp uplink:0  becomes Root |
| 32.534 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 32.534 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_PROPOSED |
| 32.534 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_SYNCED |
| 32.534 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_AGREED |
| 32.534 | access-switch log | bridge,stp,debug uplink:0  role transition REROOT |
| 32.534 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_LEARN |
| 32.534 | access-switch log | bridge,stp uplink:0  learning |
| 32.538 | access-switch log | bridge,stp,debug ether4:0  role transition DESIGNATED\_RETIRED |
| 32.538 | access-switch log | bridge,stp,debug uplink:0  role transition ROOT\_FORWARD |
| 32.538 | access-switch log | bridge,stp uplink:0  forwarding |
| 32.538 | access-switch log | bridge,stp,debug uplink:0  role transition REROOTED |
| 32.538 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.539 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.539 | switch2 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 32.540 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x1000:020000210101 cistEpc: 20000 cistRegionalRootId: 0x8000:020000210103 portId: 0x8001 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.542 | switch1 log | bridge,stp,debug access-switch:0  rcv info InferiorRootAlternate |
| 32.542 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_LEARN |
| 32.545 | switch1 log | bridge,stp access-switch:0  learning |
| 32.547 | switch1 log | bridge,stp,debug access-switch:0  role transition DESIGNATED\_FORWARD |
| 32.549 | switch1 log | bridge,stp access-switch:0  forwarding |
| 32.553 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.553 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 32.567 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 32.568 | switch1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 32.568 | switch1 log | bridge,stp,debug ether2:0  fdb flush |
| 32.568 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.578 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE start |
| 32.578 | switch2 log | bridge,stp,debug access-switch:0  fdb flush |
| 33.275 | recovery | full lab state after reboot of switch1: fail |
| 34.525 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.526 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.526 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 35.245 | switch2 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 35.528 | switch1 log | bridge,stp,debug access-switch:0  TCHANGE over |
| 35.528 | switch1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 36.526 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.528 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.528 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 38.533 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.533 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.534 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 39.666 | recovery | full lab state after reboot of switch1: pass |
| 40.551 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.552 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.552 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 42.545 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.546 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.546 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 44.546 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.550 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.550 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 46.543 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.544 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.545 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 48.544 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.546 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.546 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 50.559 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.561 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.561 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 52.563 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.563 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.563 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 54.575 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.576 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.576 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 55.667 | step | Reboot recovery |
| 56.588 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 56.588 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 56.589 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 58.601 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 58.602 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 58.602 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 58.669 | steps | last step ended |
| 60.608 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 60.608 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 60.609 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 60.671 | state | check after the steps: pass |
| 60.671 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 60.671 | state | All three switches run RSTP. pass |
| 60.671 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 60.671 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 60.671 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 60.671 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 60.671 | streams | measurement ended; captures wait for final replies |
| 61.181 | stopped | captures and streams stopped |
| 61.221 | access-switch log | script,info networka primary-reboot end |
| 61.265 | switch1 log | script,info networka primary-reboot end |
| 61.314 | switch2 log | script,info networka primary-reboot end |
| 61.316 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
