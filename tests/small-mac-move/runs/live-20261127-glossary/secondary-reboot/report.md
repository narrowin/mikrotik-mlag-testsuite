# FAIL — secondary-reboot

Reboot switch2 in its checked secondary role and measure both directions on the host bonds.

- Flood probes: 10.110.0.255 A probe was seen more than once across the sender's bond members.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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

- Uptime before dispatch was 49 s. The switch reported 16 s at +22.7906 s.
- Full lab state was pass at +23.6362 s, against a 60 s limit.

## Flood probes

**fail**
- host1:bond0 → 10.110.0.255 · 500 probes at one every 100 ms, 1 returned to the sender, 39 reached the baseline witness host2:bond0 once.
- host1:bond0 → 10.110.0.99 · 500 probes at one every 100 ms, 0 returned to the sender, 39 reached the baseline witness host2:bond0 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -1.961 | test | secondary-reboot started in lab small-mlag-mac-move |
| -1.673 | switch1 log | script,info networka secondary-reboot start |
| -1.390 | switch2 log | script,info networka secondary-reboot start |
| -1.382 | switch log | marker 'networka secondary-reboot start' written on switch1, switch2 |
| -0.129 | state | check before the steps: pass |
| -0.129 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| -0.129 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| -0.058 | capture | started at host1:bond0 |
| -0.057 | capture | started at host1:eth1 |
| -0.057 | capture | started at host1:eth2 |
| -0.057 | capture | started at host2:bond0 |
| -0.003 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.001 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| -0.000 | flood probe | started from host1:bond0 to 10.110.0.255 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host1:bond0 to 10.110.0.99 |
| 4.009 | quiet window | clean |
| 4.009 | step | Baseline |
| 8.010 | step | Reboot switch2 |
| 8.051 | reboot | dispatching the reboot to switch2 |
| 8.107 | reboot | switch2 command returned: accepted |
| 24.133 | switch1 log | bridge,warning "bridge" peer disconnected |
| 24.137 | switch1 log | bridge,warning "bridge" peer link down |
| 31.688 | recovery | full lab state after reboot of switch2: pass |
| 47.690 | step | Reboot recovery |
| 50.691 | steps | last step ended |
| 52.132 | state | check after the steps: pass |
| 52.132 | state | The primary and secondary peers are connected and run with spanning tree off. pass |
| 52.132 | state | Both cables of host1 and host2 are eligible in their LACP bonds. pass |
| 52.132 | streams | measurement ended; captures wait for final replies |
| 52.636 | stopped | captures and streams stopped |
| 52.681 | switch1 log | script,info networka secondary-reboot end |
| 52.733 | switch2 log | script,info networka secondary-reboot end |
| 52.736 | switch log | marker 'networka secondary-reboot end' written on switch1, switch2 |
