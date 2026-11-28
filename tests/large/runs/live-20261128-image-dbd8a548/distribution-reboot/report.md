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
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 8 at one ping every 100 ms | 0.719056 to 0.927201 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 178 at one ping every 100 ms | 16.3657 to 16.5695 s | fail |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 179 at one ping every 100 ms | 16.4579 to 16.6639 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 4 at one ping every 100 ms | 0.301967 to 0.513421 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 31 at one ping every 100 ms | 3.02915 to 3.23463 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 190 at one ping every 100 ms | 18.0156 to 18.2229 s | fail |
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

- Uptime before dispatch was 246 s. The switch reported 17 s at +23.9579 s.
- Full lab state was pass at +26.8056 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 293 s. The switch reported 22 s at +30.8483 s.
- Full lab state was pass at +33.8168 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.804 | test | distribution-reboot started in lab large-mlag |
| -6.496 | dc1-core1 log | script,info networka distribution-reboot start |
| -6.190 | dc1-core2 log | script,info networka distribution-reboot start |
| -5.887 | dc1-dist1 log | script,info networka distribution-reboot start |
| -5.565 | dc1-dist2 log | script,info networka distribution-reboot start |
| -5.258 | dc1-firewall log | script,info networka distribution-reboot start |
| -4.929 | dc2-core1 log | script,info networka distribution-reboot start |
| -4.620 | dc2-core2 log | script,info networka distribution-reboot start |
| -4.315 | dc2-dist1 log | script,info networka distribution-reboot start |
| -4.022 | dc2-dist2 log | script,info networka distribution-reboot start |
| -3.730 | dc2-firewall log | script,info networka distribution-reboot start |
| -3.722 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.145 | state | check before the steps: pass |
| -0.145 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.145 | state | Every switch runs with spanning tree off. pass |
| -0.145 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.145 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.145 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.145 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.134 | capture | started at dc1-service:bond0 |
| -0.134 | capture | started at dc1-traffic:bond0 |
| -0.133 | capture | started at dc1-traffic:vlan390 |
| -0.133 | capture | started at dc2-service:bond0 |
| -0.133 | capture | started at dc2-traffic:bond0 |
| -0.081 | capture | started at dc2-traffic:vlan390 |
| -0.026 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.021 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.016 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.011 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.008 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.006 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.046 | quiet window | clean |
| 4.046 | step | Baseline |
| 8.046 | step | Reboot dc1-dist1 |
| 8.102 | reboot | dispatching the reboot to dc1-dist1 |
| 8.167 | reboot | dc1-dist1 command returned: accepted |
| 8.522 | dc2-to-dc1-over-dci | 159 pings lost at one ping every 100 ms, traffic stopped for 16.458 to 16.664 s, request absent at destination |
| 8.526 | dc1-to-dc2-over-dci | 158 pings lost at one ping every 100 ms, traffic stopped for 16.366 to 16.569 s, reply absent at source, request absent at destination |
| 20.301 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.917 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 24.927 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 25.184 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.417 to 0.625 s, request absent at destination |
| 25.196 | dc1-traffic-to-dc1-service | 8 pings lost at one ping every 100 ms, traffic stopped for 0.719 to 0.927 s, request absent at destination |
| 25.197 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.405 to 0.611 s, reply absent at source, request absent at destination |
| 25.200 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.302 to 0.513 s, reply absent at source |
| 25.808 | dc1-to-dc2-over-dci | 15 pings lost at one ping every 100 ms, traffic stopped for 1.474 to 1.679 s, reply absent at source |
| 25.808 | dc2-to-dc1-over-dci | 15 pings lost at one ping every 100 ms, traffic stopped for 1.481 to 1.688 s, request absent at destination |
| 34.908 | recovery | full lab state after reboot of dc1-dist1: pass |
| 50.911 | step | dc1-dist1 reboot recovery |
| 53.931 | step | Reboot dc1-dist2 |
| 54.044 | reboot | dispatching the reboot to dc1-dist2 |
| 54.124 | reboot | dc1-dist2 command returned: accepted |
| 55.375 | dc1-traffic-to-dc1-service | 30 pings lost at one ping every 100 ms, traffic stopped for 3.029 to 3.235 s, reply absent at source, request absent at destination |
| 55.411 | dc1-traffic-to-vrrp | 174 pings lost at one ping every 100 ms, traffic stopped for 18.016 to 18.223 s, reply absent at source |
| 70.106 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 73.445 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 73.465 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 73.733 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, reply absent at source |
| 74.141 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.307 s, reply absent at source |
| 74.447 | dc1-traffic-to-vrrp | 13 pings lost at one ping every 100 ms, traffic stopped for 1.244 to 1.45 s, reply absent at source |
| 75.737 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 87.861 | recovery | full lab state after reboot of dc1-dist2: pass |
| 103.862 | step | dc1-dist2 reboot recovery |
| 106.863 | steps | last step ended |
| 111.382 | state | check after the steps: pass |
| 111.382 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 111.382 | state | Every switch runs with spanning tree off. pass |
| 111.382 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 111.382 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 111.382 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 111.382 | state | Both cables of every host are eligible in its LACP bond. pass |
| 111.384 | streams | measurement ended; captures wait for final replies |
| 111.912 | stopped | captures and streams stopped |
| 111.949 | dc1-core1 log | script,info networka distribution-reboot end |
| 111.996 | dc1-core2 log | script,info networka distribution-reboot end |
| 112.037 | dc1-dist1 log | script,info networka distribution-reboot end |
| 112.091 | dc1-dist2 log | script,info networka distribution-reboot end |
| 112.131 | dc1-firewall log | script,info networka distribution-reboot end |
| 112.189 | dc2-core1 log | script,info networka distribution-reboot end |
| 112.229 | dc2-core2 log | script,info networka distribution-reboot end |
| 112.272 | dc2-dist1 log | script,info networka distribution-reboot end |
| 112.317 | dc2-dist2 log | script,info networka distribution-reboot end |
| 112.359 | dc2-firewall log | script,info networka distribution-reboot end |
| 112.371 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
