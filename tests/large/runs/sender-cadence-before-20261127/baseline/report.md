# PASS — baseline

Check forwarding inside each site, and across the DCI in both directions, with all four MLAG pairs connected and the dc1 firewall owning the VRRP address.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -12.775 | test | baseline started in lab large-mlag |
| -12.122 | dc1-core1 log | script,info networka baseline start |
| -11.506 | dc1-core2 log | script,info networka baseline start |
| -10.889 | dc1-dist1 log | script,info networka baseline start |
| -10.249 | dc1-dist2 log | script,info networka baseline start |
| -9.615 | dc1-firewall log | script,info networka baseline start |
| -8.986 | dc2-core1 log | script,info networka baseline start |
| -8.352 | dc2-core2 log | script,info networka baseline start |
| -7.741 | dc2-dist1 log | script,info networka baseline start |
| -7.119 | dc2-dist2 log | script,info networka baseline start |
| -6.491 | dc2-firewall log | script,info networka baseline start |
| -6.483 | switch log | marker 'networka baseline start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.168 | state | check before the steps: pass |
| -0.168 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.168 | state | Every switch runs with spanning tree off. pass |
| -0.168 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.168 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.168 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.168 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.156 | capture | started at dc1-service:bond0 |
| -0.156 | capture | started at dc1-traffic:bond0 |
| -0.156 | capture | started at dc1-traffic:vlan390 |
| -0.156 | capture | started at dc2-service:bond0 |
| -0.156 | capture | started at dc2-traffic:bond0 |
| -0.105 | capture | started at dc2-traffic:vlan390 |
| -0.048 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.043 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.033 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.021 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.016 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.011 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.046 | quiet window | clean |
| 4.047 | step | Steady traffic |
| 8.050 | steps | last step ended |
| 11.410 | state | check after the steps: pass |
| 11.410 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 11.410 | state | Every switch runs with spanning tree off. pass |
| 11.410 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 11.410 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 11.410 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 11.410 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.410 | streams | measurement ended; captures wait for final replies |
| 11.918 | stopped | captures and streams stopped |
| 11.948 | dc1-core1 log | script,info networka baseline end |
| 11.990 | dc1-core2 log | script,info networka baseline end |
| 12.029 | dc1-dist1 log | script,info networka baseline end |
| 12.062 | dc1-dist2 log | script,info networka baseline end |
| 12.099 | dc1-firewall log | script,info networka baseline end |
| 12.136 | dc2-core1 log | script,info networka baseline end |
| 12.180 | dc2-core2 log | script,info networka baseline end |
| 12.217 | dc2-dist1 log | script,info networka baseline end |
| 12.271 | dc2-dist2 log | script,info networka baseline end |
| 12.329 | dc2-firewall log | script,info networka baseline end |
| 12.333 | switch log | marker 'networka baseline end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
