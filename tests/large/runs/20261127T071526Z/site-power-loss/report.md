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
| dc1 power lost | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 1 at one ping every 100 ms | 0 to 37.5531 s | pass |
| dc1 power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 2 at one ping every 100 ms | 0.105869 to 47.8096 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 314 at one ping every 100 ms | 47.5721 to 47.7825 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 2 at one ping every 100 ms | 0.103602 to 39.6754 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 28 at one ping every 100 ms | 2.80852 to 3.01625 s | pass |
| dc1 power restored | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 1 at one ping every 100 ms | 0 to 37.451 s | pass |
| dc1 power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 0 at one ping every 100 ms | 0 to 47.6019 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 314 at one ping every 100 ms | 47.5721 to 47.7825 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 0 at one ping every 100 ms | 0 to 39.4704 s | pass |
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
- dc1-core1 showed a new boot at +34.965 s.
- dc1-core2 showed a new boot at +35.419 s.
- dc1-dist1 showed a new boot at +28.525 s.
- dc1-dist2 showed a new boot at +28.993 s.
- dc1-firewall showed a new boot at +29.504 s.
- All lab checks passed at +38.066 s.

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
| -3.096 | test | site-power-loss started in lab large-mlag |
| -3.070 | dc1-core1 log | script,info networka site-power-loss start |
| -3.040 | dc1-core2 log | script,info networka site-power-loss start |
| -2.998 | dc1-dist1 log | script,info networka site-power-loss start |
| -2.963 | dc1-dist2 log | script,info networka site-power-loss start |
| -2.927 | dc1-firewall log | script,info networka site-power-loss start |
| -2.878 | dc2-core1 log | script,info networka site-power-loss start |
| -2.841 | dc2-core2 log | script,info networka site-power-loss start |
| -2.804 | dc2-dist1 log | script,info networka site-power-loss start |
| -2.755 | dc2-dist2 log | script,info networka site-power-loss start |
| -2.707 | dc2-firewall log | script,info networka site-power-loss start |
| -2.703 | switch log | marker 'networka site-power-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.136 | state | check before the steps: pass |
| -0.136 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.136 | state | Every switch runs with spanning tree off. pass |
| -0.136 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.136 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.136 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.136 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.125 | capture | started at dc1-service:bond0 |
| -0.125 | capture | started at dc1-traffic:bond0 |
| -0.125 | capture | started at dc1-traffic:vlan390 |
| -0.125 | capture | started at dc2-service:bond0 |
| -0.073 | capture | started at dc2-traffic:bond0 |
| -0.073 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.011 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.009 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.005 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 3.988 | quiet window | clean |
| 3.988 | step | Baseline |
| 7.991 | step | dc1 power lost |
| 8.285 | power | withdrawing the data cables of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) and stopping the RouterOS guests |
| 8.335 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 47.81 s, request absent at destination |
| 8.337 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 39.675 s, reply absent at source |
| 8.360 | dc2-traffic-to-vrrp | 28 pings lost at one ping every 100 ms, traffic stopped for 2.809 to 3.016 s, reply absent at source |
| 8.367 | dc2-to-dc1-over-dci | 314 pings lost at one ping every 100 ms, traffic stopped for 47.572 to 47.783 s, request absent at destination |
| 8.433 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 37.553 s, request absent at destination |
| 8.532 | dc2-core1 log | interface,info dci link down |
| 8.551 | dc2-core2 log | interface,info dci link down |
| 8.628 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests paused and all data cables down |
| 9.099 | dc2-core1 log | interface,info ether4 link down |
| 9.400 | dc2-core2 log | interface,info ether4 link down |
| 11.215 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.672 | state | dc1 power lost pass |
| 28.672 | step | dc1 power restored |
| 28.675 | power | resetting and resuming the RouterOS guests of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) |
| 29.214 | dc2-core1 log | interface,info dci link up |
| 29.231 | dc2-core2 log | interface,info dci link up |
| 29.334 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests running and all data cables up |
| 29.451 | dc2-core2 log | interface,info ether4 link up (speed 10G, full duplex) |
| 30.157 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 47.241 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.214 s, request absent at destination |
| 55.146 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 55.155 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 66.741 | recovery | full lab state after power restoration of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service: pass |
| 82.741 | step | Power recovery |
| 85.743 | steps | last step ended |
| 88.924 | state | check after the steps: pass |
| 88.924 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 88.924 | state | Every switch runs with spanning tree off. pass |
| 88.924 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 88.924 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 88.924 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 88.924 | state | Both cables of every host are eligible in its LACP bond. pass |
| 88.924 | streams | measurement ended; captures wait for final replies |
| 89.435 | stopped | captures and streams stopped |
| 89.467 | dc1-core1 log | script,info networka site-power-loss end |
| 89.497 | dc1-core2 log | script,info networka site-power-loss end |
| 89.529 | dc1-dist1 log | script,info networka site-power-loss end |
| 89.562 | dc1-dist2 log | script,info networka site-power-loss end |
| 89.604 | dc1-firewall log | script,info networka site-power-loss end |
| 89.639 | dc2-core1 log | script,info networka site-power-loss end |
| 89.677 | dc2-core2 log | script,info networka site-power-loss end |
| 89.708 | dc2-dist1 log | script,info networka site-power-loss end |
| 89.737 | dc2-dist2 log | script,info networka site-power-loss end |
| 89.773 | dc2-firewall log | script,info networka site-power-loss end |
| 89.776 | switch log | marker 'networka site-power-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
