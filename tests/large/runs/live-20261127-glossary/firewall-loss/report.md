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
| dc1-firewall power lost | dc1-traffic:vlan390 → 198.18.40.1 | 4 s | 34 at one ping every 100 ms | 3.44062 to 3.64859 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 34 at one ping every 100 ms | 3.45402 to 3.65775 s | pass |
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

- Data cables lost carrier and the guest was paused for 20.046 s.
- The new boot was detected at +28.392 s, with all lab checks passing at +31.125 s.

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
| -6.729 | test | firewall-loss started in lab large-mlag |
| -6.423 | dc1-core1 log | script,info networka firewall-loss start |
| -6.128 | dc1-core2 log | script,info networka firewall-loss start |
| -5.700 | dc1-dist1 log | script,info networka firewall-loss start |
| -5.398 | dc1-dist2 log | script,info networka firewall-loss start |
| -5.105 | dc1-firewall log | script,info networka firewall-loss start |
| -4.798 | dc2-core1 log | script,info networka firewall-loss start |
| -4.513 | dc2-core2 log | script,info networka firewall-loss start |
| -4.215 | dc2-dist1 log | script,info networka firewall-loss start |
| -3.911 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.617 | dc2-firewall log | script,info networka firewall-loss start |
| -3.613 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.135 | state | check before the steps: pass |
| -0.135 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.135 | state | Every switch runs with spanning tree off. pass |
| -0.135 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.135 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.135 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.135 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.125 | capture | started at dc1-service:bond0 |
| -0.125 | capture | started at dc1-traffic:bond0 |
| -0.124 | capture | started at dc1-traffic:vlan390 |
| -0.124 | capture | started at dc2-service:bond0 |
| -0.073 | capture | started at dc2-traffic:bond0 |
| -0.073 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.015 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.011 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.008 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.006 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.005 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.050 | quiet window | clean |
| 4.050 | step | Baseline |
| 8.053 | step | dc1-firewall power lost |
| 8.188 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.217 | dc2-traffic-to-vrrp | 34 pings lost at one ping every 100 ms, traffic stopped for 3.454 to 3.658 s, reply absent at source |
| 8.230 | dc1-traffic-to-vrrp | 34 pings lost at one ping every 100 ms, traffic stopped for 3.441 to 3.649 s, reply absent at source |
| 8.246 | dc1-core1 log | interface,info firewall link down |
| 8.329 | power | dc1-firewall guest paused and all data cables down |
| 8.342 | dc1-core2 log | interface,info firewall link down |
| 8.448 | dc1-core2 log | interface,info ether5 link down |
| 9.117 | dc1-core1 log | interface,info ether5 link down |
| 11.725 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.371 | state | dc1-firewall power lost pass |
| 28.371 | step | dc1-firewall power restored |
| 28.375 | power | resetting and resuming the guest of dc1-firewall |
| 28.513 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 28.579 | power | dc1-firewall guest running and all data cables up |
| 28.584 | dc1-core2 log | interface,info firewall link up |
| 28.597 | dc1-core1 log | interface,info firewall link up |
| 29.164 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 54.954 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 54.962 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 59.499 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 75.502 | step | Power recovery |
| 78.505 | steps | last step ended |
| 81.797 | state | check after the steps: pass |
| 81.797 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 81.797 | state | Every switch runs with spanning tree off. pass |
| 81.797 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 81.797 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 81.797 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 81.797 | state | Both cables of every host are eligible in its LACP bond. pass |
| 81.797 | streams | measurement ended; captures wait for final replies |
| 82.351 | stopped | captures and streams stopped |
| 82.381 | dc1-core1 log | script,info networka firewall-loss end |
| 82.419 | dc1-core2 log | script,info networka firewall-loss end |
| 82.453 | dc1-dist1 log | script,info networka firewall-loss end |
| 82.487 | dc1-dist2 log | script,info networka firewall-loss end |
| 82.590 | dc1-firewall log | script,info networka firewall-loss end |
| 82.628 | dc2-core1 log | script,info networka firewall-loss end |
| 82.659 | dc2-core2 log | script,info networka firewall-loss end |
| 82.716 | dc2-dist1 log | script,info networka firewall-loss end |
| 82.746 | dc2-dist2 log | script,info networka firewall-loss end |
| 82.775 | dc2-firewall log | script,info networka firewall-loss end |
| 82.779 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
