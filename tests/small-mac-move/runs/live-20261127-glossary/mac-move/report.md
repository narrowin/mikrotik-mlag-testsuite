# PASS — mac-move

Move the active-backup host to the other switch and back without changing its MAC or IP address. Check the gratuitous ARP at the new TAP and unicast at the old TAP.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Mobile moves to switch2 | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Mobile moves to switch2 state** · pass
- Both switches learned the MAC-move host on the new path. · pass

**Mobile moves back to switch1 state** · pass
- Both switches learned the MAC-move host on its original path. · pass

**Mobile moves to switch2** · pass

- The gratuitous ARP reached switch2:tap4 at 3.836 s from the start of the quiet window. switch1:tap4 saw 0 further unicast frames addressed to the host.

**Mobile moves back to switch1** · pass

- The gratuitous ARP reached switch1:tap4 at 7.915 s from the start of the quiet window. switch2:tap4 saw 0 further unicast frames addressed to the host.

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
| -2.025 | test | mac-move started in lab small-mlag-mac-move |
| -1.730 | switch1 log | script,info networka mac-move start |
| -1.436 | switch2 log | script,info networka mac-move start |
| -1.433 | switch log | marker 'networka mac-move start' written on switch1, switch2 |
| -0.160 | state | check before the steps: pass |
| -0.160 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.160 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.128 | capture | started at host1:bond0 |
| -0.128 | capture | started at host2:bond0 |
| -0.076 | capture | started at mac-move-host:bond0 |
| -0.076 | capture | started at switch1:tap4 |
| -0.076 | capture | started at switch2:tap4 |
| -0.020 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.017 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.013 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.007 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.831 | quiet window | clean |
| 3.831 | step | Mobile moves to switch2 |
| 3.834 | mobile host | mac-move-host:bond0 moves to eth2 |
| 7.911 | state | Mobile moves to switch2 pass |
| 7.911 | step | Mobile moves back to switch1 |
| 7.913 | mobile host | mac-move-host:bond0 moves to eth1 |
| 10.983 | state | Mobile moves back to switch1 pass |
| 10.983 | step | Mobile recovery |
| 13.983 | steps | last step ended |
| 15.411 | state | check after the steps: pass |
| 15.411 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 15.411 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 15.411 | streams | measurement ended; captures wait for final replies |
| 15.919 | stopped | captures and streams stopped |
| 15.967 | switch1 log | script,info networka mac-move end |
| 16.003 | switch2 log | script,info networka mac-move end |
| 16.008 | switch log | marker 'networka mac-move end' written on switch1, switch2 |
