# PASS — secondary-reboot

Reboot switch2 in its checked MLAG secondary role and measure both directions between host1 and host2.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host1:eth1 → host2:bond0 | 5 s | 27 at one ping every 100 ms | 2.71068 to 2.91781 s | pass |
| Reboot switch2 | host2:bond0 → host1:eth1 | 5 s | 27 at one ping every 100 ms | 2.71023 to 2.91409 s | pass |
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

- Uptime before dispatch was 66 s. The switch reported 16 s at +23.8523 s.
- Full lab state was pass at +24.64 s, against a 60 s limit.

## Flood check

**pass**
- host2:bond0 → 10.110.0.255 · 509 frames at one every 100 ms, 0 returned to the sender, 39 reached the witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 510 frames at one every 100 ms, 0 returned to the sender, 40 reached the witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.081 | test | secondary-reboot started in lab medium-mlag |
| -1.717 | access-switch log | script,info networka secondary-reboot start |
| -1.388 | switch1 log | script,info networka secondary-reboot start |
| -1.046 | switch2 log | script,info networka secondary-reboot start |
| -1.042 | switch log | marker 'networka secondary-reboot start' written on access-switch, switch1, switch2 |
| -0.122 | state | check before the steps: pass |
| -0.122 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.122 | state | All three switches run with spanning tree off. pass |
| -0.122 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.122 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.059 | capture | started at host1:eth1 |
| -0.059 | capture | started at host2:bond0 |
| -0.058 | capture | started at host2:eth1 |
| -0.058 | capture | started at host2:eth2 |
| -0.004 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.001 | flood check | started from host2:bond0 to 10.110.0.255 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood check | started from host2:bond0 to 10.110.0.99 |
| 4.072 | quiet window | clean |
| 4.072 | step | Baseline |
| 8.074 | step | Reboot switch2 |
| 8.135 | reboot | dispatching the reboot to switch2 |
| 8.198 | reboot | switch2 command returned: accepted |
| 8.646 | host1-to-host2 | 27 pings lost at one ping every 100 ms, traffic stopped for 2.711 to 2.918 s, request absent at destination |
| 8.647 | host2-to-host1 | 27 pings lost at one ping every 100 ms, traffic stopped for 2.71 to 2.914 s, reply absent at source |
| 25.011 | switch1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.306 | switch1 log | bridge,warning "bridge" peer disconnected |
| 25.313 | switch1 log | bridge,warning "bridge" peer link down |
| 32.775 | recovery | full lab state after reboot of switch2: pass |
| 48.776 | step | Reboot recovery |
| 51.778 | steps | last step ended |
| 53.087 | state | check after the steps: pass |
| 53.087 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 53.087 | state | All three switches run with spanning tree off. pass |
| 53.087 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 53.087 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 53.087 | streams | measurement ended; captures wait for final replies |
| 54.022 | stopped | captures and streams stopped |
| 54.057 | access-switch log | script,info networka secondary-reboot end |
| 54.106 | switch1 log | script,info networka secondary-reboot end |
| 54.176 | switch2 log | script,info networka secondary-reboot end |
| 54.188 | switch log | marker 'networka secondary-reboot end' written on access-switch, switch1, switch2 |
