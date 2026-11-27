# PASS — baseline

Check forwarding inside each site, and across the DCI in both directions, with all four MLAG pairs connected and the dc1 firewall owning the VRRP address.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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
| -10.574 | test | baseline started in lab large-mlag |
| -9.903 | dc1-core1 log | script,info networka baseline start |
| -9.246 | dc1-core2 log | script,info networka baseline start |
| -8.585 | dc1-dist1 log | script,info networka baseline start |
| -7.915 | dc1-dist2 log | script,info networka baseline start |
| -7.244 | dc1-firewall log | script,info networka baseline start |
| -6.596 | dc2-core1 log | script,info networka baseline start |
| -5.987 | dc2-core2 log | script,info networka baseline start |
| -5.389 | dc2-dist1 log | script,info networka baseline start |
| -4.652 | dc2-dist2 log | script,info networka baseline start |
| -3.969 | dc2-firewall log | script,info networka baseline start |
| -3.961 | switch log | marker 'networka baseline start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.147 | state | check before the steps: pass |
| -0.147 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.147 | state | Every switch runs with spanning tree off. pass |
| -0.147 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.147 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.147 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.147 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.139 | capture | started at dc1-service:bond0 |
| -0.139 | capture | started at dc1-traffic:bond0 |
| -0.139 | capture | started at dc1-traffic:vlan390 |
| -0.087 | capture | started at dc2-service:bond0 |
| -0.086 | capture | started at dc2-traffic:bond0 |
| -0.086 | capture | started at dc2-traffic:vlan390 |
| -0.030 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.026 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.022 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.019 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.016 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.014 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.069 | quiet window | clean |
| 4.069 | step | Steady traffic |
| 8.071 | steps | last step ended |
| 11.712 | state | check after the steps: pass |
| 11.712 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 11.712 | state | Every switch runs with spanning tree off. pass |
| 11.712 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 11.712 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 11.712 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 11.712 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.712 | streams | measurement ended; captures wait for final replies |
| 12.224 | stopped | captures and streams stopped |
| 12.253 | dc1-core1 log | script,info networka baseline end |
| 12.297 | dc1-core2 log | script,info networka baseline end |
| 12.337 | dc1-dist1 log | script,info networka baseline end |
| 12.371 | dc1-dist2 log | script,info networka baseline end |
| 12.408 | dc1-firewall log | script,info networka baseline end |
| 12.447 | dc2-core1 log | script,info networka baseline end |
| 12.485 | dc2-core2 log | script,info networka baseline end |
| 12.530 | dc2-dist1 log | script,info networka baseline end |
| 12.566 | dc2-dist2 log | script,info networka baseline end |
| 12.602 | dc2-firewall log | script,info networka baseline end |
| 12.605 | switch log | marker 'networka baseline end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
