# PASS — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond, and on the independent bypass. Check that flooded probes reach host1 once.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both MLAG bonds on both peers contain their wired bond member and use it for LACP forwarding. · pass
- Both MLAG bond bridge ports are forwarding on both peers and both peer ports have carrier. · pass

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

## Flood probes

**pass**
- host2:bond0 → 10.110.0.255 · 106 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 106 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.727 | test | baseline started in lab medium-mlag-rstp |
| -3.106 | access-switch log | script,info networka baseline start |
| -3.026 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.026 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.026 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -2.479 | switch1 log | script,info networka baseline start |
| -1.846 | switch2 log | script,info networka baseline start |
| -1.842 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| -1.016 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.014 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.014 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.127 | state | check before the steps: pass |
| -0.127 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.127 | state | All three switches run RSTP. pass |
| -0.127 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.127 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.127 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.127 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth1 |
| -0.061 | capture | started at host2:eth2 |
| -0.061 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host2:bond0 to 10.110.0.255 |
| 0.001 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 0.985 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.987 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.987 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 3.002 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.003 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.003 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 4.151 | quiet window | clean |
| 4.151 | step | Steady traffic |
| 4.995 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.998 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.998 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 7.003 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.006 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.006 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 9.009 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.012 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.012 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 9.023 | state | Steady traffic pass |
| 9.024 | steps | last step ended |
| 11.005 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.006 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.007 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 11.022 | state | check after the steps: pass |
| 11.022 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 11.022 | state | All three switches run RSTP. pass |
| 11.022 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 11.022 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 11.022 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 11.022 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 11.022 | streams | measurement ended; captures wait for final replies |
| 11.531 | stopped | captures and streams stopped |
| 11.570 | access-switch log | script,info networka baseline end |
| 11.602 | switch1 log | script,info networka baseline end |
| 11.638 | switch2 log | script,info networka baseline end |
| 11.643 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
