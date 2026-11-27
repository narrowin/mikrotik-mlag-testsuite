# PASS — member-flap-repeat

Flap the cable from host1 to switch1 five times. Measure each flap and check that the streams that do not cross this cable keep delivering.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Flap 1 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.209031 s | pass |
| Flap 1 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.210068 s | pass |
| Flap 1 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.209575 s | pass |
| Flap 1 up | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.40173 to 2.60473 s | pass |
| Flap 1 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39039 to 2.59502 s | pass |
| Flap 1 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.40109 to 2.60809 s | pass |
| Flap 2 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208409 s | pass |
| Flap 2 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.211064 s | pass |
| Flap 2 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.207061 s | pass |
| Flap 2 up | host1:bond0 → mac-move-host:bond0 | 3 s | 26 at one ping every 100 ms | 2.60088 to 2.80391 s | pass |
| Flap 2 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | mac-move-host:bond0 → host1:bond0 | 3 s | 25 at one ping every 100 ms | 2.50655 to 2.71117 s | pass |
| Flap 2 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | host1:bond0 → host2:bond0 | 3 s | 25 at one ping every 100 ms | 2.49805 to 2.70301 s | pass |
| Flap 3 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.21098 s | pass |
| Flap 3 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | mac-move-host:bond0 → host1:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | host1:bond0 → host2:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | host1:bond0 → mac-move-host:bond0 | 3 s | 25 at one ping every 100 ms | 2.49366 to 2.6987 s | pass |
| Flap 3 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39529 to 2.60366 s | pass |
| Flap 3 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39202 to 2.60091 s | pass |
| Flap 4 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.212103 s | pass |
| Flap 4 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.207936 s | pass |
| Flap 4 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.206766 s | pass |
| Flap 4 up | host1:bond0 → mac-move-host:bond0 | 3 s | 25 at one ping every 100 ms | 2.49786 to 2.70493 s | pass |
| Flap 4 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | mac-move-host:bond0 → host1:bond0 | 3 s | 25 at one ping every 100 ms | 2.49946 to 2.70568 s | pass |
| Flap 4 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39294 to 2.60008 s | pass |
| Flap 5 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.210377 s | pass |
| Flap 5 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.204996 s | pass |
| Flap 5 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.210134 s | pass |
| Flap 5 up | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.39905 to 2.60346 s | pass |
| Flap 5 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39133 to 2.59448 s | pass |
| Flap 5 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39893 to 2.60447 s | pass |
| Flap recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Bridge host entries

