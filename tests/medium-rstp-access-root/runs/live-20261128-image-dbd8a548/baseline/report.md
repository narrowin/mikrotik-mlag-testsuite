# ERROR — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond. Check that flooded probes reach host1 once.

- The state before the test is fail, so the steps were not run.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:eth1 → host2:bond0 | 0 s | unmeasured | unmeasured | error |
| Steady traffic | host2:bond0 → host1:eth1 | 0 s | unmeasured | unmeasured | error |

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| 0.000 | test | baseline started in lab medium-mlag-rstp-access-root |
| 0.609 | access-switch log | script,info networka baseline start |
| 1.242 | switch1 log | script,info networka baseline start |
| 1.322 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.324 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.327 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.327 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.327 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.327 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.327 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.327 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.328 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.330 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.331 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.331 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.331 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.884 | switch2 log | script,info networka baseline start |
| 1.890 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| 3.325 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.328 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.329 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 3.329 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.329 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 3.329 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 3.329 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.333 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.333 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 3.333 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.333 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 3.333 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 3.334 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.717 | state | check before the steps: fail |
| 3.717 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 3.717 | state | All three switches run RSTP. pass |
| 3.717 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| 3.717 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. fail |
| 3.717 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 3.717 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 3.717 | stopped | captures and streams stopped |
| 3.743 | access-switch log | script,info networka baseline end |
| 3.793 | switch1 log | script,info networka baseline end |
| 3.839 | switch2 log | script,info networka baseline end |
| 3.841 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
