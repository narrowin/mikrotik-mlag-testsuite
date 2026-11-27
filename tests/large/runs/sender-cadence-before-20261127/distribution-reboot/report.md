# FAIL — distribution-reboot

Reboot dc1-dist1 in its MLAG primary role, then dc1-dist2 in its secondary role. The dc1 site stream and both DCI directions must recover through the surviving peer; dc2 must continue.

- Step Reboot dc1-dist1 is fail.
- Step Reboot dc1-dist2 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 13 at one ping every 100 ms | 1.31454 to 1.52033 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 120 pings recorded lost, 414 sent in this step (configured interval 100 ms) | 12.3911 to 20.0675 s (diagnostic) | error. Sender cadence was invalid in this step. |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 190 at one ping every 100 ms | 19.6957 to 19.9003 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 4 at one ping every 100 ms | 0.304169 to 0.506189 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 30 at one ping every 100 ms | 2.92231 to 3.12713 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | Diagnostic only: 72 pings recorded lost, 310 sent in this step (configured interval 100 ms) | 19.6405 to 19.8451 s (diagnostic) | error. Sender cadence was invalid in this step. |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 3 at one ping every 100 ms | 0.214679 to 0.416315 s | fail |
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

- Uptime before dispatch was 105 s. The switch reported 23 s at +30.7085 s.
- Full lab state was pass at +33.4363 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 158 s. The switch reported 17 s at +25.0756 s.
- Full lab state was pass at +27.8774 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.404 | test | distribution-reboot started in lab large-mlag |
| -3.369 | dc1-core1 log | script,info networka distribution-reboot start |
| -3.334 | dc1-core2 log | script,info networka distribution-reboot start |
| -3.283 | dc1-dist1 log | script,info networka distribution-reboot start |
| -3.244 | dc1-dist2 log | script,info networka distribution-reboot start |
| -3.203 | dc1-firewall log | script,info networka distribution-reboot start |
| -3.158 | dc2-core1 log | script,info networka distribution-reboot start |
| -3.111 | dc2-core2 log | script,info networka distribution-reboot start |
| -3.054 | dc2-dist1 log | script,info networka distribution-reboot start |
| -2.997 | dc2-dist2 log | script,info networka distribution-reboot start |
| -2.939 | dc2-firewall log | script,info networka distribution-reboot start |
| -2.933 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.147 | state | check before the steps: pass |
| -0.147 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.147 | state | Every switch runs with spanning tree off. pass |
| -0.147 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.147 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.147 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.147 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.135 | capture | started at dc1-service:bond0 |
| -0.134 | capture | started at dc1-traffic:bond0 |
| -0.133 | capture | started at dc1-traffic:vlan390 |
| -0.133 | capture | started at dc2-service:bond0 |
| -0.133 | capture | started at dc2-traffic:bond0 |
| -0.081 | capture | started at dc2-traffic:vlan390 |
| -0.025 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.014 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.009 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.007 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.005 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.031 | quiet window | clean |
| 4.031 | step | Baseline |
| 8.032 | step | Reboot dc1-dist1 |
| 8.085 | reboot | dispatching the reboot to dc1-dist1 |
| 8.190 | reboot | dc1-dist1 command returned: accepted |
| 8.516 | dc1-to-dc2-over-dci | Diagnostic only: 120 pings recorded lost (configured interval 100 ms), observed outage bounds 12.3911 to 20.0675 s, reply absent at source, request absent at destination |
| 8.522 | dc2-to-dc1-over-dci | 190 pings lost at one ping every 100 ms, traffic stopped for 19.696 to 19.9 s, reply absent at destination, request absent at destination |
| 19.721 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.725 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.921 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 25.933 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 26.073 | dc1-traffic-to-dc1-service | 13 pings lost at one ping every 100 ms, traffic stopped for 1.315 to 1.52 s, request absent at destination |
| 26.126 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.304 to 0.506 s, reply absent at source |
| 41.521 | recovery | full lab state after reboot of dc1-dist1: pass |
| 57.521 | step | dc1-dist1 reboot recovery |
| 60.523 | step | Reboot dc1-dist2 |
| 60.571 | reboot | dispatching the reboot to dc1-dist2 |
| 60.622 | reboot | dc1-dist2 command returned: accepted |
| 61.115 | dc1-traffic-to-dc1-service | 29 pings lost at one ping every 100 ms, traffic stopped for 2.922 to 3.127 s, request absent at destination |
| 61.138 | dc1-traffic-to-vrrp | Diagnostic only: 72 pings recorded lost (configured interval 100 ms), observed outage bounds 19.6405 to 19.8451 s, reply absent at source |
| 71.154 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 76.147 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 78.486 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 78.498 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 78.725 | dc2-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.215 to 0.416 s, reply absent at source |
| 80.741 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 88.448 | recovery | full lab state after reboot of dc1-dist2: pass |
| 104.449 | step | dc1-dist2 reboot recovery |
| 107.451 | steps | last step ended |
| 110.844 | state | check after the steps: pass |
| 110.844 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 110.844 | state | Every switch runs with spanning tree off. pass |
| 110.844 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 110.844 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 110.844 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 110.844 | state | Both cables of every host are eligible in its LACP bond. pass |
| 110.844 | streams | measurement ended; captures wait for final replies |
| 111.357 | stopped | captures and streams stopped |
| 111.386 | dc1-core1 log | script,info networka distribution-reboot end |
| 111.427 | dc1-core2 log | script,info networka distribution-reboot end |
| 111.468 | dc1-dist1 log | script,info networka distribution-reboot end |
| 111.502 | dc1-dist2 log | script,info networka distribution-reboot end |
| 111.540 | dc1-firewall log | script,info networka distribution-reboot end |
| 111.576 | dc2-core1 log | script,info networka distribution-reboot end |
| 111.614 | dc2-core2 log | script,info networka distribution-reboot end |
| 111.643 | dc2-dist1 log | script,info networka distribution-reboot end |
| 111.679 | dc2-dist2 log | script,info networka distribution-reboot end |
| 111.712 | dc2-firewall log | script,info networka distribution-reboot end |
| 111.719 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
