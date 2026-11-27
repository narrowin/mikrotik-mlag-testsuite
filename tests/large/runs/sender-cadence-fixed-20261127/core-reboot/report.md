# FAIL — core-reboot

Reboot the core MLAG primary at dc1, then at dc2, while measuring both sites and both DCI directions. Each reboot must leave the site streams untouched and the DCI must recover through the surviving core.

- Step Reboot dc1-core1 is fail.
- Step Reboot dc2-core1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 167 at one ping every 100 ms | 17.1767 to 17.3821 s | fail |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 167 at one ping every 100 ms | 17.1428 to 17.3486 s | fail |
| Reboot dc1-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 7 at one ping every 100 ms | 0.625907 to 0.832879 s | pass |
| Reboot dc1-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 6 at one ping every 100 ms | 0.520594 to 0.727469 s | pass |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 182 at one ping every 100 ms | 18.5431 to 18.7456 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 181 at one ping every 100 ms | 18.3405 to 18.5473 s | fail |
| Reboot dc2-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 10 at one ping every 100 ms | 0.943947 to 1.15 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 12 at one ping every 100 ms | 0.847946 to 1.05466 s | pass |
| dc2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Reboot of dc1-core1

Reboot dc1-core1 · pass

- Uptime before dispatch was 219 s. The switch reported 17 s at +24.1256 s.
- Full lab state was pass at +26.933 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 265 s. The switch reported 23 s at +30.6942 s.
- Full lab state was pass at +33.4585 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.264 | test | core-reboot started in lab large-mlag |
| -3.217 | dc1-core1 log | script,info networka core-reboot start |
| -3.173 | dc1-core2 log | script,info networka core-reboot start |
| -3.132 | dc1-dist1 log | script,info networka core-reboot start |
| -3.096 | dc1-dist2 log | script,info networka core-reboot start |
| -3.049 | dc1-firewall log | script,info networka core-reboot start |
| -2.994 | dc2-core1 log | script,info networka core-reboot start |
| -2.955 | dc2-core2 log | script,info networka core-reboot start |
| -2.906 | dc2-dist1 log | script,info networka core-reboot start |
| -2.859 | dc2-dist2 log | script,info networka core-reboot start |
| -2.824 | dc2-firewall log | script,info networka core-reboot start |
| -2.812 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.131 | state | check before the steps: pass |
| -0.131 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.131 | state | Every switch runs with spanning tree off. pass |
| -0.131 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.131 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.131 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.131 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.071 | capture | started at dc1-service:bond0 |
| -0.071 | capture | started at dc1-traffic:bond0 |
| -0.071 | capture | started at dc1-traffic:vlan390 |
| -0.070 | capture | started at dc2-service:bond0 |
| -0.070 | capture | started at dc2-traffic:bond0 |
| -0.070 | capture | started at dc2-traffic:vlan390 |
| -0.014 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.011 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.008 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.002 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.005 | quiet window | clean |
| 4.005 | step | Baseline |
| 8.006 | step | Reboot dc1-core1 |
| 8.049 | reboot | dispatching the reboot to dc1-core1 |
| 8.112 | reboot | dc1-core1 command returned: accepted |
| 8.529 | dc1-to-dc2-over-dci | 165 pings lost at one ping every 100 ms, traffic stopped for 17.177 to 17.382 s, reply absent at source, request absent at destination |
| 8.545 | dc2-to-dc1-over-dci | 165 pings lost at one ping every 100 ms, traffic stopped for 17.143 to 17.349 s, request absent at destination |
| 20.976 | dc1-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.227 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 25.235 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 25.351 | dc1-traffic-to-vrrp | 7 pings lost at one ping every 100 ms, traffic stopped for 0.626 to 0.833 s, reply absent at source |
| 25.409 | dc2-traffic-to-vrrp | 6 pings lost at one ping every 100 ms, traffic stopped for 0.521 to 0.727 s, reply absent at source |
| 25.895 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 25.911 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 27.318 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 27.340 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 34.981 | recovery | full lab state after reboot of dc1-core1: pass |
| 50.984 | step | dc1 reboot recovery |
| 53.985 | step | Reboot dc2-core1 |
| 54.033 | reboot | dispatching the reboot to dc2-core1 |
| 54.076 | reboot | dc2-core1 command returned: accepted |
| 54.428 | dc1-to-dc2-over-dci | 179 pings lost at one ping every 100 ms, traffic stopped for 18.543 to 18.746 s, request absent at destination |
| 54.484 | dc2-to-dc1-over-dci | 177 pings lost at one ping every 100 ms, traffic stopped for 18.341 to 18.547 s, reply absent at source, request absent at destination |
| 72.305 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 72.311 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 72.518 | dc2-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.419 s, reply absent at source |
| 72.906 | dc1-traffic-to-vrrp | 10 pings lost at one ping every 100 ms, traffic stopped for 0.944 to 1.15 s, reply absent at source |
| 72.937 | dc2-traffic-to-vrrp | 9 pings lost at one ping every 100 ms, traffic stopped for 0.848 to 1.055 s, reply absent at source |
| 73.134 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 73.173 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 74.360 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.419 s, request absent at destination |
| 74.401 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.31 s, request absent at destination |
| 87.491 | recovery | full lab state after reboot of dc2-core1: pass |
| 103.492 | step | dc2 reboot recovery |
| 106.496 | steps | last step ended |
| 109.965 | state | check after the steps: pass |
| 109.965 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 109.965 | state | Every switch runs with spanning tree off. pass |
| 109.965 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 109.965 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 109.965 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 109.965 | state | Both cables of every host are eligible in its LACP bond. pass |
| 109.966 | streams | measurement ended; captures wait for final replies |
| 110.475 | stopped | captures and streams stopped |
| 110.510 | dc1-core1 log | script,info networka core-reboot end |
| 110.545 | dc1-core2 log | script,info networka core-reboot end |
| 110.585 | dc1-dist1 log | script,info networka core-reboot end |
| 110.640 | dc1-dist2 log | script,info networka core-reboot end |
| 110.666 | dc1-firewall log | script,info networka core-reboot end |
| 110.728 | dc2-core1 log | script,info networka core-reboot end |
| 110.772 | dc2-core2 log | script,info networka core-reboot end |
| 110.809 | dc2-dist1 log | script,info networka core-reboot end |
| 110.840 | dc2-dist2 log | script,info networka core-reboot end |
| 110.883 | dc2-firewall log | script,info networka core-reboot end |
| 110.887 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
