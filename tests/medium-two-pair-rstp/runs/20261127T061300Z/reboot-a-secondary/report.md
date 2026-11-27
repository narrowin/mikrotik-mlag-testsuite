# PASS — reboot-a-secondary

Reboot switch-a2 in its checked MLAG secondary role of pair A and measure both directions between the hosts. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-a2 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
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

## Reboot of switch-a2

Reboot switch-a2 · pass

- Uptime before dispatch was 318 s. The switch reported 16 s at +23.8451 s.
- Full lab state was pass at +26.465 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.821 | test | reboot-a-secondary started in lab medium-two-pair-rstp |
| -2.784 | switch-a1 log | script,info networka reboot-a-secondary start |
| -2.748 | switch-a2 log | script,info networka reboot-a-secondary start |
| -2.694 | switch-b1 log | script,info networka reboot-a-secondary start |
| -2.653 | switch-b2 log | script,info networka reboot-a-secondary start |
| -2.645 | switch log | marker 'networka reboot-a-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -2.320 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.319 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.319 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -2.319 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.319 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -2.319 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -2.319 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.318 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -2.318 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -2.318 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -2.317 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -2.317 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -2.317 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.320 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.318 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.318 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.318 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.318 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.318 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.318 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.316 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| -0.316 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| -0.316 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.316 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| -0.316 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| -0.316 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.116 | state | All four switches run RSTP. pass |
| -0.116 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| -0.116 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| -0.116 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.116 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host1:eth3 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host2:eth3 |
| -0.007 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.002 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 1.681 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.684 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.685 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.685 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.686 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.687 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.689 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.690 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 1.691 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 1.691 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 1.692 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 1.693 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 1.693 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.679 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.681 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.682 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.683 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.683 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.684 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.684 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.687 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 3.688 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 3.688 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.688 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 3.688 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 3.688 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 3.878 | quiet window | clean |
| 3.878 | step | Baseline |
| 5.684 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.685 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.686 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.687 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.687 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.687 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.688 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.690 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 5.690 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 5.690 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 5.690 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 5.690 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 5.690 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.694 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.698 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.698 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.698 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.698 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.698 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.698 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.700 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 7.700 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 7.700 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.700 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 7.700 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 7.700 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 7.879 | step | Reboot switch-a2 |
| 7.926 | reboot | dispatching the reboot to switch-a2 |
| 7.971 | reboot | switch-a2 command returned: accepted |
| 9.697 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.700 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.700 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.700 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.700 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.700 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.700 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.702 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 9.702 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 9.702 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 9.702 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 9.702 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 9.702 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.704 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.704 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.704 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.704 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.704 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.704 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.704 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.706 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 11.706 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 11.706 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 11.706 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 11.706 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 11.706 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.695 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.699 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.700 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.703 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.704 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.704 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.704 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.708 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 13.711 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 13.711 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 13.711 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 13.711 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 13.712 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.694 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.698 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.698 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.698 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.698 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 15.698 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 15.698 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.702 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 15.702 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 15.702 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 15.702 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 15.702 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 15.702 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 17.700 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.703 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.703 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.703 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 17.703 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 17.704 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 17.710 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 17.712 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 17.712 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 17.712 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 17.715 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 17.716 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 17.718 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.713 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.713 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.713 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.713 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.713 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 19.713 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 19.713 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.715 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 19.715 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 19.715 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 19.715 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 19.715 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 19.715 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 21.721 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.721 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.721 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.721 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 21.721 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 21.721 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 21.721 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 21.724 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 21.724 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 21.724 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 21.724 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 21.724 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 21.724 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 23.718 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.718 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.718 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.718 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 23.718 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 23.718 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 23.718 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 23.721 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 23.721 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 23.721 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 23.721 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 23.721 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 23.721 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 24.239 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210014 cistEpc: 0 cistRegionalRootId: 0x2000:020000210014 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.239 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.242 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210014 cistEpc: 0 cistRegionalRootId: 0x2000:020000210014 portId: 0x8003 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 24.242 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 24.326 | switch-a1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.217 | switch-a1 log | bridge,warning "bridge" peer disconnected |
| 25.225 | switch-a1 log | bridge,warning "bridge" peer link down |
| 25.262 | switch-a1 log | bridge,stp ether2:0  learning |
| 25.265 | switch-a1 log | bridge,stp ether2:0  forwarding |
| 25.268 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x87d3 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.268 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 25.270 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0xe { PROP DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x87d3 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.270 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info InferiorDesignated |
| 25.293 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE start |
| 25.731 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.733 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.733 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.734 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.735 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 25.735 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 25.735 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.736 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 25.736 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 25.736 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 25.737 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 25.737 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 25.737 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 27.737 | switch-a1 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.737 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.738 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.739 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 27.740 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 27.741 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 27.741 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 27.741 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 27.743 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 27.744 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 27.744 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 27.744 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 27.744 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 27.744 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 27.769 | switch-a2 log | bridge,stp,debug ether2:0  TCHANGE over |
| 27.773 | switch-a2 log | bridge,stp,debug inter-pair becomes edge port |
| 27.773 | switch-a2 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_LEARN |
| 27.773 | switch-a2 log | bridge,stp inter-pair:0  learning |
| 27.774 | switch-a2 log | bridge,stp,debug inter-pair:0  role transition DESIGNATED\_FORWARD |
| 27.774 | switch-a2 log | bridge,stp inter-pair:0  forwarding |
| 29.743 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.745 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.746 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 29.746 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 29.746 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 29.746 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 29.746 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 29.747 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 29.747 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 29.747 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 29.747 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 29.747 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 29.747 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 31.748 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.748 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.750 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 31.750 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 31.750 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 31.750 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 31.750 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 31.750 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 31.751 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 31.751 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 31.751 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 31.751 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 31.751 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 33.746 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.747 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.748 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 33.748 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 33.748 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 33.748 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 33.748 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 33.748 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 33.748 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 33.748 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 33.748 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 33.748 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 33.749 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 34.391 | recovery | full lab state after reboot of switch-a2: pass |
| 35.745 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.747 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.747 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 35.747 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 35.747 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 35.747 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 35.747 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 35.749 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 35.750 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 35.750 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 35.750 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 35.752 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 35.752 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 37.749 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.751 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.753 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 37.753 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 37.754 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 37.754 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 37.754 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 37.754 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 37.755 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 37.755 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 37.756 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 37.756 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 37.757 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 39.754 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.757 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.757 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 39.757 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 39.757 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 39.757 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 39.757 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 39.760 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 39.760 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 39.761 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 39.761 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 39.762 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 39.762 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 41.753 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.753 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.754 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 41.755 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 41.755 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 41.755 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 41.755 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 41.757 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 41.758 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 41.759 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 41.759 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 41.759 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 41.760 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 43.757 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.757 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.757 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 43.757 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 43.757 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 43.758 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 43.759 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 43.760 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 43.761 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 43.761 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 43.761 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 43.761 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 43.761 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 45.769 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.770 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.771 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 45.771 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 45.773 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 45.773 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 45.773 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 45.773 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 45.773 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 45.773 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 45.773 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 45.773 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 45.773 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 47.771 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.772 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.773 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 47.773 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 47.773 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 47.773 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 47.773 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 47.774 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 47.775 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 47.775 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 47.775 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 47.775 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 47.775 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 49.769 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.771 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.772 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 49.772 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 49.772 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 49.773 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 49.773 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 49.773 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 49.774 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 49.774 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 49.774 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 49.774 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 49.775 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 50.392 | step | Reboot recovery |
| 51.770 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.773 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.776 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 51.776 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 51.776 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 51.777 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 51.777 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 51.777 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 51.777 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 51.780 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 51.780 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 51.780 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 51.780 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 53.396 | steps | last step ended |
| 53.780 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.781 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.782 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 53.783 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 53.783 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 53.784 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 53.785 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 53.787 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 53.788 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 53.788 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 53.790 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 53.792 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 53.792 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 55.783 | switch-a1 log | bridge,stp,debug inter-pair tx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.783 | switch-b1 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.783 | switch-b1 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 55.783 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 55.783 | switch-b1 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 55.783 | switch-b1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 55.783 | switch-b1 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 55.784 | switch-b2 log | bridge,stp,debug inter-pair rx bpdu protoId: 0x0 protoVer: 0x2 type: 0x2 flags: 0x3e { PROP LEARN FWD DSGN } cistRootId: 0x2000:020000210011 cistEpc: 0 cistRegionalRootId: 0x2000:020000210011 portId: 0x8001 messageAge: 0(0) maxAge: 5120(20) helloTime: 512(2) forwardDelay: 3840(15) version1Length: 0 |
| 55.785 | switch-b2 log | bridge,stp,debug inter-pair:0  rcv info SuperiorDesignated |
| 55.785 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 55.785 | switch-b2 log | bridge,stp,debug inter-pair:0  role transition ROOT\_PROPOSED |
| 55.785 | switch-b2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 55.785 | switch-b2 log | bridge,stp,debug ether2:0  role transition DESIGNATED\_DISCARD |
| 56.511 | state | check after the steps: pass |
| 56.511 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 56.511 | state | All four switches run RSTP. pass |
| 56.511 | state | Pair A is the RSTP root bridge with switch-a1's bridge ID, and pair B reaches it through the inter-pair bond. pass |
| 56.511 | state | Every bridge port of the four switches forwards, and the host ports are edge ports. pass |
| 56.511 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 56.511 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 56.511 | state | Both cables of every host are eligible in its LACP bond. pass |
| 56.511 | streams | measurement ended; captures wait for final replies |
| 57.018 | stopped | captures and streams stopped |
| 57.046 | switch-a1 log | script,info networka reboot-a-secondary end |
| 57.084 | switch-a2 log | script,info networka reboot-a-secondary end |
| 57.121 | switch-b1 log | script,info networka reboot-a-secondary end |
| 57.160 | switch-b2 log | script,info networka reboot-a-secondary end |
| 57.165 | switch log | marker 'networka reboot-a-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
