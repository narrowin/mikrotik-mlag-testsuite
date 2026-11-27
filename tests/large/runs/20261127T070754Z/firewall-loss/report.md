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
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.61391 to 2.81785 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 26 at one ping every 100 ms | 2.63804 to 2.84551 s | pass |
| dc1-firewall power restored | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 1 at one ping every 100 ms | 0 to 0.203675 s | pass |
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

- Data cables lost carrier and the guest was paused for 20.045 s.
- The new boot was detected at +22.091 s, with all lab checks passing at +32.236 s.

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
| -9.700 | test | firewall-loss started in lab large-mlag |
| -9.099 | dc1-core1 log | script,info networka firewall-loss start |
| -8.503 | dc1-core2 log | script,info networka firewall-loss start |
| -7.879 | dc1-dist1 log | script,info networka firewall-loss start |
| -7.284 | dc1-dist2 log | script,info networka firewall-loss start |
| -6.683 | dc1-firewall log | script,info networka firewall-loss start |
| -6.098 | dc2-core1 log | script,info networka firewall-loss start |
| -5.491 | dc2-core2 log | script,info networka firewall-loss start |
| -4.901 | dc2-dist1 log | script,info networka firewall-loss start |
| -4.295 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.681 | dc2-firewall log | script,info networka firewall-loss start |
| -3.675 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.145 | state | check before the steps: pass |
| -0.145 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.145 | state | Every switch runs with spanning tree off. pass |
| -0.145 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.145 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.145 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.145 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.135 | capture | started at dc1-service:bond0 |
| -0.135 | capture | started at dc1-traffic:bond0 |
| -0.135 | capture | started at dc1-traffic:vlan390 |
| -0.082 | capture | started at dc2-service:bond0 |
| -0.082 | capture | started at dc2-traffic:bond0 |
| -0.082 | capture | started at dc2-traffic:vlan390 |
| -0.024 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.020 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.016 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.012 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.011 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.009 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.985 | quiet window | clean |
| 3.985 | step | Baseline |
| 7.986 | step | dc1-firewall power lost |
| 8.116 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.131 | dc2-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.638 to 2.846 s, reply absent at source |
| 8.132 | dc1-traffic-to-vrrp | 26 pings lost at one ping every 100 ms, traffic stopped for 2.614 to 2.818 s, reply absent at source |
| 8.186 | dc1-core2 log | interface,info firewall link down |
| 8.260 | power | dc1-firewall guest paused and all data cables down |
| 8.264 | dc1-core1 log | interface,info firewall link down |
| 8.540 | dc1-core2 log | interface,info ether5 link down |
| 9.156 | dc1-core1 log | interface,info ether5 link down |
| 10.761 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.304 | state | dc1-firewall power lost pass |
| 28.304 | step | dc1-firewall power restored |
| 28.305 | power | resetting and resuming the guest of dc1-firewall |
| 28.426 | dc1-core2 log | interface,info firewall link up |
| 28.496 | power | dc1-firewall guest running and all data cables up |
| 28.504 | dc1-core1 log | interface,info firewall link up |
| 28.605 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.188 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 53.030 | recovery | full lab state after power restoration of dc1-firewall: error |
| 53.439 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 53.443 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 53.449 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 60.540 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 76.541 | step | Power recovery |
| 79.544 | steps | last step ended |
| 82.878 | state | check after the steps: pass |
| 82.878 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 82.878 | state | Every switch runs with spanning tree off. pass |
| 82.878 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 82.878 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 82.878 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 82.878 | state | Both cables of every host are eligible in its LACP bond. pass |
| 82.879 | streams | measurement ended; captures wait for final replies |
| 83.386 | stopped | captures and streams stopped |
| 83.414 | dc1-core1 log | script,info networka firewall-loss end |
| 83.446 | dc1-core2 log | script,info networka firewall-loss end |
| 83.477 | dc1-dist1 log | script,info networka firewall-loss end |
| 83.516 | dc1-dist2 log | script,info networka firewall-loss end |
| 83.557 | dc1-firewall log | script,info networka firewall-loss end |
| 83.589 | dc2-core1 log | script,info networka firewall-loss end |
| 83.625 | dc2-core2 log | script,info networka firewall-loss end |
| 83.664 | dc2-dist1 log | script,info networka firewall-loss end |
| 83.704 | dc2-dist2 log | script,info networka firewall-loss end |
| 83.762 | dc2-firewall log | script,info networka firewall-loss end |
| 83.773 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
