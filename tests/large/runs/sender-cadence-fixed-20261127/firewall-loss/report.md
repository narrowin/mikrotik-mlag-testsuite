# PASS — firewall-loss

Withdraw all data links of the dc1 firewall and pause its guest before a cold reset. The dc2 firewall must take over the VRRP address, and dc1 must take it back after power returns. The streams between hosts cross no firewall and must continue; the pings to the VRRP address may stop only while the address moves.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 31 at one ping every 100 ms | 3.12203 to 3.32829 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 31 at one ping every 100 ms | 3.14373 to 3.34885 s | pass |
| dc1-firewall power restored | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**dc1-firewall power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

**Power loss of dc1-firewall** · pass

- Data cables lost carrier and the guest was paused for 20.048 s.
- The new boot was detected at +29.133 s, with all lab checks passing at +31.934 s.

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
| -3.223 | test | firewall-loss started in lab large-mlag |
| -3.192 | dc1-core1 log | script,info networka firewall-loss start |
| -3.155 | dc1-core2 log | script,info networka firewall-loss start |
| -3.121 | dc1-dist1 log | script,info networka firewall-loss start |
| -3.069 | dc1-dist2 log | script,info networka firewall-loss start |
| -3.029 | dc1-firewall log | script,info networka firewall-loss start |
| -2.983 | dc2-core1 log | script,info networka firewall-loss start |
| -2.950 | dc2-core2 log | script,info networka firewall-loss start |
| -2.916 | dc2-dist1 log | script,info networka firewall-loss start |
| -2.875 | dc2-dist2 log | script,info networka firewall-loss start |
| -2.831 | dc2-firewall log | script,info networka firewall-loss start |
| -2.829 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.136 | state | check before the steps: pass |
| -0.136 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.136 | state | Every switch runs with spanning tree off. pass |
| -0.136 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.136 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.136 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.136 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.127 | capture | started at dc1-service:bond0 |
| -0.127 | capture | started at dc1-traffic:bond0 |
| -0.126 | capture | started at dc1-traffic:vlan390 |
| -0.126 | capture | started at dc2-service:bond0 |
| -0.074 | capture | started at dc2-traffic:bond0 |
| -0.074 | capture | started at dc2-traffic:vlan390 |
| -0.019 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.015 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.011 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.192 | quiet window | clean |
| 4.192 | step | Baseline |
| 8.195 | step | dc1-firewall power lost |
| 8.335 | power | taking down the data cables of dc1-firewall and stopping its guest |
| 8.364 | dc1-traffic-to-vrrp | 31 pings lost at one ping every 100 ms, traffic stopped for 3.122 to 3.328 s, reply absent at source |
| 8.408 | dc2-traffic-to-vrrp | 31 pings lost at one ping every 100 ms, traffic stopped for 3.144 to 3.349 s, reply absent at source |
| 8.439 | dc1-core1 log | interface,info firewall link down |
| 8.441 | dc1-core2 log | interface,info firewall link down |
| 8.521 | power | dc1-firewall guest paused and all data cables down |
| 9.033 | dc1-core1 log | interface,info ether5 link down |
| 9.116 | dc1-core2 log | interface,info ether5 link down |
| 11.575 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.567 | state | dc1-firewall power lost pass |
| 28.567 | step | dc1-firewall power restored |
| 28.568 | power | resetting and resuming the guest of dc1-firewall |
| 28.787 | power | dc1-firewall guest running and all data cables up |
| 28.788 | dc1-core1 log | interface,info firewall link up |
| 28.788 | dc1-core2 log | interface,info firewall link up |
| 29.088 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.210 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 56.323 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 56.332 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 60.502 | recovery | full lab state after the power loss of dc1-firewall: pass |
| 76.505 | step | Power recovery |
| 79.509 | steps | last step ended |
| 82.930 | state | check after the steps: pass |
| 82.930 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 82.930 | state | Every switch runs with spanning tree off. pass |
| 82.930 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 82.930 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 82.930 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 82.930 | state | Both cables of every host are eligible in its LACP bond. pass |
| 82.930 | streams | measurement ended; captures wait for final replies |
| 83.439 | stopped | captures and streams stopped |
| 83.466 | dc1-core1 log | script,info networka firewall-loss end |
| 83.506 | dc1-core2 log | script,info networka firewall-loss end |
| 83.539 | dc1-dist1 log | script,info networka firewall-loss end |
| 83.580 | dc1-dist2 log | script,info networka firewall-loss end |
| 83.627 | dc1-firewall log | script,info networka firewall-loss end |
| 83.660 | dc2-core1 log | script,info networka firewall-loss end |
| 83.688 | dc2-core2 log | script,info networka firewall-loss end |
| 83.722 | dc2-dist1 log | script,info networka firewall-loss end |
| 83.755 | dc2-dist2 log | script,info networka firewall-loss end |
| 83.790 | dc2-firewall log | script,info networka firewall-loss end |
| 83.796 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
