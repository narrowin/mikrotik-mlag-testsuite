# PASS — reboot-b-secondary

Reboot switch-b2 in its checked MLAG secondary role of pair B and measure both directions between the hosts. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:bond0 → host2:bond0 | 5 s | 1 at one ping every 100 ms | 0 to 0.207847 s | pass |
| Reboot switch-b2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Reboot of switch-b2

Reboot switch-b2 · pass

- Uptime before dispatch was 438 s. The switch reported 17 s at +23.7812 s.
- Full lab state was pass at +26.2864 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.622 | test | reboot-b-secondary started in lab medium-two-pair-rstp |
| -2.582 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.544 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.496 | switch-b1 log | script,info networka reboot-b-secondary start |
| -2.451 | switch-b2 log | script,info networka reboot-b-secondary start |
| -2.445 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -1.556 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.555 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.555 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.553 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.553 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.553 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.553 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.552 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -1.551 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -1.551 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -1.551 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -1.551 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -1.551 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.118 | state | All four switches run RSTP. pass |
| -0.118 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.118 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.118 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.118 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.064 | capture | started at host1:bond0 |
| -0.064 | capture | started at host1:eth3 |
| -0.064 | capture | started at host2:bond0 |
| -0.064 | capture | started at host2:eth3 |
| -0.009 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.006 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.453 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.455 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.455 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.455 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.455 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.455 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.455 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.455 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 0.456 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 0.456 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 0.457 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 0.457 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 0.458 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.455 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.457 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.457 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.457 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.457 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.457 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.457 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.459 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 2.459 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 2.460 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 2.460 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 2.462 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 2.462 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.872 | quiet window | clean |
| 3.872 | step | Baseline |
| 4.458 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.460 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.461 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.461 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.461 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.462 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.462 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.463 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 4.464 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 4.465 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 4.465 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 4.467 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 4.468 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.467 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.468 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.469 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 6.469 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.469 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 6.469 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 6.469 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.470 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 6.470 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 6.470 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 6.470 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 6.470 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 6.470 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.873 | step | Reboot switch-b2 |
| 7.923 | reboot | dispatching the reboot to switch-b2 |
| 7.985 | reboot | switch-b2 command returned: accepted |
| 8.469 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.471 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 8.471 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 8.471 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 8.472 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 8.472 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 8.472 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 10.479 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.482 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 10.483 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 10.483 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 10.483 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 10.483 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 10.483 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 12.486 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.488 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 12.488 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 12.488 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 12.488 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 12.489 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 12.489 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 14.487 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.489 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 14.489 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 14.489 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 14.489 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 14.489 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 14.489 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 16.486 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.489 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 16.489 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 16.489 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 16.489 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 16.489 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 16.489 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 18.494 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.496 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 18.496 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 18.497 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 18.497 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 18.497 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 18.497 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.912 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 20.505 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.508 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 20.508 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 20.508 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 20.508 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 20.508 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 20.508 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 22.511 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.512 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 22.512 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 22.512 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 22.512 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 22.512 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 22.512 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 24.303 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 24.314 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.315 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 24.315 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 24.315 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.315 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 24.315 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.315 | switch-b1 log | bridge,warning "bridge" peer link down |
| 24.315 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_AGREED |
| 24.315 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.318 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x78 { LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.318 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 24.318 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 24.318 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.318 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 24.319 | switch-a2 log | bridge,stp,debug inter-pair:0  fdb flush |
| 24.321 | switch-a1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 24.342 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.345 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 24.403 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x4000:020000210013 cistEpc: 0 cistRegionalRootId: 0x4000:020000210013 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.403 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.407 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x4000:020000210013 cistEpc: 0 cistRegionalRootId: 0x4000:020000210013 portId: 0x8002 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.407 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.430 | switch-b1 log | bridge,stp ether2:0  learning |
| 24.430 | switch-b1 log | bridge,stp ether2:0  forwarding |
| 24.454 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x4000:020000210012 cistEpc: 0 cistRegionalRootId: 0x4000:020000210012 portId: 0x87d1 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.454 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.458 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x4000:020000210012 cistEpc: 0 cistRegionalRootId: 0x4000:020000210012 portId: 0x87d1 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.458 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.519 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.523 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3d { TC LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.525 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 24.526 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 24.526 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE start |
| 24.526 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 24.526 | switch-b1 log | bridge,stp,debug ether2:0  fdb flush |
| 24.526 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.527 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.528 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 24.529 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 24.533 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.533 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 24.533 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 24.547 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 24.588 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 24.999 | switch-b1 log | bridge,stp,debug inter-pair:0  fdb flush |
| 26.304 | switch-b1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.307 | switch-a1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.307 | switch-a1 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 26.307 | switch-a1 log | bridge,stp,debug ether2:0  fdb flush |
| 26.308 | switch-a2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x79 { TC LEARN FWD AGREE ROOT } cistRootId: 0x2000:020000210011 cistEpc: 20000 cistRegionalRootId: 0x4000:020000210012 portId: 0x8002 messageAge: 256(1) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.308 | switch-a2 log | bridge,stp,debug inter-pair:0  rcv info InferiorRootAlternate |
| 26.309 | switch-a2 log | bridge,stp,debug ether2:0  fdb flush |
| 26.530 | switch-a1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 26.530 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 26.531 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.532 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.533 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 26.537 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 26.537 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 26.633 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 26.634 | switch-a2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 26.990 | switch-b2 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 26.990 | switch-b2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.307 | switch-b1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.307 | switch-b1 log | bridge,stp,debug inter-pair:0  TCHANGE over |
| 28.533 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.534 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.534 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 28.535 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 28.536 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 30.532 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.533 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.534 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 30.537 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 30.538 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 32.537 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.539 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.539 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 32.541 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 32.541 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 34.209 | recovery | full lab state after reboot of switch-b2: pass |
| 34.538 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.540 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.540 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 34.543 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 34.543 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 36.535 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.536 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.536 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 36.538 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 36.538 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 38.538 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.540 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.540 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 38.542 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 38.543 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 40.529 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.531 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.532 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 40.534 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 40.534 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 42.546 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.548 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.548 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 42.550 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 42.550 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 44.540 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.542 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.543 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 44.545 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 44.546 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 46.546 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.547 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.548 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 46.548 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 46.549 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 48.540 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.541 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.542 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 48.544 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 48.544 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 50.214 | step | Reboot recovery |
| 50.543 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.543 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.544 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 50.547 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 50.548 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 52.546 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.547 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.548 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 52.551 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 52.551 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 53.217 | steps | last step ended |
| 54.552 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.552 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.553 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 54.555 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 54.555 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 56.280 | state | check after the steps: pass |
| 56.280 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 56.280 | state | All four switches run RSTP. pass |
| 56.280 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 56.280 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 56.280 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 56.280 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 56.280 | state | Both cables of every host are eligible in its LACP bond. pass |
| 56.280 | streams | measurement ended; captures wait for final replies |
| 56.559 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 56.560 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 56.562 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 56.563 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3c { LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 56.563 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 56.789 | stopped | captures and streams stopped |
| 56.826 | switch-a1 log | script,info networka reboot-b-secondary end |
| 56.863 | switch-a2 log | script,info networka reboot-b-secondary end |
| 56.899 | switch-b1 log | script,info networka reboot-b-secondary end |
| 56.945 | switch-b2 log | script,info networka reboot-b-secondary end |
| 56.952 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
