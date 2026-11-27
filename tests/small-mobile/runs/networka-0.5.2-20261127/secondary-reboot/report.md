# PASS — secondary-reboot

Reboot switch2 in its checked secondary role and measure both directions on the client bonds.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | client1:bond0 → client2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | client2:bond0 → client1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | client1:bond0 → client2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | client2:bond0 → client1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- client1:bond0 → client2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- client2:bond0 → client1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch2

Reboot switch2 · pass

- Uptime before dispatch was 48 s. The switch reported 16 s at +22.8037 s.
- Full lab state was pass at +23.613 s, against a 60 s limit.

## Flood probes

**pass**
- client1:bond0 → 10.110.0.255 · 500 probes at one every 100 ms, 0 returned to the sender, 39 reached the baseline witness client2:bond0 once.
- client1:bond0 → 10.110.0.99 · 501 probes at one every 100 ms, 0 returned to the sender, 39 reached the baseline witness client2:bond0 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.001 | test | secondary-reboot started in lab small-mlag-mobile |
| -1.700 | switch1 log | script,info networka secondary-reboot start |
| -1.399 | switch2 log | script,info networka secondary-reboot start |
| -1.391 | switch log | marker 'networka secondary-reboot start' written on switch1, switch2 |
| -0.123 | state | check before the steps: pass |
| -0.123 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.123 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| -0.057 | capture | started at client1:bond0 |
| -0.057 | capture | started at client1:eth1 |
| -0.057 | capture | started at client1:eth2 |
| -0.056 | capture | started at client2:bond0 |
| -0.004 | client1-to-client2 | started from client1:bond0 to client2:bond0 at 10.110.0.12 |
| -0.001 | client2-to-client1 | started from client2:bond0 to client1:bond0 at 10.110.0.11 |
| -0.000 | flood probe | started from client1:bond0 to 10.110.0.255 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.001 | flood probe | started from client1:bond0 to 10.110.0.99 |
| 3.996 | quiet window | clean |
| 3.997 | step | Baseline |
| 7.998 | step | Reboot switch2 |
| 8.045 | reboot | dispatching the reboot to switch2 |
| 8.099 | reboot | switch2 command returned: accepted |
| 23.865 | switch1 log | bridge,warning MLAG: remote heartbeat timeout |
| 23.865 | switch1 log | bridge,warning "bridge" peer disconnected |
| 23.872 | switch1 log | bridge,warning "bridge" peer link down |
| 31.658 | recovery | full lab state after reboot of switch2: pass |
| 47.661 | step | Reboot recovery |
| 50.664 | steps | last step ended |
| 52.161 | state | check after the steps: pass |
| 52.161 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 52.161 | state | Both cables of client1 and client2 are eligible in their LACP bonds. pass |
| 52.161 | streams | measurement ended; captures wait for final replies |
| 52.665 | stopped | captures and streams stopped |
| 52.696 | switch1 log | script,info networka secondary-reboot end |
| 52.738 | switch2 log | script,info networka secondary-reboot end |
| 52.742 | switch log | marker 'networka secondary-reboot end' written on switch1, switch2 |
