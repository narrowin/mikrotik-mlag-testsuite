# FAIL — bond-member-loss

Check that client1 stays reachable when each of its two cables goes down and comes back. The stream from client2 to client3 crosses neither cable and must continue throughout.

- Step Cable client1 to switch2 down is fail.
- Step Cable client1 to switch2 back is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable client1 to switch1 down | client1:bond0 → client2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client1:bond0 → client2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 down | client1:bond0 → client2:bond0 | 1 s | 73 at one ping every 100 ms | 7.49089 to 7.69914 s | fail |
| Cable client1 to switch2 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable client1 to switch2 back | client1:bond0 → client2:bond0 | 4 s | 73 at one ping every 100 ms | 7.49089 to 7.69914 s | fail |
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
| Whole test | switch1 -3.33887 to 31.4715 s, switch2 -2.72051 to 31.5008 s | must\_not heartbeat timeout | pass | not logged |
| Cable client1 to switch1 down | switch1 3.81642 to 8.84473 s | must ether3 link down | pass | 2026-11-27T07:57:10.147122+00:00 switch1 interface,info ether3 link down |
| Cable client1 to switch1 back | switch1 8.84473 to 15.865 s | must ether3 link up | pass | 2026-11-27T07:57:15.154737+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable client1 to switch2 down | switch2 15.865 to 20.8821 s | must ether3 link down | pass | 2026-11-27T07:57:22.353414+00:00 switch2 interface,info ether3 link down |
| Cable client1 to switch2 back | switch2 20.8821 to 27.9006 s | must ether3 link up | pass | 2026-11-27T07:57:27.382100+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.983 | test | bond-member-loss started in lab small-mlag-rstp |
| -3.339 | switch1 log | script,info networka bond-member-loss start |
| -2.721 | switch2 log | script,info networka bond-member-loss start |
| -2.712 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.126 | state | check before the steps: pass |
| -0.126 | state | Both switches show MLAG connected. pass |
| -0.126 | state | Both switches run RSTP. pass |
| -0.126 | state | Both MLAG peers are the RSTP root bridge. pass |
| -0.126 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| -0.126 | state | Both cables of every client are eligible in its LACP bond. pass |
| -0.115 | capture | started at client1:bond0 |
| -0.114 | capture | started at client1:eth1 |
| -0.112 | capture | started at client1:eth2 |
| -0.111 | capture | started at client2:bond0 |
| -0.111 | capture | started at client3:bond0 |
| -0.111 | capture | started at switch1:eth2 |
| -0.059 | capture | started at switch2:eth2 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.0.10.2 |
| -0.001 | client2-to-client3 | started from client2:bond0 to client3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.816 | quiet window | clean |
| 3.816 | step | Cable client1 to switch1 down |
| 3.839 | cable | client1:eth1 set down |
| 3.841 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 3.920 | switch1 log | interface,info client1 link down |
| 4.109 | switch1 log | interface,info ether3 link down |
| 8.845 | step | Cable client1 to switch1 back |
| 8.862 | cable | client1:eth1 set up |
| 8.864 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 8.878 | switch1 log | interface,info client1 link up |
| 8.929 | switch1 log | bridge,stp client1:0  becomes Designated |
| 8.930 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 8.931 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_LEARN |
| 8.932 | switch1 log | bridge,stp client1:0  learning |
| 8.932 | switch1 log | bridge,stp,debug client1:0  role transition DESIGNATED\_FORWARD |
| 8.933 | switch1 log | bridge,stp client1:0  forwarding |
| 9.117 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.865 | step | Cable client1 to switch2 down |
| 15.880 | cable | client1:eth2 set down |
| 15.882 | cable | client1:eth2 down at both ends, seen at client1:eth2 after 2 ms |
| 15.896 | client1-to-client2 | 73 pings lost at one ping every 100 ms, traffic stopped for 7.491 to 7.699 s, reply absent at source |
| 15.958 | switch2 log | interface,info client1 link down |
| 16.315 | switch2 log | interface,info ether3 link down |
| 20.882 | step | Cable client1 to switch2 back |
| 20.898 | cable | client1:eth2 set up |
| 20.900 | cable | client1:eth2 up at both ends, seen at client1:eth2 after 2 ms |
| 20.906 | switch2 log | interface,info client1 link up |
| 20.931 | switch2 log | bridge,stp client1:0  becomes Designated |
| 20.932 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_SYNCED |
| 20.932 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_LEARN |
| 20.933 | switch2 log | bridge,stp client1:0  learning |
| 20.935 | switch2 log | bridge,stp,debug client1:0  role transition DESIGNATED\_FORWARD |
| 20.938 | switch2 log | bridge,stp client1:0  forwarding |
| 21.344 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.901 | steps | last step ended |
| 30.936 | state | check after the steps: pass |
| 30.936 | state | Both switches show MLAG connected. pass |
| 30.936 | state | Both switches run RSTP. pass |
| 30.936 | state | Both MLAG peers are the RSTP root bridge. pass |
| 30.936 | state | Every bridge port of both peers forwards, and the client ports are edge ports. pass |
| 30.936 | state | Both cables of every client are eligible in its LACP bond. pass |
| 30.936 | streams | measurement ended; captures wait for final replies |
| 31.443 | stopped | captures and streams stopped |
| 31.472 | switch1 log | script,info networka bond-member-loss end |
| 31.501 | switch2 log | script,info networka bond-member-loss end |
| 31.503 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
