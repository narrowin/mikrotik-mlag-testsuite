# PASS — baseline

Check forwarding inside each site, and across the DCI in both directions, with all four MLAG pairs connected and the dc1 firewall owning the VRRP address.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -9.904 | test | baseline started in lab large-mlag |
| -9.271 | dc1-core1 log | script,info networka baseline start |
| -8.675 | dc1-core2 log | script,info networka baseline start |
| -8.049 | dc1-dist1 log | script,info networka baseline start |
| -7.436 | dc1-dist2 log | script,info networka baseline start |
| -6.795 | dc1-firewall log | script,info networka baseline start |
| -6.202 | dc2-core1 log | script,info networka baseline start |
| -5.604 | dc2-core2 log | script,info networka baseline start |
| -5.001 | dc2-dist1 log | script,info networka baseline start |
| -4.405 | dc2-dist2 log | script,info networka baseline start |
| -3.806 | dc2-firewall log | script,info networka baseline start |
| -3.802 | switch log | marker 'networka baseline start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.129 | state | check before the steps: pass |
| -0.129 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.129 | state | Every switch runs with spanning tree off. pass |
| -0.129 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.129 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.129 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.129 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.121 | capture | started at dc1-service:bond0 |
| -0.121 | capture | started at dc1-traffic:bond0 |
| -0.121 | capture | started at dc1-traffic:vlan390 |
| -0.121 | capture | started at dc2-service:bond0 |
| -0.068 | capture | started at dc2-traffic:bond0 |
| -0.068 | capture | started at dc2-traffic:vlan390 |
| -0.011 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.008 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.006 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.003 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.038 | quiet window | clean |
| 4.038 | step | Steady traffic |
| 8.038 | steps | last step ended |
| 11.362 | state | check after the steps: pass |
| 11.362 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 11.362 | state | Every switch runs with spanning tree off. pass |
| 11.362 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 11.362 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 11.362 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 11.362 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.363 | streams | measurement ended; captures wait for final replies |
| 11.867 | stopped | captures and streams stopped |
| 11.894 | dc1-core1 log | script,info networka baseline end |
| 11.929 | dc1-core2 log | script,info networka baseline end |
| 11.961 | dc1-dist1 log | script,info networka baseline end |
| 11.994 | dc1-dist2 log | script,info networka baseline end |
| 12.035 | dc1-firewall log | script,info networka baseline end |
| 12.083 | dc2-core1 log | script,info networka baseline end |
| 12.111 | dc2-core2 log | script,info networka baseline end |
| 12.152 | dc2-dist1 log | script,info networka baseline end |
| 12.199 | dc2-dist2 log | script,info networka baseline end |
| 12.237 | dc2-firewall log | script,info networka baseline end |
| 12.244 | switch log | marker 'networka baseline end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
