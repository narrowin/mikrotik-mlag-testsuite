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
| Mobile silent | host1:bond0 → mac-move-host:bond0 | Host silence | 26 s | 240 at one ping every 100 ms | 24.9608 to 25.1686 s | pass |
| Mobile silent | host2:bond0 → mac-move-host:bond0 | Host silence | 26 s | 240 at one ping every 100 ms | 24.9697 to 25.1763 s | pass |
| Mobile silent | mac-move-host:bond0 → host1:bond0 | Host silence | 26 s | 245 at one ping every 100 ms | 24.9117 to 25.1195 s | pass |
| Mobile silent | mac-move-host:bond0 → host2:bond0 | Host silence | 26 s | 246 at one ping every 100 ms | 24.9924 to 25.2017 s | pass |
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

- The deliberate silence lasted 25.075 s. The first host frame reached a switch TAP at 33.119 s from the start of the quiet window.
- The relearning limit is 1 s from that first returning host frame, for delivery and the end of unknown-unicast flooding.
- host1:bond0 → mac-move-host:bond0 · first reply 0.051 s after the first host frame.
- host2:bond0 → mac-move-host:bond0 · first reply 0.017 s after the first host frame.
- mac-move-host:bond0 → host1:bond0 · first reply 0.001 s after the first host frame.
- mac-move-host:bond0 → host2:bond0 · first reply 0.011 s after the first host frame.
- host1:bond0 → mac-move-host:bond0 · 144 frames flooded while the host was silent, no flood after its first frame.
- host2:bond0 → mac-move-host:bond0 · 144 frames flooded while the host was silent, no flood after its first frame.

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
| -2.735 | test | mac-age-relearn started in lab small-mlag-mac-move |
| -2.110 | switch1 log | script,info networka mac-age-relearn start |
| -1.501 | switch2 log | script,info networka mac-age-relearn start |
| -1.493 | switch log | marker 'networka mac-age-relearn start' written on switch1, switch2 |
| -0.152 | state | check before the steps: pass |
| -0.152 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.152 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.116 | capture | started at host1:bond0 |
| -0.116 | capture | started at host1:eth1 |
| -0.115 | capture | started at host1:eth2 |
| -0.115 | capture | started at host2:bond0 |
| -0.115 | capture | started at host2:eth1 |
| -0.115 | capture | started at host2:eth2 |
| -0.115 | capture | started at mac-move-host:bond0 |
| -0.115 | capture | started at switch1:tap4 |
| -0.064 | capture | started at switch2:tap4 |
| -0.011 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.009 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.006 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.847 | quiet window | clean |
| 3.847 | step | Mobile learned |
| 7.991 | state | Mobile learned pass |
| 7.991 | step | Mobile silent |
| 8.008 | mobile host | mac-move-host:bond0 egress filters installed on both members |
| 8.033 | mac-move-host-to-host2 | 246 pings lost at one ping every 100 ms, traffic stopped for 24.992 to 25.202 s, request absent at destination |
| 8.063 | host2-to-mac-move-host | 240 pings lost at one ping every 100 ms, traffic stopped for 24.97 to 25.176 s, reply absent at source |
| 8.104 | host1-to-mac-move-host | 240 pings lost at one ping every 100 ms, traffic stopped for 24.961 to 25.169 s, reply absent at source |
| 8.104 | mac-move-host-to-host1 | 245 pings lost at one ping every 100 ms, traffic stopped for 24.912 to 25.119 s, request absent at destination |
| 33.081 | state | Mobile silent pass |
| 33.081 | step | Mobile sends again |
| 33.094 | mobile host | mac-move-host:bond0 egress filters removed |
| 38.238 | state | Mobile sends again pass |
| 38.238 | step | Mobile recovery |
| 41.240 | steps | last step ended |
| 42.719 | state | check after the steps: pass |
| 42.719 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 42.719 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 42.719 | streams | measurement ended; captures wait for final replies |
| 43.226 | stopped | captures and streams stopped |
| 43.273 | switch1 log | script,info networka mac-age-relearn end |
| 43.320 | switch2 log | script,info networka mac-age-relearn end |
| 43.329 | switch log | marker 'networka mac-age-relearn end' written on switch1, switch2 |
