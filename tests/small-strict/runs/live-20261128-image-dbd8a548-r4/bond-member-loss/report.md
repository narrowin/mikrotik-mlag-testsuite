# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.208793 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 2 at one ping every 100 ms | 0.105579 to 0.308232 s | pass |
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
| Whole test | switch1 -2.90048 to 30.5969 s, switch2 -2.33018 to 30.6461 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.84071 to 8.86181 s | must ether3 link down | pass | 2026-11-28T07:36:35.012574+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.86181 to 15.9084 s | must ether3 link up | pass | 2026-11-28T07:36:40.014133+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.9084 to 20.923 s | must ether3 link down | pass | 2026-11-28T07:36:46.945405+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.923 to 27.9371 s | must ether3 link up | pass | 2026-11-28T07:36:51.966825+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.472 | test | bond-member-loss started in lab small-strict |
| -2.900 | switch1 log | script,info networka bond-member-loss start |
| -2.330 | switch2 log | script,info networka bond-member-loss start |
| -2.323 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both switches show MLAG connected. pass |
| -0.118 | state | Both switches run with spanning tree off. pass |
| -0.118 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.111 | capture | started at host1:bond0 |
| -0.111 | capture | started at host1:eth1 |
| -0.058 | capture | started at host1:eth2 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.058 | capture | started at switch1:eth2 |
| -0.057 | capture | started at switch2:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.002 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.840 | quiet window | clean |
| 3.841 | step | Cable host1 to switch1 down |
| 3.860 | cable | host1:eth1 set down |
| 3.861 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.934 | switch1 log | interface,info host1 link down |
| 4.708 | switch1 log | interface,info ether3 link down |
| 8.862 | step | Cable host1 to switch1 back |
| 8.904 | cable | host1:eth1 set up |
| 8.906 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 9.710 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.413 | switch1 log | interface,info host1 link up |
| 15.908 | step | Cable host1 to switch2 down |
| 15.919 | cable | host1:eth2 set down |
| 15.921 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 1 ms |
| 15.966 | switch2 log | interface,info host1 link down |
| 15.984 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 16.641 | switch2 log | interface,info ether3 link down |
| 20.923 | step | Cable host1 to switch2 back |
| 20.933 | cable | host1:eth2 set up |
| 20.934 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 21.663 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.556 | switch2 log | interface,info host1 link up |
| 23.655 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.308 s, reply absent at source |
| 27.937 | steps | last step ended |
| 30.062 | state | check after the steps: pass |
| 30.062 | state | Both switches show MLAG connected. pass |
| 30.062 | state | Both switches run with spanning tree off. pass |
| 30.062 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 30.062 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.062 | streams | measurement ended; captures wait for final replies |
| 30.569 | stopped | captures and streams stopped |
| 30.597 | switch1 log | script,info networka bond-member-loss end |
| 30.646 | switch2 log | script,info networka bond-member-loss end |
| 30.651 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
