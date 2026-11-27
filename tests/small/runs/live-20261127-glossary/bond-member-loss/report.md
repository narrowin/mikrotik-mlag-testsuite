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
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 73 at one ping every 100 ms | 7.50724 to 7.71446 s | fail |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 73 at one ping every 100 ms | 7.50724 to 7.71446 s | fail |
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
| Whole test | switch1 -2.39131 to 30.0096 s, switch2 -1.81133 to 30.0392 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.8183 to 8.84204 s | must ether3 link down | pass | 2026-11-27T09:13:41.113942+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.84204 to 15.8541 s | must ether3 link up | pass | 2026-11-27T09:13:46.133676+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8541 to 20.8715 s | must ether3 link down | pass | 2026-11-27T09:13:53.000601+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8715 to 27.885 s | must ether3 link up | pass | 2026-11-27T09:13:57.996882+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.979 | test | bond-member-loss started in lab small-mlag |
| -2.391 | switch1 log | script,info networka bond-member-loss start |
| -1.811 | switch2 log | script,info networka bond-member-loss start |
| -1.807 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.128 | state | check before the steps: pass |
| -0.128 | state | Both switches show MLAG connected. pass |
| -0.128 | state | Both switches run with spanning tree off. pass |
| -0.128 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.118 | capture | started at host1:bond0 |
| -0.118 | capture | started at host1:eth1 |
| -0.118 | capture | started at host1:eth2 |
| -0.118 | capture | started at host2:bond0 |
| -0.067 | capture | started at host3:bond0 |
| -0.066 | capture | started at switch1:eth2 |
| -0.064 | capture | started at switch2:eth2 |
| -0.008 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.004 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.818 | quiet window | clean |
| 3.818 | step | Cable host1 to switch1 down |
| 3.837 | cable | host1:eth1 set down |
| 3.839 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.840 | switch1 log | interface,info host1 link down |
| 4.227 | switch1 log | interface,info ether3 link down |
| 8.842 | step | Cable host1 to switch1 back |
| 8.852 | cable | host1:eth1 set up |
| 8.854 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.901 | switch1 log | interface,info host1 link up |
| 9.247 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.854 | step | Cable host1 to switch2 down |
| 15.866 | cable | host1:eth2 set down |
| 15.868 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.920 | switch2 log | interface,info host1 link down |
| 15.965 | host1-to-host2 | 73 pings lost at one ping every 100 ms, traffic stopped for 7.507 to 7.714 s, reply absent at source |
| 16.114 | switch2 log | interface,info ether3 link down |
| 20.871 | step | Cable host1 to switch2 back |
| 20.882 | cable | host1:eth2 set up |
| 20.883 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 20.978 | switch2 log | interface,info host1 link up |
| 21.110 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.885 | steps | last step ended |
| 29.476 | state | check after the steps: pass |
| 29.476 | state | Both switches show MLAG connected. pass |
| 29.476 | state | Both switches run with spanning tree off. pass |
| 29.476 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.477 | streams | measurement ended; captures wait for final replies |
| 29.981 | stopped | captures and streams stopped |
| 30.010 | switch1 log | script,info networka bond-member-loss end |
| 30.039 | switch2 log | script,info networka bond-member-loss end |
| 30.042 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
