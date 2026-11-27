# FAIL — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

- Step Cable host1 to switch2 down is fail.
- Step Cable host1 to switch2 back is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 73 at one ping every 100 ms | 7.50595 to 7.71413 s | fail |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 73 at one ping every 100 ms | 7.50595 to 7.71413 s | fail |
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
| Whole test | switch1 -3.26887 to 30.8183 s, switch2 -2.68889 to 30.8564 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.8252 to 8.83728 s | must ether3 link down | pass | 2026-11-27T09:13:41.196854+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.83728 to 15.8512 s | must ether3 link up | pass | 2026-11-27T09:13:46.199989+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8512 to 20.8647 s | must ether3 link down | pass | 2026-11-27T09:13:53.280189+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8647 to 27.8773 s | must ether3 link up | pass | 2026-11-27T09:13:58.289432+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.886 | test | bond-member-loss started in lab small-mlag-rstp |
| -3.269 | switch1 log | script,info networka bond-member-loss start |
| -2.689 | switch2 log | script,info networka bond-member-loss start |
| -2.682 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.127 | state | check before the steps: pass |
| -0.127 | state | Both switches show MLAG connected. pass |
| -0.127 | state | Both switches run RSTP. pass |
| -0.127 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.127 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| -0.127 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.115 | capture | started at host1:bond0 |
| -0.113 | capture | started at host1:eth1 |
| -0.112 | capture | started at host1:eth2 |
| -0.112 | capture | started at host2:bond0 |
| -0.111 | capture | started at host3:bond0 |
| -0.111 | capture | started at switch1:eth2 |
| -0.060 | capture | started at switch2:eth2 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.003 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.825 | quiet window | clean |
| 3.825 | step | Cable host1 to switch1 down |
| 3.835 | cable | host1:eth1 set down |
| 3.836 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.902 | switch1 log | interface,info host1 link down |
| 4.258 | switch1 log | interface,info ether3 link down |
| 8.837 | step | Cable host1 to switch1 back |
| 8.849 | cable | host1:eth1 set up |
| 8.851 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.851 | switch1 log | interface,info host1 link up |
| 8.865 | switch1 log | bridge,stp host1:0  becomes Designated |
| 8.867 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 8.868 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_LEARN |
| 8.871 | switch1 log | bridge,stp host1:0  learning |
| 8.873 | switch1 log | bridge,stp,debug host1:0  role transition DESIGNATED\_FORWARD |
| 8.874 | switch1 log | bridge,stp host1:0  forwarding |
| 9.262 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.851 | step | Cable host1 to switch2 down |
| 15.862 | cable | host1:eth2 set down |
| 15.864 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.867 | host1-to-host2 | 73 pings lost at one ping every 100 ms, traffic stopped for 7.506 to 7.714 s, reply absent at source |
| 15.911 | switch2 log | interface,info host1 link down |
| 16.342 | switch2 log | interface,info ether3 link down |
| 20.865 | step | Cable host1 to switch2 back |
| 20.873 | cable | host1:eth2 set up |
| 20.874 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 20.970 | switch2 log | interface,info host1 link up |
| 21.001 | switch2 log | bridge,stp host1:0  becomes Designated |
| 21.002 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_SYNCED |
| 21.002 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_LEARN |
| 21.004 | switch2 log | bridge,stp host1:0  learning |
| 21.004 | switch2 log | bridge,stp,debug host1:0  role transition DESIGNATED\_FORWARD |
| 21.006 | switch2 log | bridge,stp host1:0  forwarding |
| 21.351 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.877 | steps | last step ended |
| 30.289 | state | check after the steps: pass |
| 30.289 | state | Both switches show MLAG connected. pass |
| 30.289 | state | Both switches run RSTP. pass |
| 30.289 | state | Both MLAG peers are the RSTP root bridge. pass |
| 30.289 | state | Every bridge port of both peers forwards, and the host ports are edge ports. pass |
| 30.289 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.289 | streams | measurement ended; captures wait for final replies |
| 30.793 | stopped | captures and streams stopped |
| 30.818 | switch1 log | script,info networka bond-member-loss end |
| 30.856 | switch2 log | script,info networka bond-member-loss end |
| 30.864 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
