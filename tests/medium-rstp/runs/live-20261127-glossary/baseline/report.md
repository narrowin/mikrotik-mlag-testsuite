# PASS — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond. Check that flooded probes reach host1 once.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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

## Flood probes

**pass**
- host2:bond0 → 10.110.0.255 · 107 probes at one every 100 ms, 0 returned to the sender, 38 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 107 probes at one every 100 ms, 0 returned to the sender, 38 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.824 | test | baseline started in lab medium-mlag-rstp |
| -3.237 | access-switch log | script,info networka baseline start |
| -3.213 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.212 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -3.211 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -2.599 | switch1 log | script,info networka baseline start |
| -1.934 | switch2 log | script,info networka baseline start |
| -1.929 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| -1.207 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.206 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.206 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| -0.126 | state | check before the steps: pass |
| -0.126 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.126 | state | All three switches run RSTP. pass |
| -0.126 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| -0.126 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| -0.126 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.126 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:eth1 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth1 |
| -0.061 | capture | started at host2:eth2 |
| -0.007 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | flood probe | started from host2:bond0 to 10.110.0.255 |
| -0.002 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.794 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.796 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.796 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 2.791 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.792 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.792 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 4.034 | quiet window | clean |
| 4.034 | step | Steady traffic |
| 4.800 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.800 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 4.800 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.806 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.807 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.807 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 8.798 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.800 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.800 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 8.947 | state | Steady traffic pass |
| 8.947 | steps | last step ended |
| 10.802 | switch1 log | bridge,stp,debug access-switch tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.806 | access-switch log | bridge,stp,debug uplink rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x1000:020000210101 cistEpc: 0 cistRegionalRootId: 0x1000:020000210101 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.806 | access-switch log | bridge,stp,debug uplink:0  rcv info SuperiorDesignated |
| 11.221 | state | check after the steps: pass |
| 11.221 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 11.221 | state | All three switches run RSTP. pass |
| 11.221 | state | The MLAG pair is the RSTP root bridge with switch1's bridge ID, and the access switch reaches it through its uplink. pass |
| 11.221 | state | Every bridge port of the three switches forwards, and the host ports are edge ports. pass |
| 11.221 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 11.221 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 11.221 | streams | measurement ended; captures wait for final replies |
| 11.726 | stopped | captures and streams stopped |
| 11.765 | access-switch log | script,info networka baseline end |
| 11.796 | switch1 log | script,info networka baseline end |
| 11.825 | switch2 log | script,info networka baseline end |
| 11.838 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
