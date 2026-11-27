# FAIL — distribution-reboot

Reboot dc1-dist1 in its MLAG primary role, then dc1-dist2 in its secondary role. The dc1 site stream and both DCI directions must recover through the surviving peer; dc2 and the bypass must continue.

- Not valid: dc1-to-dc2-over-dci sent a ping at least every 450 ms.
- Step Reboot dc1-dist1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 10 at one ping every 100 ms | 0.918121 to 1.12338 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 196 pings recorded lost, 471 sent in this step (configured interval 100 ms) | 19.8781 to 20.0845 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 212 at one ping every 100 ms | 19.8843 to 20.0918 s | fail |
| Reboot dc1-dist1 | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 31 at one ping every 100 ms | 2.9204 to 3.1287 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist2 reboot recovery | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:eth3 → dc2-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:eth3 → dc1-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:eth3 → dc2-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:eth3 → dc1-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Reboot of dc1-dist1

Reboot dc1-dist1 · pass

- Uptime before dispatch was 386 s. The switch reported 23 s at +30.8772 s.
- Full lab state was pass at +33.8242 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 439 s. The switch reported 23 s at +30.9446 s.
- Full lab state was pass at +33.8819 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -7.387 | test | distribution-reboot started in lab large-mlag |
| -6.992 | dc1-core1 log | script,info networka distribution-reboot start |
| -6.651 | dc1-core2 log | script,info networka distribution-reboot start |
| -6.306 | dc1-dist1 log | script,info networka distribution-reboot start |
| -5.971 | dc1-dist2 log | script,info networka distribution-reboot start |
| -5.640 | dc1-firewall log | script,info networka distribution-reboot start |
| -5.236 | dc2-core1 log | script,info networka distribution-reboot start |
| -4.910 | dc2-core2 log | script,info networka distribution-reboot start |
| -4.584 | dc2-dist1 log | script,info networka distribution-reboot start |
| -4.257 | dc2-dist2 log | script,info networka distribution-reboot start |
| -3.908 | dc2-firewall log | script,info networka distribution-reboot start |
| -3.904 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.138 | state | check before the steps: pass |
| -0.138 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.138 | state | Every switch runs with spanning tree off. pass |
| -0.138 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.138 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.138 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.138 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.127 | capture | started at dc1-service:bond0 |
| -0.126 | capture | started at dc1-traffic:bond0 |
| -0.126 | capture | started at dc1-traffic:eth3 |
| -0.126 | capture | started at dc1-traffic:vlan390 |
| -0.125 | capture | started at dc2-service:bond0 |
| -0.074 | capture | started at dc2-traffic:bond0 |
| -0.074 | capture | started at dc2-traffic:eth3 |
| -0.074 | capture | started at dc2-traffic:vlan390 |
| -0.019 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.015 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.012 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.008 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | bypass-dc1-to-dc2 | started from dc1-traffic:eth3 to dc2-traffic:eth3 at 198.51.100.2 |
| -0.001 | bypass-dc2-to-dc1 | started from dc2-traffic:eth3 to dc1-traffic:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.313 | quiet window | clean |
| 4.313 | step | Baseline |
| 8.314 | step | Reboot dc1-dist1 |
| 8.363 | reboot | dispatching the reboot to dc1-dist1 |
| 8.415 | reboot | dc1-dist1 command returned: accepted |
| 8.840 | dc1-to-dc2-over-dci | Diagnostic only: 192 pings recorded lost (configured interval 100 ms), observed stop bounds 19.8781 to 20.0845 s, reply absent at source, request absent at destination |
| 8.842 | dc2-to-dc1-over-dci | 192 pings lost at one ping every 100 ms, traffic stopped for 19.884 to 20.092 s, request absent at destination |
| 25.922 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 28.669 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 28.676 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 28.848 | dc1-traffic-to-dc1-service | 10 pings lost at one ping every 100 ms, traffic stopped for 0.918 to 1.123 s, request absent at destination |
| 28.923 | dc1-to-dc2-over-dci | Diagnostic only: 4 pings recorded lost (configured interval 100 ms), observed stop bounds 0.302383 to 2.55027 s, request absent at destination |
| 28.934 | dc2-to-dc1-over-dci | 20 pings lost at one ping every 100 ms, traffic stopped for 1.978 to 2.185 s, request absent at destination |
| 42.187 | recovery | full lab state after reboot of dc1-dist1: pass |
| 58.189 | step | dc1-dist1 reboot recovery |
| 61.190 | step | Reboot dc1-dist2 |
| 61.241 | reboot | dispatching the reboot to dc1-dist2 |
| 61.284 | reboot | dc1-dist2 command returned: accepted |
| 61.721 | dc1-traffic-to-dc1-service | 29 pings lost at one ping every 100 ms, traffic stopped for 2.92 to 3.129 s, reply absent at source, request absent at destination |
| 73.852 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 78.858 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 81.225 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 81.233 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 82.015 | dc1-traffic-to-dc1-service | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.311 s, request absent at destination |
| 95.123 | recovery | full lab state after reboot of dc1-dist2: pass |
| 111.125 | step | dc1-dist2 reboot recovery |
| 114.127 | steps | last step ended |
| 117.634 | state | check after the steps: pass |
| 117.634 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 117.634 | state | Every switch runs with spanning tree off. pass |
| 117.634 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 117.634 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 117.634 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 117.634 | state | Both cables of every host are eligible in its LACP bond. pass |
| 117.634 | streams | measurement ended; captures wait for final replies |
| 118.146 | stopped | captures and streams stopped |
| 118.176 | dc1-core1 log | script,info networka distribution-reboot end |
| 118.211 | dc1-core2 log | script,info networka distribution-reboot end |
| 118.247 | dc1-dist1 log | script,info networka distribution-reboot end |
| 118.284 | dc1-dist2 log | script,info networka distribution-reboot end |
| 118.316 | dc1-firewall log | script,info networka distribution-reboot end |
| 118.351 | dc2-core1 log | script,info networka distribution-reboot end |
| 118.408 | dc2-core2 log | script,info networka distribution-reboot end |
| 118.454 | dc2-dist1 log | script,info networka distribution-reboot end |
| 118.486 | dc2-dist2 log | script,info networka distribution-reboot end |
| 118.526 | dc2-firewall log | script,info networka distribution-reboot end |
| 118.538 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
