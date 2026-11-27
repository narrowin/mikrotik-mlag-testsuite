# PASS — member-flap-repeat

Flap the cable from client1 to switch1 five times. Measure each flap and check that the streams that do not cross this cable keep delivering.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Flap 1 down | client1:bond0 → client3:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208393 s | pass |
| Flap 1 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | client3:bond0 → client1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208472 s | pass |
| Flap 1 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208435 s | pass |
| Flap 1 up | client1:bond0 → client3:bond0 | 3 s | 25 at one ping every 100 ms | 2.5023 to 2.70496 s | pass |
| Flap 1 up | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | client3:bond0 → client1:bond0 | 3 s | 25 at one ping every 100 ms | 2.50532 to 2.71004 s | pass |
| Flap 1 up | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 1 up | client1:bond0 → client2:bond0 | 3 s | 25 at one ping every 100 ms | 2.50161 to 2.70458 s | pass |
| Flap 2 down | client1:bond0 → client3:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.207989 s | pass |
| Flap 2 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | client3:bond0 → client1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208039 s | pass |
| Flap 2 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.213493 s | pass |
| Flap 2 up | client1:bond0 → client3:bond0 | 3 s | 24 at one ping every 100 ms | 2.40427 to 2.6087 s | pass |
| Flap 2 up | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | client3:bond0 → client1:bond0 | 3 s | 25 at one ping every 100 ms | 2.49609 to 2.70118 s | pass |
| Flap 2 up | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 2 up | client1:bond0 → client2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39151 to 2.60101 s | pass |
| Flap 3 down | client1:bond0 → client3:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | client3:bond0 → client1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.205549 s | pass |
| Flap 3 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.214273 s | pass |
| Flap 3 up | client1:bond0 → client3:bond0 | 3 s | 25 at one ping every 100 ms | 2.49505 to 2.70045 s | pass |
| Flap 3 up | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | client3:bond0 → client1:bond0 | 3 s | 25 at one ping every 100 ms | 2.50397 to 2.71767 s | pass |
| Flap 3 up | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 3 up | client1:bond0 → client2:bond0 | 3 s | 25 at one ping every 100 ms | 2.51362 to 2.7194 s | pass |
| Flap 4 down | client1:bond0 → client3:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.208036 s | pass |
| Flap 4 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | client3:bond0 → client1:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.211787 s | pass |
| Flap 4 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.20903 s | pass |
| Flap 4 up | client1:bond0 → client3:bond0 | 3 s | 25 at one ping every 100 ms | 2.50349 to 2.7079 s | pass |
| Flap 4 up | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | client3:bond0 → client1:bond0 | 3 s | 26 at one ping every 100 ms | 2.6022 to 2.80455 s | pass |
| Flap 4 up | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 4 up | client1:bond0 → client2:bond0 | 3 s | 25 at one ping every 100 ms | 2.49885 to 2.7034 s | pass |
| Flap 5 down | client1:bond0 → client3:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.207553 s | pass |
| Flap 5 down | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | client3:bond0 → client1:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 down | client1:bond0 → client2:bond0 | 3 s | 1 at one ping every 100 ms | 0 to 0.205916 s | pass |
| Flap 5 up | client1:bond0 → client3:bond0 | 3 s | 23 at one ping every 100 ms | 2.30076 to 2.5126 s | pass |
| Flap 5 up | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | client3:bond0 → client1:bond0 | 3 s | 24 at one ping every 100 ms | 2.39336 to 2.6002 s | pass |
| Flap 5 up | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap 5 up | client1:bond0 → client2:bond0 | 3 s | 24 at one ping every 100 ms | 2.39225 to 2.60171 s | pass |
| Flap recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Flap recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Bridge host entries

