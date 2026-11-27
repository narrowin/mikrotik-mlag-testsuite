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
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 5 at one ping every 100 ms | 0.408289 to 0.613968 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 181 at one ping every 100 ms | 18.5772 to 18.7824 s | fail |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 181 at one ping every 100 ms | 18.5807 to 18.7893 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 3 at one ping every 100 ms | 0.201723 to 0.405852 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 23 at one ping every 100 ms | 2.28916 to 2.49741 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | Diagnostic only: 89 pings recorded lost, 319 sent in this step (configured interval 100 ms) | 9.17071 to 19.8191 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
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

- Uptime before dispatch was 248 s. The switch reported 17 s at +24.9621 s.
- Full lab state was pass at +27.7902 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 295 s. The switch reported 17 s at +23.8434 s.
- Full lab state was pass at +26.5633 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.812 | test | distribution-reboot started in lab large-mlag |
| -6.505 | dc1-core1 log | script,info networka distribution-reboot start |
| -6.198 | dc1-core2 log | script,info networka distribution-reboot start |
| -5.904 | dc1-dist1 log | script,info networka distribution-reboot start |
| -5.579 | dc1-dist2 log | script,info networka distribution-reboot start |
| -5.251 | dc1-firewall log | script,info networka distribution-reboot start |
| -4.934 | dc2-core1 log | script,info networka distribution-reboot start |
| -4.639 | dc2-core2 log | script,info networka distribution-reboot start |
| -4.338 | dc2-dist1 log | script,info networka distribution-reboot start |
| -4.048 | dc2-dist2 log | script,info networka distribution-reboot start |
| -3.744 | dc2-firewall log | script,info networka distribution-reboot start |
| -3.739 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.174 | state | check before the steps: pass |
| -0.174 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.174 | state | Every switch runs with spanning tree off. pass |
| -0.174 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.174 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.174 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.174 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.112 | capture | started at dc1-service:bond0 |
| -0.112 | capture | started at dc1-traffic:bond0 |
| -0.112 | capture | started at dc1-traffic:vlan390 |
| -0.112 | capture | started at dc2-service:bond0 |
| -0.112 | capture | started at dc2-traffic:bond0 |
| -0.112 | capture | started at dc2-traffic:vlan390 |
| -0.055 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.050 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.043 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.037 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.033 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.014 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.035 | quiet window | clean |
| 4.035 | step | Baseline |
| 8.036 | step | Reboot dc1-dist1 |
| 8.084 | reboot | dispatching the reboot to dc1-dist1 |
| 8.144 | reboot | dc1-dist1 command returned: accepted |
| 8.503 | dc1-to-dc2-over-dci | 179 pings lost at one ping every 100 ms, traffic stopped for 18.577 to 18.782 s, reply absent at source, request absent at destination |
| 8.518 | dc2-to-dc1-over-dci | 179 pings lost at one ping every 100 ms, traffic stopped for 18.581 to 18.789 s, request absent at destination |
| 22.072 | dc1-dist2 log | bridge,warning MLAG: remote heartbeat timeout |
| 25.637 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 25.644 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 25.848 | dc1-traffic-to-dc1-service | 5 pings lost at one ping every 100 ms, traffic stopped for 0.408 to 0.614 s, request absent at destination |
| 25.875 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.202 to 0.406 s, reply absent at source |
| 27.286 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.312 s, request absent at destination |
| 27.305 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.308 s, request absent at destination |
| 35.874 | recovery | full lab state after reboot of dc1-dist1: pass |
| 51.875 | step | dc1-dist1 reboot recovery |
| 54.876 | step | Reboot dc1-dist2 |
| 54.934 | reboot | dispatching the reboot to dc1-dist2 |
| 55.004 | reboot | dc1-dist2 command returned: accepted |
| 55.309 | dc1-traffic-to-vrrp | Diagnostic only: 89 pings recorded lost (configured interval 100 ms), observed stop bounds 9.17071 to 19.8191 s, reply absent at source |
| 55.328 | dc1-traffic-to-dc1-service | 23 pings lost at one ping every 100 ms, traffic stopped for 2.289 to 2.497 s, reply absent at source, request absent at destination |
| 65.892 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 70.898 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 71.633 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 71.637 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 81.497 | recovery | full lab state after reboot of dc1-dist2: pass |
| 97.498 | step | dc1-dist2 reboot recovery |
| 100.499 | steps | last step ended |
| 103.895 | state | check after the steps: pass |
| 103.895 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 103.895 | state | Every switch runs with spanning tree off. pass |
| 103.895 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 103.895 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 103.895 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 103.895 | state | Both cables of every host are eligible in its LACP bond. pass |
| 103.895 | streams | measurement ended; captures wait for final replies |
| 104.405 | stopped | captures and streams stopped |
| 104.433 | dc1-core1 log | script,info networka distribution-reboot end |
| 104.464 | dc1-core2 log | script,info networka distribution-reboot end |
| 104.503 | dc1-dist1 log | script,info networka distribution-reboot end |
| 104.537 | dc1-dist2 log | script,info networka distribution-reboot end |
| 104.575 | dc1-firewall log | script,info networka distribution-reboot end |
| 104.606 | dc2-core1 log | script,info networka distribution-reboot end |
| 104.640 | dc2-core2 log | script,info networka distribution-reboot end |
| 104.672 | dc2-dist1 log | script,info networka distribution-reboot end |
| 104.700 | dc2-dist2 log | script,info networka distribution-reboot end |
| 104.734 | dc2-firewall log | script,info networka distribution-reboot end |
| 104.745 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
