# PASS — member-flap-repeat

Flap the cable from host1 to switch1 five times. Measure each flap and check that the streams that do not cross this cable keep delivering.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Flap 1 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.204948 s | pass |
| Flap 1 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.212264 s | pass |
| Flap 1 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.209626 s | pass |
| Flap 1 up | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.39103 to 2.59414 s | pass |
| Flap 1 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.40139 to 2.60769 s | pass |
| Flap 1 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | host1:bond0 → host2:bond0 | 3 s | 23 at one ping every 100 ms | 2.29997 to 2.50679 s | pass |
| Flap 2 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.211628 s | pass |
| Flap 2 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.21197 s | pass |
| Flap 2 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | host1:bond0 → host2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208886 s | pass |
| Flap 2 up | host1:bond0 → mac-move-host:bond0 | 3 s | 23 at one ping every 100 ms | 2.29262 to 2.49959 s | pass |
| Flap 2 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | mac-move-host:bond0 → host1:bond0 | 3 s | 23 at one ping every 100 ms | 2.28485 to 2.49151 s | pass |
| Flap 2 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | host1:bond0 → host2:bond0 | 3 s | 23 at one ping every 100 ms | 2.28841 to 2.49052 s | pass |
| Flap 3 down | host1:bond0 → mac-move-host:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | mac-move-host:bond0 → host1:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | host1:bond0 → host2:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | host1:bond0 → mac-move-host:bond0 | 3 s | 25 at one ping every 100 ms | 2.49472 to 2.6999 s | pass |
| Flap 3 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | mac-move-host:bond0 → host1:bond0 | 3 s | 25 at one ping every 100 ms | 2.50379 to 2.70918 s | pass |
| Flap 3 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | host1:bond0 → host2:bond0 | 3 s | 25 at one ping every 100 ms | 2.50057 to 2.70495 s | pass |
| Flap 4 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.211154 s | pass |
| Flap 4 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.21206 s | pass |
| Flap 4 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | host1:bond0 → host2:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.40625 to 2.61848 s | pass |
| Flap 4 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | mac-move-host:bond0 → host1:bond0 | 3 s | 25 at one ping every 100 ms | 2.50797 to 2.7132 s | pass |
| Flap 4 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | host1:bond0 → host2:bond0 | 3 s | 25 at one ping every 100 ms | 2.5127 to 2.72099 s | pass |
| Flap 5 down | host1:bond0 → mac-move-host:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208256 s | pass |
| Flap 5 down | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | mac-move-host:bond0 → host1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.209964 s | pass |
| Flap 5 down | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | host1:bond0 → host2:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | host1:bond0 → mac-move-host:bond0 | 3 s | 24 at one ping every 100 ms | 2.40097 to 2.60308 s | pass |
| Flap 5 up | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | mac-move-host:bond0 → host1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39518 to 2.60247 s | pass |
| Flap 5 up | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | host1:bond0 → host2:bond0 | 3 s | 24 at one ping every 100 ms | 2.40656 to 2.62113 s | pass |
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
- switch1 · 76 samples across 11 steps, longest interval 0.353528 s.
- switch2 · 76 samples across 11 steps, longest interval 0.353172 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.89519 to 34.1487 s, switch2 -1.53549 to 34.1982 s | must\_not heartbeat timeout | pass | not logged |
| Flap 1 down | switch1 3.90937 to 4.9363 s | must ether3 link down | pass | 2026-11-28T07:06:39.232963+00:00 switch1 interface,info ether3 link down |
| Flap 1 up | switch1 4.9363 to 7.96225 s | must ether3 link up | pass | 2026-11-28T07:06:40.239212+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 2 down | switch1 7.96225 to 8.98206 s | must ether3 link down | pass | 2026-11-28T07:06:43.232426+00:00 switch1 interface,info ether3 link down |
| Flap 2 up | switch1 8.98206 to 12.0011 s | must ether3 link up | pass | 2026-11-28T07:06:44.238488+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 3 down | switch1 12.0011 to 13.0222 s | must ether3 link down | pass | 2026-11-28T07:06:47.242281+00:00 switch1 interface,info ether3 link down |
| Flap 3 up | switch1 13.0222 to 16.0602 s | must ether3 link up | pass | 2026-11-28T07:06:48.238849+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 4 down | switch1 16.0602 to 17.0769 s | must ether3 link down | pass | 2026-11-28T07:06:51.245456+00:00 switch1 interface,info ether3 link down |
| Flap 4 up | switch1 17.0769 to 20.0971 s | must ether3 link up | pass | 2026-11-28T07:06:52.246121+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 5 down | switch1 20.0971 to 21.1149 s | must ether3 link down | pass | 2026-11-28T07:06:55.256476+00:00 switch1 interface,info ether3 link down |
| Flap 5 up | switch1 21.1149 to 29.1348 s | must ether3 link up | pass | 2026-11-28T07:06:56.263593+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.389 | test | member-flap-repeat started in lab small-mlag-mac-move |
| -1.895 | switch1 log | script,info networka member-flap-repeat start |
| -1.535 | switch2 log | script,info networka member-flap-repeat start |
| -1.526 | switch log | marker 'networka member-flap-repeat start' written on switch1, switch2 |
| -0.137 | state | check before the steps: pass |
| -0.137 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.137 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.079 | capture | started at host1:bond0 |
| -0.079 | capture | started at host1:eth1 |
| -0.079 | capture | started at host2:bond0 |
| -0.079 | capture | started at mac-move-host:bond0 |
| -0.079 | capture | started at switch1:eth2 |
| -0.022 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.017 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.013 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.008 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.908 | quiet window | clean |
| 3.908 | state | watching bridge host entries on switch1, switch2 |
| 3.909 | step | Flap 1 down |
| 3.934 | cable | host1:eth1 set down |
| 3.936 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 4.015 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, request absent at destination |
| 4.016 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 4.019 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 4.020 | switch1 log | interface,info host1 link down |
| 4.417 | switch1 log | interface,info ether3 link down |
| 4.936 | step | Flap 1 up |
| 4.960 | cable | host1:eth1 set up |
| 4.962 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 5.012 | switch1 log | interface,info host1 link up |
| 5.133 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.401 to 2.608 s, request absent at destination |
| 5.136 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.391 to 2.594 s, reply absent at source, request absent at destination |
| 5.148 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.3 to 2.507 s, reply absent at source |
| 5.423 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 7.962 | step | Flap 2 down |
| 7.980 | cable | host1:eth1 set down |
| 7.981 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 8.047 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, reply absent at source |
| 8.056 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, request absent at destination |
| 8.071 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 8.091 | switch1 log | interface,info host1 link down |
| 8.417 | switch1 log | interface,info ether3 link down |
| 8.982 | step | Flap 2 up |
| 8.998 | cable | host1:eth1 set up |
| 9.000 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 9.085 | switch1 log | interface,info host1 link up |
| 9.162 | host1-to-mac-move-host | 23 pings lost at one ping every 100 ms, traffic stopped for 2.293 to 2.5 s, reply absent at source, request absent at destination |
| 9.169 | mac-move-host-to-host1 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.285 to 2.492 s, request absent at destination |
| 9.200 | host1-to-host2 | 23 pings lost at one ping every 100 ms, traffic stopped for 2.288 to 2.491 s, reply absent at source, request absent at destination |
| 9.423 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 12.001 | step | Flap 3 down |
| 12.019 | cable | host1:eth1 set down |
| 12.022 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 12.050 | switch1 log | interface,info host1 link down |
| 12.426 | switch1 log | interface,info ether3 link down |
| 13.022 | step | Flap 3 up |
| 13.056 | cable | host1:eth1 set up |
| 13.060 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 3 ms |
| 13.149 | switch1 log | interface,info host1 link up |
| 13.200 | mac-move-host-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.504 to 2.709 s, request absent at destination |
| 13.208 | host1-to-mac-move-host | 25 pings lost at one ping every 100 ms, traffic stopped for 2.495 to 2.7 s, reply absent at source |
| 13.227 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.501 to 2.705 s, reply absent at source |
| 13.423 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 16.060 | step | Flap 4 down |
| 16.074 | cable | host1:eth1 set down |
| 16.077 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 16.118 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, request absent at destination |
| 16.118 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 16.122 | switch1 log | interface,info host1 link down |
| 16.430 | switch1 log | interface,info ether3 link down |
| 17.077 | step | Flap 4 up |
| 17.092 | cable | host1:eth1 set up |
| 17.094 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 17.109 | switch1 log | interface,info host1 link up |
| 17.147 | mac-move-host-to-host1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.508 to 2.713 s, request absent at destination |
| 17.175 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.513 to 2.721 s, reply absent at source, request absent at destination |
| 17.236 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.406 to 2.618 s, reply absent at source, request absent at destination |
| 17.430 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 20.097 | step | Flap 5 down |
| 20.113 | cable | host1:eth1 set down |
| 20.114 | cable | host1:eth1 down at both ends, seen at host1:eth1 after 2 ms |
| 20.166 | host1-to-mac-move-host | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 20.171 | mac-move-host-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 20.190 | switch1 log | interface,info host1 link down |
| 20.441 | switch1 log | interface,info ether3 link down |
| 21.115 | step | Flap 5 up |
| 21.131 | cable | host1:eth1 set up |
| 21.133 | cable | host1:eth1 up at both ends, seen at host1:eth1 after 2 ms |
| 21.179 | switch1 log | interface,info host1 link up |
| 21.203 | mac-move-host-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.395 to 2.602 s, request absent at destination |
| 21.248 | host1-to-host2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.407 to 2.621 s, reply absent at source |
| 21.288 | host1-to-mac-move-host | 24 pings lost at one ping every 100 ms, traffic stopped for 2.401 to 2.603 s, reply absent at source |
| 21.448 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 29.135 | step | Flap recovery |
| 32.137 | state | bridge host-entry sampling stopped |
| 32.138 | steps | last step ended |
| 33.605 | state | check after the steps: pass |
| 33.605 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 33.605 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 33.605 | streams | measurement ended; captures wait for final replies |
| 34.114 | stopped | captures and streams stopped |
| 34.149 | switch1 log | script,info networka member-flap-repeat end |
| 34.198 | switch2 log | script,info networka member-flap-repeat end |
| 34.201 | switch log | marker 'networka member-flap-repeat end' written on switch1, switch2 |
