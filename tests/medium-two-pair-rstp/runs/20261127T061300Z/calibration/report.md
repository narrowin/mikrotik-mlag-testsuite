# PASS — calibration

Verify that measurement isolates a two-second one-way bypass cut, outside both MLAG pairs, while the host streams across both pairs continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| One-way bypass cut | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| One-way bypass cut | host1:eth3 → host2:eth3 | 2.3 s | 19 at one ping every 100 ms | 1.88026 to 2.08902 s | pass |
| One-way bypass cut | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host1:eth3 → host2:eth3 | 2.3 s | 0 at one ping every 100 ms | 0 s | pass |
| Bypass restored | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| After calibration | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.601 | test | calibration started in lab medium-two-pair-rstp |
| -2.559 | switch-a1 log | script,info networka calibration start |
| -2.514 | switch-a2 log | script,info networka calibration start |
| -2.484 | switch-b1 log | script,info networka calibration start |
| -2.453 | switch-b2 log | script,info networka calibration start |
| -2.447 | switch log | marker 'networka calibration start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.705 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.705 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.705 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.705 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.705 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.705 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.705 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.704 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.704 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.704 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.703 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.703 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.703 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run RSTP. pass |
| -0.118 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.118 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.063 | capture | started at host1:bond0 |
| -0.063 | capture | started at host1:eth3 |
| -0.063 | capture | started at host2:bond0 |
| -0.063 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.293 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.295 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.295 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.295 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.296 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.296 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.296 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.297 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.297 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.297 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.297 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.297 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.297 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.297 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.298 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.298 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.299 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.299 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.299 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.300 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.302 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.302 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.302 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.303 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.303 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.303 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.870 | quiet window | clean |
| 3.870 | step | One-way bypass cut |
| 3.877 | fault | applying the rule for bypass-host1-to-host2 on host2:eth3 |
| 3.883 | fault | read back the rule for bypass-host1-to-host2 |
| 3.969 | bypass-host1-to-host2 | 19 pings lost at one ping every 100 ms, traffic stopped for 1.88 to 2.089 s, reply absent at destination |
| 5.301 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.303 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.303 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.303 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.303 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.304 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.304 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.305 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.305 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.306 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.306 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.307 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.884 | step | Bypass restored |
| 5.890 | fault | removed the rule for bypass-host1-to-host2, 19 packets dropped |
| 7.304 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.306 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.306 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.306 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.306 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.307 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.307 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.308 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.308 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.308 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.891 | step | After calibration |
| 9.303 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.306 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.306 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.306 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.306 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.307 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.307 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.307 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.307 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.304 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.306 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.306 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.306 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.306 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.306 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.307 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.307 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.307 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.307 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.307 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.894 | steps | last step ended |
| 13.312 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.313 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.313 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.313 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.313 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.314 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.314 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.314 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.315 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.315 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.315 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.315 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.315 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 14.901 | state | check after the steps: pass |
| 14.901 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 14.901 | state | All four switches run RSTP. pass |
| 14.901 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 14.901 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 14.901 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 14.901 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 14.901 | state | Both cables of every host are eligible in its LACP bond. pass |
| 14.901 | streams | measurement ended; captures wait for final replies |
| 15.320 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.322 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.323 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.323 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.323 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 15.323 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 15.323 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.325 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.325 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.325 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.325 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 15.325 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 15.325 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.405 | stopped | captures and streams stopped |
| 15.445 | switch-a1 log | script,info networka calibration end |
| 15.482 | switch-a2 log | script,info networka calibration end |
| 15.523 | switch-b1 log | script,info networka calibration end |
| 15.555 | switch-b2 log | script,info networka calibration end |
| 15.560 | switch log | marker 'networka calibration end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
