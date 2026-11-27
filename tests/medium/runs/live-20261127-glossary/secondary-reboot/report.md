# FAIL — secondary-reboot

Reboot switch2 in its checked MLAG secondary role and measure both directions between host1 and host2.

- Flood probes: 10.110.0.255 A probe was seen more than once across the sender's bond members.; 10.110.0.99 A probe was seen more than once across the sender's bond members.
- Step Reboot switch2 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host1:eth1 → host2:bond0 | 5 s | 101 at one ping every 100 ms | 7.79966 to 8.00916 s | fail |
| Reboot switch2 | host2:bond0 → host1:eth1 | 5 s | 100 at one ping every 100 ms | 7.80877 to 8.0127 s | fail |
| Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch2

Reboot switch2 · pass

- Uptime before dispatch was 55 s. The switch reported 16 s at +22.7614 s.
- Full lab state was pass at +23.4714 s, against a 60 s limit.

## Flood probes

**fail**
- host2:bond0 → 10.110.0.255 · 497 probes at one every 100 ms, 2 returned to the sender, 39 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 498 probes at one every 100 ms, 1 returned to the sender, 39 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.914 | test | secondary-reboot started in lab medium-mlag |
| -1.584 | access-switch log | script,info networka secondary-reboot start |
| -1.275 | switch1 log | script,info networka secondary-reboot start |
| -0.974 | switch2 log | script,info networka secondary-reboot start |
| -0.967 | switch log | marker 'networka secondary-reboot start' written on access-switch, switch1, switch2 |
| -0.121 | state | check before the steps: pass |
| -0.121 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.121 | state | All three switches run with spanning tree off. pass |
| -0.121 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.121 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host2:bond0 |
| -0.059 | capture | started at host2:eth1 |
| -0.059 | capture | started at host2:eth2 |
| -0.003 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.000 | flood probe | started from host2:bond0 to 10.110.0.255 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 4.015 | quiet window | clean |
| 4.015 | step | Baseline |
| 8.016 | step | Reboot switch2 |
| 8.069 | reboot | dispatching the reboot to switch2 |
| 8.130 | reboot | switch2 command returned: accepted |
| 8.444 | host1-to-host2 | 25 pings lost at one ping every 100 ms, traffic stopped for 2.5 to 2.704 s, request absent at destination |
| 8.479 | host2-to-host1 | 24 pings lost at one ping every 100 ms, traffic stopped for 2.399 to 2.607 s, reply absent at source |
| 24.452 | switch1 log | bridge,warning "bridge" peer disconnected |
| 24.456 | switch1 log | bridge,warning "bridge" peer link down |
| 25.413 | host2-to-host1 | 76 pings lost at one ping every 100 ms, traffic stopped for 7.809 to 8.013 s, reply absent at source |
| 25.446 | host1-to-host2 | 76 pings lost at one ping every 100 ms, traffic stopped for 7.8 to 8.009 s, request absent at destination |
| 31.540 | recovery | full lab state after reboot of switch2: pass |
| 47.541 | step | Reboot recovery |
| 50.543 | steps | last step ended |
| 51.795 | state | check after the steps: pass |
| 51.795 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 51.795 | state | All three switches run with spanning tree off. pass |
| 51.795 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 51.795 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 51.795 | streams | measurement ended; captures wait for final replies |
| 52.299 | stopped | captures and streams stopped |
| 52.348 | access-switch log | script,info networka secondary-reboot end |
| 52.386 | switch1 log | script,info networka secondary-reboot end |
| 52.432 | switch2 log | script,info networka secondary-reboot end |
| 52.436 | switch log | marker 'networka secondary-reboot end' written on access-switch, switch1, switch2 |
