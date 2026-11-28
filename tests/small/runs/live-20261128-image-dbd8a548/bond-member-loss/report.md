# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.207977 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 23 at one ping every 100 ms | 2.29411 to 2.50838 s | pass |
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
| Whole test | switch1 -2.42618 to 30.0257 s, switch2 -1.84719 to 30.0771 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.81958 to 8.84868 s | must ether3 link down | pass | 2026-11-28T07:59:04.002441+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.84868 to 15.8649 s | must ether3 link up | pass | 2026-11-28T07:59:09.000896+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8649 to 20.8798 s | must ether3 link down | pass | 2026-11-28T07:59:16.163260+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8798 to 27.8944 s | must ether3 link up | pass | 2026-11-28T07:59:21.174269+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.194 | test | bond-member-loss started in lab small-mlag |
| -2.426 | switch1 log | script,info networka bond-member-loss start |
| -1.847 | switch2 log | script,info networka bond-member-loss start |
| -1.840 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.118 | state | check before the steps: pass |
| -0.118 | state | Both switches show MLAG connected. pass |
| -0.118 | state | Both switches run with spanning tree off. pass |
| -0.118 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth2 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host3:bond0 |
| -0.060 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.002 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.819 | quiet window | clean |
| 3.820 | step | Cable host1 to switch1 down |
| 3.844 | cable | host1:eth1 set down |
| 3.846 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.925 | switch1 log | interface,info host1 link down |
| 4.400 | switch1 log | interface,info ether3 link down |
| 8.849 | step | Cable host1 to switch1 back |
| 8.860 | cable | host1:eth1 set up |
| 8.862 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.873 | switch1 log | interface,info host1 link up |
| 9.399 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.865 | step | Cable host1 to switch2 down |
| 15.877 | cable | host1:eth2 set down |
| 15.879 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.893 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 15.915 | switch2 log | interface,info host1 link down |
| 16.561 | switch2 log | interface,info ether3 link down |
| 20.880 | step | Cable host1 to switch2 back |
| 20.890 | cable | host1:eth2 set up |
| 20.891 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 20.973 | switch2 log | interface,info host1 link up |
| 21.022 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.294 to 2.508 s, reply absent at source |
| 21.572 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.894 | steps | last step ended |
| 29.486 | state | check after the steps: pass |
| 29.486 | state | Both switches show MLAG connected. pass |
| 29.486 | state | Both switches run with spanning tree off. pass |
| 29.486 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.487 | streams | measurement ended; captures wait for final replies |
| 29.991 | stopped | captures and streams stopped |
| 30.026 | switch1 log | script,info networka bond-member-loss end |
| 30.077 | switch2 log | script,info networka bond-member-loss end |
| 30.083 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
