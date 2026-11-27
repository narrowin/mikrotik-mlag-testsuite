# PASS — site-power-loss

Cut power to the whole dc1 site at once: both cores, both distribution switches, the firewall and both hosts. dc2 must keep forwarding inside its site, and the dc2 firewall must take over the VRRP address. After power returns, dc1 must boot, rejoin the DCI and take the VRRP address back.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 2 at one ping every 100 ms | 0.104896 to 38.6952 s | pass |
| dc1 power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 3 at one ping every 100 ms | 0.211752 to 39.7586 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 202 at one ping every 100 ms | 20.9685 to 39.8504 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 2 at one ping every 100 ms | 0.102885 to 39.6564 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 31 at one ping every 100 ms | 3.12148 to 3.32914 s | pass |
| dc1 power restored | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 0 at one ping every 100 ms | 0 to 38.485 s | pass |
| dc1 power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 0 at one ping every 100 ms | 0 to 39.4461 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 202 at one ping every 100 ms | 20.9685 to 39.8504 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 0 at one ping every 100 ms | 0 to 39.4521 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**dc1 power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

**Power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service** · pass

- Every data cable of these nodes lost carrier for 20.047 s, and their RouterOS guests were paused.
- dc1-core1 showed a new boot at +48.038 s.
- dc1-core2 showed a new boot at +48.483 s.
- dc1-dist1 showed a new boot at +41.615 s.
- dc1-dist2 showed a new boot at +42.105 s.
- dc1-firewall showed a new boot at +42.591 s.
- All lab checks passed at +51.109 s.

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
| -3.044 | test | site-power-loss started in lab large-mlag |
| -3.014 | dc1-core1 log | script,info networka site-power-loss start |
| -2.974 | dc1-core2 log | script,info networka site-power-loss start |
| -2.923 | dc1-dist1 log | script,info networka site-power-loss start |
| -2.883 | dc1-dist2 log | script,info networka site-power-loss start |
| -2.828 | dc1-firewall log | script,info networka site-power-loss start |
| -2.787 | dc2-core1 log | script,info networka site-power-loss start |
| -2.757 | dc2-core2 log | script,info networka site-power-loss start |
| -2.714 | dc2-dist1 log | script,info networka site-power-loss start |
| -2.680 | dc2-dist2 log | script,info networka site-power-loss start |
| -2.634 | dc2-firewall log | script,info networka site-power-loss start |
| -2.630 | switch log | marker 'networka site-power-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.139 | state | check before the steps: pass |
| -0.139 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.139 | state | Every switch runs with spanning tree off. pass |
| -0.139 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.139 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.139 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.139 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.130 | capture | started at dc1-service:bond0 |
| -0.130 | capture | started at dc1-traffic:bond0 |
| -0.130 | capture | started at dc1-traffic:vlan390 |
| -0.130 | capture | started at dc2-service:bond0 |
| -0.073 | capture | started at dc2-traffic:bond0 |
| -0.073 | capture | started at dc2-traffic:vlan390 |
| -0.017 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.012 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.009 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.002 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.011 | quiet window | clean |
| 4.011 | step | Baseline |
| 8.013 | step | dc1 power lost |
| 8.315 | power | withdrawing the data cables of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) and stopping the RouterOS guests |
| 8.340 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 39.759 s, request absent at destination |
| 8.343 | dc2-to-dc1-over-dci | 202 pings lost at one ping every 100 ms, traffic stopped for 20.968 to 39.85 s, request absent at destination |
| 8.366 | dc2-traffic-to-vrrp | 31 pings lost at one ping every 100 ms, traffic stopped for 3.121 to 3.329 s, reply absent at source |
| 8.441 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 39.656 s, reply absent at source |
| 8.448 | dc1-traffic-to-dc1-service | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 38.695 s, request absent at destination |
| 8.578 | dc2-core1 log | interface,info ether4 link down |
| 8.578 | dc2-core1 log | interface,info dci link down |
| 8.623 | dc2-core2 log | interface,info dci link down |
| 8.689 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests paused and all data cables down |
| 9.432 | dc2-core2 log | interface,info ether4 link down |
| 11.520 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.732 | state | dc1 power lost pass |
| 28.732 | step | dc1 power restored |
| 28.736 | power | resetting and resuming the RouterOS guests of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) |
| 29.302 | dc2-core2 log | interface,info dci link up |
| 29.373 | dc2-core1 log | interface,info dci link up |
| 29.462 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests running and all data cables up |
| 29.480 | dc2-core2 log | interface,info ether4 link up (speed 10G, full duplex) |
| 29.627 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 62.209 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 62.217 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 79.844 | recovery | full lab state after power restoration of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service: pass |
| 95.848 | step | Power recovery |
| 98.851 | steps | last step ended |
| 102.133 | state | check after the steps: pass |
| 102.133 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 102.133 | state | Every switch runs with spanning tree off. pass |
| 102.133 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 102.133 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 102.133 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 102.133 | state | Both cables of every host are eligible in its LACP bond. pass |
| 102.134 | streams | measurement ended; captures wait for final replies |
| 102.640 | stopped | captures and streams stopped |
| 102.672 | dc1-core1 log | script,info networka site-power-loss end |
| 102.706 | dc1-core2 log | script,info networka site-power-loss end |
| 102.739 | dc1-dist1 log | script,info networka site-power-loss end |
| 102.768 | dc1-dist2 log | script,info networka site-power-loss end |
| 102.802 | dc1-firewall log | script,info networka site-power-loss end |
| 102.832 | dc2-core1 log | script,info networka site-power-loss end |
| 102.867 | dc2-core2 log | script,info networka site-power-loss end |
| 102.899 | dc2-dist1 log | script,info networka site-power-loss end |
| 102.955 | dc2-dist2 log | script,info networka site-power-loss end |
| 102.996 | dc2-firewall log | script,info networka site-power-loss end |
| 103.001 | switch log | marker 'networka site-power-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
