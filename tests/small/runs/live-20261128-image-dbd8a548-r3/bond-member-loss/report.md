# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.210948 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 24 at one ping every 100 ms | 2.4016 to 2.60645 s | pass |
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
| Whole test | switch1 -2.39327 to 30.0028 s, switch2 -1.82699 to 30.0331 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.81291 to 8.83227 s | must ether3 link down | pass | 2026-11-28T08:05:51.629012+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.83227 to 15.8506 s | must ether3 link up | pass | 2026-11-28T08:05:56.668402+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8506 to 20.8666 s | must ether3 link down | pass | 2026-11-28T08:06:03.629701+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8666 to 27.8803 s | must ether3 link up | pass | 2026-11-28T08:06:08.656043+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.008 | test | bond-member-loss started in lab small-mlag |
| -2.393 | switch1 log | script,info networka bond-member-loss start |
| -1.827 | switch2 log | script,info networka bond-member-loss start |
| -1.819 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both switches show MLAG connected. pass |
| -0.118 | state | Both switches run with spanning tree off. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:bond0 |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host1:eth2 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.059 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.003 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.813 | quiet window | clean |
| 3.813 | step | Cable host1 to switch1 down |
| 3.826 | cable | host1:eth1 set down |
| 3.828 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 1 ms |
| 3.890 | switch1 log | interface,info host1 link down |
| 4.109 | switch1 log | interface,info ether3 link down |
| 8.832 | step | Cable host1 to switch1 back |
| 8.846 | cable | host1:eth1 set up |
| 8.848 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.949 | switch1 log | interface,info host1 link up |
| 9.149 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.851 | step | Cable host1 to switch2 down |
| 15.864 | cable | host1:eth2 set down |
| 15.866 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.955 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 15.968 | switch2 log | interface,info host1 link down |
| 16.110 | switch2 log | interface,info ether3 link down |
| 20.867 | step | Cable host1 to switch2 back |
| 20.877 | cable | host1:eth2 set up |
| 20.879 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 20.916 | switch2 log | interface,info host1 link up |
| 21.022 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.402 to 2.606 s, reply absent at source, request absent at destination |
| 21.136 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.880 | steps | last step ended |
| 29.466 | state | check after the steps: pass |
| 29.466 | state | Both switches show MLAG connected. pass |
| 29.466 | state | Both switches run with spanning tree off. pass |
| 29.466 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.466 | streams | measurement ended; captures wait for final replies |
| 29.971 | stopped | captures and streams stopped |
| 30.003 | switch1 log | script,info networka bond-member-loss end |
| 30.033 | switch2 log | script,info networka bond-member-loss end |
| 30.035 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
