# PASS — bond-member-loss

Withdraw the cable between host1 and switch1, then measure delivery while it returns to the LACP bond.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Host1 cable to switch1 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.205715 s | pass |
| Host1 cable to switch1 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.207738 s | pass |
| Host1 cable to switch1 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.203711 s | pass |
| Host1 cable to switch1 back | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.39282 to 2.59872 s | pass |
| Host1 cable to switch1 back | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 back | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.40212 to 2.60679 s | pass |
| Host1 cable to switch1 back | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Host1 cable to switch1 back | host1:bond0 → host2:bond0 | 3 s | 23 at one ping every 100 ms | 2.29958 to 2.50364 s | pass |
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
| Whole test | switch1 -1.7861 to 25.0896 s, switch2 -1.47763 to 25.1384 s | must\_not heartbeat timeout | pass | not logged |
| Host1 cable to switch1 down | switch1 3.86366 to 11.9413 s | must ether3 link down | pass | 2026-11-28T07:05:19.023109+00:00 switch1 interface,info ether3 link down |
| Host1 cable to switch1 back | switch1 11.9413 to 20.0465 s | must ether3 link up | pass | 2026-11-28T07:05:27.055765+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.108 | test | bond-member-loss started in lab small-mlag-mac-move |
| -1.786 | switch1 log | script,info networka bond-member-loss start |
| -1.478 | switch2 log | script,info networka bond-member-loss start |
| -1.465 | switch log | marker 'networka bond-member-loss start' written on switch1, switch2 |
| -0.128 | state | check before the steps: pass |
| -0.128 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.128 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.070 | capture | started at host1:bond0 |
| -0.070 | capture | started at host1:eth1 |
| -0.070 | capture | started at host2:bond0 |
| -0.070 | capture | started at mac-move-host:bond0 |
| -0.070 | capture | started at switch1:eth2 |
| -0.013 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.010 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.007 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.863 | quiet window | clean |
| 3.864 | step | Host1 cable to switch1 down |
| 3.892 | cable | host1:eth1 set down |
| 3.896 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 4 ms |
| 3.931 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 3.941 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 3.959 | switch1 log | interface,info host1 link down |
| 3.965 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 4.876 | switch1 log | interface,info ether3 link down |
| 11.941 | state | Host1 cable to switch1 down pass |
| 11.941 | step | Host1 cable to switch1 back |
| 11.960 | cable | host1:eth1 set up |
| 11.963 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 3 ms |
| 11.990 | switch1 log | interface,info host1 link up |
| 12.018 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.393 to 2.599 s, reply absent at source |
| 12.066 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.402 to 2.607 s, request absent at destination |
| 12.103 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.3 to 2.504 s, reply absent at source |
| 12.909 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 20.046 | state | Host1 cable to switch1 back pass |
| 20.047 | step | Cable recovery |
| 23.050 | steps | last step ended |
| 24.544 | state | check after the steps: pass |
| 24.544 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 24.544 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 24.544 | streams | measurement ended; captures wait for final replies |
| 25.049 | stopped | captures and streams stopped |
| 25.090 | switch1 log | script,info networka bond-member-loss end |
| 25.138 | switch2 log | script,info networka bond-member-loss end |
| 25.142 | switch log | marker 'networka bond-member-loss end' written on switch1, switch2 |
