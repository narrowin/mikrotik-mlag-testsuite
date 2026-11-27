# PASS — firewall-loss

Withdraw all data links of the dc1 firewall and pause its guest before a cold reset. The dc2 firewall must take over the VRRP address, and dc1 must take it back after power returns. No stream crosses a firewall, so every stream must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:eth3 → dc2-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:eth3 → dc1-traffic:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**dc1-firewall power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

**Power loss of dc1-firewall** · pass

- Data cables lost carrier and the guest was paused for 20.057 s.
- The new boot was detected at +41.538 s, with all lab checks passing at +44.865 s.

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
| -16.159 | test | firewall-loss started in lab large-mlag |
| -15.458 | dc1-core1 log | script,info networka firewall-loss start |
| -14.777 | dc1-core2 log | script,info networka firewall-loss start |
| -13.705 | dc1-dist1 log | script,info networka firewall-loss start |
| -12.200 | dc1-dist2 log | script,info networka firewall-loss start |
| -11.093 | dc1-firewall log | script,info networka firewall-loss start |
| -9.686 | dc2-core1 log | script,info networka firewall-loss start |
| -8.096 | dc2-core2 log | script,info networka firewall-loss start |
| -6.147 | dc2-dist1 log | script,info networka firewall-loss start |
| -5.160 | dc2-dist2 log | script,info networka firewall-loss start |
| -4.363 | dc2-firewall log | script,info networka firewall-loss start |
| -4.355 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.150 | state | check before the steps: pass |
| -0.150 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.150 | state | Every switch runs with spanning tree off. pass |
| -0.150 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.150 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.150 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.150 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.134 | capture | started at dc1-service:bond0 |
| -0.134 | capture | started at dc1-traffic:bond0 |
| -0.134 | capture | started at dc1-traffic:eth3 |
| -0.133 | capture | started at dc1-traffic:vlan390 |
| -0.133 | capture | started at dc2-service:bond0 |
| -0.133 | capture | started at dc2-traffic:bond0 |
| -0.081 | capture | started at dc2-traffic:eth3 |
| -0.081 | capture | started at dc2-traffic:vlan390 |
| -0.024 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.015 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.011 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | bypass-dc1-to-dc2 | started from dc1-traffic:eth3 to dc2-traffic:eth3 at 198.51.100.2 |
| -0.001 | bypass-dc2-to-dc1 | started from dc2-traffic:eth3 to dc1-traffic:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.478 | quiet window | clean |
| 4.478 | step | Baseline |
| 8.480 | step | dc1-firewall power lost |
| 8.622 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.707 | dc1-core1 log | interface,info firewall link down |
| 8.707 | dc1-core2 log | interface,info firewall link down |
| 8.805 | power | dc1-firewall guest paused and all data cables down |
| 9.134 | dc1-core1 log | interface,info ether5 link down |
| 9.569 | dc1-core2 log | interface,info ether5 link down |
| 12.118 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.860 | state | dc1-firewall power lost pass |
| 28.861 | step | dc1-firewall power restored |
| 28.862 | power | resetting and resuming the guest of dc1-firewall |
| 29.064 | dc1-core1 log | interface,info firewall link up |
| 29.073 | dc1-core2 log | interface,info firewall link up |
| 29.205 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.226 | power | dc1-firewall guest running and all data cables up |
| 29.648 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 64.657 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 64.672 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 73.728 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 89.728 | step | Power recovery |
| 92.730 | steps | last step ended |
| 96.763 | state | check after the steps: pass |
| 96.763 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 96.763 | state | Every switch runs with spanning tree off. pass |
| 96.763 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 96.763 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 96.763 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 96.763 | state | Both cables of every host are eligible in its LACP bond. pass |
| 96.764 | streams | measurement ended; captures wait for final replies |
| 97.287 | stopped | captures and streams stopped |
| 97.341 | dc1-core1 log | script,info networka firewall-loss end |
| 97.392 | dc1-core2 log | script,info networka firewall-loss end |
| 97.493 | dc1-dist1 log | script,info networka firewall-loss end |
| 97.544 | dc1-dist2 log | script,info networka firewall-loss end |
| 97.613 | dc1-firewall log | script,info networka firewall-loss end |
| 97.669 | dc2-core1 log | script,info networka firewall-loss end |
| 97.719 | dc2-core2 log | script,info networka firewall-loss end |
| 97.765 | dc2-dist1 log | script,info networka firewall-loss end |
| 97.814 | dc2-dist2 log | script,info networka firewall-loss end |
| 97.866 | dc2-firewall log | script,info networka firewall-loss end |
| 97.874 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
