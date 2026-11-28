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
| -10.119 | test | baseline started in lab large-mlag |
| -9.422 | dc1-core1 log | script,info networka baseline start |
| -8.779 | dc1-core2 log | script,info networka baseline start |
| -8.148 | dc1-dist1 log | script,info networka baseline start |
| -7.533 | dc1-dist2 log | script,info networka baseline start |
| -6.916 | dc1-firewall log | script,info networka baseline start |
| -6.299 | dc2-core1 log | script,info networka baseline start |
| -5.658 | dc2-core2 log | script,info networka baseline start |
| -5.061 | dc2-dist1 log | script,info networka baseline start |
| -4.425 | dc2-dist2 log | script,info networka baseline start |
| -3.843 | dc2-firewall log | script,info networka baseline start |
| -3.839 | switch log | marker 'networka baseline start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.167 | state | check before the steps: pass |
| -0.167 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.167 | state | Every switch runs with spanning tree off. pass |
| -0.167 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.167 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.167 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.167 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.104 | capture | started at dc1-service:bond0 |
| -0.104 | capture | started at dc1-traffic:bond0 |
| -0.104 | capture | started at dc1-traffic:vlan390 |
| -0.104 | capture | started at dc2-service:bond0 |
| -0.104 | capture | started at dc2-traffic:bond0 |
| -0.104 | capture | started at dc2-traffic:vlan390 |
| -0.044 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.040 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.035 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.030 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.027 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.025 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.086 | quiet window | clean |
| 4.086 | step | Steady traffic |
| 8.088 | steps | last step ended |
| 11.605 | state | check after the steps: pass |
| 11.605 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 11.605 | state | Every switch runs with spanning tree off. pass |
| 11.605 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 11.605 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 11.605 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 11.605 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.605 | streams | measurement ended; captures wait for final replies |
| 12.113 | stopped | captures and streams stopped |
| 12.139 | dc1-core1 log | script,info networka baseline end |
| 12.176 | dc1-core2 log | script,info networka baseline end |
| 12.206 | dc1-dist1 log | script,info networka baseline end |
| 12.246 | dc1-dist2 log | script,info networka baseline end |
| 12.297 | dc1-firewall log | script,info networka baseline end |
| 12.328 | dc2-core1 log | script,info networka baseline end |
| 12.363 | dc2-core2 log | script,info networka baseline end |
| 12.423 | dc2-dist1 log | script,info networka baseline end |
| 12.467 | dc2-dist2 log | script,info networka baseline end |
| 12.499 | dc2-firewall log | script,info networka baseline end |
| 12.501 | switch log | marker 'networka baseline end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
