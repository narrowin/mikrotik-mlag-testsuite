# FAIL — distribution-reboot

Reboot dc1-dist1 in its MLAG primary role, then dc1-dist2 in its secondary role. The dc1 site stream and both DCI directions must recover through the surviving peer; dc2 must continue.

- Step Reboot dc1-dist1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 162 at one ping every 100 ms | 16.7956 to 17.0008 s | fail |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 162 at one ping every 100 ms | 16.7783 to 16.983 s | fail |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 29 at one ping every 100 ms | 2.91919 to 3.12691 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of dc1-dist1

Reboot dc1-dist1 · pass

- Uptime before dispatch was 233 s. The switch reported 16 s at +22.8968 s.
- Full lab state was pass at +25.476 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 277 s. The switch reported 16 s at +22.886 s.
- Full lab state was pass at +25.5031 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.718 | test | distribution-reboot started in lab large-mlag |
| -6.382 | dc1-core1 log | script,info networka distribution-reboot start |
| -6.084 | dc1-core2 log | script,info networka distribution-reboot start |
| -5.786 | dc1-dist1 log | script,info networka distribution-reboot start |
| -5.488 | dc1-dist2 log | script,info networka distribution-reboot start |
| -5.180 | dc1-firewall log | script,info networka distribution-reboot start |
| -4.889 | dc2-core1 log | script,info networka distribution-reboot start |
| -4.605 | dc2-core2 log | script,info networka distribution-reboot start |
| -4.304 | dc2-dist1 log | script,info networka distribution-reboot start |
| -3.993 | dc2-dist2 log | script,info networka distribution-reboot start |
| -3.677 | dc2-firewall log | script,info networka distribution-reboot start |
| -3.673 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.134 | state | check before the steps: pass |
| -0.134 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.134 | state | Every switch runs with spanning tree off. pass |
| -0.134 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.134 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.134 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.134 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.123 | capture | started at dc1-service:bond0 |
| -0.123 | capture | started at dc1-traffic:bond0 |
| -0.123 | capture | started at dc1-traffic:vlan390 |
| -0.071 | capture | started at dc2-service:bond0 |
| -0.071 | capture | started at dc2-traffic:bond0 |
| -0.071 | capture | started at dc2-traffic:vlan390 |
| -0.015 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.011 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.006 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.002 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.048 | quiet window | clean |
| 4.049 | step | Baseline |
| 8.051 | step | Reboot dc1-dist1 |
| 8.104 | reboot | dispatching the reboot to dc1-dist1 |
| 8.149 | reboot | dc1-dist1 command returned: accepted |
| 8.467 | dc1-to-dc2-over-dci | 162 pings lost at one ping every 100 ms, traffic stopped for 16.796 to 17.001 s, reply absent at source, request absent at destination |
| 8.484 | dc2-to-dc1-over-dci | 162 pings lost at one ping every 100 ms, traffic stopped for 16.778 to 16.983 s, reply absent at source, request absent at destination |
| 24.319 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 24.328 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 33.580 | recovery | full lab state after reboot of dc1-dist1: pass |
| 49.581 | step | dc1-dist1 reboot recovery |
| 52.583 | step | Reboot dc1-dist2 |
| 52.652 | reboot | dispatching the reboot to dc1-dist2 |
| 52.722 | reboot | dc1-dist2 command returned: accepted |
| 53.047 | dc1-traffic-to-dc1-service | 29 pings lost at one ping every 100 ms, traffic stopped for 2.919 to 3.127 s, request absent at destination |
| 64.494 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 68.773 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 68.787 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 78.155 | recovery | full lab state after reboot of dc1-dist2: pass |
| 94.156 | step | dc1-dist2 reboot recovery |
| 97.158 | steps | last step ended |
| 100.606 | state | check after the steps: pass |
| 100.606 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 100.606 | state | Every switch runs with spanning tree off. pass |
| 100.606 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 100.606 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 100.606 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 100.606 | state | Both cables of every host are eligible in its LACP bond. pass |
| 100.606 | streams | measurement ended; captures wait for final replies |
| 101.115 | stopped | captures and streams stopped |
| 101.141 | dc1-core1 log | script,info networka distribution-reboot end |
| 101.184 | dc1-core2 log | script,info networka distribution-reboot end |
| 101.216 | dc1-dist1 log | script,info networka distribution-reboot end |
| 101.251 | dc1-dist2 log | script,info networka distribution-reboot end |
| 101.287 | dc1-firewall log | script,info networka distribution-reboot end |
| 101.335 | dc2-core1 log | script,info networka distribution-reboot end |
| 101.376 | dc2-core2 log | script,info networka distribution-reboot end |
| 101.411 | dc2-dist1 log | script,info networka distribution-reboot end |
| 101.446 | dc2-dist2 log | script,info networka distribution-reboot end |
| 101.498 | dc2-firewall log | script,info networka distribution-reboot end |
| 101.505 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
