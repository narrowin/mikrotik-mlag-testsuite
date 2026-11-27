# PASS — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond. Check that flooded probes reach host1 once.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both MLAG bonds on both peers contain their wired bond member and use it for LACP forwarding. · pass
- Both MLAG bond bridge ports are forwarding on both peers and both peer ports have carrier. · pass

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Flood check

**pass**
- host2:bond0 → 10.110.0.255 · 107 frames at one every 100 ms, 0 returned to the sender, 38 reached the witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 108 frames at one every 100 ms, 0 returned to the sender, 38 reached the witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.749 | test | baseline started in lab medium-mlag-rstp-access-root |
| -2.450 | access-switch log | script,info networka baseline start |
| -2.119 | switch1 log | script,info networka baseline start |
| -2.106 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.104 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.102 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| -2.102 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.102 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| -2.102 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.102 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| -2.102 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.100 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.099 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| -2.099 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.099 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| -2.099 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| -2.099 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.772 | switch2 log | script,info networka baseline start |
| -1.762 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| -0.127 | state | check before the steps: pass |
| -0.127 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.127 | state | All three switches run RSTP. pass |
| -0.127 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| -0.127 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.127 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.127 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.100 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.099 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.099 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| -0.099 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.098 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| -0.098 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.097 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| -0.097 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.095 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.095 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| -0.095 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.095 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| -0.095 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| -0.095 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.063 | capture | started at host1:eth1 |
| -0.063 | capture | started at host2:bond0 |
| -0.062 | capture | started at host2:eth1 |
| -0.062 | capture | started at host2:eth2 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | flood check | started from host2:bond0 to 10.110.0.255 |
| -0.003 | flood check | started from host2:bond0 to 10.110.0.99 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.904 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.906 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.907 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.907 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.908 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.908 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.908 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.908 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.911 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.911 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 1.911 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.911 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 1.911 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 1.911 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.908 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.909 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.909 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 3.909 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.910 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 3.911 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.912 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 3.912 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.914 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.914 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 3.914 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.914 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 3.915 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 3.915 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.025 | quiet window | clean |
| 4.025 | step | Steady traffic |
| 5.913 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.914 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.915 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 5.915 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.917 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 5.917 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.918 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 5.918 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.918 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.920 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 5.922 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.923 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 5.924 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 5.925 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.915 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.916 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.917 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 7.917 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.917 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 7.917 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.918 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 7.918 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.921 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.922 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 7.922 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.922 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 7.922 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 7.923 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.014 | state | Steady traffic pass |
| 9.015 | steps | last step ended |
| 9.922 | access-switch log | bridge,stp,debug uplink tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.926 | switch2 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.926 | switch2 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 9.926 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.926 | switch2 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 9.926 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.926 | switch2 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 9.926 | switch2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.930 | switch1 log | bridge,stp,debug access-switch rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x1000:020000210103 cistEpc: 0 cistRegionalRootId: 0x1000:020000210103 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.930 | switch1 log | bridge,stp,debug access-switch:0  rcv info SuperiorDesignated |
| 9.930 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.930 | switch1 log | bridge,stp,debug access-switch:0  role transition ROOT\_PROPOSED |
| 9.930 | switch1 log | bridge,stp,debug host2:0  role transition DESIGNATED\_SYNCED |
| 9.930 | switch1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.263 | state | check after the steps: pass |
| 11.263 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 11.263 | state | All three switches run RSTP. pass |
| 11.263 | state | The access switch is the RSTP root bridge, and both MLAG peers reach it through their MLAG bond to it. pass |
| 11.263 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 11.263 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 11.263 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 11.263 | streams | measurement ended; captures wait for final replies |
| 11.770 | stopped | captures and streams stopped |
| 11.810 | access-switch log | script,info networka baseline end |
| 11.853 | switch1 log | script,info networka baseline end |
| 11.914 | switch2 log | script,info networka baseline end |
| 11.917 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
