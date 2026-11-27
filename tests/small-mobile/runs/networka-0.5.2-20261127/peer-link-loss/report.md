# PASS — peer-link-loss

Withdraw the peer link at both switches, watch the LACP peers separate and rejoin, and measure every stream.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Peer cable down | client1:bond0 → client3:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | client2:bond0 → client3:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | client3:bond0 → client1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | client3:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | client1:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | client1:bond0 → client3:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | client2:bond0 → client3:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | client3:bond0 → client1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | client3:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | client1:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Peer cable down state** · pass
- Both peer ports have lost carrier and MLAG is disconnected. · pass

**Peer cable back state** · pass
- Both peer ports have carrier again and the peers are connected. · pass

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

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.947 | test | peer-link-loss started in lab small-mlag-mobile |
| -1.656 | switch1 log | script,info networka peer-link-loss start |
| -1.365 | switch2 log | script,info networka peer-link-loss start |
| -1.361 | switch log | marker 'networka peer-link-loss start' written on switch1, switch2 |
| -0.129 | state | check before the steps: pass |
| -0.129 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.129 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.124 | capture | started at client1:bond0 |
| -0.124 | capture | started at client2:bond0 |
| -0.120 | capture | started at client3:bond0 |
| -0.118 | capture | started at switch1:eth1 |
| -0.064 | capture | started at switch2:eth1 |
| -0.010 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.007 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.005 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.003 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.804 | quiet window | clean |
| 3.804 | step | Peer cable down |
| 3.817 | cable | switch1:eth1 set down |
| 3.817 | cable | switch1:eth1 down at both ends |
| 4.170 | switch1 log | interface,info ether2 link down |
| 4.196 | switch1 log | bridge,warning "bridge" peer link down |
| 4.464 | switch2 log | interface,info ether2 link down |
| 4.490 | switch2 log | bridge,warning "bridge" peer link down |
| 19.051 | state | Peer cable down pass |
| 19.051 | step | Peer cable back |
| 19.063 | cable | switch1:eth1 set up |
| 19.063 | cable | switch1:eth1 up at both ends |
| 19.207 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 19.509 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 84.288 | state | Peer cable back pass |
| 84.289 | step | Peer cable recovery |
| 87.291 | steps | last step ended |
| 88.724 | state | check after the steps: pass |
| 88.724 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 88.724 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 88.724 | streams | measurement ended; captures wait for final replies |
| 89.231 | stopped | captures and streams stopped |
| 89.260 | switch1 log | script,info networka peer-link-loss end |
| 89.312 | switch2 log | script,info networka peer-link-loss end |
| 89.324 | switch log | marker 'networka peer-link-loss end' written on switch1, switch2 |
