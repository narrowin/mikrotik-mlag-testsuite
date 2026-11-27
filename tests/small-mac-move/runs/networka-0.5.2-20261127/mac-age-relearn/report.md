# PASS — mac-age-relearn

Silence the active-backup host beyond the bridge ageing interval and measure how quickly flooding stops once its first frame returns.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Mobile learned | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile silent | client1:bond0 → client3:bond0 | 26 s | 240 at one ping every 100 ms | 24.9316 to 25.1455 s | pass |
| Mobile silent | client2:bond0 → client3:bond0 | 26 s | 240 at one ping every 100 ms | 24.9486 to 25.154 s | pass |
| Mobile silent | client3:bond0 → client1:bond0 | 26 s | 245 at one ping every 100 ms | 24.9926 to 25.2018 s | pass |
| Mobile silent | client3:bond0 → client2:bond0 | 26 s | 245 at one ping every 100 ms | 24.9365 to 25.1455 s | pass |
| Mobile silent | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | client1:bond0 → client3:bond0 | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | client2:bond0 → client3:bond0 | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | client3:bond0 → client1:bond0 | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | client3:bond0 → client2:bond0 | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Mobile learned state** · pass
- Both switches use the ten-second ageing profile and know the mobile MAC. · pass

**Mobile silent state** · pass
- Neither switch holds the mobile MAC during the silence. · pass

**Mobile sends again state** · pass
- Both switches relearned the mobile MAC on the original path. · pass

**Mobile sends again** · pass

- The hold was 25.063 s. The first host frame reached a switch TAP at 33.054 s from the start of the quiet window.
- client1:bond0 → client3:bond0 · first reply 0.031 s after the first host frame.
- client2:bond0 → client3:bond0 · first reply 0.040 s after the first host frame.
- client3:bond0 → client1:bond0 · first reply 0.057 s after the first host frame.
- client3:bond0 → client2:bond0 · first reply 0.001 s after the first host frame.
- client1:bond0 → client3:bond0 · 0 frames flooded while the host was silent, no flood after its first frame.
- client2:bond0 → client3:bond0 · 0 frames flooded while the host was silent, no flood after its first frame.

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
| -2.653 | test | mac-age-relearn started in lab small-mlag-mobile |
| -2.013 | switch1 log | script,info networka mac-age-relearn start |
| -1.452 | switch2 log | script,info networka mac-age-relearn start |
| -1.436 | switch log | marker 'networka mac-age-relearn start' written on switch1, switch2 |
| -0.141 | state | check before the steps: pass |
| -0.141 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.141 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.117 | capture | started at client1:bond0 |
| -0.117 | capture | started at client1:eth1 |
| -0.117 | capture | started at client1:eth2 |
| -0.117 | capture | started at client2:bond0 |
| -0.117 | capture | started at client2:eth1 |
| -0.117 | capture | started at client2:eth2 |
| -0.066 | capture | started at client3:bond0 |
| -0.066 | capture | started at switch1:tap4 |
| -0.066 | capture | started at switch2:tap4 |
| -0.012 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.009 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.007 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.005 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.003 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.810 | quiet window | clean |
| 3.810 | step | Mobile learned |
| 7.946 | state | Mobile learned pass |
| 7.946 | step | Mobile silent |
| 7.962 | mobile host | client3:bond0 egress filters installed on both members |
| 8.010 | mobile-to-client1 | 245 pings lost at one ping every 100 ms, traffic stopped for 24.993 to 25.202 s, request absent at destination |
| 8.010 | mobile-to-client2 | 245 pings lost at one ping every 100 ms, traffic stopped for 24.937 to 25.145 s, request absent at destination |
| 8.040 | client2-to-mobile | 240 pings lost at one ping every 100 ms, traffic stopped for 24.949 to 25.154 s, reply absent at source |
| 8.047 | client1-to-mobile | 240 pings lost at one ping every 100 ms, traffic stopped for 24.932 to 25.145 s, reply absent at source |
| 33.022 | state | Mobile silent pass |
| 33.023 | step | Mobile sends again |
| 33.035 | mobile host | client3:bond0 egress filters removed |
| 38.092 | state | Mobile sends again pass |
| 38.092 | step | Mobile recovery |
| 41.092 | steps | last step ended |
| 42.526 | state | check after the steps: pass |
| 42.526 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 42.526 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 42.526 | streams | measurement ended; captures wait for final replies |
| 43.032 | stopped | captures and streams stopped |
| 43.061 | switch1 log | script,info networka mac-age-relearn end |
| 43.105 | switch2 log | script,info networka mac-age-relearn end |
| 43.108 | switch log | marker 'networka mac-age-relearn end' written on switch1, switch2 |
