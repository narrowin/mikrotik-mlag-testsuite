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
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.6007 to 2.80323 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.61804 to 2.82486 s | pass |
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

- Data cables lost carrier and the guest was paused for 20.052 s.
- The new boot was detected at +34.977 s, with all lab checks passing at +37.974 s after power-on dispatch, against a 180 s recovery deadline.

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
| -7.439 | test | firewall-loss started in lab large-mlag |
| -7.008 | dc1-core1 log | script,info networka firewall-loss start |
| -6.658 | dc1-core2 log | script,info networka firewall-loss start |
| -6.275 | dc1-dist1 log | script,info networka firewall-loss start |
| -5.913 | dc1-dist2 log | script,info networka firewall-loss start |
| -5.495 | dc1-firewall log | script,info networka firewall-loss start |
| -5.159 | dc2-core1 log | script,info networka firewall-loss start |
| -4.828 | dc2-core2 log | script,info networka firewall-loss start |
| -4.484 | dc2-dist1 log | script,info networka firewall-loss start |
| -4.145 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.819 | dc2-firewall log | script,info networka firewall-loss start |
| -3.808 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.140 | state | check before the steps: pass |
| -0.140 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.140 | state | Every switch runs with spanning tree off. pass |
| -0.140 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.140 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.140 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.140 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.129 | capture | started at dc1-service:bond0 |
| -0.129 | capture | started at dc1-traffic:bond0 |
| -0.129 | capture | started at dc1-traffic:vlan390 |
| -0.129 | capture | started at dc2-service:bond0 |
| -0.078 | capture | started at dc2-traffic:bond0 |
| -0.077 | capture | started at dc2-traffic:vlan390 |
| -0.022 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.018 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.013 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.008 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.006 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.278 | quiet window | clean |
| 4.279 | step | Baseline |
| 8.279 | step | dc1-firewall power lost |
| 8.439 | power | taking down the data cables of dc1-firewall and stopping its guest |
| 8.489 | dc1-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.601 to 2.803 s, reply absent at source |
| 8.510 | dc2-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.618 to 2.825 s, reply absent at source |
| 8.581 | dc1-core1 log | interface,info firewall link down |
| 8.591 | dc1-core2 log | interface,info ether5 link down |
| 8.607 | dc1-core2 log | interface,info firewall link down |
| 8.649 | power | dc1-firewall guest paused and all data cables down |
| 9.061 | dc1-core1 log | interface,info ether5 link down |
| 11.168 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.700 | state | dc1-firewall power lost pass |
| 28.700 | step | dc1-firewall power restored |
| 28.701 | power | resetting and resuming the guest of dc1-firewall |
| 28.831 | dc1-core2 log | interface,info firewall link up |
| 28.928 | dc1-core1 log | interface,info firewall link up |
| 28.936 | power | dc1-firewall guest running and all data cables up |
| 29.108 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.629 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 61.889 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 61.917 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 66.676 | recovery | full lab state after the power loss of dc1-firewall: pass |
| 82.677 | step | Power recovery |
| 85.682 | steps | last step ended |
| 90.237 | state | check after the steps: pass |
| 90.237 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 90.237 | state | Every switch runs with spanning tree off. pass |
| 90.237 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 90.237 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 90.237 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 90.237 | state | Both cables of every host are eligible in its LACP bond. pass |
| 90.238 | streams | measurement ended; captures wait for final replies |
| 90.764 | stopped | captures and streams stopped |
| 90.801 | dc1-core1 log | script,info networka firewall-loss end |
| 90.844 | dc1-core2 log | script,info networka firewall-loss end |
| 90.919 | dc1-dist1 log | script,info networka firewall-loss end |
| 90.958 | dc1-dist2 log | script,info networka firewall-loss end |
| 91.053 | dc1-firewall log | script,info networka firewall-loss end |
| 91.149 | dc2-core1 log | script,info networka firewall-loss end |
| 91.195 | dc2-core2 log | script,info networka firewall-loss end |
| 91.257 | dc2-dist1 log | script,info networka firewall-loss end |
| 91.318 | dc2-dist2 log | script,info networka firewall-loss end |
| 91.421 | dc2-firewall log | script,info networka firewall-loss end |
| 91.431 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
