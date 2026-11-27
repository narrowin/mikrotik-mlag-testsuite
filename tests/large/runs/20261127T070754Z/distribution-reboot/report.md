# FAIL — distribution-reboot

Reboot dc1-dist1 in its MLAG primary role, then dc1-dist2 in its secondary role. The dc1 site stream and both DCI directions must recover through the surviving peer; dc2 must continue.

- Step Reboot dc1-dist1 is fail.
- Step Reboot dc1-dist2 is error.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 4 at one ping every 100 ms | 0.31482 to 0.52248 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 174 at one ping every 100 ms | 16.373 to 16.5777 s | fail |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 175 at one ping every 100 ms | 18.1493 to 18.3549 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 3 at one ping every 100 ms | 0.208415 to 0.414804 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 26 at one ping every 100 ms | 2.59814 to 2.80893 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | Diagnostic only: 113 pings recorded lost, 344 sent in this step (configured interval 100 ms) | 11.6631 to 18.0564 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of dc1-dist1

Reboot dc1-dist1 · pass

- Uptime before dispatch was 225 s. The switch reported 16 s at +22.9425 s.
- Full lab state was pass at +25.5304 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 270 s. The switch reported 16 s at +22.7285 s.
- Full lab state was pass at +25.348 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.986 | test | distribution-reboot started in lab large-mlag |
| -2.950 | dc1-core1 log | script,info networka distribution-reboot start |
| -2.912 | dc1-core2 log | script,info networka distribution-reboot start |
| -2.877 | dc1-dist1 log | script,info networka distribution-reboot start |
| -2.828 | dc1-dist2 log | script,info networka distribution-reboot start |
| -2.780 | dc1-firewall log | script,info networka distribution-reboot start |
| -2.740 | dc2-core1 log | script,info networka distribution-reboot start |
| -2.691 | dc2-core2 log | script,info networka distribution-reboot start |
| -2.657 | dc2-dist1 log | script,info networka distribution-reboot start |
| -2.604 | dc2-dist2 log | script,info networka distribution-reboot start |
| -2.569 | dc2-firewall log | script,info networka distribution-reboot start |
| -2.565 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.131 | state | check before the steps: pass |
| -0.131 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.131 | state | Every switch runs with spanning tree off. pass |
| -0.131 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.131 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.131 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.131 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.123 | capture | started at dc1-service:bond0 |
| -0.123 | capture | started at dc1-traffic:bond0 |
| -0.122 | capture | started at dc1-traffic:vlan390 |
| -0.071 | capture | started at dc2-service:bond0 |
| -0.071 | capture | started at dc2-traffic:bond0 |
| -0.071 | capture | started at dc2-traffic:vlan390 |
| -0.013 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.010 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.007 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.002 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.033 | quiet window | clean |
| 4.034 | step | Baseline |
| 8.035 | step | Reboot dc1-dist1 |
| 8.096 | reboot | dispatching the reboot to dc1-dist1 |
| 8.175 | reboot | dc1-dist1 command returned: accepted |
| 8.529 | dc1-to-dc2-over-dci | 158 pings lost at one ping every 100 ms, traffic stopped for 16.373 to 16.578 s, reply absent at source, request absent at destination |
| 8.555 | dc2-to-dc1-over-dci | 175 pings lost at one ping every 100 ms, traffic stopped for 18.149 to 18.355 s, reply absent at source, request absent at destination |
| 24.333 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 24.340 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 24.444 | dc1-traffic-to-dc1-service | 4 pings lost at one ping every 100 ms, traffic stopped for 0.315 to 0.522 s, request absent at destination |
| 24.590 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.415 s, reply absent at source |
| 25.107 | dc1-to-dc2-over-dci | 16 pings lost at one ping every 100 ms, traffic stopped for 1.574 to 1.777 s, reply absent at source |
| 33.626 | recovery | full lab state after reboot of dc1-dist1: pass |
| 49.627 | step | dc1-dist1 reboot recovery |
| 52.629 | step | Reboot dc1-dist2 |
| 52.673 | reboot | dispatching the reboot to dc1-dist2 |
| 52.730 | reboot | dc1-dist2 command returned: accepted |
| 53.032 | dc1-traffic-to-dc1-service | 26 pings lost at one ping every 100 ms, traffic stopped for 2.598 to 2.809 s, request absent at destination |
| 53.103 | dc1-traffic-to-vrrp | Diagnostic only: 113 pings recorded lost (configured interval 100 ms), observed stop bounds 11.6631 to 18.0564 s, reply absent at source |
| 64.471 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 68.346 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 68.356 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 78.021 | recovery | full lab state after reboot of dc1-dist2: pass |
| 94.021 | step | dc1-dist2 reboot recovery |
| 97.024 | steps | last step ended |
| 100.185 | state | check after the steps: pass |
| 100.185 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 100.185 | state | Every switch runs with spanning tree off. pass |
| 100.185 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 100.185 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 100.185 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 100.185 | state | Both cables of every host are eligible in its LACP bond. pass |
| 100.186 | streams | measurement ended; captures wait for final replies |
| 100.695 | stopped | captures and streams stopped |
| 100.723 | dc1-core1 log | script,info networka distribution-reboot end |
| 100.757 | dc1-core2 log | script,info networka distribution-reboot end |
| 100.787 | dc1-dist1 log | script,info networka distribution-reboot end |
| 100.822 | dc1-dist2 log | script,info networka distribution-reboot end |
| 100.853 | dc1-firewall log | script,info networka distribution-reboot end |
| 100.897 | dc2-core1 log | script,info networka distribution-reboot end |
| 100.924 | dc2-core2 log | script,info networka distribution-reboot end |
| 100.972 | dc2-dist1 log | script,info networka distribution-reboot end |
| 101.020 | dc2-dist2 log | script,info networka distribution-reboot end |
| 101.054 | dc2-firewall log | script,info networka distribution-reboot end |
| 101.056 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