**pass**
- switch1 · 80 samples across 11 steps, longest interval 0.354867 s.
- switch2 · 80 samples across 11 steps, longest interval 0.3536 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.70642 to 33.9683 s, switch2 -1.40644 to 34.0103 s | must\_not heartbeat timeout | pass | not logged |
| Flap 1 down | switch1 3.8289 to 4.84917 s | must ether3 link down | pass | 2026-11-27T09:15:10.303060+00:00 switch1 interface,info ether3 link down |
| Flap 1 up | switch1 4.84917 to 7.86076 s | must ether3 link up | pass | 2026-11-27T09:15:11.296715+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 2 down | switch1 7.86076 to 8.87435 s | must ether3 link down | pass | 2026-11-27T09:15:14.314038+00:00 switch1 interface,info ether3 link down |
| Flap 2 up | switch1 8.87435 to 11.8867 s | must ether3 link up | pass | 2026-11-27T09:15:15.324626+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 3 down | switch1 11.8867 to 12.899 s | must ether3 link down | pass | 2026-11-27T09:15:18.351422+00:00 switch1 interface,info ether3 link down |
| Flap 3 up | switch1 12.899 to 15.9132 s | must ether3 link up | pass | 2026-11-27T09:15:19.352181+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 4 down | switch1 15.9132 to 16.9284 s | must ether3 link down | pass | 2026-11-27T09:15:22.355824+00:00 switch1 interface,info ether3 link down |
| Flap 4 up | switch1 16.9284 to 19.9415 s | must ether3 link up | pass | 2026-11-27T09:15:23.357243+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 5 down | switch1 19.9415 to 20.9553 s | must ether3 link down | pass | 2026-11-27T09:15:26.357989+00:00 switch1 interface,info ether3 link down |
| Flap 5 up | switch1 20.9553 to 28.9662 s | must ether3 link up | pass | 2026-11-27T09:15:27.366550+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.020 | test | member-flap-repeat started in lab small-mlag-mac-move |
| -1.706 | switch1 log | script,info networka member-flap-repeat start |
| -1.406 | switch2 log | script,info networka member-flap-repeat start |
| -1.400 | switch log | marker 'networka member-flap-repeat start' written on switch1, switch2 |
| -0.124 | state | check before the steps: pass |
| -0.124 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.124 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.064 | capture | started at host1:bond0 |
| -0.064 | capture | started at host1:eth1 |
| -0.064 | capture | started at host2:bond0 |
| -0.064 | capture | started at mac-move-host:bond0 |
| -0.064 | capture | started at switch1:eth2 |
| -0.009 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.007 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.005 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.827 | quiet window | clean |
| 3.828 | state | watching bridge host entries on switch1, switch2 |
| 3.829 | step | Flap 1 down |
| 3.844 | cable | host1:eth1 set down |
| 3.847 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 3.847 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 3.870 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 3.887 | switch1 log | interface,info host1 link down |
| 3.894 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 4.592 | switch1 log | interface,info ether3 link down |
| 4.849 | step | Flap 1 up |
| 4.858 | cable | host1:eth1 set up |
| 4.860 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 1 ms |
| 4.876 | switch1 log | interface,info host1 link up |
| 4.919 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.401 to 2.608 s, reply absent at source |
| 4.967 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.402 to 2.605 s, reply absent at source, request absent at destination |
| 5.001 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.39 to 2.595 s, request absent at destination |
| 5.585 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 7.861 | step | Flap 2 down |
| 7.871 | cable | host1:eth1 set down |
| 7.873 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 1 ms |
| 7.888 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 7.919 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 7.942 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 7.958 | switch1 log | interface,info host1 link down |
| 8.603 | switch1 log | interface,info ether3 link down |
| 8.874 | step | Flap 2 up |
| 8.883 | cable | host1:eth1 set up |
| 8.885 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 8.944 | switch1 log | interface,info host1 link up |
| 9.016 | host1-to-mac-move-host | 26 pings lost at one ping every 100 ms, traffic stopped for 2.601 to 2.804 s, reply absent at source |
| 9.052 | mac-move-host-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.507 to 2.711 s, request absent at destination |
| 9.060 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.498 to 2.703 s, reply absent at source |
| 9.613 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.887 | step | Flap 3 down |
| 11.897 | cable | host1:eth1 set down |
| 11.899 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 11.911 | switch1 log | interface,info host1 link down |
| 11.928 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 12.640 | switch1 log | interface,info ether3 link down |
| 12.899 | step | Flap 3 up |
| 12.909 | cable | host1:eth1 set up |
| 12.912 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 3 ms |
| 13.014 | switch1 log | interface,info host1 link up |
| 13.057 | host1-to-mac-move-host | 25 pings lost at one ping every 100 ms, traffic stopped for 2.494 to 2.699 s, reply absent at source |
| 13.100 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.395 to 2.604 s, request absent at destination |
| 13.118 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.392 to 2.601 s, reply absent at source |
| 13.641 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.913 | step | Flap 4 down |
| 15.924 | cable | host1:eth1 set down |
| 15.925 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 15.926 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 15.966 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, reply absent at source |
| 15.986 | switch1 log | interface,info host1 link down |
| 16.015 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 16.645 | switch1 log | interface,info ether3 link down |
| 16.928 | step | Flap 4 up |
| 16.937 | cable | host1:eth1 set up |
| 16.939 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 16.971 | switch1 log | interface,info host1 link up |
| 16.996 | host1-to-mac-move-host | 25 pings lost at one ping every 100 ms, traffic stopped for 2.498 to 2.705 s, reply absent at source |
| 17.034 | mac-move-host-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.499 to 2.706 s, request absent at destination |
| 17.063 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.393 to 2.6 s, reply absent at source |
| 17.646 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 19.942 | step | Flap 5 down |
| 19.952 | cable | host1:eth1 set down |
| 19.954 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 19.975 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 20.017 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 20.046 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 20.055 | switch1 log | interface,info host1 link down |
| 20.647 | switch1 log | interface,info ether3 link down |
| 20.955 | step | Flap 5 up |
| 20.964 | cable | host1:eth1 set up |
| 20.966 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 21.047 | switch1 log | interface,info host1 link up |
| 21.104 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.399 to 2.604 s, reply absent at source, request absent at destination |
| 21.137 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.399 to 2.603 s, reply absent at source, request absent at destination |
| 21.161 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.391 to 2.594 s, request absent at destination |
| 21.655 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 28.966 | step | Flap recovery |
| 31.969 | state | bridge host-entry sampling stopped |
| 31.969 | steps | last step ended |
| 33.437 | state | check after the steps: pass |
| 33.437 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 33.437 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 33.437 | streams | measurement ended; captures wait for final replies |
| 33.942 | stopped | captures and streams stopped |
| 33.968 | switch1 log | script,info networka member-flap-repeat end |
| 34.010 | switch2 log | script,info networka member-flap-repeat end |
| 34.014 | switch log | marker 'networka member-flap-repeat end' written on switch1, switch2 |
