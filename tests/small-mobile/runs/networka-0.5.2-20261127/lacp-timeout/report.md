# PASS — lacp-timeout

Suppress only the LACPDUs from client1 to switch1 while the cable keeps carrier.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| LACPDUs blocked | client1:bond0 → client3:bond0 | 4 s | 32 at one ping every 100 ms | 3.23088 to 3.43828 s | pass |
| LACPDUs blocked | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | client3:bond0 → client1:bond0 | 4 s | 32 at one ping every 100 ms | 3.24068 to 3.44855 s | pass |
| LACPDUs blocked | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs blocked | client1:bond0 → client2:bond0 | 4 s | 32 at one ping every 100 ms | 3.22521 to 3.43097 s | pass |
| LACPDUs resumed | client1:bond0 → client3:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | client3:bond0 → client1:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACPDUs resumed | client1:bond0 → client2:bond0 | 3 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | client1:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | client2:bond0 → client3:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | client3:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | client3:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| LACP recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**LACPDUs blocked state** · pass
- The switch carrier stays up while the member stops collecting and distributing. · pass

**LACPDUs resumed state** · pass
- The switch member is synchronized, collecting and distributing again. · pass

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

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | switch1 -1.66318 to 25.4136 s | must\_not ether3 link down | pass | not logged |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.955 | test | lacp-timeout started in lab small-mlag-mobile |
| -1.663 | switch1 log | script,info networka lacp-timeout start |
| -1.372 | switch2 log | script,info networka lacp-timeout start |
| -1.369 | switch log | marker 'networka lacp-timeout start' written on switch1, switch2 |
| -0.121 | state | check before the steps: pass |
| -0.121 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.121 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.064 | capture | started at client1:bond0 |
| -0.064 | capture | started at client2:bond0 |
| -0.063 | capture | started at client3:bond0 |
| -0.010 | client1-to-mobile | started from client1:bond0 to client3:bond0 at 10.110.0.50 |
| -0.007 | client2-to-mobile | started from client2:bond0 to client3:bond0 at 10.110.0.50 |
| -0.005 | mobile-to-client1 | started from client3:bond0 to client1:bond0 at 10.110.0.11 |
| -0.003 | mobile-to-client2 | started from client3:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.827 | quiet window | clean |
| 3.827 | step | LACPDUs blocked |
| 3.833 | fault | applying the rule for client1:eth1 on client1:eth1 |
| 3.838 | fault | read back the rule for client1:eth1 |
| 6.982 | mobile-to-client1 | 32 pings lost at one ping every 100 ms, traffic stopped for 3.241 to 3.449 s, request absent at destination |
| 6.982 | client1-to-client2 | 32 pings lost at one ping every 100 ms, traffic stopped for 3.225 to 3.431 s, request absent at destination |
| 6.992 | client1-to-mobile | 32 pings lost at one ping every 100 ms, traffic stopped for 3.231 to 3.438 s, request absent at destination |
| 11.917 | state | LACPDUs blocked pass |
| 11.917 | step | LACPDUs resumed |
| 11.927 | fault | removed the rule for client1:eth1, 11 packets dropped |
| 12.339 | recovery | the client bond member is eligible again |
| 20.394 | state | LACPDUs resumed pass |
| 20.394 | step | LACP recovery |
| 23.395 | steps | last step ended |
| 24.862 | state | check after the steps: pass |
| 24.862 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 24.862 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 24.862 | streams | measurement ended; captures wait for final replies |
| 25.368 | stopped | captures and streams stopped |
| 25.414 | switch1 log | script,info networka lacp-timeout end |
| 25.454 | switch2 log | script,info networka lacp-timeout end |
| 25.460 | switch log | marker 'networka lacp-timeout end' written on switch1, switch2 |
