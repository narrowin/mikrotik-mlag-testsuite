# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.209653 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 1 at one ping every 100 ms | 0 to 0.212515 s | pass |
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
| Whole test | switch1 -2.8496 to 30.6385 s, switch2 -2.29277 to 30.6901 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.94784 to 8.96767 s | must ether3 link down | pass | 2026-11-28T07:40:01.075023+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.96767 to 15.9834 s | must ether3 link up | pass | 2026-11-28T07:40:06.095096+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.9834 to 20.9979 s | must ether3 link down | pass | 2026-11-28T07:40:12.947360+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.9979 to 28.0102 s | must ether3 link up | pass | 2026-11-28T07:40:17.974493+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.397 | test | bond-member-loss started in lab small-strict |
| -2.850 | switch1 log | script,info networka bond-member-loss start |
| -2.293 | switch2 log | script,info networka bond-member-loss start |
| -2.289 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.117 | state | check before the steps: pass |
| -0.117 | state | Both switches show MLAG connected. pass |
| -0.117 | state | Both switches run with spanning tree off. pass |
| -0.117 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.117 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.058 | capture | started at host1:eth1 |
| -0.058 | capture | started at host1:eth2 |
| -0.058 | capture | started at host2:bond0 |
| -0.058 | capture | started at host3:bond0 |
| -0.058 | capture | started at switch1:eth2 |
| -0.058 | capture | started at switch2:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.001 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.947 | quiet window | clean |
| 3.948 | step | Cable host1 to switch1 down |
| 3.965 | cable | host1:eth1 set down |
| 3.967 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.990 | switch1 log | interface,info host1 link down |
| 4.522 | switch1 log | interface,info ether3 link down |
| 8.968 | step | Cable host1 to switch1 back |
| 8.979 | cable | host1:eth1 set up |
| 8.981 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 9.542 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.479 | switch1 log | interface,info host1 link up |
| 15.983 | step | Cable host1 to switch2 down |
| 15.994 | cable | host1:eth2 set down |
| 15.995 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 1 ms |
| 16.000 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 16.051 | switch2 log | interface,info host1 link down |
| 16.395 | switch2 log | interface,info ether3 link down |
| 20.998 | step | Cable host1 to switch2 back |
| 21.007 | cable | host1:eth2 set up |
| 21.008 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 21.422 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.970 | switch2 log | interface,info host1 link up |
| 24.004 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.213 s, reply absent at source |
| 28.010 | steps | last step ended |
| 30.099 | state | check after the steps: pass |
| 30.099 | state | Both switches show MLAG connected. pass |
| 30.099 | state | Both switches run with spanning tree off. pass |
| 30.099 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 30.099 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.099 | streams | measurement ended; captures wait for final replies |
| 30.604 | stopped | captures and streams stopped |
| 30.639 | switch1 log | script,info networka bond-member-loss end |
| 30.690 | switch2 log | script,info networka bond-member-loss end |
| 30.692 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
