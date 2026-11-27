# PASS — bond-member-loss

Withdraw the cable between client1 and switch1, then measure delivery while it returns to the LACP bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Client1 cable to switch1 down | client1:bond0 → client3:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.205309 s | pass |
| Client1 cable to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Client1 cable to switch1 down | client3:bond0 → client1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.211714 s | pass |
| Client1 cable to switch1 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Client1 cable to switch1 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.210313 s | pass |
| Client1 cable to switch1 back | client1:bond0 → client3:bond0 | 3 s | 25 at one ping every 100 ms | 2.50675 to 2.71437 s | pass |
| Client1 cable to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Client1 cable to switch1 back | client3:bond0 → client1:bond0 | 3 s | 26 at one ping every 100 ms | 2.61967 to 2.82616 s | pass |
| Client1 cable to switch1 back | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Client1 cable to switch1 back | client1:bond0 → client2:bond0 | 3 s | 26 at one ping every 100 ms | 2.60087 to 2.80747 s | pass |
| Cable recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Client1 cable to switch1 down state** · pass
- The switch sees no carrier on the withdrawn port. · pass

**Client1 cable to switch1 back state** · pass
- The switch sees carrier on the returned port and its LACP member is working. · pass

**quiet window** · pass

- client1:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client3:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client3:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client3:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client3:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client3:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.70184 to 24.9465 s, switch2 -1.41046 to 24.9803 s | must\_not heartbeat timeout | pass | not logged |
| Client1 cable to switch1 down | switch1 3.81614 to 11.875 s | must ether3 link down | pass | 2026-11-27T08:12:10.314918+00:00 switch1 interface,info ether3 link down |
| Client1 cable to switch1 back | switch1 11.875 to 19.9795 s | must ether3 link up | pass | 2026-11-27T08:12:18.337617+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.001 | test | bond-member-loss started in lab small-mlag-mobile |
| -1.702 | switch1 log | script,info networka bond-member-loss start |
| -1.410 | switch2 log | script,info networka bond-member-loss start |
| -1.403 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.123 | state | check before the steps: pass |
| -0.123 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.123 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.066 | capture | started at client1:bond0 |
| -0.066 | capture | started at client1:eth1 |
| -0.066 | capture | started at client2:bond0 |
| -0.066 | capture | started at client3:bond0 |
| -0.065 | capture | started at switch1:eth2 |
| -0.011 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.008 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.005 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.003 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.816 | quiet window | clean |
| 3.816 | step | Client1 cable to switch1 down |
| 3.831 | cable | client1:eth1 set down |
| 3.833 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 3.850 | client1-to-mobile | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 3.857 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 3.860 | switch1 log | interface,info client1 link down |
| 3.874 | mobile-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, request absent at destination |
| 4.111 | switch1 log | interface,info ether3 link down |
| 11.875 | state | Client1 cable to switch1 down pass |
| 11.875 | step | Client1 cable to switch1 back |
| 11.883 | cable | client1:eth1 set up |
| 11.884 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 11.889 | switch1 log | interface,info client1 link up |
| 11.905 | client1-to-client2 | 26 pings lost at one ping every 100 ms, traffic stopped for 2.601 to 2.807 s, reply absent at source |
| 11.926 | mobile-to-client1 | 26 pings lost at one ping every 100 ms, traffic stopped for 2.62 to 2.826 s, request absent at destination |
| 11.969 | client1-to-mobile | 25 pings lost at one ping every 100 ms, traffic stopped for 2.507 to 2.714 s, reply absent at source |
| 12.133 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 19.979 | state | Client1 cable to switch1 back pass |
| 19.979 | step | Cable recovery |
| 22.980 | steps | last step ended |
| 24.399 | state | check after the steps: pass |
| 24.399 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 24.399 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 24.399 | streams | measurement ended; captures wait for final replies |
| 24.904 | stopped | captures and streams stopped |
| 24.947 | switch1 log | script,info networka bond-member-loss end |
| 24.980 | switch2 log | script,info networka bond-member-loss end |
| 24.984 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
