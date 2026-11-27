# PASS — firewall-loss

Withdraw all data links of the dc1 firewall and pause its guest before a cold reset. The dc2 firewall must take over the VRRP address, and dc1 must take it back after power returns. The streams between hosts cross no firewall and must continue; the pings to the VRRP address may stop only while the address moves.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
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
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.60824 to 2.81878 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.63567 to 2.84307 s | pass |
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

- Data cables lost carrier and the guest was paused for 20.039 s.
- The new boot was detected at +30.891 s, with all lab checks passing at +33.486 s.

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
| -6.505 | test | firewall-loss started in lab large-mlag |
| -6.214 | dc1-core1 log | script,info networka firewall-loss start |
| -5.929 | dc1-core2 log | script,info networka firewall-loss start |
| -5.648 | dc1-dist1 log | script,info networka firewall-loss start |
| -5.352 | dc1-dist2 log | script,info networka firewall-loss start |
| -5.052 | dc1-firewall log | script,info networka firewall-loss start |
| -4.769 | dc2-core1 log | script,info networka firewall-loss start |
| -4.460 | dc2-core2 log | script,info networka firewall-loss start |
| -4.174 | dc2-dist1 log | script,info networka firewall-loss start |
| -3.883 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.589 | dc2-firewall log | script,info networka firewall-loss start |
| -3.581 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.132 | state | check before the steps: pass |
| -0.132 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.132 | state | Every switch runs with spanning tree off. pass |
| -0.132 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.132 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.132 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.132 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.124 | capture | started at dc1-service:bond0 |
| -0.124 | capture | started at dc1-traffic:bond0 |
| -0.124 | capture | started at dc1-traffic:vlan390 |
| -0.070 | capture | started at dc2-service:bond0 |
| -0.070 | capture | started at dc2-traffic:bond0 |
| -0.070 | capture | started at dc2-traffic:vlan390 |
| -0.015 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.012 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.008 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.003 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.002 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.987 | quiet window | clean |
| 3.987 | step | Baseline |
| 7.988 | step | dc1-firewall power lost |
| 8.126 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.162 | dc2-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.636 to 2.843 s, reply absent at source |
| 8.175 | dc1-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.608 to 2.819 s, reply absent at source |
| 8.178 | dc1-core2 log | interface,info ether5 link down |
| 8.194 | dc1-core2 log | interface,info firewall link down |
| 8.224 | dc1-core1 log | interface,info firewall link down |
| 8.295 | power | dc1-firewall guest paused and all data cables down |
| 8.951 | dc1-core1 log | interface,info ether5 link down |
| 10.826 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.333 | state | dc1-firewall power lost pass |
| 28.333 | step | dc1-firewall power restored |
| 28.334 | power | resetting and resuming the guest of dc1-firewall |
| 28.462 | dc1-core1 log | interface,info firewall link up |
| 28.537 | dc1-core2 log | interface,info firewall link up |
| 28.576 | power | dc1-firewall guest running and all data cables up |
| 29.011 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.207 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 60.264 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 60.271 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 61.821 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 77.823 | step | Power recovery |
| 80.825 | steps | last step ended |
| 84.026 | state | check after the steps: pass |
| 84.026 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 84.026 | state | Every switch runs with spanning tree off. pass |
| 84.026 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 84.026 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 84.026 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 84.026 | state | Both cables of every host are eligible in its LACP bond. pass |
| 84.027 | streams | measurement ended; captures wait for final replies |
| 84.533 | stopped | captures and streams stopped |
| 84.558 | dc1-core1 log | script,info networka firewall-loss end |
| 84.598 | dc1-core2 log | script,info networka firewall-loss end |
| 84.630 | dc1-dist1 log | script,info networka firewall-loss end |
| 84.671 | dc1-dist2 log | script,info networka firewall-loss end |
| 84.713 | dc1-firewall log | script,info networka firewall-loss end |
| 84.742 | dc2-core1 log | script,info networka firewall-loss end |
| 84.770 | dc2-core2 log | script,info networka firewall-loss end |
| 84.805 | dc2-dist1 log | script,info networka firewall-loss end |
| 84.838 | dc2-dist2 log | script,info networka firewall-loss end |
| 84.871 | dc2-firewall log | script,info networka firewall-loss end |
| 84.874 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
