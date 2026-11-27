# PASS — peer-link-loss

Withdraw the peer link at both switches, watch the LACP peers separate and rejoin, and measure every stream.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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
| -2.071 | test | peer-link-loss started in lab small-mlag-mac-move |
| -1.764 | switch1 log | script,info networka peer-link-loss start |
| -1.454 | switch2 log | script,info networka peer-link-loss start |
| -1.441 | switch log | marker 'networka peer-link-loss start' written on switch1, switch2 |
| -0.126 | state | check before the steps: pass |
| -0.126 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.126 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.120 | capture | started at host1:bond0 |
| -0.120 | capture | started at host2:bond0 |
| -0.119 | capture | started at mac-move-host:bond0 |
| -0.066 | capture | started at switch1:eth1 |
| -0.065 | capture | started at switch2:eth1 |
| -0.012 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.010 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.006 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.004 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.898 | quiet window | clean |
| 3.899 | step | Peer cable down |
| 3.917 | cable | switch1:eth1 set down |
| 3.917 | cable | switch1:eth1 down at both ends |
| 4.366 | switch2 log | interface,info ether2 link down |
| 4.373 | switch1 log | interface,info ether2 link down |
| 4.399 | switch2 log | bridge,warning "bridge" peer link down |
| 4.403 | switch1 log | bridge,warning "bridge" peer link down |
| 19.234 | state | Peer cable down pass |
| 19.234 | step | Peer cable back |
| 19.249 | cable | switch1:eth1 set up |
| 19.250 | cable | switch1:eth1 up at both ends |
| 19.392 | switch2 log | interface,info ether2 link up (speed 10G, full duplex) |
| 19.416 | switch1 log | interface,info ether2 link up (speed 10G, full duplex) |
| 84.516 | state | Peer cable back pass |
| 84.516 | step | Peer cable recovery |
| 87.519 | steps | last step ended |
| 88.994 | state | check after the steps: pass |
| 88.994 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 88.994 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 88.994 | streams | measurement ended; captures wait for final replies |
| 89.503 | stopped | captures and streams stopped |
| 89.545 | switch1 log | script,info networka peer-link-loss end |
| 89.581 | switch2 log | script,info networka peer-link-loss end |
| 89.585 | switch log | marker 'networka peer-link-loss end' written on switch1, switch2 |
