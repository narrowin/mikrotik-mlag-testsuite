# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 1 at one ping every 100 ms | 0 to 0.208091 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 25 at one ping every 100 ms | 2.50288 to 2.70975 s | pass |
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
| Whole test | switch1 -2.32519 to 30.0068 s, switch2 -1.77659 to 30.0595 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 3.82631 to 8.84443 s | must ether3 link down | pass | 2026-11-28T08:09:22.782813+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 8.84443 to 15.8628 s | must ether3 link up | pass | 2026-11-28T08:09:27.800506+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 15.8628 to 20.8798 s | must ether3 link down | pass | 2026-11-28T08:09:35.149440+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 20.8798 to 27.8956 s | must ether3 link up | pass | 2026-11-28T08:09:40.160445+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.905 | test | bond-member-loss started in lab small-mlag |
| -2.325 | switch1 log | script,info networka bond-member-loss start |
| -1.777 | switch2 log | script,info networka bond-member-loss start |
| -1.773 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.119 | state | check before the steps: pass |
| -0.119 | state | Both switches show MLAG connected. pass |
| -0.119 | state | Both switches run with spanning tree off. pass |
| -0.119 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:bond0 |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host1:eth2 |
| -0.062 | capture | started at host2:bond0 |
| -0.062 | capture | started at host3:bond0 |
| -0.062 | capture | started at switch1:eth2 |
| -0.062 | capture | started at switch2:eth2 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.002 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.826 | quiet window | clean |
| 3.826 | step | Cable host1 to switch1 down |
| 3.842 | cable | host1:eth1 set down |
| 3.844 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 1 ms |
| 3.953 | switch1 log | interface,info host1 link down |
| 4.197 | switch1 log | interface,info ether3 link down |
| 8.844 | step | Cable host1 to switch1 back |
| 8.860 | cable | host1:eth1 set up |
| 8.862 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.904 | switch1 log | interface,info host1 link up |
| 9.214 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.863 | step | Cable host1 to switch2 down |
| 15.876 | cable | host1:eth2 set down |
| 15.877 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 15.908 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 15.972 | switch2 log | interface,info host1 link down |
| 16.563 | switch2 log | interface,info ether3 link down |
| 20.880 | step | Cable host1 to switch2 back |
| 20.891 | cable | host1:eth2 set up |
| 20.893 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 20.922 | switch2 log | interface,info host1 link up |
| 20.958 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.503 to 2.71 s, reply absent at source |
| 21.574 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 27.896 | steps | last step ended |
| 29.461 | state | check after the steps: pass |
| 29.461 | state | Both switches show MLAG connected. pass |
| 29.461 | state | Both switches run with spanning tree off. pass |
| 29.461 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.461 | streams | measurement ended; captures wait for final replies |
| 29.968 | stopped | captures and streams stopped |
| 30.007 | switch1 log | script,info networka bond-member-loss end |
| 30.059 | switch2 log | script,info networka bond-member-loss end |
| 30.064 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
