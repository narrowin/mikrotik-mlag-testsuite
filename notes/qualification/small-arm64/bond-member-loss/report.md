# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.206281 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 2 at one ping every 100 ms | 0.102219 to 0.308697 s | pass |
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
| Whole test | switch1 -2.1446 to 30.1134 s, switch2 -1.80887 to 30.1426 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.88544 to 8.90904 s | must ether3 link down | pass | 2026-11-27T22:53:07.632153+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.90904 to 15.9248 s | must ether3 link up | pass | 2026-11-27T22:53:12.649709+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.9248 to 20.9409 s | must ether3 link down | pass | 2026-11-27T22:53:20.388369+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.9409 to 27.9551 s | must ether3 link up | pass | 2026-11-27T22:53:25.400168+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.489 | test | bond-member-loss started in lab small-mlag |
| -2.145 | switch1 log | script,info networka bond-member-loss start |
| -1.809 | switch2 log | script,info networka bond-member-loss start |
| -1.801 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both switches show MLAG connected. pass |
| -0.118 | state | Both switches run with spanning tree off. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.111 | capture | started at host1:bond0 |
| -0.111 | capture | started at host1:eth1 |
| -0.110 | capture | started at host1:eth2 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.059 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.885 | quiet window | clean |
| 3.885 | step | Cable host1 to switch1 down |
| 3.905 | cable | host1:eth1 set down |
| 3.907 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.959 | switch1 log | interface,info host1 link down |
| 4.033 | switch1 log | interface,info ether3 link down |
| 8.909 | step | Cable host1 to switch1 back |
| 8.922 | cable | host1:eth1 set up |
| 8.924 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 9.051 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.447 | switch1 log | interface,info host1 link up |
| 15.925 | step | Cable host1 to switch2 down |
| 15.937 | cable | host1:eth2 set down |
| 15.939 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.959 | switch2 log | interface,info host1 link down |
| 15.982 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 16.790 | switch2 log | interface,info ether3 link down |
| 20.941 | step | Cable host1 to switch2 back |
| 20.952 | cable | host1:eth2 set up |
| 20.954 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 21.801 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.540 | switch2 log | interface,info host1 link up |
| 23.648 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.309 s, reply absent at source |
| 27.955 | steps | last step ended |
| 29.559 | state | check after the steps: pass |
| 29.559 | state | Both switches show MLAG connected. pass |
| 29.559 | state | Both switches run with spanning tree off. pass |
| 29.559 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.559 | streams | measurement ended; captures wait for final replies |
| 30.076 | stopped | captures and streams stopped |
| 30.113 | switch1 log | script,info networka bond-member-loss end |
| 30.143 | switch2 log | script,info networka bond-member-loss end |
| 30.147 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
