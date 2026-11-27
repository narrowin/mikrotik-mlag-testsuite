# FAIL — core-reboot

Reboot the core MLAG primary at dc1, then at dc2, while measuring both sites and both DCI directions. Each reboot must leave the site streams and the bypass untouched and the DCI must recover through the surviving core.

- Step Reboot dc1-core1 is fail.
- Step Reboot dc2-core1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 200 at one ping every 100 ms | 20.6411 to 20.8464 s | fail |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 198 at one ping every 100 ms | 20.4247 to 20.6318 s | fail |
| Reboot dc1-core1 | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 190 at one ping every 100 ms | 19.3961 to 19.6004 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 191 at one ping every 100 ms | 19.3835 to 19.5984 s | fail |
| Reboot dc2-core1 | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Reboot of dc1-core1

Reboot dc1-core1 · pass

- Uptime before dispatch was 388 s. The switch reported 23 s at +30.8604 s.
- Full lab state was pass at +33.7595 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 388 s. The switch reported 23 s at +30.9765 s.
- Full lab state was pass at +33.9062 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -7.435 | test | core-reboot started in lab large-mlag |
| -7.105 | dc1-core1 log | script,info networka core-reboot start |
| -6.779 | dc1-core2 log | script,info networka core-reboot start |
| -6.438 | dc1-dist1 log | script,info networka core-reboot start |
| -6.107 | dc1-dist2 log | script,info networka core-reboot start |
| -5.687 | dc1-firewall log | script,info networka core-reboot start |
| -5.363 | dc2-core1 log | script,info networka core-reboot start |
| -5.032 | dc2-core2 log | script,info networka core-reboot start |
| -4.674 | dc2-dist1 log | script,info networka core-reboot start |
| -4.335 | dc2-dist2 log | script,info networka core-reboot start |
| -4.001 | dc2-firewall log | script,info networka core-reboot start |
| -3.997 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.141 | state | check before the steps: pass |
| -0.141 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.141 | state | Every switch runs with spanning tree off. pass |
| -0.141 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.141 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.141 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.141 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.131 | capture | started at dc1-service:bond0 |
| -0.131 | capture | started at dc1-traffic:bond0 |
| -0.130 | capture | started at dc1-traffic:eth3 |
| -0.130 | capture | started at dc1-traffic:vlan390 |
| -0.130 | capture | started at dc2-service:bond0 |
| -0.076 | capture | started at dc2-traffic:bond0 |
| -0.076 | capture | started at dc2-traffic:eth3 |
| -0.076 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.014 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.011 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.007 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | bypass-dc1-to-dc2 | started from dc1-traffic:eth3 to dc2-traffic:eth3 at 198.51.100.2 |
| -0.000 | bypass-dc2-to-dc1 | started from dc2-traffic:eth3 to dc1-traffic:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.626 | quiet window | clean |
| 4.627 | step | Baseline |
| 8.629 | step | Reboot dc1-core1 |
| 8.686 | reboot | dispatching the reboot to dc1-core1 |
| 8.743 | reboot | dc1-core1 command returned: accepted |
| 9.145 | dc1-to-dc2-over-dci | 199 pings lost at one ping every 100 ms, traffic stopped for 20.641 to 20.846 s, reply absent at source, request absent at destination |
| 9.240 | dc2-to-dc1-over-dci | 197 pings lost at one ping every 100 ms, traffic stopped for 20.425 to 20.632 s, request absent at destination |
| 27.958 | dc1-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 29.025 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 29.036 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 30.989 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 31.010 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 42.446 | recovery | full lab state after reboot of dc1-core1: pass |
| 58.446 | step | dc1 reboot recovery |
| 61.447 | step | Reboot dc2-core1 |
| 61.497 | reboot | dispatching the reboot to dc2-core1 |
| 61.542 | reboot | dc2-core1 command returned: accepted |
| 61.957 | dc1-to-dc2-over-dci | 187 pings lost at one ping every 100 ms, traffic stopped for 19.396 to 19.6 s, request absent at destination |
| 61.968 | dc2-to-dc1-over-dci | 187 pings lost at one ping every 100 ms, traffic stopped for 19.383 to 19.598 s, reply absent at source, request absent at destination |
| 81.092 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 81.111 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 81.557 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.417 s, request absent at destination |
| 81.559 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.416 s, request absent at destination |
| 82.074 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, request absent at destination |
| 95.403 | recovery | full lab state after reboot of dc2-core1: pass |
| 111.404 | step | dc2 reboot recovery |
| 114.406 | steps | last step ended |
| 117.897 | state | check after the steps: pass |
| 117.897 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 117.897 | state | Every switch runs with spanning tree off. pass |
| 117.897 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 117.897 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 117.897 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 117.897 | state | Both cables of every host are eligible in its LACP bond. pass |
| 117.897 | streams | measurement ended; captures wait for final replies |
| 118.403 | stopped | captures and streams stopped |
| 118.439 | dc1-core1 log | script,info networka core-reboot end |
| 118.471 | dc1-core2 log | script,info networka core-reboot end |
| 118.502 | dc1-dist1 log | script,info networka core-reboot end |
| 118.550 | dc1-dist2 log | script,info networka core-reboot end |
| 118.600 | dc1-firewall log | script,info networka core-reboot end |
| 118.633 | dc2-core1 log | script,info networka core-reboot end |
| 118.664 | dc2-core2 log | script,info networka core-reboot end |
| 118.697 | dc2-dist1 log | script,info networka core-reboot end |
| 118.731 | dc2-dist2 log | script,info networka core-reboot end |
| 118.782 | dc2-firewall log | script,info networka core-reboot end |
| 118.790 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
