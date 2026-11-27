# FAIL — bond-member-loss

Check that client1 stays reachable when each of its two cables goes down and comes back. The stream from client2 to client3 crosses neither cable and must continue throughout.

- Step Cable client1 to switch2 down is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable client1 to switch1 down | client1:bond0 → client2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 down | client1:bond0 → client2:bond0 | 1 s | 43 at one ping every 100 ms | 4.39178 to 4.60168 s | fail |
| Cable client1 to switch2 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 back | client1:bond0 → client2:bond0 | 4 s | 24 at one ping every 100 ms | 2.40658 to 2.615 s | pass |
| Cable client1 to switch2 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -2.55706 to 30.0741 s, switch2 -1.88803 to 30.1117 s | must\_not heartbeat timeout | pass | not logged |
| Cable client1 to switch1 down | switch1 3.84348 to 8.87035 s | must ether3 link down | pass | 2026-11-27T07:53:49.022537+00:00 switch1 interface,info ether3 link down |
| Cable client1 to switch1 back | switch1 8.87035 to 15.89 s | must ether3 link up | pass | 2026-11-27T07:53:54.038497+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable client1 to switch2 down | switch2 15.89 to 20.9094 s | must ether3 link down | pass | 2026-11-27T07:54:01.136456+00:00 switch2 interface,info ether3 link down |
| Cable client1 to switch2 back | switch2 20.9094 to 27.927 s | must ether3 link up | pass | 2026-11-27T07:54:06.143122+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.183 | test | bond-member-loss started in lab small-mlag |
| -2.557 | switch1 log | script,info networka bond-member-loss start |
| -1.888 | switch2 log | script,info networka bond-member-loss start |
| -1.876 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.130 | state | check before the steps: pass |
| -0.130 | state | Both switches show MLAG connected. pass |
| -0.130 | state | Both switches run with spanning tree off. pass |
| -0.130 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.069 | capture | started at client1:bond0 |
| -0.068 | capture | started at client1:eth1 |
| -0.068 | capture | started at client1:eth2 |
| -0.068 | capture | started at client2:bond0 |
| -0.068 | capture | started at client3:bond0 |
| -0.068 | capture | started at switch1:eth2 |
| -0.068 | capture | started at switch2:eth2 |
| -0.009 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.007 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.843 | quiet window | clean |
| 3.843 | step | Cable client1 to switch1 down |
| 3.867 | cable | client1:eth1 set down |
| 3.869 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 3.967 | switch1 log | interface,info client1 link down |
| 4.416 | switch1 log | interface,info ether3 link down |
| 8.870 | step | Cable client1 to switch1 back |
| 8.886 | cable | client1:eth1 set up |
| 8.888 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 8.913 | switch1 log | interface,info client1 link up |
| 9.432 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.890 | step | Cable client1 to switch2 down |
| 15.907 | cable | client1:eth2 set down |
| 15.909 | cable | client1:eth2 down at both ends, seen at client1:eth2 after 2 ms |
| 15.911 | client1-to-client2 | 43 pings lost at one ping every 100 ms, traffic stopped for 4.392 to 4.602 s, reply absent at source |
| 16.008 | switch2 log | interface,info client1 link down |
| 16.530 | switch2 log | interface,info ether3 link down |
| 20.909 | step | Cable client1 to switch2 back |
| 20.923 | cable | client1:eth2 set up |
| 20.925 | cable | client1:eth2 up at both ends, seen at client1:eth2 after 2 ms |
| 20.957 | switch2 log | interface,info client1 link up |
| 21.021 | client1-to-client2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.407 to 2.615 s, reply absent at source |
| 21.537 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.927 | steps | last step ended |
| 29.529 | state | check after the steps: pass |
| 29.529 | state | Both switches show MLAG connected. pass |
| 29.529 | state | Both switches run with spanning tree off. pass |
| 29.529 | state | Both cables of every client are eligible in its LACP bond. pass |
| 29.530 | streams | measurement ended; captures wait for final replies |
| 30.035 | stopped | captures and streams stopped |
| 30.074 | switch1 log | script,info networka bond-member-loss end |
| 30.112 | switch2 log | script,info networka bond-member-loss end |
| 30.122 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
