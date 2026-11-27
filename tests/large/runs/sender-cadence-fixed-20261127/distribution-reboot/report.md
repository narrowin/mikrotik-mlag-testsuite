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
| Reboot dc1-dist1 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 11 at one ping every 100 ms | 1.03314 to 1.23966 s | pass |
| Reboot dc1-dist1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 181 at one ping every 100 ms | 18.7535 to 18.9575 s | fail |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 180 at one ping every 100 ms | 17.1903 to 17.397 s | fail |
| Reboot dc1-dist1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 4 at one ping every 100 ms | 0.303946 to 0.506157 s | pass |
| Reboot dc1-dist1 | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-dist1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:bond0 → dc1-service:bond0 | 5 s | 25 at one ping every 100 ms | 2.40416 to 2.61108 s | pass |
| Reboot dc1-dist2 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc1-dist2 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 179 at one ping every 100 ms | 18.5708 to 18.7773 s | fail |
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

- Uptime before dispatch was 112 s. The switch reported 17 s at +23.8756 s.
- Full lab state was pass at +26.6098 s, against a 60 s limit.

## Reboot of dc1-dist2

Reboot dc1-dist2 · pass

- Uptime before dispatch was 158 s. The switch reported 17 s at +23.8188 s.
- Full lab state was pass at +26.5328 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -3.200 | test | distribution-reboot started in lab large-mlag |
| -3.156 | dc1-core1 log | script,info networka distribution-reboot start |
| -3.117 | dc1-core2 log | script,info networka distribution-reboot start |
| -3.078 | dc1-dist1 log | script,info networka distribution-reboot start |
| -3.041 | dc1-dist2 log | script,info networka distribution-reboot start |
| -2.993 | dc1-firewall log | script,info networka distribution-reboot start |
| -2.949 | dc2-core1 log | script,info networka distribution-reboot start |
| -2.892 | dc2-core2 log | script,info networka distribution-reboot start |
| -2.846 | dc2-dist1 log | script,info networka distribution-reboot start |
| -2.815 | dc2-dist2 log | script,info networka distribution-reboot start |
| -2.784 | dc2-firewall log | script,info networka distribution-reboot start |
| -2.771 | switch log | marker 'networka distribution-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.142 | state | check before the steps: pass |
| -0.142 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.142 | state | Every switch runs with spanning tree off. pass |
| -0.142 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.142 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.142 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.142 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.083 | capture | started at dc1-service:bond0 |
| -0.083 | capture | started at dc1-traffic:bond0 |
| -0.083 | capture | started at dc1-traffic:vlan390 |
| -0.083 | capture | started at dc2-service:bond0 |
| -0.083 | capture | started at dc2-traffic:bond0 |
| -0.083 | capture | started at dc2-traffic:vlan390 |
| -0.027 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.024 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.020 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.016 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.013 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.007 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.088 | quiet window | clean |
| 4.088 | step | Baseline |
| 8.092 | step | Reboot dc1-dist1 |
| 8.142 | reboot | dispatching the reboot to dc1-dist1 |
| 8.185 | reboot | dc1-dist1 command returned: accepted |
| 8.541 | dc2-to-dc1-over-dci | 166 pings lost at one ping every 100 ms, traffic stopped for 17.19 to 17.397 s, request absent at destination |
| 8.617 | dc1-to-dc2-over-dci | 181 pings lost at one ping every 100 ms, traffic stopped for 18.753 to 18.957 s, reply absent at source, request absent at destination |
| 24.975 | dc1-dist2 log | bridge,warning "bridge" peer disconnected |
| 24.985 | dc1-dist2 log | bridge,warning "bridge" peer link down |
| 25.090 | dc1-traffic-to-dc1-service | 11 pings lost at one ping every 100 ms, traffic stopped for 1.033 to 1.24 s, request absent at destination |
| 25.116 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.304 to 0.506 s, reply absent at source |
| 25.935 | dc2-to-dc1-over-dci | 14 pings lost at one ping every 100 ms, traffic stopped for 1.356 to 1.559 s, request absent at destination |
| 34.751 | recovery | full lab state after reboot of dc1-dist1: pass |
| 50.755 | step | dc1-dist1 reboot recovery |
| 53.757 | step | Reboot dc1-dist2 |
| 53.815 | reboot | dispatching the reboot to dc1-dist2 |
| 53.864 | reboot | dc1-dist2 command returned: accepted |
| 54.254 | dc1-traffic-to-vrrp | 179 pings lost at one ping every 100 ms, traffic stopped for 18.571 to 18.777 s, reply absent at source |
| 54.286 | dc1-traffic-to-dc1-service | 24 pings lost at one ping every 100 ms, traffic stopped for 2.404 to 2.611 s, request absent at destination |
| 65.112 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 70.115 | dc1-dist1 log | bridge,warning MLAG: remote heartbeat timeout |
| 70.608 | dc1-dist1 log | bridge,warning "bridge" peer disconnected |
| 70.614 | dc1-dist1 log | bridge,warning "bridge" peer link down |
| 72.924 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 80.348 | recovery | full lab state after reboot of dc1-dist2: pass |
| 96.348 | step | dc1-dist2 reboot recovery |
| 99.351 | steps | last step ended |
| 102.590 | state | check after the steps: pass |
| 102.590 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 102.590 | state | Every switch runs with spanning tree off. pass |
| 102.590 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 102.590 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 102.590 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 102.590 | state | Both cables of every host are eligible in its LACP bond. pass |
| 102.590 | streams | measurement ended; captures wait for final replies |
| 103.098 | stopped | captures and streams stopped |
| 103.123 | dc1-core1 log | script,info networka distribution-reboot end |
| 103.159 | dc1-core2 log | script,info networka distribution-reboot end |
| 103.189 | dc1-dist1 log | script,info networka distribution-reboot end |
| 103.225 | dc1-dist2 log | script,info networka distribution-reboot end |
| 103.270 | dc1-firewall log | script,info networka distribution-reboot end |
| 103.301 | dc2-core1 log | script,info networka distribution-reboot end |
| 103.329 | dc2-core2 log | script,info networka distribution-reboot end |
| 103.384 | dc2-dist1 log | script,info networka distribution-reboot end |
| 103.414 | dc2-dist2 log | script,info networka distribution-reboot end |
| 103.443 | dc2-firewall log | script,info networka distribution-reboot end |
| 103.445 | switch log | marker 'networka distribution-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
