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
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 155 at one ping every 100 ms | 15.6454 to 15.8523 s | fail |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 153 at one ping every 100 ms | 15.6203 to 15.8274 s | fail |
| Reboot dc1-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 191 at one ping every 100 ms | 19.6682 to 19.872 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 193 at one ping every 100 ms | 19.6832 to 19.8948 s | fail |
| Reboot dc2-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 3 at one ping every 100 ms | 0.208833 to 0.413959 s | pass |
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

- Uptime before dispatch was 95 s. The switch reported 16 s at +23.8723 s.
- Full lab state was pass at +26.6109 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 140 s. The switch reported 23 s at +30.869 s.
- Full lab state was pass at +33.7381 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.860 | test | core-reboot started in lab large-mlag |
| -6.561 | dc1-core1 log | script,info networka core-reboot start |
| -6.264 | dc1-core2 log | script,info networka core-reboot start |
| -5.967 | dc1-dist1 log | script,info networka core-reboot start |
| -5.646 | dc1-dist2 log | script,info networka core-reboot start |
| -5.339 | dc1-firewall log | script,info networka core-reboot start |
| -5.041 | dc2-core1 log | script,info networka core-reboot start |
| -4.744 | dc2-core2 log | script,info networka core-reboot start |
| -4.441 | dc2-dist1 log | script,info networka core-reboot start |
| -4.126 | dc2-dist2 log | script,info networka core-reboot start |
| -3.829 | dc2-firewall log | script,info networka core-reboot start |
| -3.818 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.144 | state | check before the steps: pass |
| -0.144 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.144 | state | Every switch runs with spanning tree off. pass |
| -0.144 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.144 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.144 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.144 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.133 | capture | started at dc1-service:bond0 |
| -0.133 | capture | started at dc1-traffic:bond0 |
| -0.133 | capture | started at dc1-traffic:vlan390 |
| -0.133 | capture | started at dc2-service:bond0 |
| -0.081 | capture | started at dc2-traffic:bond0 |
| -0.081 | capture | started at dc2-traffic:vlan390 |
| -0.025 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.013 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.008 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.004 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.103 | quiet window | clean |
| 4.104 | step | Baseline |
| 8.105 | step | Reboot dc1-core1 |
| 8.172 | reboot | dispatching the reboot to dc1-core1 |
| 8.237 | reboot | dc1-core1 command returned: accepted |
| 8.624 | dc2-to-dc1-over-dci | 151 pings lost at one ping every 100 ms, traffic stopped for 15.62 to 15.827 s, request absent at destination |
| 8.639 | dc1-to-dc2-over-dci | 151 pings lost at one ping every 100 ms, traffic stopped for 15.645 to 15.852 s, request absent at destination |
| 25.197 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 25.209 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 25.505 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.347 to 0.556 s, request absent at destination |
| 25.670 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.308 s, request absent at destination |
| 34.783 | recovery | full lab state after reboot of dc1-core1: pass |
| 50.785 | step | dc1 reboot recovery |
| 53.799 | step | Reboot dc2-core1 |
| 53.888 | reboot | dispatching the reboot to dc2-core1 |
| 53.959 | reboot | dc2-core1 command returned: accepted |
| 54.341 | dc2-to-dc1-over-dci | 190 pings lost at one ping every 100 ms, traffic stopped for 19.683 to 19.895 s, request absent at destination |
| 54.410 | dc1-to-dc2-over-dci | 190 pings lost at one ping every 100 ms, traffic stopped for 19.668 to 19.872 s, request absent at destination |
| 71.532 | dc2-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 73.571 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 73.587 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 73.780 | dc2-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.414 s, reply absent at source |
| 74.235 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 74.439 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 75.761 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 75.802 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 87.626 | recovery | full lab state after reboot of dc2-core1: pass |
| 103.629 | step | dc2 reboot recovery |
| 106.634 | steps | last step ended |
| 111.158 | state | check after the steps: pass |
| 111.158 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 111.158 | state | Every switch runs with spanning tree off. pass |
| 111.158 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 111.158 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 111.158 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 111.158 | state | Both cables of every host are eligible in its LACP bond. pass |
| 111.158 | streams | measurement ended; captures wait for final replies |
| 111.665 | stopped | captures and streams stopped |
| 111.707 | dc1-core1 log | script,info networka core-reboot end |
| 111.745 | dc1-core2 log | script,info networka core-reboot end |
| 111.800 | dc1-dist1 log | script,info networka core-reboot end |
| 111.844 | dc1-dist2 log | script,info networka core-reboot end |
| 111.883 | dc1-firewall log | script,info networka core-reboot end |
| 111.932 | dc2-core1 log | script,info networka core-reboot end |
| 111.977 | dc2-core2 log | script,info networka core-reboot end |
| 112.012 | dc2-dist1 log | script,info networka core-reboot end |
| 112.055 | dc2-dist2 log | script,info networka core-reboot end |
| 112.106 | dc2-firewall log | script,info networka core-reboot end |
| 112.111 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
