# PASS — baseline

Check forwarding inside each site, across the DCI in both directions and on the bypass, with all four MLAG pairs connected and the dc1 firewall owning the VRRP address.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

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

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -11.137 | test | baseline started in lab large-mlag |
| -10.405 | dc1-core1 log | script,info networka baseline start |
| -9.669 | dc1-core2 log | script,info networka baseline start |
| -8.923 | dc1-dist1 log | script,info networka baseline start |
| -8.203 | dc1-dist2 log | script,info networka baseline start |
| -7.612 | dc1-firewall log | script,info networka baseline start |
| -6.882 | dc2-core1 log | script,info networka baseline start |
| -6.153 | dc2-core2 log | script,info networka baseline start |
| -5.414 | dc2-dist1 log | script,info networka baseline start |
| -4.684 | dc2-dist2 log | script,info networka baseline start |
| -4.099 | dc2-firewall log | script,info networka baseline start |
| -4.094 | switch log | marker 'networka baseline start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.147 | state | check before the steps: pass |
| -0.147 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.147 | state | Every switch runs with spanning tree off. pass |
| -0.147 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.147 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.147 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.147 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.133 | capture | started at dc1-service:bond0 |
| -0.133 | capture | started at dc1-traffic:bond0 |
| -0.133 | capture | started at dc1-traffic:eth3 |
| -0.133 | capture | started at dc1-traffic:vlan390 |
| -0.132 | capture | started at dc2-service:bond0 |
| -0.132 | capture | started at dc2-traffic:bond0 |
| -0.081 | capture | started at dc2-traffic:eth3 |
| -0.081 | capture | started at dc2-traffic:vlan390 |
| -0.024 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.015 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.010 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | bypass-dc1-to-dc2 | started from dc1-traffic:eth3 to dc2-traffic:eth3 at 198.51.100.2 |
| -0.001 | bypass-dc2-to-dc1 | started from dc2-traffic:eth3 to dc1-traffic:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.349 | quiet window | clean |
| 4.349 | step | Steady traffic |
| 8.351 | steps | last step ended |
| 11.883 | state | check after the steps: pass |
| 11.883 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 11.883 | state | Every switch runs with spanning tree off. pass |
| 11.883 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 11.883 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 11.883 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 11.883 | state | Both cables of every host are eligible in its LACP bond. pass |
| 11.883 | streams | measurement ended; captures wait for final replies |
| 12.391 | stopped | captures and streams stopped |
| 12.420 | dc1-core1 log | script,info networka baseline end |
| 12.450 | dc1-core2 log | script,info networka baseline end |
| 12.486 | dc1-dist1 log | script,info networka baseline end |
| 12.546 | dc1-dist2 log | script,info networka baseline end |
| 12.600 | dc1-firewall log | script,info networka baseline end |
| 12.634 | dc2-core1 log | script,info networka baseline end |
| 12.677 | dc2-core2 log | script,info networka baseline end |
| 12.727 | dc2-dist1 log | script,info networka baseline end |
| 12.760 | dc2-dist2 log | script,info networka baseline end |
| 12.810 | dc2-firewall log | script,info networka baseline end |
| 12.813 | switch log | marker 'networka baseline end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
