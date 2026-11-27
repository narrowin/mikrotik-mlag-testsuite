# PASS — bond-member-loss

Check that client1 stays reachable when each of its two cables goes down and comes back. The stream from client2 to client3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable client1 to switch1 down | client1:bond0 → client2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 down | client1:bond0 → client2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 back | client1:bond0 → client2:bond0 | 4 s | 24 at one ping every 100 ms | 2.3994 to 2.60738 s | pass |
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
| Whole test | switch1 -2.43798 to 29.9984 s, switch2 -1.8366 to 30.0265 s | must\_not heartbeat timeout | pass | not logged |
| Cable client1 to switch1 down | switch1 3.79131 to 8.80315 s | must ether3 link down | pass | 2026-11-26T18:41:19.999064+00:00 switch1 interface,info ether3 link down |
| Cable client1 to switch1 back | switch1 8.80315 to 15.8131 s | must ether3 link up | pass | 2026-11-26T18:41:25.008173+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable client1 to switch2 down | switch2 15.8131 to 20.8255 s | must ether3 link down | pass | 2026-11-26T18:41:31.858915+00:00 switch2 interface,info ether3 link down |
| Cable client1 to switch2 back | switch2 20.8255 to 27.8392 s | must ether3 link up | pass | 2026-11-26T18:41:36.852734+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.033 | test | bond-member-loss started in lab small-mlag |
| -2.438 | switch1 log | script,info networka bond-member-loss start |
| -1.837 | switch2 log | script,info networka bond-member-loss start |
| -1.832 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.115 | state | check before the steps: pass |
| -0.115 | state | Both switches show MLAG connected. pass |
| -0.115 | state | Both switches run with spanning tree off. pass |
| -0.115 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.110 | capture | started at client1:bond0 |
| -0.109 | capture | started at client1:eth1 |
| -0.109 | capture | started at client1:eth2 |
| -0.109 | capture | started at client2:bond0 |
| -0.058 | capture | started at client3:bond0 |
| -0.057 | capture | started at switch1:eth2 |
| -0.057 | capture | started at switch2:eth2 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.791 | quiet window | clean |
| 3.791 | step | Cable client1 to switch1 down |
| 3.801 | cable | client1:eth1 set down |
| 3.802 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 1 ms |
| 3.912 | switch1 log | interface,info client1 link down |
| 4.619 | switch1 log | interface,info ether3 link down |
| 8.803 | step | Cable client1 to switch1 back |
| 8.811 | cable | client1:eth1 set up |
| 8.812 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 1 ms |
| 8.861 | switch1 log | interface,info client1 link up |
| 9.628 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.813 | step | Cable client1 to switch2 down |
| 15.823 | cable | client1:eth2 set down |
| 15.825 | cable | client1:eth2 down at both ends, seen at client1:eth2 after 1 ms |
| 15.835 | switch2 log | interface,info client1 link down |
| 16.479 | switch2 log | interface,info ether3 link down |
| 20.825 | step | Cable client1 to switch2 back |
| 20.836 | cable | client1:eth2 set up |
| 20.838 | cable | client1:eth2 up at both ends, seen at client1:eth2 after 2 ms |
| 20.895 | switch2 log | interface,info client1 link up |
| 21.013 | client1-to-client2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.399 to 2.607 s, reply absent at source |
| 21.473 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.839 | steps | last step ended |
| 29.446 | state | check after the steps: pass |
| 29.446 | state | Both switches show MLAG connected. pass |
| 29.446 | state | Both switches run with spanning tree off. pass |
| 29.446 | state | Both cables of every client are eligible in its LACP bond. pass |
| 29.447 | streams | measurement ended; captures wait for final replies |
| 29.953 | stopped | captures and streams stopped |
| 29.998 | switch1 log | script,info networka bond-member-loss end |
| 30.027 | switch2 log | script,info networka bond-member-loss end |
| 30.028 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
