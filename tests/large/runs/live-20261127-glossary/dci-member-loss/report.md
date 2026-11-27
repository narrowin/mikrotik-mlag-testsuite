# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.210493 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.202296 s | pass |
| DCI member down | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:vlan390 → 198.18.40.1 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.204036 to 0.411018 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.211917 to 0.420428 s | pass |
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
| Whole test | dc1-core1 -6.57062 to 20.3323 s, dc1-core2 -6.27664 to 20.362 s, dc1-dist1 -5.98223 to 20.3925 s, dc1-dist2 -5.65383 to 20.4435 s, dc1-firewall -5.3566 to 20.4724 s, dc2-core1 -5.05894 to 20.5195 s, dc2-core2 -4.77146 to 20.5524 s, dc2-dist1 -4.4741 to 20.5922 s, dc2-dist2 -4.17397 to 20.621 s, dc2-firewall -3.85371 to 20.669 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 4.05988 to 9.08682 s | must ether4 link down | pass | 2026-11-27T09:37:53.877418+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 4.05988 to 9.08682 s | must ether4 link down | pass | 2026-11-27T09:37:53.470546+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.08682 to 16.2066 s | must ether4 link up | pass | 2026-11-27T09:37:58.899167+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.08682 to 16.2066 s | must ether4 link up | pass | 2026-11-27T09:37:58.482911+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.869 | test | dci-member-loss started in lab large-mlag |
| -6.571 | dc1-core1 log | script,info networka dci-member-loss start |
| -6.277 | dc1-core2 log | script,info networka dci-member-loss start |
| -5.982 | dc1-dist1 log | script,info networka dci-member-loss start |
| -5.654 | dc1-dist2 log | script,info networka dci-member-loss start |
| -5.357 | dc1-firewall log | script,info networka dci-member-loss start |
| -5.059 | dc2-core1 log | script,info networka dci-member-loss start |
| -4.771 | dc2-core2 log | script,info networka dci-member-loss start |
| -4.474 | dc2-dist1 log | script,info networka dci-member-loss start |
| -4.174 | dc2-dist2 log | script,info networka dci-member-loss start |
| -3.854 | dc2-firewall log | script,info networka dci-member-loss start |
| -3.851 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.140 | state | check before the steps: pass |
| -0.140 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.140 | state | Every switch runs with spanning tree off. pass |
| -0.140 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.140 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.140 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.140 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.128 | capture | started at dc1-core1:eth3 |
| -0.127 | capture | started at dc1-service:bond0 |
| -0.127 | capture | started at dc1-traffic:bond0 |
| -0.127 | capture | started at dc1-traffic:vlan390 |
| -0.127 | capture | started at dc2-core1:eth3 |
| -0.127 | capture | started at dc2-service:bond0 |
| -0.076 | capture | started at dc2-traffic:bond0 |
| -0.076 | capture | started at dc2-traffic:vlan390 |
| -0.020 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.016 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.012 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.007 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.004 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.060 | quiet window | clean |
| 4.060 | step | DCI member down |
| 4.085 | cable | dc1-core1:eth3 set down |
| 4.086 | cable | dc1-core1:eth3 down at both ends |
| 4.132 | dc1-core1 log | interface,info dci link down |
| 4.164 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, request absent at destination |
| 4.168 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 4.186 | dc2-core1 log | interface,info dci link down |
| 4.243 | dc2-core1 log | interface,info ether4 link down |
| 4.650 | dc1-core1 log | interface,info ether4 link down |
| 9.087 | step | DCI member back |
| 9.109 | cable | dc1-core1:eth3 set up |
| 9.110 | cable | dc1-core1:eth3 up at both ends |
| 9.137 | dc2-core1 log | interface,info dci link up |
| 9.192 | dc1-core1 log | interface,info dci link up |
| 9.244 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 9.246 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 9.256 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 9.672 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.478 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.204 to 0.411 s, request absent at destination |
| 11.480 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.42 s, request absent at destination |
| 16.206 | state | DCI member back pass |
| 16.207 | steps | last step ended |
| 19.794 | state | check after the steps: pass |
| 19.794 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 19.794 | state | Every switch runs with spanning tree off. pass |
| 19.794 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 19.794 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 19.794 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 19.794 | state | Both cables of every host are eligible in its LACP bond. pass |
| 19.795 | streams | measurement ended; captures wait for final replies |
| 20.303 | stopped | captures and streams stopped |
| 20.332 | dc1-core1 log | script,info networka dci-member-loss end |
| 20.362 | dc1-core2 log | script,info networka dci-member-loss end |
| 20.393 | dc1-dist1 log | script,info networka dci-member-loss end |
| 20.443 | dc1-dist2 log | script,info networka dci-member-loss end |
| 20.472 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.520 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.552 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.592 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.621 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.669 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.676 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
