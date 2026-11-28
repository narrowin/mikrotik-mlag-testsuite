# FAIL — secondary-reboot

Reboot switch2 in its checked secondary role and measure both directions on the host bonds.

- Flood check: 10.110.0.255 A frame was seen more than once across the sender's bond members.; 10.110.0.99 A frame was seen more than once across the sender's bond members.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch2

Reboot switch2 · pass

- Uptime before dispatch was 57 s. The switch reported 17 s at +24.8365 s.
- Full lab state was pass at +25.6739 s, against a 60 s limit.

## Flood check

**fail**
- host1:bond0 → 10.110.0.255 · 521 frames at one every 100 ms, 3 returned to the sender, 40 reached the witness host2:bond0 once.
- host1:bond0 → 10.110.0.99 · 521 frames at one every 100 ms, 4 returned to the sender, 40 reached the witness host2:bond0 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.822 | test | secondary-reboot started in lab small-mlag-mac-move |
| -2.362 | switch1 log | script,info networka secondary-reboot start |
| -1.941 | switch2 log | script,info networka secondary-reboot start |
| -1.922 | switch log | marker 'networka secondary-reboot start' written on switch1, switch2 |
| -0.173 | state | check before the steps: pass |
| -0.173 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.173 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.105 | capture | started at host1:bond0 |
| -0.104 | capture | started at host1:eth1 |
| -0.104 | capture | started at host1:eth2 |
| -0.104 | capture | started at host2:bond0 |
| -0.047 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.013 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.018 | flood check | started from host1:bond0 to 10.110.0.255 |
| 0.022 | flood check | started from host1:bond0 to 10.110.0.99 |
| 4.086 | quiet window | clean |
| 4.086 | step | Baseline |
| 8.088 | step | Reboot switch2 |
| 8.137 | reboot | dispatching the reboot to switch2 |
| 8.179 | reboot | switch2 command returned: accepted |
| 25.943 | switch1 log | bridge,warning "bridge" peer disconnected |
| 25.952 | switch1 log | bridge,warning "bridge" peer link down |
| 33.811 | recovery | full lab state after reboot of switch2: pass |
| 49.814 | step | Reboot recovery |
| 52.816 | steps | last step ended |
| 54.274 | state | check after the steps: pass |
| 54.274 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 54.274 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 54.275 | streams | measurement ended; captures wait for final replies |
| 54.790 | stopped | captures and streams stopped |
| 54.829 | switch1 log | script,info networka secondary-reboot end |
| 54.878 | switch2 log | script,info networka secondary-reboot end |
| 54.884 | switch log | marker 'networka secondary-reboot end' written on switch1, switch2 |
