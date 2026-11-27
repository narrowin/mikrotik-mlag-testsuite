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
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 27 at one ping every 100 ms | 2.70768 to 2.91114 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 27 at one ping every 100 ms | 2.70428 to 2.90796 s | pass |
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

- Data cables lost carrier and the guest was paused for 20.055 s.
- The new boot was detected at +30.463 s, with all lab checks passing at +41.961 s.

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
| -6.826 | test | firewall-loss started in lab large-mlag |
| -6.514 | dc1-core1 log | script,info networka firewall-loss start |
| -6.217 | dc1-core2 log | script,info networka firewall-loss start |
| -5.922 | dc1-dist1 log | script,info networka firewall-loss start |
| -5.620 | dc1-dist2 log | script,info networka firewall-loss start |
| -5.321 | dc1-firewall log | script,info networka firewall-loss start |
| -5.022 | dc2-core1 log | script,info networka firewall-loss start |
| -4.720 | dc2-core2 log | script,info networka firewall-loss start |
| -4.401 | dc2-dist1 log | script,info networka firewall-loss start |
| -4.105 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.781 | dc2-firewall log | script,info networka firewall-loss start |
| -3.771 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.132 | state | check before the steps: pass |
| -0.132 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.132 | state | Every switch runs with spanning tree off. pass |
| -0.132 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.132 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.132 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.132 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.123 | capture | started at dc1-service:bond0 |
| -0.123 | capture | started at dc1-traffic:bond0 |
| -0.123 | capture | started at dc1-traffic:vlan390 |
| -0.123 | capture | started at dc2-service:bond0 |
| -0.072 | capture | started at dc2-traffic:bond0 |
| -0.072 | capture | started at dc2-traffic:vlan390 |
| -0.017 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.013 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.010 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.028 | quiet window | clean |
| 4.029 | step | Baseline |
| 8.029 | step | dc1-firewall power lost |
| 8.179 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.212 | dc2-traffic-to-vrrp | 27 pings lost at one ping every 100 ms, traffic stopped for 2.704 to 2.908 s, reply absent at source |
| 8.217 | dc1-traffic-to-vrrp | 27 pings lost at one ping every 100 ms, traffic stopped for 2.708 to 2.911 s, reply absent at source |
| 8.311 | dc1-core2 log | interface,info firewall link down |
| 8.311 | dc1-core1 log | interface,info firewall link down |
| 8.364 | power | dc1-firewall guest paused and all data cables down |
| 9.099 | dc1-core1 log | interface,info ether5 link down |
| 9.231 | dc1-core2 log | interface,info ether5 link down |
| 10.954 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.415 | state | dc1-firewall power lost pass |
| 28.416 | step | dc1-firewall power restored |
| 28.419 | power | resetting and resuming the guest of dc1-firewall |
| 28.555 | dc1-core1 log | interface,info firewall link up |
| 28.555 | dc1-core2 log | interface,info firewall link up |
| 28.697 | power | dc1-firewall guest running and all data cables up |
| 29.161 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.324 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 62.600 | recovery | full lab state after power restoration of dc1-firewall: error |
| 62.622 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 62.644 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 70.380 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 86.383 | step | Power recovery |
| 89.386 | steps | last step ended |
| 92.773 | state | check after the steps: pass |
| 92.773 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 92.773 | state | Every switch runs with spanning tree off. pass |
| 92.773 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 92.773 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 92.773 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 92.773 | state | Both cables of every host are eligible in its LACP bond. pass |
| 92.773 | streams | measurement ended; captures wait for final replies |
| 93.281 | stopped | captures and streams stopped |
| 93.310 | dc1-core1 log | script,info networka firewall-loss end |
| 93.344 | dc1-core2 log | script,info networka firewall-loss end |
| 93.378 | dc1-dist1 log | script,info networka firewall-loss end |
| 93.414 | dc1-dist2 log | script,info networka firewall-loss end |
| 93.462 | dc1-firewall log | script,info networka firewall-loss end |
| 93.489 | dc2-core1 log | script,info networka firewall-loss end |
| 93.524 | dc2-core2 log | script,info networka firewall-loss end |
| 93.556 | dc2-dist1 log | script,info networka firewall-loss end |
| 93.588 | dc2-dist2 log | script,info networka firewall-loss end |
| 93.619 | dc2-firewall log | script,info networka firewall-loss end |
| 93.623 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
