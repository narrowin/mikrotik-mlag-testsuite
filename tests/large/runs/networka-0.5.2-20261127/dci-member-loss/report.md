# PASS — dci-member-loss

Take the DCI member between dc1-core1 and dc2-core1 down and back. The DCI streams must move to the other member; the site streams cross neither core and must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| DCI member down | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.206877 s | pass |
| DCI member down | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 1 s | 1 at one ping every 100 ms | 0 to 0.207126 s | pass |
| DCI member down | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member down | dc2-traffic:vlan390 → 198.18.40.1 | 1 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| DCI member back | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 4 s | 4 at one ping every 100 ms | 0.208561 to 0.414061 s | pass |
| DCI member back | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 4 s | 3 at one ping every 100 ms | 0.2128 to 0.418074 s | pass |
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
| Whole test | dc1-core1 -7.72963 to 20.361 s, dc1-core2 -7.41642 to 20.3958 s, dc1-dist1 -7.10999 to 20.4292 s, dc1-dist2 -6.75245 to 20.4642 s, dc1-firewall -6.39427 to 20.5003 s, dc2-core1 -5.99962 to 20.5377 s, dc2-core2 -5.53211 to 20.5866 s, dc2-dist1 -5.11224 to 20.6179 s, dc2-dist2 -4.7058 to 20.6734 s, dc2-firewall -4.32066 to 20.7045 s | must\_not heartbeat timeout | pass | not logged |
| DCI member down | dc1-core1 4.14355 to 9.18144 s | must ether4 link down | pass | 2026-11-27T07:56:13.657889+00:00 dc1-core1 interface,info ether4 link down |
| DCI member down | dc2-core1 4.14355 to 9.18144 s | must ether4 link down | pass | 2026-11-27T07:56:13.465885+00:00 dc2-core1 interface,info ether4 link down |
| DCI member back | dc1-core1 9.18144 to 16.3154 s | must ether4 link up | pass | 2026-11-27T07:56:18.674817+00:00 dc1-core1 interface,info ether4 link up (speed 10G, full duplex) |
| DCI member back | dc2-core1 9.18144 to 16.3154 s | must ether4 link up | pass | 2026-11-27T07:56:18.506159+00:00 dc2-core1 interface,info ether4 link up (speed 10G, full duplex) |

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -8.034 | test | dci-member-loss started in lab large-mlag |
| -7.730 | dc1-core1 log | script,info networka dci-member-loss start |
| -7.416 | dc1-core2 log | script,info networka dci-member-loss start |
| -7.110 | dc1-dist1 log | script,info networka dci-member-loss start |
| -6.752 | dc1-dist2 log | script,info networka dci-member-loss start |
| -6.394 | dc1-firewall log | script,info networka dci-member-loss start |
| -6.000 | dc2-core1 log | script,info networka dci-member-loss start |
| -5.532 | dc2-core2 log | script,info networka dci-member-loss start |
| -5.112 | dc2-dist1 log | script,info networka dci-member-loss start |
| -4.706 | dc2-dist2 log | script,info networka dci-member-loss start |
| -4.321 | dc2-firewall log | script,info networka dci-member-loss start |
| -4.313 | switch log | marker 'networka dci-member-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.140 | state | check before the steps: pass |
| -0.140 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.140 | state | Every switch runs with spanning tree off. pass |
| -0.140 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.140 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.140 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.140 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.126 | capture | started at dc1-core1:eth3 |
| -0.126 | capture | started at dc1-service:bond0 |
| -0.126 | capture | started at dc1-traffic:bond0 |
| -0.126 | capture | started at dc1-traffic:vlan390 |
| -0.126 | capture | started at dc2-core1:eth3 |
| -0.126 | capture | started at dc2-service:bond0 |
| -0.075 | capture | started at dc2-traffic:bond0 |
| -0.074 | capture | started at dc2-traffic:vlan390 |
| -0.017 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.013 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.009 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.143 | quiet window | clean |
| 4.144 | step | DCI member down |
| 4.179 | cable | dc1-core1:eth3 set down |
| 4.180 | cable | dc1-core1:eth3 down at both ends |
| 4.237 | dc1-core1 log | interface,info dci link down |
| 4.250 | dc2-core1 log | interface,info dci link down |
| 4.251 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 4.251 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 4.306 | dc2-core1 log | interface,info ether4 link down |
| 4.498 | dc1-core1 log | interface,info ether4 link down |
| 9.181 | step | DCI member back |
| 9.210 | cable | dc1-core1:eth3 set up |
| 9.210 | cable | dc1-core1:eth3 up at both ends |
| 9.295 | dc1-core1 log | interface,info dci link up |
| 9.321 | dc2-core1 log | interface,info dci link up |
| 9.346 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 9.411 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 9.515 | dc1-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 11.757 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.414 s, request absent at destination |
| 11.777 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.418 s, request absent at destination |
| 16.315 | state | DCI member back pass |
| 16.315 | steps | last step ended |
| 19.823 | state | check after the steps: pass |
| 19.823 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 19.823 | state | Every switch runs with spanning tree off. pass |
| 19.823 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 19.823 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 19.823 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 19.823 | state | Both cables of every host are eligible in its LACP bond. pass |
| 19.823 | streams | measurement ended; captures wait for final replies |
| 20.334 | stopped | captures and streams stopped |
| 20.361 | dc1-core1 log | script,info networka dci-member-loss end |
| 20.396 | dc1-core2 log | script,info networka dci-member-loss end |
| 20.429 | dc1-dist1 log | script,info networka dci-member-loss end |
| 20.464 | dc1-dist2 log | script,info networka dci-member-loss end |
| 20.500 | dc1-firewall log | script,info networka dci-member-loss end |
| 20.538 | dc2-core1 log | script,info networka dci-member-loss end |
| 20.587 | dc2-core2 log | script,info networka dci-member-loss end |
| 20.618 | dc2-dist1 log | script,info networka dci-member-loss end |
| 20.673 | dc2-dist2 log | script,info networka dci-member-loss end |
| 20.705 | dc2-firewall log | script,info networka dci-member-loss end |
| 20.709 | switch log | marker 'networka dci-member-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
