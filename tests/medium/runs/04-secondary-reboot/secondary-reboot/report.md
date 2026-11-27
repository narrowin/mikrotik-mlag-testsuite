# PASS — secondary-reboot

Reboot switch2 in its checked MLAG secondary role and measure both directions between host1 and host2. Both bypass streams must continue while it restarts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host1:eth1 → host2:bond0 | 5 s | 26 at one ping every 100 ms | 2.50509 to 2.71263 s | pass |
| Reboot switch2 | host2:bond0 → host1:eth1 | 5 s | 25 at one ping every 100 ms | 2.39518 to 2.59804 s | pass |
| Reboot switch2 | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch2

Reboot switch2 · pass

- Uptime before dispatch was 117 s. The switch reported 16 s at +22.9969 s.
- Full lab state was pass at +23.7038 s, against a 60 s limit.

## Flood probes

**pass**
- host2:bond0 → 10.110.0.255 · 501 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 501 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.835 | test | secondary-reboot started in lab medium-mlag |
| -1.548 | access-switch log | script,info networka secondary-reboot start |
| -1.269 | switch1 log | script,info networka secondary-reboot start |
| -0.980 | switch2 log | script,info networka secondary-reboot start |
| -0.977 | switch log | marker 'networka secondary-reboot start' written on access-switch, switch1, switch2 |
| -0.124 | state | check before the steps: pass |
| -0.124 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.124 | state | All three switches run with spanning tree off. pass |
| -0.124 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.124 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:eth1 |
| -0.060 | capture | started at host1:eth3 |
| -0.060 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth1 |
| -0.060 | capture | started at host2:eth2 |
| -0.060 | capture | started at host2:eth3 |
| -0.006 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.004 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.002 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.000 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host2:bond0 to 10.110.0.255 |
| 0.001 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 4.123 | quiet window | clean |
| 4.123 | step | Baseline |
| 8.123 | step | Reboot switch2 |
| 8.174 | reboot | dispatching the reboot to switch2 |
| 8.241 | reboot | switch2 command returned: accepted |
| 8.581 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.505 to 2.713 s, request absent at destination |
| 8.598 | host2-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.395 to 2.598 s, reply absent at source |
| 19.475 | switch1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.476 | switch1 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.574 | switch1 log | bridge,warning "bridge" peer disconnected |
| 24.579 | switch1 log | bridge,warning "bridge" peer link down |
| 26.996 | host1-to-host2 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 27.029 | host2-to-host1 | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 31.878 | recovery | full lab state after reboot of switch2: pass |
| 47.881 | step | Reboot recovery |
| 50.882 | steps | last step ended |
| 52.128 | state | check after the steps: pass |
| 52.128 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 52.128 | state | All three switches run with spanning tree off. pass |
| 52.128 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 52.128 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 52.128 | streams | measurement ended; captures wait for final replies |
| 52.632 | stopped | captures and streams stopped |
| 52.676 | access-switch log | script,info networka secondary-reboot end |
| 52.723 | switch1 log | script,info networka secondary-reboot end |
| 52.795 | switch2 log | script,info networka secondary-reboot end |
| 52.811 | switch log | marker 'networka secondary-reboot end' written on access-switch, switch1, switch2 |
