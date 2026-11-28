# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 2 at one ping every 100 ms | 0.107169 to 0.314787 s | pass |
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
| Whole test | switch1 -2.94809 to 30.5611 s, switch2 -2.35584 to 30.6036 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.81252 to 8.82718 s | must ether3 link down | pass | 2026-11-28T07:26:03.110237+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.82718 to 15.8411 s | must ether3 link up | pass | 2026-11-28T07:26:08.135367+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8411 to 20.854 s | must ether3 link down | pass | 2026-11-28T07:26:15.902544+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.854 to 27.8652 s | must ether3 link up | pass | 2026-11-28T07:26:20.903831+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.534 | test | bond-member-loss started in lab small-strict |
| -2.948 | switch1 log | script,info networka bond-member-loss start |
| -2.356 | switch2 log | script,info networka bond-member-loss start |
| -2.350 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both switches show MLAG connected. pass |
| -0.119 | state | Both switches run with spanning tree off. pass |
| -0.119 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.113 | capture | started at host1:bond0 |
| -0.113 | capture | started at host1:eth1 |
| -0.113 | capture | started at host1:eth2 |
| -0.113 | capture | started at host2:bond0 |
| -0.061 | capture | started at host3:bond0 |
| -0.060 | capture | started at switch1:eth2 |
| -0.060 | capture | started at switch2:eth2 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.003 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.812 | quiet window | clean |
| 3.813 | step | Cable host1 to switch1 down |
| 3.823 | cable | host1:eth1 set down |
| 3.824 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.875 | switch1 log | interface,info host1 link down |
| 3.950 | switch1 log | interface,info ether3 link down |
| 8.827 | step | Cable host1 to switch1 back |
| 8.838 | cable | host1:eth1 set up |
| 8.840 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 1 ms |
| 8.976 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.465 | switch1 log | interface,info host1 link up |
| 15.841 | step | Cable host1 to switch2 down |
| 15.852 | cable | host1:eth2 set down |
| 15.854 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.864 | switch2 log | interface,info host1 link down |
| 16.743 | switch2 log | interface,info ether3 link down |
| 20.854 | step | Cable host1 to switch2 back |
| 20.863 | cable | host1:eth2 set up |
| 20.865 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 21.744 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.452 | switch2 log | interface,info host1 link up |
| 23.516 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.315 s, reply absent at source |
| 27.865 | steps | last step ended |
| 30.006 | state | check after the steps: pass |
| 30.006 | state | Both switches show MLAG connected. pass |
| 30.006 | state | Both switches run with spanning tree off. pass |
| 30.006 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 30.006 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.006 | streams | measurement ended; captures wait for final replies |
| 30.513 | stopped | captures and streams stopped |
| 30.561 | switch1 log | script,info networka bond-member-loss end |
| 30.604 | switch2 log | script,info networka bond-member-loss end |
| 30.610 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
