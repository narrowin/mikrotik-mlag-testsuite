# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.208002 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.208242 s | pass |
| DCI member down | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:vlan390 → 198.18.40.1 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 8 at one ping every 100 ms | 0.412441 to 0.619122 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 8 at one ping every 100 ms | 0.419535 to 0.624132 s | pass |
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
| Whole test | dc1-core1 -7.24529 to 20.1888 s, dc1-core2 -6.94109 to 20.2248 s, dc1-dist1 -6.63487 to 20.2593 s, dc1-dist2 -6.3349 to 20.2948 s, dc1-firewall -6.03798 to 20.3459 s, dc2-core1 -5.72107 to 20.38 s, dc2-core2 -5.39777 to 20.4307 s, dc2-dist1 -5.0551 to 20.4738 s, dc2-dist2 -4.72181 to 20.5322 s, dc2-firewall -4.34038 to 20.5731 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 4.1164 to 9.16792 s | must ether4 link down | pass | 2026-11-28T07:05:09.730458+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 4.1164 to 9.16792 s | must ether4 link down | pass | 2026-11-28T07:05:10.667726+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.16792 to 16.3132 s | must ether4 link up | pass | 2026-11-28T07:05:14.734779+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.16792 to 16.3132 s | must ether4 link up | pass | 2026-11-28T07:05:15.674183+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -7.587 | test | dci-member-loss started in lab large-mlag |
| -7.245 | dc1-core1 log | script,info networka dci-member-loss start |
| -6.941 | dc1-core2 log | script,info networka dci-member-loss start |
| -6.635 | dc1-dist1 log | script,info networka dci-member-loss start |
| -6.335 | dc1-dist2 log | script,info networka dci-member-loss start |
| -6.038 | dc1-firewall log | script,info networka dci-member-loss start |
| -5.721 | dc2-core1 log | script,info networka dci-member-loss start |
| -5.398 | dc2-core2 log | script,info networka dci-member-loss start |
| -5.055 | dc2-dist1 log | script,info networka dci-member-loss start |
| -4.722 | dc2-dist2 log | script,info networka dci-member-loss start |
| -4.340 | dc2-firewall log | script,info networka dci-member-loss start |
| -4.308 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.150 | state | check before the steps: pass |
| -0.150 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.150 | state | Every switch runs with spanning tree off. pass |
| -0.150 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.150 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.150 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.150 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.136 | capture | started at dc1-core1:eth3 |
| -0.136 | capture | started at dc1-service:bond0 |
| -0.136 | capture | started at dc1-traffic:bond0 |
| -0.135 | capture | started at dc1-traffic:vlan390 |
| -0.135 | capture | started at dc2-core1:eth3 |
| -0.135 | capture | started at dc2-service:bond0 |
| -0.084 | capture | started at dc2-traffic:bond0 |
| -0.083 | capture | started at dc2-traffic:vlan390 |
| -0.027 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.022 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.016 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.011 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.008 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.005 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.116 | quiet window | clean |
| 4.116 | step | DCI member down |
| 4.166 | cable | dc1-core1:eth3 set down |
| 4.167 | cable | dc1-core1:eth3 down at both ends |
| 4.217 | dc1-core1 log | interface,info ether4 link down |
| 4.217 | dc1-core1 log | interface,info dci link down |
| 4.244 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 4.250 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 4.264 | dc2-core1 log | interface,info dci link down |
| 5.154 | dc2-core1 log | interface,info ether4 link down |
| 9.168 | step | DCI member back |
| 9.206 | cable | dc1-core1:eth3 set up |
| 9.206 | cable | dc1-core1:eth3 up at both ends |
| 9.215 | dc2-core1 log | interface,info dci link up |
| 9.221 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 9.274 | dc1-core1 log | interface,info dci link up |
| 9.329 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.42 to 0.624 s, request absent at destination |
| 9.335 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.412 to 0.619 s, request absent at destination |
| 10.161 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.574 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.206 to 0.414 s, request absent at destination |
| 11.576 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.214 to 0.42 s, request absent at destination |
| 16.313 | state | DCI member back pass |
| 16.313 | steps | last step ended |
| 19.652 | state | check after the steps: pass |
| 19.652 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 19.652 | state | Every switch runs with spanning tree off. pass |
| 19.652 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 19.652 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 19.652 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 19.652 | state | Both cables of every host are eligible in its LACP bond. pass |
| 19.653 | streams | measurement ended; captures wait for final replies |
| 20.163 | stopped | captures and streams stopped |
| 20.189 | dc1-core1 log | script,info networka dci-member-loss end |
| 20.225 | dc1-core2 log | script,info networka dci-member-loss end |
| 20.259 | dc1-dist1 log | script,info networka dci-member-loss end |
| 20.295 | dc1-dist2 log | script,info networka dci-member-loss end |
| 20.346 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.380 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.431 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.474 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.532 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.573 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.588 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
