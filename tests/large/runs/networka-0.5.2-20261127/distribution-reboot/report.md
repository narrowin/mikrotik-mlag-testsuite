# FAIL — distribution-reboot

Reboot dc1-dist1 in its MLAG primary role, then dc1-dist2 in its secondary role. The dc1 site stream and both DCI directions must recover through the surviving peer; dc2 must continue.

- Step Reboot dc1-dist1 is fail.
- Step Reboot dc1-dist2 is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 14 at one ping every 100 ms | 1.35298 to 1.56086 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 112 pings recorded lost, 396 sent in this step (configured interval 100 ms) | 11.5521 to 21.051 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 201 at one ping every 100 ms | 20.8559 to 21.0594 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 21 at one ping every 100 ms | 2.08352 to 2.28994 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 154 at one ping every 100 ms | 15.9606 to 19.2843 s | fail |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 2 at one ping every 100 ms | 0.10745 to 0.314317 s | fail |
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

- Uptime before dispatch was 239 s. The switch reported 23 s at +30.8171 s.
- Full lab state was pass at +33.8595 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 292 s. The switch reported 17 s at +23.9752 s.
- Full lab state was pass at +26.6952 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -7.002 | test | distribution-reboot started in lab large-mlag |
| -6.676 | dc1-core1 log | script,info networka distribution-reboot start |
| -6.366 | dc1-core2 log | script,info networka distribution-reboot start |
| -6.054 | dc1-dist1 log | script,info networka distribution-reboot start |
| -5.724 | dc1-dist2 log | script,info networka distribution-reboot start |
| -5.395 | dc1-firewall log | script,info networka distribution-reboot start |
| -5.072 | dc2-core1 log | script,info networka distribution-reboot start |
| -4.762 | dc2-core2 log | script,info networka distribution-reboot start |
| -4.448 | dc2-dist1 log | script,info networka distribution-reboot start |
| -4.101 | dc2-dist2 log | script,info networka distribution-reboot start |
| -3.775 | dc2-firewall log | script,info networka distribution-reboot start |
| -3.761 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.137 | state | check before the steps: pass |
| -0.137 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.137 | state | Every switch runs with spanning tree off. pass |
| -0.137 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.137 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.137 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.137 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.126 | capture | started at dc1-traffic:bond0 |
| -0.126 | capture | started at dc2-service:bond0 |
| -0.074 | capture | started at dc1-service:bond0 |
| -0.074 | capture | started at dc1-traffic:vlan390 |
| -0.074 | capture | started at dc2-traffic:bond0 |
| -0.074 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.015 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.010 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.030 | quiet window | clean |
| 4.030 | step | Baseline |
| 8.030 | step | Reboot dc1-dist1 |
| 8.079 | reboot | dispatching the reboot to dc1-dist1 |
| 8.127 | reboot | dc1-dist1 command returned: accepted |
| 8.533 | dc2-to-dc1-over-dci | 201 pings lost at one ping every 100 ms, traffic stopped for 20.856 to 21.059 s, reply absent at destination, request absent at destination |
| 8.533 | dc1-to-dc2-over-dci | Diagnostic only: 112 pings recorded lost (configured interval 100 ms), observed stop bounds 11.5521 to 21.051 s, reply absent at source, request absent at destination |
| 22.420 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 26.985 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 27.000 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 27.154 | dc1-traffic-to-dc1-service | 14 pings lost at one ping every 100 ms, traffic stopped for 1.353 to 1.561 s, request absent at destination |
| 41.939 | recovery | full lab state after reboot of dc1-dist1: pass |
| 57.940 | step | dc1-dist1 reboot recovery |
| 60.943 | step | Reboot dc1-dist2 |
| 60.992 | reboot | dispatching the reboot to dc1-dist2 |
| 61.039 | reboot | dc1-dist2 command returned: accepted |
| 61.488 | dc1-traffic-to-dc1-service | 21 pings lost at one ping every 100 ms, traffic stopped for 2.084 to 2.29 s, request absent at destination |
| 61.491 | dc1-traffic-to-vrrp | 154 pings lost at one ping every 100 ms, traffic stopped for 15.961 to 19.284 s, reply absent at source |
| 72.163 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 77.162 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 77.883 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 77.893 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 78.415 | dc2-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.314 s, reply absent at source |
| 87.687 | recovery | full lab state after reboot of dc1-dist2: pass |
| 103.687 | step | dc1-dist2 reboot recovery |
| 106.691 | steps | last step ended |
| 110.171 | state | check after the steps: pass |
| 110.171 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 110.171 | state | Every switch runs with spanning tree off. pass |
| 110.171 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 110.171 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 110.171 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 110.171 | state | Both cables of every host are eligible in its LACP bond. pass |
| 110.171 | streams | measurement ended; captures wait for final replies |
| 110.682 | stopped | captures and streams stopped |
| 110.709 | dc1-core1 log | script,info networka distribution-reboot end |
| 110.748 | dc1-core2 log | script,info networka distribution-reboot end |
| 110.779 | dc1-dist1 log | script,info networka distribution-reboot end |
| 110.823 | dc1-dist2 log | script,info networka distribution-reboot end |
| 110.862 | dc1-firewall log | script,info networka distribution-reboot end |
| 110.895 | dc2-core1 log | script,info networka distribution-reboot end |
| 110.926 | dc2-core2 log | script,info networka distribution-reboot end |
| 110.969 | dc2-dist1 log | script,info networka distribution-reboot end |
| 111.006 | dc2-dist2 log | script,info networka distribution-reboot end |
| 111.041 | dc2-firewall log | script,info networka distribution-reboot end |
| 111.047 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
