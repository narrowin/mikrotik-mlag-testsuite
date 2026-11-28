# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.207877 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 3 at one ping every 100 ms | 0.209278 to 0.416981 s | pass |
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
| Whole test | switch1 -2.84478 to 30.5219 s, switch2 -2.28089 to 30.5652 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.80078 to 8.81962 s | must ether3 link down | pass | 2026-11-28T07:33:02.101386+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.81962 to 15.8326 s | must ether3 link up | pass | 2026-11-28T07:33:07.115492+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8326 to 20.8461 s | must ether3 link down | pass | 2026-11-28T07:33:13.784728+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8461 to 27.8634 s | must ether3 link up | pass | 2026-11-28T07:33:18.814980+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.419 | test | bond-member-loss started in lab small-strict |
| -2.845 | switch1 log | script,info networka bond-member-loss start |
| -2.281 | switch2 log | script,info networka bond-member-loss start |
| -2.274 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | Both switches show MLAG connected. pass |
| -0.116 | state | Both switches run with spanning tree off. pass |
| -0.116 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.116 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host1:eth2 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host3:bond0 |
| -0.059 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.003 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.800 | quiet window | clean |
| 3.801 | step | Cable host1 to switch1 down |
| 3.815 | cable | host1:eth1 set down |
| 3.817 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 1 ms |
| 3.908 | switch1 log | interface,info host1 link down |
| 4.343 | switch1 log | interface,info ether3 link down |
| 8.820 | step | Cable host1 to switch1 back |
| 8.830 | cable | host1:eth1 set up |
| 8.832 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 1 ms |
| 9.357 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.391 | switch1 log | interface,info host1 link up |
| 15.833 | step | Cable host1 to switch2 down |
| 15.844 | cable | host1:eth2 set down |
| 15.846 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 1 ms |
| 15.896 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 15.901 | switch2 log | interface,info host1 link down |
| 16.026 | switch2 log | interface,info ether3 link down |
| 20.846 | step | Cable host1 to switch2 back |
| 20.860 | cable | host1:eth2 set up |
| 20.862 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 21.056 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.381 | switch2 log | interface,info host1 link up |
| 23.440 | host1-to-host2 | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.417 s, reply absent at source |
| 27.863 | steps | last step ended |
| 29.979 | state | check after the steps: pass |
| 29.979 | state | Both switches show MLAG connected. pass |
| 29.979 | state | Both switches run with spanning tree off. pass |
| 29.979 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 29.979 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.979 | streams | measurement ended; captures wait for final replies |
| 30.484 | stopped | captures and streams stopped |
| 30.522 | switch1 log | script,info networka bond-member-loss end |
| 30.565 | switch2 log | script,info networka bond-member-loss end |
| 30.568 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
