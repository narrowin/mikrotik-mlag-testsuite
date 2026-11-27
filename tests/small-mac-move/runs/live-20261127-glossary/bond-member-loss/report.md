# PASS — bond-member-loss

Withdraw the cable between host1 and switch1, then measure delivery while it returns to the LACP bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Host1 cable to switch1 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.209185 s | pass |
| Host1 cable to switch1 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208266 s | pass |
| Host1 cable to switch1 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208139 s | pass |
| Host1 cable to switch1 back | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.39289 to 2.59841 s | pass |
| Host1 cable to switch1 back | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 back | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39229 to 2.60194 s | pass |
| Host1 cable to switch1 back | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 back | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39746 to 2.60007 s | pass |
| Cable recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Cable recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Host1 cable to switch1 down state** · pass
- The switch sees no carrier on the withdrawn port. · pass

**Host1 cable to switch1 back state** · pass
- The switch sees carrier on the returned port and its LACP member is working. · pass

**quiet window** · pass

- host1:bond0 → mac-move-host:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → mac-move-host:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- mac-move-host:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- mac-move-host:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → mac-move-host:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → mac-move-host:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- mac-move-host:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- mac-move-host:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.72628 to 24.9344 s, switch2 -1.42818 to 24.98 s | must\_not heartbeat timeout | pass | not logged |
| Host1 cable to switch1 down | switch1 3.80474 to 11.8601 s | must ether3 link down | pass | 2026-11-27T09:13:53.129134+00:00 switch1 interface,info ether3 link down |
| Host1 cable to switch1 back | switch1 11.8601 to 19.9557 s | must ether3 link up | pass | 2026-11-27T09:14:01.137555+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.032 | test | bond-member-loss started in lab small-mlag-mac-move |
| -1.726 | switch1 log | script,info networka bond-member-loss start |
| -1.428 | switch2 log | script,info networka bond-member-loss start |
| -1.423 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.120 | state | check before the steps: pass |
| -0.120 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.120 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.064 | capture | started at host1:bond0 |
| -0.063 | capture | started at host1:eth1 |
| -0.063 | capture | started at host2:bond0 |
| -0.063 | capture | started at mac-move-host:bond0 |
| -0.063 | capture | started at switch1:eth2 |
| -0.010 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.008 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.006 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.804 | quiet window | clean |
| 3.805 | step | Host1 cable to switch1 down |
| 3.814 | cable | host1:eth1 set down |
| 3.816 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.830 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 3.850 | switch1 log | interface,info host1 link down |
| 3.853 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 3.853 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 3.944 | switch1 log | interface,info ether3 link down |
| 11.860 | state | Host1 cable to switch1 down pass |
| 11.860 | step | Host1 cable to switch1 back |
| 11.870 | cable | host1:eth1 set up |
| 11.871 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 11.881 | switch1 log | interface,info host1 link up |
| 11.917 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.392 to 2.602 s, request absent at destination |
| 11.937 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.397 to 2.6 s, reply absent at source, request absent at destination |
| 11.949 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.393 to 2.598 s, reply absent at source, request absent at destination |
| 11.953 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 19.956 | state | Host1 cable to switch1 back pass |
| 19.956 | step | Cable recovery |
| 22.957 | steps | last step ended |
| 24.399 | state | check after the steps: pass |
| 24.399 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 24.399 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 24.399 | streams | measurement ended; captures wait for final replies |
| 24.902 | stopped | captures and streams stopped |
| 24.934 | switch1 log | script,info networka bond-member-loss end |
| 24.980 | switch2 log | script,info networka bond-member-loss end |
| 24.983 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
