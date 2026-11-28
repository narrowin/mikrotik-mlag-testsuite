# PASS — mac-move

Move the active-backup host to the other switch and back without changing its MAC or IP address. Check the gratuitous ARP at the new TAP and unicast at the old TAP.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
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

- The gratuitous ARP reached switch2:tap4 at 3.820 s from the start of the quiet window. switch1:tap4 saw 0 further unicast frames addressed to the host.

**Mobile moves back to switch1** · pass

- The gratuitous ARP reached switch1:tap4 at 8.098 s from the start of the quiet window. switch2:tap4 saw 0 further unicast frames addressed to the host.

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
| -2.139 | test | mac-move started in lab small-mlag-mac-move |
| -1.818 | switch1 log | script,info networka mac-move start |
| -1.461 | switch2 log | script,info networka mac-move start |
| -1.457 | switch log | marker 'networka mac-move start' written on switch1, switch2 |
| -0.161 | state | check before the steps: pass |
| -0.161 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.161 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.073 | capture | started at host1:bond0 |
| -0.073 | capture | started at host2:bond0 |
| -0.073 | capture | started at mac-move-host:bond0 |
| -0.073 | capture | started at switch1:tap4 |
| -0.073 | capture | started at switch2:tap4 |
| -0.017 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.013 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.009 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.006 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.815 | quiet window | clean |
| 3.815 | step | Mobile moves to switch2 |
| 3.817 | mobile host | mac-move-host:bond0 moves to eth2 |
| 7.991 | state | Mobile moves to switch2 pass |
| 7.992 | step | Mobile moves back to switch1 |
| 8.093 | mobile host | mac-move-host:bond0 moves to eth1 |
| 11.274 | state | Mobile moves back to switch1 pass |
| 11.275 | step | Mobile recovery |
| 14.279 | steps | last step ended |
| 15.796 | state | check after the steps: pass |
| 15.796 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 15.796 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 15.797 | streams | measurement ended; captures wait for final replies |
| 16.322 | stopped | captures and streams stopped |
| 16.361 | switch1 log | script,info networka mac-move end |
| 16.404 | switch2 log | script,info networka mac-move end |
| 16.407 | switch log | marker 'networka mac-move end' written on switch1, switch2 |
