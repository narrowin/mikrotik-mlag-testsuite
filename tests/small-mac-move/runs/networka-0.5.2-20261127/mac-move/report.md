# PASS — mac-move

Move the active-backup host to the other switch and back without changing its MAC or IP address. Check the gratuitous ARP at the new TAP and unicast at the old TAP.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Mobile moves to switch2 | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves to switch2 | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile moves back to switch1 | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Mobile recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Mobile moves to switch2 state** · pass
- Both switches learned the mobile host on the new path. · pass

**Mobile moves back to switch1 state** · pass
- Both switches learned the mobile host on its original path. · pass

**Mobile moves to switch2** · pass

- The gratuitous ARP reached switch2:tap4 at 3.816 s from the start of the quiet window. switch1:tap4 saw 0 further unicast frames addressed to the host.

**Mobile moves back to switch1** · pass

- The gratuitous ARP reached switch1:tap4 at 7.888 s from the start of the quiet window. switch2:tap4 saw 0 further unicast frames addressed to the host.

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
| -1.942 | test | mac-move started in lab small-mlag-mobile |
| -1.655 | switch1 log | script,info networka mac-move start |
| -1.377 | switch2 log | script,info networka mac-move start |
| -1.373 | switch log | marker 'networka mac-move start' written on switch1, switch2 |
| -0.135 | state | check before the steps: pass |
| -0.135 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.135 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.114 | capture | started at client1:bond0 |
| -0.064 | capture | started at client2:bond0 |
| -0.064 | capture | started at client3:bond0 |
| -0.063 | capture | started at switch1:tap4 |
| -0.063 | capture | started at switch2:tap4 |
| -0.009 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.007 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.005 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.003 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.812 | quiet window | clean |
| 3.813 | step | Mobile moves to switch2 |
| 3.815 | mobile host | client3:bond0 moves to eth2 |
| 7.885 | state | Mobile moves to switch2 pass |
| 7.885 | step | Mobile moves back to switch1 |
| 7.887 | mobile host | client3:bond0 moves to eth1 |
| 10.954 | state | Mobile moves back to switch1 pass |
| 10.954 | step | Mobile recovery |
| 13.959 | steps | last step ended |
| 15.405 | state | check after the steps: pass |
| 15.405 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 15.405 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 15.406 | streams | measurement ended; captures wait for final replies |
| 15.911 | stopped | captures and streams stopped |
| 15.946 | switch1 log | script,info networka mac-move end |
| 15.989 | switch2 log | script,info networka mac-move end |
| 15.993 | switch log | marker 'networka mac-move end' written on switch1, switch2 |
