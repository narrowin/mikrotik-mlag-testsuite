# ERROR — lacp-timeout

Suppress only the LACPDUs from host1 to switch1 while the cable keeps carrier.

- Step LACPDUs resumed is error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| LACPDUs blocked | host1:bond0 → mac-move-host:bond0 | 4 s | 60 at one ping every 100 ms | 3.2231 to 3.4302 s | pass |
| LACPDUs blocked | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | mac-move-host:bond0 → host1:bond0 | 4 s | 59 at one ping every 100 ms | 3.22161 to 3.43094 s | pass |
| LACPDUs blocked | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | host1:bond0 → host2:bond0 | 4 s | 59 at one ping every 100 ms | 3.22621 to 3.43194 s | pass |
| LACPDUs resumed | host1:bond0 → mac-move-host:bond0 | 3 s | 28 at one ping every 100 ms | 2.80604 to 3.01658 s | error |
| LACPDUs resumed | host2:bond0 → mac-move-host:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | mac-move-host:bond0 → host1:bond0 | 3 s | 27 at one ping every 100 ms | 2.70505 to 2.91423 s | pass |
| LACPDUs resumed | mac-move-host:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | host1:bond0 → host2:bond0 | 3 s | 27 at one ping every 100 ms | 2.70739 to 2.91823 s | pass |
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
| Whole test | switch1 -1.7247 to 26.3434 s | must\_not ether3 link down | pass | not logged |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.021 | test | lacp-timeout started in lab small-mlag-mac-move |
| -1.725 | switch1 log | script,info networka lacp-timeout start |
| -1.409 | switch2 log | script,info networka lacp-timeout start |
| -1.396 | switch log | marker 'networka lacp-timeout start' written on switch1, switch2 |
| -0.122 | state | check before the steps: pass |
| -0.122 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.122 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.065 | capture | started at host1:bond0 |
| -0.065 | capture | started at host2:bond0 |
| -0.065 | capture | started at mac-move-host:bond0 |
| -0.011 | host1-to-mac-move-host | started from host1:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.008 | host2-to-mac-move-host | started from host2:bond0 to mac-move-host:bond0 at 10.110.0.50 |
| -0.006 | mac-move-host-to-host1 | started from mac-move-host:bond0 to host1:bond0 at 10.110.0.11 |
| -0.003 | mac-move-host-to-host2 | started from mac-move-host:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.877 | quiet window | clean |
| 3.878 | step | LACPDUs blocked |
| 3.884 | fault | applying the rule for host1:eth1 on host1:eth1 |
| 3.891 | fault | read back the rule for host1:eth1 |
| 6.748 | host1-to-mac-move-host | 32 pings lost at one ping every 100 ms, traffic stopped for 3.223 to 3.43 s, request absent at destination |
| 6.779 | host1-to-host2 | 32 pings lost at one ping every 100 ms, traffic stopped for 3.226 to 3.432 s, request absent at destination |
| 6.781 | mac-move-host-to-host1 | 32 pings lost at one ping every 100 ms, traffic stopped for 3.222 to 3.431 s, request absent at destination |
| 10.285 | host1-to-mac-move-host | 28 pings lost at one ping every 100 ms, traffic stopped for 2.806 to 3.017 s, reply absent at source |
| 10.315 | mac-move-host-to-host1 | 27 pings lost at one ping every 100 ms, traffic stopped for 2.705 to 2.914 s, request absent at destination |
| 10.315 | host1-to-host2 | 27 pings lost at one ping every 100 ms, traffic stopped for 2.707 to 2.918 s, reply absent at source |
| 11.977 | state | LACPDUs blocked pass |
| 11.978 | step | LACPDUs resumed |
| 11.986 | fault | removed the rule for host1:eth1, 12 packets dropped |
| 13.232 | recovery | the host bond member is eligible again |
| 21.339 | state | LACPDUs resumed pass |
| 21.339 | step | LACP recovery |
| 24.340 | steps | last step ended |
| 25.803 | state | check after the steps: pass |
| 25.803 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 25.803 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 25.803 | streams | measurement ended; captures wait for final replies |
| 26.311 | stopped | captures and streams stopped |
| 26.343 | switch1 log | script,info networka lacp-timeout end |
| 26.379 | switch2 log | script,info networka lacp-timeout end |
| 26.381 | switch log | marker 'networka lacp-timeout end' written on switch1, switch2 |
