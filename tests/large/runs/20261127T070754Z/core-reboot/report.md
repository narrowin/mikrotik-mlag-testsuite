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
| Reboot dc1-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | 159 at one ping every 100 ms | 16.4658 to 16.6752 s | fail |
| Reboot dc1-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 143 at one ping every 100 ms | 14.8064 to 17.0475 s | fail |
| Reboot dc1-core1 | dc1-traffic:vlan390 → 198.18.40.1 | 5 s | 6 at one ping every 100 ms | 0.521049 to 0.727591 s | pass |
| Reboot dc1-core1 | dc2-traffic:vlan390 → 198.18.40.1 | 5 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 reboot recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Reboot dc2-core1 | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 5 s | Diagnostic only: 66 pings recorded lost, 319 sent in this step (configured interval 100 ms) | 6.56965 to 18.1101 s (diagnostic) | unverified. Sender cadence was invalid in this step. |
| Reboot dc2-core1 | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 5 s | 171 at one ping every 100 ms | 17.4928 to 17.7054 s | fail |
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

- Uptime before dispatch was 118 s. The switch reported 16 s at +22.7902 s.
- Full lab state was pass at +25.4989 s, against a 60 s limit.

## Reboot of dc2-core1

Reboot dc2-core1 · pass

- Uptime before dispatch was 361 s. The switch reported 18 s at +24.8248 s.
- Full lab state was pass at +27.4584 s, against a 60 s limit.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.982 | test | core-reboot started in lab large-mlag |
| -2.948 | dc1-core1 log | script,info networka core-reboot start |
| -2.894 | dc1-core2 log | script,info networka core-reboot start |
| -2.854 | dc1-dist1 log | script,info networka core-reboot start |
| -2.825 | dc1-dist2 log | script,info networka core-reboot start |
| -2.781 | dc1-firewall log | script,info networka core-reboot start |
| -2.736 | dc2-core1 log | script,info networka core-reboot start |
| -2.702 | dc2-core2 log | script,info networka core-reboot start |
| -2.657 | dc2-dist1 log | script,info networka core-reboot start |
| -2.615 | dc2-dist2 log | script,info networka core-reboot start |
| -2.558 | dc2-firewall log | script,info networka core-reboot start |
| -2.553 | switch log | marker 'networka core-reboot start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.131 | state | check before the steps: pass |
| -0.131 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.131 | state | Every switch runs with spanning tree off. pass |
| -0.131 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.131 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.131 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.131 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.122 | capture | started at dc1-service:bond0 |
| -0.121 | capture | started at dc1-traffic:bond0 |
| -0.121 | capture | started at dc1-traffic:vlan390 |
| -0.121 | capture | started at dc2-service:bond0 |
| -0.070 | capture | started at dc2-traffic:bond0 |
| -0.070 | capture | started at dc2-traffic:vlan390 |
| -0.014 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.011 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.008 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.017 | quiet window | clean |
| 4.018 | step | Baseline |
| 8.020 | step | Reboot dc1-core1 |
| 8.073 | reboot | dispatching the reboot to dc1-core1 |
| 8.139 | reboot | dc1-core1 command returned: accepted |
| 8.437 | dc1-to-dc2-over-dci | 159 pings lost at one ping every 100 ms, traffic stopped for 16.466 to 16.675 s, late reply, request absent at destination |
| 8.457 | dc2-to-dc1-over-dci | 143 pings lost at one ping every 100 ms, traffic stopped for 14.806 to 17.047 s, request absent at destination |
| 24.064 | dc1-core2 log | bridge,warning "bridge" peer disconnected |
| 24.070 | dc1-core2 log | bridge,warning "bridge" peer link down |
| 24.253 | dc1-traffic-to-vrrp | 6 pings lost at one ping every 100 ms, traffic stopped for 0.521 to 0.728 s, reply absent at source |
| 33.572 | recovery | full lab state after reboot of dc1-core1: pass |
| 49.574 | step | dc1 reboot recovery |
| 52.576 | step | Reboot dc2-core1 |
| 52.622 | reboot | dispatching the reboot to dc2-core1 |
| 52.666 | reboot | dc2-core1 command returned: accepted |
| 53.013 | dc2-to-dc1-over-dci | 169 pings lost at one ping every 100 ms, traffic stopped for 17.493 to 17.705 s, request absent at destination |
| 53.028 | dc1-to-dc2-over-dci | Diagnostic only: 64 pings recorded lost (configured interval 100 ms), observed stop bounds 6.56965 to 18.1101 s, request absent at destination |
| 65.283 | dc2-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 70.277 | dc2-core2 log | bridge,warning MLAG: remote heartbeat timeout |
| 70.470 | dc2-core2 log | bridge,warning "bridge" peer disconnected |
| 70.478 | dc2-core2 log | bridge,warning "bridge" peer link down |
| 70.718 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 71.127 | dc1-to-dc2-over-dci | Diagnostic only: 1 pings recorded lost (configured interval 100 ms), observed stop bounds 0 to 0.192701 s, request absent at destination |
| 72.550 | dc1-to-dc2-over-dci | Diagnostic only: 1 pings recorded lost (configured interval 100 ms), observed stop bounds 0 to 0.204399 s, request absent at destination |
| 72.554 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 80.081 | recovery | full lab state after reboot of dc2-core1: pass |
| 96.082 | step | dc2 reboot recovery |
| 99.085 | steps | last step ended |
| 102.332 | state | check after the steps: pass |
| 102.332 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 102.332 | state | Every switch runs with spanning tree off. pass |
| 102.332 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 102.332 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 102.332 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 102.332 | state | Both cables of every host are eligible in its LACP bond. pass |
| 102.333 | streams | measurement ended; captures wait for final replies |
| 102.851 | stopped | captures and streams stopped |
| 102.882 | dc1-core1 log | script,info networka core-reboot end |
| 102.912 | dc1-core2 log | script,info networka core-reboot end |
| 102.965 | dc1-dist1 log | script,info networka core-reboot end |
| 102.992 | dc1-dist2 log | script,info networka core-reboot end |
| 103.021 | dc1-firewall log | script,info networka core-reboot end |
| 103.060 | dc2-core1 log | script,info networka core-reboot end |
| 103.093 | dc2-core2 log | script,info networka core-reboot end |
| 103.125 | dc2-dist1 log | script,info networka core-reboot end |
| 103.182 | dc2-dist2 log | script,info networka core-reboot end |
| 103.228 | dc2-firewall log | script,info networka core-reboot end |
| 103.232 | switch log | marker 'networka core-reboot end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
