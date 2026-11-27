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
| 0.300 | access-switch log | script,info networka baseline start |
| 0.642 | switch1 log | script,info networka baseline start |
| 0.988 | switch2 log | script,info networka baseline start |
| 0.993 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| 1.571 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.574 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.575 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.577 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.577 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.577 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.578 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.578 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.579 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.580 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.580 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.580 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.580 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.580 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.769 | state | check before the steps: fail |
| 2.769 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 2.769 | state | All three switches run RSTP. pass |
| 2.769 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| 2.769 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. fail |
| 2.769 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 2.769 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 2.769 | stopped | captures and streams stopped |
| 2.805 | access-switch log | script,info networka baseline end |
| 2.853 | switch1 log | script,info networka baseline end |
| 2.887 | switch2 log | script,info networka baseline end |
| 2.891 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
