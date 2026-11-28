# PASS — bond-member-loss

Check that host1 stays reachable when each of its two cables goes down and comes back. The stream from host2 to host3 crosses neither cable and must continue throughout.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cable host1 to switch1 down | host1:bond0 → host2:bond0 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host1:bond0 → host2:bond0 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch1 back | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 down | host1:bond0 → host2:bond0 | 1 s | 2 at one ping every 100 ms | 0.104135 to 0.317504 s | pass |
| Cable host1 to switch2 down | host2:bond0 → host3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable host1 to switch2 back | host1:bond0 → host2:bond0 | 4 s | 23 at one ping every 100 ms | 2.28788 to 2.50135 s | pass |
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
| Whole test | switch1 -2.40325 to 30.333 s, switch2 -1.81273 to 30.3666 s | must\_not heartbeat timeout | pass | not logged |
| Cable host1 to switch1 down | switch1 4.11467 to 9.14103 s | must ether3 link down | pass | 2026-11-28T08:02:32.565451+00:00 switch1 interface,info ether3 link down |
| Cable host1 to switch1 back | switch1 9.14103 to 16.1542 s | must ether3 link up | pass | 2026-11-28T08:02:37.601227+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Cable host1 to switch2 down | switch2 16.1542 to 21.1897 s | must ether3 link down | pass | 2026-11-28T08:02:44.239394+00:00 switch2 interface,info ether3 link down |
| Cable host1 to switch2 back | switch2 21.1897 to 28.2061 s | must ether3 link up | pass | 2026-11-28T08:02:49.243674+00:00 switch2 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.008 | test | bond-member-loss started in lab small-mlag |
| -2.403 | switch1 log | script,info networka bond-member-loss start |
| -1.813 | switch2 log | script,info networka bond-member-loss start |
| -1.804 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.130 | state | check before the steps: pass |
| -0.130 | state | Both switches show MLAG connected. pass |
| -0.130 | state | Both switches run with spanning tree off. pass |
| -0.130 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.072 | capture | started at host1:bond0 |
| -0.072 | capture | started at host1:eth1 |
| -0.071 | capture | started at host1:eth2 |
| -0.071 | capture | started at host2:bond0 |
| -0.071 | capture | started at host3:bond0 |
| -0.071 | capture | started at switch1:eth2 |
| -0.071 | capture | started at switch2:eth2 |
| -0.010 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.0.10.2 |
| -0.007 | host2-to-host3 | started from host2:bond0 to host3:bond0 at 10.0.10.3 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.114 | quiet window | clean |
| 4.115 | step | Cable host1 to switch1 down |
| 4.138 | cable | host1:eth1 set down |
| 4.141 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 3 ms |
| 4.164 | switch1 log | interface,info host1 link down |
| 5.099 | switch1 log | interface,info ether3 link down |
| 9.141 | step | Cable host1 to switch1 back |
| 9.152 | cable | host1:eth1 set up |
| 9.154 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 9.226 | switch1 log | interface,info host1 link up |
| 10.135 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 16.154 | step | Cable host1 to switch2 down |
| 16.186 | cable | host1:eth2 set down |
| 16.188 | cable | host1:eth2 down at both ends, seen at host1:eth2 after 2 ms |
| 16.212 | host1-to-host2 | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.318 s, reply absent at source |
| 16.243 | switch2 log | interface,info host1 link down |
| 16.773 | switch2 log | interface,info ether3 link down |
| 21.190 | step | Cable host1 to switch2 back |
| 21.204 | cable | host1:eth2 set up |
| 21.205 | cable | host1:eth2 up at both ends, seen at host1:eth2 after 2 ms |
| 21.297 | switch2 log | interface,info host1 link up |
| 21.420 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.288 to 2.501 s, reply absent at source, request absent at destination |
| 21.778 | switch2 log | interface,info ether3 link up (speed 10G, full duplex) |
| 28.206 | steps | last step ended |
| 29.789 | state | check after the steps: pass |
| 29.789 | state | Both switches show MLAG connected. pass |
| 29.789 | state | Both switches run with spanning tree off. pass |
| 29.789 | state | Both cables of every host are eligible in its LACP bond. pass |
| 29.790 | streams | measurement ended; captures wait for final replies |
| 30.296 | stopped | captures and streams stopped |
| 30.333 | switch1 log | script,info networka bond-member-loss end |
| 30.367 | switch2 log | script,info networka bond-member-loss end |
| 30.372 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
