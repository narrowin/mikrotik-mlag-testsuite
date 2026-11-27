# FAIL — core-reboot

Reboot the core MLAG primary at dc1, then at dc2, while measuring both sites and both DCI directions. Each reboot must leave the site streams untouched and the DCI must recover through the surviving core.

- Step Reboot dc1-core1 is fail.
- Step Reboot dc2-core1 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 166 pings recorded lost, 437 sent in this step (configured interval 100 ms) | 17.1303 to 22.4263 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 211 at one ping every 100 ms | 21.7702 to 21.9759 s | fail |
| Reboot dc1-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 10 at one ping every 100 ms | 0.936226 to 1.1396 s | pass |
| Reboot dc1-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 10 at one ping every 100 ms | 0.939774 to 1.145 s | pass |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 167 at one ping every 100 ms | 17.1048 to 17.3103 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 169 at one ping every 100 ms | 17.0883 to 17.2947 s | fail |
| Reboot dc2-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 3 at one ping every 100 ms | 0.208652 to 0.414864 s | pass |
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

- Uptime before dispatch was 97 s. The switch reported 23 s at +30.7882 s.
- Full lab state was pass at +33.5277 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 150 s. The switch reported 17 s at +24.2614 s.
- Full lab state was pass at +27.0129 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.882 | test | core-reboot started in lab large-mlag |
| -6.584 | dc1-core1 log | script,info networka core-reboot start |
| -6.295 | dc1-core2 log | script,info networka core-reboot start |
| -5.976 | dc1-dist1 log | script,info networka core-reboot start |
| -5.672 | dc1-dist2 log | script,info networka core-reboot start |
| -5.354 | dc1-firewall log | script,info networka core-reboot start |
| -5.057 | dc2-core1 log | script,info networka core-reboot start |
| -4.727 | dc2-core2 log | script,info networka core-reboot start |
| -4.429 | dc2-dist1 log | script,info networka core-reboot start |
| -4.129 | dc2-dist2 log | script,info networka core-reboot start |
| -3.813 | dc2-firewall log | script,info networka core-reboot start |
| -3.802 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.148 | state | check before the steps: pass |
| -0.148 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.148 | state | Every switch runs with spanning tree off. pass |
| -0.148 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.148 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.148 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.148 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.135 | capture | started at dc1-service:bond0 |
| -0.135 | capture | started at dc1-traffic:bond0 |
| -0.135 | capture | started at dc1-traffic:vlan390 |
| -0.134 | capture | started at dc2-service:bond0 |
| -0.082 | capture | started at dc2-traffic:bond0 |
| -0.082 | capture | started at dc2-traffic:vlan390 |
| -0.024 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.014 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.010 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.008 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.004 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.085 | quiet window | clean |
| 4.086 | step | Baseline |
| 8.087 | step | Reboot dc1-core1 |
| 8.150 | reboot | dispatching the reboot to dc1-core1 |
| 8.228 | reboot | dc1-core1 command returned: accepted |
| 8.604 | dc2-to-dc1-over-dci | 209 pings lost at one ping every 100 ms, traffic stopped for 21.77 to 21.976 s, late reply, request absent at destination |
| 8.613 | dc1-to-dc2-over-dci | Diagnostic only: 164 pings recorded lost (configured interval 100 ms), observed stop bounds 17.1303 to 22.4263 s, request absent at destination |
| 20.348 | dc1-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.309 | dc1-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 29.257 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 29.267 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 29.540 | dc2-traffic-to-vrrp | 10 pings lost at one ping every 100 ms, traffic stopped for 0.94 to 1.145 s, reply absent at source |
| 29.617 | dc1-traffic-to-vrrp | 10 pings lost at one ping every 100 ms, traffic stopped for 0.936 to 1.14 s, reply absent at source |
| 31.294 | dc1-to-dc2-over-dci | Diagnostic only: 2 pings recorded lost (configured interval 100 ms), observed stop bounds 0.105625 to 0.313886 s, request absent at destination |
| 31.298 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.309 s, request absent at destination |
| 41.678 | recovery | full lab state after reboot of dc1-core1: pass |
| 57.680 | step | dc1 reboot recovery |
| 60.682 | step | Reboot dc2-core1 |
| 60.762 | reboot | dispatching the reboot to dc2-core1 |
| 60.823 | reboot | dc2-core1 command returned: accepted |
| 61.271 | dc2-to-dc1-over-dci | 165 pings lost at one ping every 100 ms, traffic stopped for 17.088 to 17.295 s, reply absent at source, request absent at destination |
| 61.320 | dc1-to-dc2-over-dci | 165 pings lost at one ping every 100 ms, traffic stopped for 17.105 to 17.31 s, request absent at destination |
| 72.957 | dc2-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 77.908 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 77.918 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 78.168 | dc2-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.415 s, reply absent at source |
| 78.565 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 78.773 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 79.997 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.313 s, request absent at destination |
| 80.053 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.314 s, request absent at destination |
| 87.775 | recovery | full lab state after reboot of dc2-core1: pass |
| 103.778 | step | dc2 reboot recovery |
| 106.782 | steps | last step ended |
| 110.169 | state | check after the steps: pass |
| 110.169 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 110.169 | state | Every switch runs with spanning tree off. pass |
| 110.169 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 110.169 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 110.169 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 110.169 | state | Both cables of every host are eligible in its LACP bond. pass |
| 110.169 | streams | measurement ended; captures wait for final replies |
| 110.683 | stopped | captures and streams stopped |
| 110.714 | dc1-core1 log | script,info networka core-reboot end |
| 110.752 | dc1-core2 log | script,info networka core-reboot end |
| 110.786 | dc1-dist1 log | script,info networka core-reboot end |
| 110.824 | dc1-dist2 log | script,info networka core-reboot end |
| 110.873 | dc1-firewall log | script,info networka core-reboot end |
| 110.911 | dc2-core1 log | script,info networka core-reboot end |
| 110.960 | dc2-core2 log | script,info networka core-reboot end |
| 110.995 | dc2-dist1 log | script,info networka core-reboot end |
| 111.027 | dc2-dist2 log | script,info networka core-reboot end |
| 111.080 | dc2-firewall log | script,info networka core-reboot end |
| 111.094 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
