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
| Reboot dc1-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 74 pings recorded lost, 320 sent in this step (configured interval 100 ms) | 16.1767 to 16.3821 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 142 at one ping every 100 ms | 14.4685 to 16.7598 s | fail |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 79 pings recorded lost, 342 sent in this step (configured interval 100 ms) | 7.81002 to 16.1718 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 154 at one ping every 100 ms | 15.766 to 15.9704 s | fail |
| dc2 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc2 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

## Reboot of dc1-core1

Reboot dc1-core1 · pass

- Uptime before dispatch was 122 s. The switch reported 16 s at +22.8341 s.
- Full lab state was pass at +25.4821 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 166 s. The switch reported 17 s at +23.7713 s.
- Full lab state was pass at +26.704 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.813 | test | core-reboot started in lab large-mlag |
| -6.508 | dc1-core1 log | script,info networka core-reboot start |
| -6.213 | dc1-core2 log | script,info networka core-reboot start |
| -5.910 | dc1-dist1 log | script,info networka core-reboot start |
| -5.615 | dc1-dist2 log | script,info networka core-reboot start |
| -5.307 | dc1-firewall log | script,info networka core-reboot start |
| -5.003 | dc2-core1 log | script,info networka core-reboot start |
| -4.715 | dc2-core2 log | script,info networka core-reboot start |
| -4.419 | dc2-dist1 log | script,info networka core-reboot start |
| -4.109 | dc2-dist2 log | script,info networka core-reboot start |
| -3.786 | dc2-firewall log | script,info networka core-reboot start |
| -3.769 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.081 | state | check before the steps: pass |
| -0.081 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.081 | state | Every switch runs with spanning tree off. pass |
| -0.081 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.081 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.081 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.081 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.073 | capture | started at dc1-service:bond0 |
| -0.073 | capture | started at dc1-traffic:bond0 |
| -0.070 | capture | started at dc1-traffic:vlan390 |
| -0.069 | capture | started at dc2-service:bond0 |
| -0.069 | capture | started at dc2-traffic:bond0 |
| -0.069 | capture | started at dc2-traffic:vlan390 |
| -0.014 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.011 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.008 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.002 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.276 | quiet window | clean |
| 4.276 | step | Baseline |
| 8.276 | step | Reboot dc1-core1 |
| 8.330 | reboot | dispatching the reboot to dc1-core1 |
| 8.385 | reboot | dc1-core1 command returned: accepted |
| 8.703 | dc1-to-dc2-over-dci | Diagnostic only: 72 pings recorded lost (configured interval 100 ms), observed stop bounds 16.1767 to 16.3821 s, late reply, request absent at destination |
| 8.740 | dc2-to-dc1-over-dci | 140 pings lost at one ping every 100 ms, traffic stopped for 14.469 to 16.76 s, request absent at destination |
| 19.452 | dc1-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 24.370 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 24.379 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 26.491 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.109 to 0.318 s, request absent at destination |
| 26.518 | dc1-to-dc2-over-dci | Diagnostic only: 2 pings recorded lost (configured interval 100 ms), observed stop bounds 0.104555 to 0.313593 s, request absent at destination |
| 33.812 | recovery | full lab state after reboot of dc1-core1: pass |
| 49.814 | step | dc1 reboot recovery |
| 52.815 | step | Reboot dc2-core1 |
| 52.861 | reboot | dispatching the reboot to dc2-core1 |
| 52.919 | reboot | dc2-core1 command returned: accepted |
| 53.290 | dc2-to-dc1-over-dci | 151 pings lost at one ping every 100 ms, traffic stopped for 15.766 to 15.97 s, request absent at destination |
| 53.300 | dc1-to-dc2-over-dci | Diagnostic only: 76 pings recorded lost (configured interval 100 ms), observed stop bounds 7.81002 to 16.1718 s, request absent at destination |
| 69.080 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 69.090 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 69.571 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.314 s, request absent at destination |
| 69.618 | dc1-to-dc2-over-dci | Diagnostic only: 3 pings recorded lost (configured interval 100 ms), observed stop bounds 0.205209 to 0.411403 s, request absent at destination |
| 69.884 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 79.565 | recovery | full lab state after reboot of dc2-core1: pass |
| 95.565 | step | dc2 reboot recovery |
| 98.569 | steps | last step ended |
| 101.794 | state | check after the steps: pass |
| 101.794 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 101.794 | state | Every switch runs with spanning tree off. pass |
| 101.794 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 101.794 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 101.794 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 101.794 | state | Both cables of every host are eligible in its LACP bond. pass |
| 101.795 | streams | measurement ended; captures wait for final replies |
| 102.303 | stopped | captures and streams stopped |
| 102.334 | dc1-core1 log | script,info networka core-reboot end |
| 102.366 | dc1-core2 log | script,info networka core-reboot end |
| 102.415 | dc1-dist1 log | script,info networka core-reboot end |
| 102.464 | dc1-dist2 log | script,info networka core-reboot end |
| 102.514 | dc1-firewall log | script,info networka core-reboot end |
| 102.544 | dc2-core1 log | script,info networka core-reboot end |
| 102.573 | dc2-core2 log | script,info networka core-reboot end |
| 102.601 | dc2-dist1 log | script,info networka core-reboot end |
| 102.644 | dc2-dist2 log | script,info networka core-reboot end |
| 102.689 | dc2-firewall log | script,info networka core-reboot end |
| 102.691 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
