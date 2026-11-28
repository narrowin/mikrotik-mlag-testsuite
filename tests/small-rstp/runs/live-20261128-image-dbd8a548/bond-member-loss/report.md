# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.21057 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 23 at one ping every 100 ms | 2.2858 to 2.49838 s | pass |
| Cable host1 to switch2 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -3.32695 to 30.7851 s, switch2 -2.68462 to 30.8291 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.80709 to 8.82524 s | must ether3 link down | pass | 2026-11-28T07:26:03.207320+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.82524 to 15.8383 s | must ether3 link up | pass | 2026-11-28T07:26:08.239442+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8383 to 20.8537 s | must ether3 link down | pass | 2026-11-28T07:26:14.484599+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8537 to 27.8661 s | must ether3 link up | pass | 2026-11-28T07:26:19.494171+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.932 | test | bond-member-loss started in lab small-mlag-rstp |
| -3.327 | switch1 log | script,info networka bond-member-loss start |
| -2.685 | switch2 log | script,info networka bond-member-loss start |
| -2.678 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | Both switches show MLAG connected. pass |
| -0.120 | state | Both switches run RSTP. pass |
| -0.120 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.120 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| -0.120 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host1:eth1 |
| -0.059 | capture | started at host1:eth2 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.059 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.002 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.807 | quiet window | clean |
| 3.807 | step | Cable host1 to switch1 down |
| 3.822 | cable | host1:eth1 set down |
| 3.824 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 1 ms |
| 3.886 | switch1 log | interface,info host1 link down |
| 4.680 | switch1 log | interface,info ether3 link down |
| 8.825 | step | Cable host1 to switch1 back |
| 8.836 | cable | host1:eth1 set up |
| 8.837 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 1 ms |
| 8.946 | switch1 log | interface,info host1 link up |
| 8.964 | switch1 log | bridge,stp host1:0  becomes Designated |
| 8.964 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 8.965 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_LEARN |
| 8.966 | switch1 log | bridge,stp host1:0  learning |
| 8.967 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_FORWARD |
| 8.969 | switch1 log | bridge,stp host1:0  forwarding |
| 9.712 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.838 | step | Cable host1 to switch2 down |
| 15.849 | cable | host1:eth2 set down |
| 15.851 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.864 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 15.904 | switch2 log | interface,info host1 link down |
| 15.957 | switch2 log | interface,info ether3 link down |
| 20.854 | step | Cable host1 to switch2 back |
| 20.864 | cable | host1:eth2 set up |
| 20.866 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 20.966 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 20.968 | switch2 log | interface,info host1 link up |
| 20.976 | switch2 log | bridge,stp host1:0  becomes Designated |
| 20.990 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 20.992 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_LEARN |
| 20.993 | switch2 log | bridge,stp host1:0  learning |
| 20.994 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_FORWARD |
| 20.996 | switch2 log | bridge,stp host1:0  forwarding |
| 21.056 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.286 to 2.498 s, reply absent at source |
| 27.866 | steps | last step ended |
| 30.246 | state | check after the steps: pass |
| 30.246 | state | Both switches show MLAG connected. pass |
| 30.246 | state | Both switches run RSTP. pass |
| 30.246 | state | Both MLAG peers are the RSTP root bridge. pass |
| 30.246 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| 30.246 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.246 | streams | measurement ended; captures wait for final replies |
| 30.755 | stopped | captures and streams stopped |
| 30.785 | switch1 log | script,info networka bond-member-loss end |
| 30.829 | switch2 log | script,info networka bond-member-loss end |
| 30.833 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
