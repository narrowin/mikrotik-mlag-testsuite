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
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 109 pings recorded lost, 362 sent in this step (configured interval 100 ms) | 11.0495 to 18.5972 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 176 at one ping every 100 ms | 17.9132 to 18.1196 s | fail |
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
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 165 at one ping every 100 ms | 16.9808 to 17.1876 s | fail |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | Diagnostic only: 40 pings recorded lost, 289 sent in this step (configured interval 100 ms) | 4.05814 to 17.7609 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc2-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
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

- Uptime before dispatch was 94 s. The switch reported 18 s at +24.9921 s.
- Full lab state was pass at +27.9123 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 141 s. The switch reported 16 s at +23.7941 s.
- Full lab state was pass at +26.5243 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.889 | test | core-reboot started in lab large-mlag |
| -6.569 | dc1-core1 log | script,info networka core-reboot start |
| -6.273 | dc1-core2 log | script,info networka core-reboot start |
| -5.965 | dc1-dist1 log | script,info networka core-reboot start |
| -5.603 | dc1-dist2 log | script,info networka core-reboot start |
| -5.282 | dc1-firewall log | script,info networka core-reboot start |
| -4.981 | dc2-core1 log | script,info networka core-reboot start |
| -4.681 | dc2-core2 log | script,info networka core-reboot start |
| -4.381 | dc2-dist1 log | script,info networka core-reboot start |
| -4.074 | dc2-dist2 log | script,info networka core-reboot start |
| -3.769 | dc2-firewall log | script,info networka core-reboot start |
| -3.761 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.133 | state | check before the steps: pass |
| -0.133 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.133 | state | Every switch runs with spanning tree off. pass |
| -0.133 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.133 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.133 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.133 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.124 | capture | started at dc1-service:bond0 |
| -0.124 | capture | started at dc1-traffic:bond0 |
| -0.124 | capture | started at dc1-traffic:vlan390 |
| -0.123 | capture | started at dc2-service:bond0 |
| -0.073 | capture | started at dc2-traffic:bond0 |
| -0.073 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.014 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.011 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.007 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.095 | quiet window | clean |
| 4.095 | step | Baseline |
| 8.096 | step | Reboot dc1-core1 |
| 8.149 | reboot | dispatching the reboot to dc1-core1 |
| 8.214 | reboot | dc1-core1 command returned: accepted |
| 8.626 | dc1-to-dc2-over-dci | Diagnostic only: 107 pings recorded lost (configured interval 100 ms), observed stop bounds 11.0495 to 18.5972 s, request absent at destination |
| 8.636 | dc2-to-dc1-over-dci | 173 pings lost at one ping every 100 ms, traffic stopped for 17.913 to 18.12 s, request absent at destination |
| 25.971 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 25.980 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 26.861 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 28.063 | dc1-to-dc2-over-dci | Diagnostic only: 2 pings recorded lost (configured interval 100 ms), observed stop bounds 0.101244 to 0.305611 s, request absent at destination |
| 28.083 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.313 s, request absent at destination |
| 36.061 | recovery | full lab state after reboot of dc1-core1: pass |
| 52.062 | step | dc1 reboot recovery |
| 55.063 | step | Reboot dc2-core1 |
| 55.116 | reboot | dispatching the reboot to dc2-core1 |
| 55.178 | reboot | dc2-core1 command returned: accepted |
| 55.540 | dc2-to-dc1-over-dci | Diagnostic only: 40 pings recorded lost (configured interval 100 ms), observed stop bounds 4.05814 to 17.7609 s, request absent at destination |
| 55.633 | dc1-to-dc2-over-dci | 164 pings lost at one ping every 100 ms, traffic stopped for 16.981 to 17.188 s, late reply, request absent at destination |
| 68.816 | dc2-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 72.348 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 72.357 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 72.925 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 81.641 | recovery | full lab state after reboot of dc2-core1: pass |
| 97.641 | step | dc2 reboot recovery |
| 100.642 | steps | last step ended |
| 104.165 | state | check after the steps: pass |
| 104.165 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 104.165 | state | Every switch runs with spanning tree off. pass |
| 104.165 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 104.165 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 104.165 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 104.165 | state | Both cables of every host are eligible in its LACP bond. pass |
| 104.165 | streams | measurement ended; captures wait for final replies |
| 104.676 | stopped | captures and streams stopped |
| 104.708 | dc1-core1 log | script,info networka core-reboot end |
| 104.739 | dc1-core2 log | script,info networka core-reboot end |
| 104.770 | dc1-dist1 log | script,info networka core-reboot end |
| 104.819 | dc1-dist2 log | script,info networka core-reboot end |
| 104.850 | dc1-firewall log | script,info networka core-reboot end |
| 104.898 | dc2-core1 log | script,info networka core-reboot end |
| 104.929 | dc2-core2 log | script,info networka core-reboot end |
| 104.967 | dc2-dist1 log | script,info networka core-reboot end |
| 104.999 | dc2-dist2 log | script,info networka core-reboot end |
| 105.044 | dc2-firewall log | script,info networka core-reboot end |
| 105.062 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
