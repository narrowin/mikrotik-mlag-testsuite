# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.20537 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.203583 s | pass |
| DCI member down | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:vlan390 → 198.18.40.1 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 2 at one ping every 100 ms | 0 to 0.209251 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 2 at one ping every 100 ms | 0 to 0.205826 s | pass |
| DCI member back | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 0 at one ping every 100 ms | 0 s | pass |

**DCI member back state** · pass
- Both ends of the returned member are synchronized, collecting and distributing. · pass

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

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | dc1-core1 -2.91642 to 19.8244 s, dc1-core2 -2.86712 to 19.8517 s, dc1-dist1 -2.82494 to 19.8807 s, dc1-dist2 -2.78309 to 19.9227 s, dc1-firewall -2.74536 to 19.9782 s, dc2-core1 -2.70652 to 20.0105 s, dc2-core2 -2.65972 to 20.043 s, dc2-dist1 -2.61563 to 20.0887 s, dc2-dist2 -2.57322 to 20.1247 s, dc2-firewall -2.53756 to 20.1562 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 3.9921 to 9.00851 s | must ether4 link down | pass | 2026-11-27T07:11:38.384338+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 3.9921 to 9.00851 s | must ether4 link down | pass | 2026-11-27T07:11:38.956567+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.00851 to 16.1128 s | must ether4 link up | pass | 2026-11-27T07:11:43.388314+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.00851 to 16.1128 s | must ether4 link up | pass | 2026-11-27T07:11:43.996581+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.947 | test | dci-member-loss started in lab large-mlag |
| -2.916 | dc1-core1 log | script,info networka dci-member-loss start |
| -2.867 | dc1-core2 log | script,info networka dci-member-loss start |
| -2.825 | dc1-dist1 log | script,info networka dci-member-loss start |
| -2.783 | dc1-dist2 log | script,info networka dci-member-loss start |
| -2.745 | dc1-firewall log | script,info networka dci-member-loss start |
| -2.707 | dc2-core1 log | script,info networka dci-member-loss start |
| -2.660 | dc2-core2 log | script,info networka dci-member-loss start |
| -2.616 | dc2-dist1 log | script,info networka dci-member-loss start |
| -2.573 | dc2-dist2 log | script,info networka dci-member-loss start |
| -2.538 | dc2-firewall log | script,info networka dci-member-loss start |
| -2.533 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.135 | state | check before the steps: pass |
| -0.135 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.135 | state | Every switch runs with spanning tree off. pass |
| -0.135 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.135 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.135 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.135 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.125 | capture | started at dc1-core1:eth3 |
| -0.125 | capture | started at dc1-service:bond0 |
| -0.125 | capture | started at dc1-traffic:bond0 |
| -0.124 | capture | started at dc1-traffic:vlan390 |
| -0.124 | capture | started at dc2-core1:eth3 |
| -0.124 | capture | started at dc2-service:bond0 |
| -0.072 | capture | started at dc2-traffic:bond0 |
| -0.071 | capture | started at dc2-traffic:vlan390 |
| -0.015 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.012 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.010 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.992 | quiet window | clean |
| 3.992 | step | DCI member down |
| 4.007 | cable | dc1-core1:eth3 set down |
| 4.007 | cable | dc1-core1:eth3 down at both ends |
| 4.048 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 4.065 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, request absent at destination |
| 4.083 | dc2-core1 log | interface,info dci link down |
| 4.089 | dc1-core1 log | interface,info ether4 link down |
| 4.106 | dc1-core1 log | interface,info dci link down |
| 4.661 | dc2-core1 log | interface,info ether4 link down |
| 9.009 | step | DCI member back |
| 9.023 | cable | dc1-core1:eth3 set up |
| 9.024 | cable | dc1-core1:eth3 up at both ends |
| 9.031 | dc2-core1 log | interface,info dci link up |
| 9.045 | dc1-core1 log | interface,info dci link up |
| 9.062 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 9.093 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 9.141 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 9.701 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.489 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 11.511 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 16.113 | state | DCI member back pass |
| 16.113 | steps | last step ended |
| 19.292 | state | check after the steps: pass |
| 19.292 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 19.292 | state | Every switch runs with spanning tree off. pass |
| 19.292 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 19.292 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 19.292 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 19.292 | state | Both cables of every host are eligible in its LACP bond. pass |
| 19.293 | streams | measurement ended; captures wait for final replies |
| 19.798 | stopped | captures and streams stopped |
| 19.824 | dc1-core1 log | script,info networka dci-member-loss end |
| 19.852 | dc1-core2 log | script,info networka dci-member-loss end |
| 19.881 | dc1-dist1 log | script,info networka dci-member-loss end |
| 19.923 | dc1-dist2 log | script,info networka dci-member-loss end |
| 19.978 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.011 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.043 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.089 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.125 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.156 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.159 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
