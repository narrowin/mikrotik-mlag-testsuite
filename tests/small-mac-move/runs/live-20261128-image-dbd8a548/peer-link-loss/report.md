# PASS — peer-link-loss

Withdraw the peer link at both switches, watch the LACP peers separate and rejoin, and measure every stream.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Peer cable down | host1:bond0 → mac-move-host:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | host2:bond0 → mac-move-host:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | mac-move-host:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | mac-move-host:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable down | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | host1:bond0 → mac-move-host:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | host2:bond0 → mac-move-host:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | mac-move-host:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | mac-move-host:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable back | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Peer cable recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Peer cable down state** · pass
- Both peer ports have lost carrier and MLAG is disconnected. · pass

**Peer cable back state** · pass
- Both peer ports have carrier again and the peers are connected. · pass

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
| -2.182 | test | peer-link-loss started in lab small-mlag-mac-move |
| -1.857 | switch1 log | script,info networka peer-link-loss start |
| -1.524 | switch2 log | script,info networka peer-link-loss start |
| -1.519 | switch log | marker 'networka peer-link-loss start' written on switch1, switch2 |
| -0.202 | state | check before the steps: pass |
| -0.202 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.202 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.146 | capture | started at host1:bond0 |
| -0.146 | capture | started at host2:bond0 |
| -0.145 | capture | started at mac-move-host:bond0 |
| -0.145 | capture | started at switch1:eth1 |
| -0.144 | capture | started at switch2:eth1 |
| -0.085 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.070 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.033 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.014 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.004 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.831 | quiet window | clean |
| 3.831 | step | Peer cable down |
| 3.860 | cable | switch1:eth1 set down |
| 3.860 | cable | switch1:eth1 down at both ends |
| 4.601 | switch2 log | interface,info ether2 link down |
| 4.631 | switch1 log | interface,info ether2 link down |
| 4.673 | switch2 log | bridge,warning "bridge" peer link down |
| 4.674 | switch1 log | bridge,warning "bridge" peer link down |
| 19.200 | state | Peer cable down pass |
| 19.200 | step | Peer cable back |
| 19.249 | cable | switch1:eth1 set up |
| 19.249 | cable | switch1:eth1 up at both ends |
| 19.667 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 19.671 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 84.517 | state | Peer cable back pass |
| 84.517 | step | Peer cable recovery |
| 87.518 | steps | last step ended |
| 88.983 | state | check after the steps: pass |
| 88.983 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 88.983 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 88.984 | streams | measurement ended; captures wait for final replies |
| 89.492 | stopped | captures and streams stopped |
| 89.525 | switch1 log | script,info networka peer-link-loss end |
| 89.585 | switch2 log | script,info networka peer-link-loss end |
| 89.592 | switch log | marker 'networka peer-link-loss end' written on switch1, switch2 |
