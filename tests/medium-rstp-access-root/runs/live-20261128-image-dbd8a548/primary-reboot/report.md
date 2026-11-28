# ERROR — primary-reboot

Reboot switch1 in its checked MLAG primary role and measure both directions between host1 and host2.

- The state before the test is fail, so the steps were not run.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | unmeasured | unmeasured | error |
| Baseline | host2:bond0 → host1:eth1 | 0 s | unmeasured | unmeasured | error |
| Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | unmeasured | unmeasured | error |
| Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | unmeasured | unmeasured | error |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | unmeasured | unmeasured | error |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | unmeasured | unmeasured | error |

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| 0.000 | test | primary-reboot started in lab medium-mlag-rstp-access-root |
| 0.322 | access-switch log | script,info networka primary-reboot start |
| 0.641 | switch1 log | script,info networka primary-reboot start |
| 0.996 | switch2 log | script,info networka primary-reboot start |
| 1.006 | switch log | marker 'networka primary-reboot start' written on access-switch, switch1, switch2 |
| 1.033 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.036 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.036 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.036 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.036 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.036 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.036 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.040 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.040 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.041 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.042 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.042 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.043 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.826 | state | check before the steps: fail |
| 2.826 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 2.826 | state | All three switches run RSTP. pass |
| 2.826 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| 2.826 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. fail |
| 2.826 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 2.826 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 2.826 | stopped | captures and streams stopped |
| 2.866 | access-switch log | script,info networka primary-reboot end |
| 2.916 | switch1 log | script,info networka primary-reboot end |
| 2.985 | switch2 log | script,info networka primary-reboot end |
| 2.994 | switch log | marker 'networka primary-reboot end' written on access-switch, switch1, switch2 |
