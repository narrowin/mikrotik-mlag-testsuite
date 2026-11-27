# FAIL — primary-power-loss

Withdraw all data links of switch1 in its checked MLAG primary role and pause the guest before a cold reset. Measure both directions between host1 and host2.

- The state before the test is fail, so no cable was changed.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | unmeasured | unmeasured | unverified |
| Baseline | host2:bond0 → host1:eth1 | 0 s | unmeasured | unmeasured | unverified |
| switch1 power lost | host1:eth1 → host2:bond0 | 5 s | unmeasured | unmeasured | unverified |
| switch1 power lost | host2:bond0 → host1:eth1 | 5 s | unmeasured | unmeasured | unverified |
| switch1 power restored | host1:eth1 → host2:bond0 | 5 s | unmeasured | unmeasured | unverified |
| switch1 power restored | host2:bond0 → host1:eth1 | 5 s | unmeasured | unmeasured | unverified |
| Power recovery | host1:eth1 → host2:bond0 | 0 s | unmeasured | unmeasured | unverified |
| Power recovery | host2:bond0 → host1:eth1 | 0 s | unmeasured | unmeasured | unverified |

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| 0.000 | test | primary-power-loss started in lab medium-mlag-rstp-access-root |
| 0.300 | access-switch log | script,info networka primary-power-loss start |
| 0.590 | switch1 log | script,info networka primary-power-loss start |
| 0.736 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.737 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.738 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 0.738 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.738 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 0.739 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 0.739 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.739 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.741 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 0.741 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.741 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 0.741 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 0.741 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.894 | switch2 log | script,info networka primary-power-loss start |
| 0.900 | switch log | marker 'networka primary-power-loss start' written on access-switch, switch1, switch2 |
| 2.680 | state | check before the steps: fail |
| 2.680 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 2.680 | state | All three switches run RSTP. pass |
| 2.680 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| 2.680 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. fail |
| 2.680 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 2.680 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 2.680 | stopped | captures and streams stopped |
| 2.710 | access-switch log | script,info networka primary-power-loss end |
| 2.743 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.743 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.745 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 2.745 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.745 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 2.745 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 2.745 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.747 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.747 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 2.747 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.747 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 2.747 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 2.747 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.759 | switch1 log | script,info networka primary-power-loss end |
| 2.794 | switch2 log | script,info networka primary-power-loss end |
| 2.797 | switch log | marker 'networka primary-power-loss end' written on access-switch, switch1, switch2 |
