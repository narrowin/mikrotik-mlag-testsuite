# PASS — mac-age-relearn

Silence the active-backup host beyond the bridge ageing interval and measure how quickly flooding stops once its first frame returns.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Mobile learned | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile learned | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile silent | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

## Intentional interruptions

These measured interruptions include deliberate host silence or power loss at a host. The combined interruption limits remain in force; they are not failover limits for a path that should stay available. Recovery is checked separately below.

| Step | Stream | Cause | Combined limit | Total lost pings | Longest measured interruption | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Mobile silent | host1:bond0 → mac-move-host:bond0 | Host silence | 26 s | 240 at one ping every 100 ms | 24.9253 to 25.1364 s | pass |
| Mobile silent | host2:bond0 → mac-move-host:bond0 | Host silence | 26 s | 241 at one ping every 100 ms | 25.0096 to 25.2132 s | pass |
| Mobile silent | mac-move-host:bond0 → host1:bond0 | Host silence | 26 s | 245 at one ping every 100 ms | 24.9555 to 25.1607 s | pass |
| Mobile silent | mac-move-host:bond0 → host2:bond0 | Host silence | 26 s | 245 at one ping every 100 ms | 24.9517 to 25.1622 s | pass |
| Mobile sends again | host1:bond0 → mac-move-host:bond0 | Host silence | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | host2:bond0 → mac-move-host:bond0 | Host silence | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | mac-move-host:bond0 → host1:bond0 | Host silence | 26 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile sends again | mac-move-host:bond0 → host2:bond0 | Host silence | 26 s | 0 at one ping every 100 ms | 0 s | pass |

## Recovery and state checks

**Mobile learned state** · pass
- Both switches use the ten-second ageing profile and know the MAC address of the MAC-move host. · pass

**Mobile silent state** · pass
- Neither switch holds the MAC address of the MAC-move host during the silence. · pass

**Mobile sends again state** · pass
- Both switches relearned the MAC address of the MAC-move host on the original path. · pass

**Mobile sends again** · pass

- The deliberate silence lasted 25.081 s. The first host frame reached a switch TAP at 33.072 s from the start of the quiet window.
- The relearning limit is 1 s from that first returning host frame, for delivery and the end of unknown-unicast flooding.
- host1:bond0 → mac-move-host:bond0 · first reply 0.000 s after the first host frame.
- host2:bond0 → mac-move-host:bond0 · first reply 0.079 s after the first host frame.
- mac-move-host:bond0 → host1:bond0 · first reply 0.002 s after the first host frame.
- mac-move-host:bond0 → host2:bond0 · first reply 0.034 s after the first host frame.
- host1:bond0 → mac-move-host:bond0 · 0 frames flooded while the host was silent, no flood after its first frame.
- host2:bond0 → mac-move-host:bond0 · 0 frames flooded while the host was silent, no flood after its first frame.

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

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.709 | test | mac-age-relearn started in lab small-mlag-mac-move |
| -2.120 | switch1 log | script,info networka mac-age-relearn start |
| -1.497 | switch2 log | script,info networka mac-age-relearn start |
| -1.480 | switch log | marker 'networka mac-age-relearn start' written on switch1, switch2 |
| -0.141 | state | check before the steps: pass |
| -0.141 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.141 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.120 | capture | started at host1:bond0 |
| -0.120 | capture | started at host1:eth1 |
| -0.120 | capture | started at host1:eth2 |
| -0.120 | capture | started at host2:bond0 |
| -0.119 | capture | started at host2:eth1 |
| -0.119 | capture | started at host2:eth2 |
| -0.119 | capture | started at mac-move-host:bond0 |
| -0.066 | capture | started at switch1:tap4 |
| -0.066 | capture | started at switch2:tap4 |
| -0.011 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.009 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.006 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.817 | quiet window | clean |
| 3.817 | step | Mobile learned |
| 7.971 | state | Mobile learned pass |
| 7.971 | step | Mobile silent |
| 7.984 | mobile host | mac-move-host:bond0 egress filters installed on both members |
| 8.015 | mac-move-host-to-host1 | 245 pings lost at one ping every 100 ms, traffic stopped for 24.955 to 25.161 s, request absent at destination |
| 8.039 | host2-to-mac-move-host | 241 pings lost at one ping every 100 ms, traffic stopped for 25.01 to 25.213 s, reply absent at source |
| 8.042 | host1-to-mac-move-host | 240 pings lost at one ping every 100 ms, traffic stopped for 24.925 to 25.136 s, reply absent at source |
| 8.048 | mac-move-host-to-host2 | 245 pings lost at one ping every 100 ms, traffic stopped for 24.952 to 25.162 s, request absent at destination |
| 33.063 | state | Mobile silent pass |
| 33.063 | step | Mobile sends again |
| 33.075 | mobile host | mac-move-host:bond0 egress filters removed |
| 38.139 | state | Mobile sends again pass |
| 38.139 | step | Mobile recovery |
| 41.140 | steps | last step ended |
| 42.594 | state | check after the steps: pass |
| 42.594 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 42.594 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 42.594 | streams | measurement ended; captures wait for final replies |
| 43.100 | stopped | captures and streams stopped |
| 43.148 | switch1 log | script,info networka mac-age-relearn end |
| 43.197 | switch2 log | script,info networka mac-age-relearn end |
| 43.205 | switch log | marker 'networka mac-age-relearn end' written on switch1, switch2 |
