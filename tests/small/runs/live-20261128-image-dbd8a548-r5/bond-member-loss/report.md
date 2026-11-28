# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.209175 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 23 at one ping every 100 ms | 2.31914 to 2.5257 s | pass |
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
| Whole test | switch1 -2.47944 to 30.0362 s, switch2 -1.87205 to 30.0732 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.83541 to 8.85595 s | must ether3 link down | pass | 2026-11-28T08:12:46.238237+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.85595 to 15.8711 s | must ether3 link up | pass | 2026-11-28T08:12:51.240216+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8711 to 20.8881 s | must ether3 link down | pass | 2026-11-28T08:12:58.580103+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8881 to 27.9053 s | must ether3 link up | pass | 2026-11-28T08:13:03.592124+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.073 | test | bond-member-loss started in lab small-mlag |
| -2.479 | switch1 log | script,info networka bond-member-loss start |
| -1.872 | switch2 log | script,info networka bond-member-loss start |
| -1.864 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both switches show MLAG connected. pass |
| -0.119 | state | Both switches run with spanning tree off. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:bond0 |
| -0.061 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth2 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.060 | capture | started at switch1:eth2 |
| -0.060 | capture | started at switch2:eth2 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.002 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.835 | quiet window | clean |
| 3.835 | step | Cable host1 to switch1 down |
| 3.852 | cable | host1:eth1 set down |
| 3.854 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.936 | switch1 log | interface,info host1 link down |
| 4.032 | switch1 log | interface,info ether3 link down |
| 8.856 | step | Cable host1 to switch1 back |
| 8.868 | cable | host1:eth1 set up |
| 8.870 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.884 | switch1 log | interface,info host1 link up |
| 9.034 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.871 | step | Cable host1 to switch2 down |
| 15.885 | cable | host1:eth2 set down |
| 15.887 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.898 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 15.960 | switch2 log | interface,info host1 link down |
| 16.374 | switch2 log | interface,info ether3 link down |
| 20.888 | step | Cable host1 to switch2 back |
| 20.902 | cable | host1:eth2 set up |
| 20.904 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 20.907 | switch2 log | interface,info host1 link up |
| 21.011 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.319 to 2.526 s, reply absent at source, request absent at destination |
| 21.386 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.905 | steps | last step ended |
| 29.484 | state | check after the steps: pass |
| 29.484 | state | Both switches show MLAG connected. pass |
| 29.484 | state | Both switches run with spanning tree off. pass |
| 29.484 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.484 | streams | measurement ended; captures wait for final replies |
| 29.988 | stopped | captures and streams stopped |
| 30.036 | switch1 log | script,info networka bond-member-loss end |
| 30.073 | switch2 log | script,info networka bond-member-loss end |
| 30.076 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
