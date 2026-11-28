# PASS — reboot-b-secondary

Reboot switch-b2 in its checked MLAG secondary role of pair B and measure both directions between the hosts.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host1:bond0 → host2:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot switch-b2 | host2:bond0 → host1:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:bond0 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of switch-b2

Reboot switch-b2 · pass

- Uptime before dispatch was 285 s. The switch reported 18 s at +25.0988 s.
- Full lab state was pass at +26.6685 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.198 | test | reboot-b-secondary started in lab two-pair |
| -2.869 | switch-a1 log | script,info networka reboot-b-secondary start |
| -2.561 | switch-a2 log | script,info networka reboot-b-secondary start |
| -2.256 | switch-b1 log | script,info networka reboot-b-secondary start |
| -1.935 | switch-b2 log | script,info networka reboot-b-secondary start |
| -1.927 | switch log | marker 'networka reboot-b-secondary start' written on switch-a1, switch-a2, switch-b1, switch-b2 |
| -0.113 | state | check before the steps: pass |
| -0.113 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| -0.113 | state | All four switches run with spanning tree off. pass |
| -0.113 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| -0.113 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| -0.113 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.060 | capture | started at host1:bond0 |
| -0.060 | capture | started at host2:bond0 |
| -0.005 | host1-to-host2 | started from host1:bond0 to host2:bond0 at 10.110.0.12 |
| -0.002 | host2-to-host1 | started from host2:bond0 to host1:bond0 at 10.110.0.11 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.758 | quiet window | clean |
| 3.758 | step | Baseline |
| 7.759 | step | Reboot switch-b2 |
| 7.814 | reboot | dispatching the reboot to switch-b2 |
| 7.928 | reboot | switch-b2 command returned: accepted |
| 20.955 | switch-b1 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.554 | switch-b1 log | bridge,warning "bridge" peer disconnected |
| 25.568 | switch-b1 log | bridge,warning "bridge" peer link down |
| 34.483 | recovery | full lab state after reboot of switch-b2: pass |
| 50.484 | step | Reboot recovery |
| 53.485 | steps | last step ended |
| 55.499 | state | check after the steps: pass |
| 55.499 | state | Both MLAG pairs are connected, with switch-a1 and switch-b1 as MLAG primaries. pass |
| 55.499 | state | All four switches run with spanning tree off. pass |
| 55.499 | state | The inter-pair bond runs with lacp-strict=no on all four switches. pass |
| 55.499 | state | Both inter-pair bond members are synchronized, collecting and distributing at all four ends. pass |
| 55.499 | state | Both cables of every host are eligible in its LACP bond. pass |
| 55.499 | streams | measurement ended; captures wait for final replies |
| 56.004 | stopped | captures and streams stopped |
| 56.034 | switch-a1 log | script,info networka reboot-b-secondary end |
| 56.075 | switch-a2 log | script,info networka reboot-b-secondary end |
| 56.125 | switch-b1 log | script,info networka reboot-b-secondary end |
| 56.176 | switch-b2 log | script,info networka reboot-b-secondary end |
| 56.182 | switch log | marker 'networka reboot-b-secondary end' written on switch-a1, switch-a2, switch-b1, switch-b2 |
