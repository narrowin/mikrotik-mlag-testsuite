# PASS — bond-member-loss

Check that client1 stays reachable when each of its two cables goes down and comes back. The stream from client2 to client3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable client1 to switch1 down | client1:bond0 → client2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 down | client1:bond0 → client2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.208647 s | pass |
| Cable client1 to switch2 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 back | client1:bond0 → client2:bond0 | 4 s | 24 at one ping every 100 ms | 2.42515 to 2.63643 s | pass |
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
| Whole test | switch1 -3.27394 to 30.8008 s, switch2 -2.66293 to 30.8379 s | must\_not heartbeat timeout | pass | not logged |
| Cable client1 to switch1 down | switch1 3.81641 to 8.83766 s | must ether3 link down | pass | 2026-11-27T06:16:18.563193+00:00 switch1 interface,info ether3 link down |
| Cable client1 to switch1 back | switch1 8.83766 to 15.8559 s | must ether3 link up | pass | 2026-11-27T06:16:23.558561+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable client1 to switch2 down | switch2 15.8559 to 20.8688 s | must ether3 link down | pass | 2026-11-27T06:16:30.392216+00:00 switch2 interface,info ether3 link down |
| Cable client1 to switch2 back | switch2 20.8688 to 27.8803 s | must ether3 link up | pass | 2026-11-27T06:16:35.394518+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.923 | test | bond-member-loss started in lab small-mlag-rstp |
| -3.274 | switch1 log | script,info networka bond-member-loss start |
| -2.663 | switch2 log | script,info networka bond-member-loss start |
| -2.659 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.129 | state | check before the steps: pass |
| -0.129 | state | Both switches show MLAG connected. pass |
| -0.129 | state | Both switches run RSTP. pass |
| -0.129 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.129 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.129 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.121 | capture | started at client1:bond0 |
| -0.120 | capture | started at client1:eth1 |
| -0.120 | capture | started at client1:eth2 |
| -0.120 | capture | started at client2:bond0 |
| -0.068 | capture | started at client3:bond0 |
| -0.068 | capture | started at switch1:eth2 |
| -0.068 | capture | started at switch2:eth2 |
| -0.014 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.005 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.816 | quiet window | clean |
| 3.816 | step | Cable client1 to switch1 down |
| 3.835 | cable | client1:eth1 set down |
| 3.837 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 3.908 | switch1 log | interface,info client1 link down |
| 4.070 | switch1 log | interface,info ether3 link down |
| 8.838 | step | Cable client1 to switch1 back |
| 8.851 | cable | client1:eth1 set up |
| 8.853 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 8.861 | switch1 log | interface,info client1 link up |
| 8.896 | switch1 log | bridge,stp client1:0  becomes Designated |
| 8.896 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 8.897 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_LEARN |
| 8.899 | switch1 log | bridge,stp client1:0  learning |
| 8.899 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_FORWARD |
| 8.900 | switch1 log | bridge,stp client1:0  forwarding |
| 9.066 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.856 | step | Cable client1 to switch2 down |
| 15.866 | cable | client1:eth2 set down |
| 15.868 | cable | client1:eth2 down at both ends, seen at client1:eth2 after 2 ms |
| 15.899 | switch2 log | interface,info ether3 link down |
| 15.959 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 15.978 | switch2 log | interface,info client1 link down |
| 20.869 | step | Cable client1 to switch2 back |
| 20.878 | cable | client1:eth2 set up |
| 20.880 | cable | client1:eth2 up at both ends, seen at client1:eth2 after 2 ms |
| 20.902 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 20.926 | switch2 log | interface,info client1 link up |
| 20.936 | switch2 log | bridge,stp client1:0  becomes Designated |
| 20.937 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 20.937 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_LEARN |
| 20.940 | switch2 log | bridge,stp client1:0  learning |
| 20.940 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_FORWARD |
| 20.943 | switch2 log | bridge,stp client1:0  forwarding |
| 21.026 | client1-to-client2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.425 to 2.636 s, reply absent at source |
| 27.880 | steps | last step ended |
| 30.251 | state | check after the steps: pass |
| 30.251 | state | Both switches show MLAG connected. pass |
| 30.251 | state | Both switches run RSTP. pass |
| 30.251 | state | Both MLAG peers are the RSTP root bridge. pass |
| 30.251 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| 30.251 | state | Both cables of every client are eligible in its LACP bond. pass |
| 30.251 | streams | measurement ended; captures wait for final replies |
| 30.755 | stopped | captures and streams stopped |
| 30.801 | switch1 log | script,info networka bond-member-loss end |
| 30.838 | switch2 log | script,info networka bond-member-loss end |
| 30.841 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
