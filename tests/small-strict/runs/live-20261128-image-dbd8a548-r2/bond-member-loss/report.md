# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.208083 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 1 at one ping every 100 ms | 0 to 0.209666 s | pass |
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
| Whole test | switch1 -2.89262 to 30.6486 s, switch2 -2.33319 to 30.6893 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.91525 to 8.93422 s | must ether3 link down | pass | 2026-11-28T07:29:30.493412+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.93422 to 15.9466 s | must ether3 link up | pass | 2026-11-28T07:29:35.530740+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.9466 to 20.9588 s | must ether3 link down | pass | 2026-11-28T07:29:42.118133+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.9588 to 27.9722 s | must ether3 link up | pass | 2026-11-28T07:29:47.124734+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.468 | test | bond-member-loss started in lab small-strict |
| -2.893 | switch1 log | script,info networka bond-member-loss start |
| -2.333 | switch2 log | script,info networka bond-member-loss start |
| -2.329 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both switches show MLAG connected. pass |
| -0.119 | state | Both switches run with spanning tree off. pass |
| -0.119 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.062 | capture | started at host1:eth1 |
| -0.061 | capture | started at host1:eth2 |
| -0.061 | capture | started at host2:bond0 |
| -0.061 | capture | started at host3:bond0 |
| -0.061 | capture | started at switch1:eth2 |
| -0.061 | capture | started at switch2:eth2 |
| -0.006 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.004 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.915 | quiet window | clean |
| 3.915 | step | Cable host1 to switch1 down |
| 3.931 | cable | host1:eth1 set down |
| 3.933 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 4.004 | switch1 log | interface,info host1 link down |
| 4.833 | switch1 log | interface,info ether3 link down |
| 8.934 | step | Cable host1 to switch1 back |
| 8.945 | cable | host1:eth1 set up |
| 8.946 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 1 ms |
| 9.870 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.482 | switch1 log | interface,info host1 link up |
| 15.947 | step | Cable host1 to switch2 down |
| 15.957 | cable | host1:eth2 set down |
| 15.958 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 1 ms |
| 16.003 | switch2 log | interface,info host1 link down |
| 16.009 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 16.458 | switch2 log | interface,info ether3 link down |
| 20.959 | step | Cable host1 to switch2 back |
| 20.968 | cable | host1:eth2 set up |
| 20.970 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 1 ms |
| 21.464 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 23.592 | switch2 log | interface,info host1 link up |
| 23.663 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 27.972 | steps | last step ended |
| 30.095 | state | check after the steps: pass |
| 30.095 | state | Both switches show MLAG connected. pass |
| 30.095 | state | Both switches run with spanning tree off. pass |
| 30.095 | state | Every host bond runs with lacp-strict=yes and min-links=1 on both switches. pass |
| 30.095 | state | Both cables of every host are eligible in its LACP bond. pass |
| 30.095 | streams | measurement ended; captures wait for final replies |
| 30.600 | stopped | captures and streams stopped |
| 30.649 | switch1 log | script,info networka bond-member-loss end |
| 30.689 | switch2 log | script,info networka bond-member-loss end |
| 30.693 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
