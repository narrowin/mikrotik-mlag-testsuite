# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 2 at one ping every 100 ms | 0.105371 to 0.312481 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 2 at one ping every 100 ms | 0.10693 to 0.308616 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.21055 to 0.413167 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 5 at one ping every 100 ms | 0.209239 to 0.41713 s | pass |

**DCI member back state** · pass
- Both ends of the returned member are synchronized, collecting and distributing. · pass

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

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | dc1-core1 -6.26258 to 20.1254 s, dc1-core2 -5.96072 to 20.1555 s, dc1-dist1 -5.65513 to 20.1929 s, dc1-dist2 -5.36156 to 20.2326 s, dc1-firewall -5.05403 to 20.2873 s, dc2-core1 -4.7586 to 20.3193 s, dc2-core2 -4.46618 to 20.3727 s, dc2-dist1 -4.17279 to 20.4025 s, dc2-dist2 -3.87549 to 20.4324 s, dc2-firewall -3.581 to 20.4776 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 4.01966 to 9.04683 s | must ether4 link down | pass | 2026-11-27T06:56:05.744074+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 4.01966 to 9.04683 s | must ether4 link down | pass | 2026-11-27T06:56:05.616110+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.04683 to 16.1852 s | must ether4 link up | pass | 2026-11-27T06:56:10.766090+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.04683 to 16.1852 s | must ether4 link up | pass | 2026-11-27T06:56:10.630987+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.575 | test | dci-member-loss started in lab large-mlag |
| -6.263 | dc1-core1 log | script,info networka dci-member-loss start |
| -5.961 | dc1-core2 log | script,info networka dci-member-loss start |
| -5.655 | dc1-dist1 log | script,info networka dci-member-loss start |
| -5.362 | dc1-dist2 log | script,info networka dci-member-loss start |
| -5.054 | dc1-firewall log | script,info networka dci-member-loss start |
| -4.759 | dc2-core1 log | script,info networka dci-member-loss start |
| -4.466 | dc2-core2 log | script,info networka dci-member-loss start |
| -4.173 | dc2-dist1 log | script,info networka dci-member-loss start |
| -3.875 | dc2-dist2 log | script,info networka dci-member-loss start |
| -3.581 | dc2-firewall log | script,info networka dci-member-loss start |
| -3.574 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.132 | state | check before the steps: pass |
| -0.132 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.132 | state | Every switch runs with spanning tree off. pass |
| -0.132 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.132 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.132 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.132 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.121 | capture | started at dc1-core1:eth3 |
| -0.121 | capture | started at dc1-service:bond0 |
| -0.121 | capture | started at dc1-traffic:bond0 |
| -0.120 | capture | started at dc1-traffic:vlan390 |
| -0.120 | capture | started at dc2-core1:eth3 |
| -0.120 | capture | started at dc2-service:bond0 |
| -0.120 | capture | started at dc2-traffic:bond0 |
| -0.068 | capture | started at dc2-traffic:vlan390 |
| -0.013 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.010 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.006 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.002 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.019 | quiet window | clean |
| 4.020 | step | DCI member down |
| 4.043 | cable | dc1-core1:eth3 set down |
| 4.043 | cable | dc1-core1:eth3 down at both ends |
| 4.069 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.312 s, request absent at destination |
| 4.070 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.309 s, reply absent at source, request absent at destination |
| 4.119 | dc2-core1 log | interface,info dci link down |
| 4.154 | dc1-core1 log | interface,info dci link down |
| 4.368 | dc2-core1 log | interface,info ether4 link down |
| 4.496 | dc1-core1 log | interface,info ether4 link down |
| 9.047 | step | DCI member back |
| 9.064 | cable | dc1-core1:eth3 set up |
| 9.065 | cable | dc1-core1:eth3 up at both ends |
| 9.103 | dc1-core1 log | interface,info dci link up |
| 9.158 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.311 s, reply absent at source, request absent at destination |
| 9.176 | dc2-core1 log | interface,info dci link up |
| 9.180 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 9.383 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 9.518 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.430 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.413 s, request absent at destination |
| 11.500 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.417 s, request absent at destination |
| 16.185 | state | DCI member back pass |
| 16.185 | steps | last step ended |
| 19.593 | state | check after the steps: pass |
| 19.593 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 19.593 | state | Every switch runs with spanning tree off. pass |
| 19.593 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 19.593 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 19.593 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 19.593 | state | Both cables of every host are eligible in its LACP bond. pass |
| 19.593 | streams | measurement ended; captures wait for final replies |
| 20.099 | stopped | captures and streams stopped |
| 20.125 | dc1-core1 log | script,info networka dci-member-loss end |
| 20.156 | dc1-core2 log | script,info networka dci-member-loss end |
| 20.193 | dc1-dist1 log | script,info networka dci-member-loss end |
| 20.233 | dc1-dist2 log | script,info networka dci-member-loss end |
| 20.287 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.319 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.373 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.402 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.432 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.478 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.485 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