**pass**
- switch1 · 80 samples across 11 steps, longest interval 0.355093 s.
- switch2 · 80 samples across 11 steps, longest interval 0.354781 s.

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.68992 to 33.9734 s, switch2 -1.40142 to 34.0171 s | must\_not heartbeat timeout | pass | not logged |
| Flap 1 down | switch1 3.81367 to 4.82854 s | must ether3 link down | pass | 2026-11-27T08:13:26.501442+00:00 switch1 interface,info ether3 link down |
| Flap 1 up | switch1 4.82854 to 7.84343 s | must ether3 link up | pass | 2026-11-27T08:13:27.499832+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 2 down | switch1 7.84343 to 8.85755 s | must ether3 link down | pass | 2026-11-27T08:13:30.515241+00:00 switch1 interface,info ether3 link down |
| Flap 2 up | switch1 8.85755 to 11.8674 s | must ether3 link up | pass | 2026-11-27T08:13:31.525201+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 3 down | switch1 11.8674 to 12.8802 s | must ether3 link down | pass | 2026-11-27T08:13:34.533762+00:00 switch1 interface,info ether3 link down |
| Flap 3 up | switch1 12.8802 to 15.8913 s | must ether3 link up | pass | 2026-11-27T08:13:35.531150+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 4 down | switch1 15.8913 to 16.9015 s | must ether3 link down | pass | 2026-11-27T08:13:38.538466+00:00 switch1 interface,info ether3 link down |
| Flap 4 up | switch1 16.9015 to 19.9119 s | must ether3 link up | pass | 2026-11-27T08:13:39.547337+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |
| Flap 5 down | switch1 19.9119 to 20.9275 s | must ether3 link down | pass | 2026-11-27T08:13:42.567575+00:00 switch1 interface,info ether3 link down |
| Flap 5 up | switch1 20.9275 to 28.9406 s | must ether3 link up | pass | 2026-11-27T08:13:43.576573+00:00 switch1 interface,info ether3 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.979 | test | member-flap-repeat started in lab small-mlag-mobile |
| -1.690 | switch1 log | script,info networka member-flap-repeat start |
| -1.401 | switch2 log | script,info networka member-flap-repeat start |
| -1.394 | switch log | marker 'networka member-flap-repeat start' written on switch1, switch2 |
| -0.122 | state | check before the steps: pass |
| -0.122 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.122 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.065 | capture | started at client1:bond0 |
| -0.065 | capture | started at client1:eth1 |
| -0.065 | capture | started at client2:bond0 |
| -0.065 | capture | started at client3:bond0 |
| -0.065 | capture | started at switch1:eth2 |
| -0.010 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.008 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.006 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.004 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.812 | quiet window | clean |
| 3.813 | state | watching bridge host entries on switch1, switch2 |
| 3.814 | step | Flap 1 down |
| 3.825 | cable | client1:eth1 set down |
| 3.827 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 3.851 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 3.851 | client1-to-mobile | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 3.863 | mobile-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 3.879 | switch1 log | interface,info client1 link down |
| 4.195 | switch1 log | interface,info ether3 link down |
| 4.829 | step | Flap 1 up |
| 4.840 | cable | client1:eth1 set up |
| 4.843 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 4.870 | switch1 log | interface,info client1 link up |
| 4.898 | mobile-to-client1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.505 to 2.71 s, request absent at destination |
| 4.976 | client1-to-mobile | 25 pings lost at one ping every 100 ms, traffic stopped for 2.502 to 2.705 s, reply absent at source, request absent at destination |
| 4.992 | client1-to-client2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.502 to 2.705 s, reply absent at source, request absent at destination |
| 5.194 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 7.843 | step | Flap 2 down |
| 7.855 | cable | client1:eth1 set down |
| 7.857 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 7.894 | client1-to-mobile | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 7.918 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.213 s, reply absent at source |
| 7.926 | mobile-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 7.950 | switch1 log | interface,info client1 link down |
| 8.209 | switch1 log | interface,info ether3 link down |
| 8.858 | step | Flap 2 up |
| 8.865 | cable | client1:eth1 set up |
| 8.866 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 1 ms |
| 8.938 | switch1 log | interface,info client1 link up |
| 8.963 | mobile-to-client1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.496 to 2.701 s, request absent at destination |
| 9.024 | client1-to-mobile | 24 pings lost at one ping every 100 ms, traffic stopped for 2.404 to 2.609 s, reply absent at source, request absent at destination |
| 9.060 | client1-to-client2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.392 to 2.601 s, reply absent at source, request absent at destination |
| 9.219 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 11.867 | step | Flap 3 down |
| 11.876 | mobile-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 11.877 | cable | client1:eth1 set down |
| 11.879 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 11.884 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.214 s, reply absent at source |
| 11.911 | switch1 log | interface,info client1 link down |
| 12.228 | switch1 log | interface,info ether3 link down |
| 12.880 | step | Flap 3 up |
| 12.888 | cable | client1:eth1 set up |
| 12.890 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 12.901 | switch1 log | interface,info client1 link up |
| 12.929 | client1-to-client2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.514 to 2.719 s, reply absent at source, request absent at destination |
| 12.972 | client1-to-mobile | 25 pings lost at one ping every 100 ms, traffic stopped for 2.495 to 2.7 s, reply absent at source, request absent at destination |
| 13.011 | mobile-to-client1 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.504 to 2.718 s, request absent at destination |
| 13.225 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 15.891 | step | Flap 4 down |
| 15.899 | cable | client1:eth1 set down |
| 15.901 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 15.931 | mobile-to-client1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, request absent at destination |
| 15.963 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 15.981 | switch1 log | interface,info client1 link down |
| 15.988 | client1-to-mobile | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 16.232 | switch1 log | interface,info ether3 link down |
| 16.901 | step | Flap 4 up |
| 16.909 | cable | client1:eth1 set up |
| 16.911 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 16.969 | switch1 log | interface,info client1 link up |
| 16.987 | mobile-to-client1 | 26 pings lost at one ping every 100 ms, traffic stopped for 2.602 to 2.805 s, request absent at destination |
| 17.009 | client1-to-client2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.499 to 2.703 s, reply absent at source |
| 17.021 | client1-to-mobile | 25 pings lost at one ping every 100 ms, traffic stopped for 2.503 to 2.708 s, reply absent at source |
| 17.241 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 19.912 | step | Flap 5 down |
| 19.923 | cable | client1:eth1 set down |
| 19.923 | client1-to-client2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 19.925 | cable | client1:eth1 down at both ends, seen at client1:eth1 after 2 ms |
| 19.940 | client1-to-mobile | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 19.943 | switch1 log | interface,info client1 link down |
| 20.262 | switch1 log | interface,info ether3 link down |
| 20.928 | step | Flap 5 up |
| 20.936 | cable | client1:eth1 set up |
| 20.938 | cable | client1:eth1 up at both ends, seen at client1:eth1 after 2 ms |
| 21.040 | switch1 log | interface,info client1 link up |
| 21.155 | mobile-to-client1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.393 to 2.6 s, request absent at destination |
| 21.172 | client1-to-client2 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.392 to 2.602 s, reply absent at source |
| 21.184 | client1-to-mobile | 23 pings lost at one ping every 100 ms, traffic stopped for 2.301 to 2.513 s, reply absent at source |
| 21.271 | switch1 log | interface,info ether3 link up (speed 10G, full duplex) |
| 28.941 | step | Flap recovery |
| 31.965 | state | bridge host-entry sampling stopped |
| 31.966 | steps | last step ended |
| 33.425 | state | check after the steps: pass |
| 33.425 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 33.425 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 33.425 | streams | measurement ended; captures wait for final replies |
| 33.940 | stopped | captures and streams stopped |
| 33.973 | switch1 log | script,info networka member-flap-repeat end |
| 34.017 | switch2 log | script,info networka member-flap-repeat end |
| 34.019 | switch log | marker 'networka member-flap-repeat end' written on switch1, switch2 |
