# FAIL — lacp-timeout

Suppress only the LACPDUs from host1 to switch1 while the cable keeps carrier.

- Step LACPDUs blocked is fail.
- Step LACPDUs resumed is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| LACPDUs blocked | host1:bond0 → mac-move-host:bond0 | 4 s | 51 at one ping every 100 ms | 5.21816 to 5.42388 s | fail |
| LACPDUs blocked | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | mac-move-host:bond0 → host1:bond0 | 4 s | 51 at one ping every 100 ms | 5.20742 to 5.4194 s | fail |
| LACPDUs blocked | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | host1:bond0 → host2:bond0 | 4 s | 51 at one ping every 100 ms | 5.20708 to 5.41476 s | fail |
| LACPDUs resumed | host1:bond0 → mac-move-host:bond0 | 3 s | 51 at one ping every 100 ms | 5.21816 to 5.42388 s | fail |
| LACPDUs resumed | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | mac-move-host:bond0 → host1:bond0 | 3 s | 51 at one ping every 100 ms | 5.20742 to 5.4194 s | fail |
| LACPDUs resumed | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | host1:bond0 → host2:bond0 | 3 s | 51 at one ping every 100 ms | 5.20708 to 5.41476 s | fail |
| LACP recovery | host1:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | mac-move-host:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**LACPDUs blocked state** · pass
- The switch carrier stays up while the member stops collecting and distributing. · pass

**LACPDUs resumed state** · pass
- The switch member is synchronized, collecting and distributing again. · pass

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

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.72398 to 25.3647 s | must\_not ether3 link down | pass | not logged |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.033 | test | lacp-timeout started in lab small-mlag-mac-move |
| -1.724 | switch1 log | script,info networka lacp-timeout start |
| -1.424 | switch2 log | script,info networka lacp-timeout start |
| -1.416 | switch log | marker 'networka lacp-timeout start' written on switch1, switch2 |
| -0.116 | state | check before the steps: pass |
| -0.116 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.116 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.063 | capture | started at host1:bond0 |
| -0.063 | capture | started at host2:bond0 |
| -0.063 | capture | started at mac-move-host:bond0 |
| -0.009 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.007 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.005 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.827 | quiet window | clean |
| 3.827 | step | LACPDUs blocked |
| 3.831 | fault | applying the rule for host1:eth1 on host1:eth1 |
| 3.838 | fault | read back the rule for host1:eth1 |
| 6.862 | host1-to-mac-move-host | 51 pings lost at one ping every 100 ms, traffic stopped for 5.218 to 5.424 s, reply absent at source, request absent at destination |
| 6.874 | host1-to-host2 | 51 pings lost at one ping every 100 ms, traffic stopped for 5.207 to 5.415 s, reply absent at source, request absent at destination |
| 6.895 | mac-move-host-to-host1 | 51 pings lost at one ping every 100 ms, traffic stopped for 5.207 to 5.419 s, request absent at destination |
| 11.943 | state | LACPDUs blocked pass |
| 11.943 | step | LACPDUs resumed |
| 11.951 | fault | removed the rule for host1:eth1, 11 packets dropped |
| 12.363 | recovery | the client bond member is eligible again |
| 20.408 | state | LACPDUs resumed pass |
| 20.408 | step | LACP recovery |
| 23.409 | steps | last step ended |
| 24.827 | state | check after the steps: pass |
| 24.827 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 24.827 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 24.827 | streams | measurement ended; captures wait for final replies |
| 25.331 | stopped | captures and streams stopped |
| 25.365 | switch1 log | script,info networka lacp-timeout end |
| 25.395 | switch2 log | script,info networka lacp-timeout end |
| 25.404 | switch log | marker 'networka lacp-timeout end' written on switch1, switch2 |
