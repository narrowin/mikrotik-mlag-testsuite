# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams and the bypass cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.210132 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.205471 s | pass |
| DCI member down | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.207103 to 0.413152 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.2078 to 0.412622 s | pass |
| DCI member back | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**DCI member back state** · pass
- Both ends of the returned member are synchronized, collecting and distributing. · pass

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:eth3 → dc2-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:eth3 → dc1-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:eth3 → dc2-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:eth3 → dc1-traffic:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

| Scope | Switch | Rule | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| Whole test | dc1-core1 -7.53488 to 20.5593 s, dc1-core2 -7.14711 to 20.594 s, dc1-dist1 -6.75607 to 20.6275 s, dc1-dist2 -6.34899 to 20.6753 s, dc1-firewall -5.95263 to 20.7102 s, dc2-core1 -5.5617 to 20.7465 s, dc2-core2 -5.1687 to 20.7803 s, dc2-dist1 -4.76981 to 20.8069 s, dc2-dist2 -4.37636 to 20.8573 s, dc2-firewall -3.98962 to 20.9139 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 4.34611 to 9.37515 s | must ether4 link down | pass | 2026-11-26T18:50:22.643192+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 4.34611 to 9.37515 s | must ether4 link down | pass | 2026-11-26T18:50:21.957088+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.37515 to 16.5009 s | must ether4 link up | pass | 2026-11-26T18:50:27.651288+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.37515 to 16.5009 s | must ether4 link up | pass | 2026-11-26T18:50:26.959086+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -7.933 | test | dci-member-loss started in lab large-mlag |
| -7.535 | dc1-core1 log | script,info networka dci-member-loss start |
| -7.147 | dc1-core2 log | script,info networka dci-member-loss start |
| -6.756 | dc1-dist1 log | script,info networka dci-member-loss start |
| -6.349 | dc1-dist2 log | script,info networka dci-member-loss start |
| -5.953 | dc1-firewall log | script,info networka dci-member-loss start |
| -5.562 | dc2-core1 log | script,info networka dci-member-loss start |
| -5.169 | dc2-core2 log | script,info networka dci-member-loss start |
| -4.770 | dc2-dist1 log | script,info networka dci-member-loss start |
| -4.376 | dc2-dist2 log | script,info networka dci-member-loss start |
| -3.990 | dc2-firewall log | script,info networka dci-member-loss start |
| -3.986 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.155 | state | check before the steps: pass |
| -0.155 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.155 | state | Every switch runs with spanning tree off. pass |
| -0.155 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.155 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.155 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.155 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.137 | capture | started at dc1-core1:eth3 |
| -0.137 | capture | started at dc1-service:bond0 |
| -0.137 | capture | started at dc1-traffic:bond0 |
| -0.136 | capture | started at dc1-traffic:eth3 |
| -0.136 | capture | started at dc1-traffic:vlan390 |
| -0.136 | capture | started at dc2-core1:eth3 |
| -0.135 | capture | started at dc2-service:bond0 |
| -0.135 | capture | started at dc2-traffic:bond0 |
| -0.082 | capture | started at dc2-traffic:eth3 |
| -0.082 | capture | started at dc2-traffic:vlan390 |
| -0.022 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.018 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.013 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.009 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | bypass-dc1-to-dc2 | started from dc1-traffic:eth3 to dc2-traffic:eth3 at 198.51.100.2 |
| -0.001 | bypass-dc2-to-dc1 | started from dc2-traffic:eth3 to dc1-traffic:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.346 | quiet window | clean |
| 4.346 | step | DCI member down |
| 4.371 | cable | dc1-core1:eth3 set down |
| 4.372 | cable | dc1-core1:eth3 down at both ends |
| 4.391 | dc1-core1 log | interface,info dci link down |
| 4.436 | dc2-core1 log | interface,info dci link down |
| 4.456 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 4.467 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 4.624 | dc2-core1 log | interface,info ether4 link down |
| 5.310 | dc1-core1 log | interface,info ether4 link down |
| 9.375 | step | DCI member back |
| 9.398 | cable | dc1-core1:eth3 set up |
| 9.398 | cable | dc1-core1:eth3 up at both ends |
| 9.448 | dc1-core1 log | interface,info dci link up |
| 9.498 | dc2-core1 log | interface,info dci link up |
| 9.548 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 9.552 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.213 s, request absent at destination |
| 9.626 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 10.318 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.892 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.413 s, request absent at destination |
| 11.901 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.413 s, request absent at destination |
| 16.501 | state | DCI member back pass |
| 16.501 | steps | last step ended |
| 20.023 | state | check after the steps: pass |
| 20.023 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 20.023 | state | Every switch runs with spanning tree off. pass |
| 20.023 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 20.023 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 20.023 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 20.023 | state | Both cables of every host are eligible in its LACP bond. pass |
| 20.023 | streams | measurement ended; captures wait for final replies |
| 20.533 | stopped | captures and streams stopped |
| 20.559 | dc1-core1 log | script,info networka dci-member-loss end |
| 20.594 | dc1-core2 log | script,info networka dci-member-loss end |
| 20.627 | dc1-dist1 log | script,info networka dci-member-loss end |
| 20.675 | dc1-dist2 log | script,info networka dci-member-loss end |
| 20.710 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.747 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.780 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.807 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.857 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.914 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.922 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
