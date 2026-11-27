# FAIL — site-power-loss

Cut power to the whole dc1 site at once: both cores, both distribution switches, the firewall and both hosts. dc2 must keep forwarding inside its site, and the dc2 firewall must take over the VRRP address. After power returns, dc1 must boot, rejoin the DCI and take the VRRP address back.

- After the steps, dc1-to-dc2-over-dci: 10 pings lost in total at one ping every 100 ms, longest measured stop at least 0.309572 s, 0 duplicated.
- After the steps, dc2-to-dc1-over-dci: 22 pings lost in total at one ping every 100 ms, longest measured stop at least 0.417909 s, 0 duplicated.
- After the steps, dc1-traffic-to-vrrp: 6 pings lost in total at one ping every 100 ms, longest measured stop 0.101374 to 0.308247 s, 0 duplicated.
- Step dc1 power restored is fail.
- Step Power recovery is fail.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 2 at one ping every 100 ms | 0.103068 to 41.1938 s | pass |
| dc1 power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 3 at one ping every 100 ms | 0.207816 to 41.0916 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 275 at one ping every 100 ms | 41.0301 to 41.2365 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 2 at one ping every 100 ms | 0.103785 to 38.7269 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 28 at one ping every 100 ms | 2.8047 to 3.01374 s | pass |
| dc1 power restored | dc1-traffic:bond0 → dc1-service:bond0 | 216 s | 0 at one ping every 100 ms | 0 to 40.9847 s | pass |
| dc1 power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 216 s | 156 at one ping every 100 ms | 0.517257 to 40.7813 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 216 s | 452 at one ping every 100 ms | 41.0301 to 41.2365 s | fail |
| dc1 power restored | dc1-traffic:vlan390 → 198.18.40.1 | 216 s | 173 at one ping every 100 ms | 1.55937 to 38.5224 s | fail |
| dc1 power restored | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 9 at one ping every 100 ms | 0.829714 to 1.03407 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 13 at one ping every 100 ms | 0.208847 to 0.416491 s | fail |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 14 at one ping every 100 ms | 0.209325 to 0.418419 s | fail |
| Power recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 11 at one ping every 100 ms | 0.211004 to 0.419488 s | fail |
| Power recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**dc1 power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

**Power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service** · pass

- Every data cable of these nodes lost carrier for 20.051 s, and their RouterOS guests were paused.
- dc1-core1 showed a new boot at +37.174 s.
- dc1-core2 showed a new boot at +37.672 s.
- dc1-dist1 showed a new boot at +30.360 s.
- dc1-dist2 showed a new boot at +31.102 s.
- dc1-firewall showed a new boot at +31.643 s.
- All lab checks passed at +40.715 s.

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · fail

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 10 pings lost in total at one ping every 100 ms, longest measured stop at least 0.309572 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 22 pings lost in total at one ping every 100 ms, longest measured stop at least 0.417909 s · 0 duplicates
- dc1-traffic:vlan390 → 198.18.40.1 · 6 pings lost in total at one ping every 100 ms, longest measured stop 0.101374 to 0.308247 s · 0 duplicates
- dc2-traffic:vlan390 → 198.18.40.1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.927 | test | site-power-loss started in lab large-mlag |
| -6.616 | dc1-core1 log | script,info networka site-power-loss start |
| -6.281 | dc1-core2 log | script,info networka site-power-loss start |
| -5.975 | dc1-dist1 log | script,info networka site-power-loss start |
| -5.664 | dc1-dist2 log | script,info networka site-power-loss start |
| -5.302 | dc1-firewall log | script,info networka site-power-loss start |
| -4.997 | dc2-core1 log | script,info networka site-power-loss start |
| -4.671 | dc2-core2 log | script,info networka site-power-loss start |
| -4.372 | dc2-dist1 log | script,info networka site-power-loss start |
| -4.080 | dc2-dist2 log | script,info networka site-power-loss start |
| -3.740 | dc2-firewall log | script,info networka site-power-loss start |
| -3.736 | switch log | marker 'networka site-power-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.134 | state | check before the steps: pass |
| -0.134 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.134 | state | Every switch runs with spanning tree off. pass |
| -0.134 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.134 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.134 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.134 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.124 | capture | started at dc1-service:bond0 |
| -0.124 | capture | started at dc1-traffic:bond0 |
| -0.124 | capture | started at dc1-traffic:vlan390 |
| -0.124 | capture | started at dc2-service:bond0 |
| -0.073 | capture | started at dc2-traffic:bond0 |
| -0.073 | capture | started at dc2-traffic:vlan390 |
| -0.018 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.014 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.010 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.004 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.003 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.051 | quiet window | clean |
| 4.051 | step | Baseline |
| 8.053 | step | dc1 power lost |
| 8.400 | power | withdrawing the data cables of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) and stopping the RouterOS guests |
| 8.410 | dc2-to-dc1-over-dci | 275 pings lost at one ping every 100 ms, traffic stopped for 41.03 to 41.236 s, reply absent at destination, request absent at destination |
| 8.425 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 41.092 s, request absent at destination |
| 8.519 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 38.727 s, reply absent at source |
| 8.530 | dc2-traffic-to-vrrp | 28 pings lost at one ping every 100 ms, traffic stopped for 2.805 to 3.014 s, reply absent at source |
| 8.600 | dc1-traffic-to-dc1-service | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 41.194 s, request absent at destination |
| 8.730 | dc2-core1 log | interface,info dci link down |
| 8.743 | dc2-core2 log | interface,info dci link down |
| 8.882 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests paused and all data cables down |
| 9.171 | dc2-core2 log | interface,info ether4 link down |
| 9.379 | dc2-core1 log | interface,info ether4 link down |
| 11.338 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.925 | state | dc1 power lost pass |
| 28.925 | step | dc1 power restored |
| 28.932 | power | resetting and resuming the RouterOS guests of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) |
| 29.543 | dc2-core2 log | interface,info dci link up |
| 29.631 | dc2-core1 log | interface,info dci link up |
| 29.743 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests running and all data cables up |
| 30.202 | dc2-core2 log | interface,info ether4 link up (speed 10G, full duplex) |
| 30.421 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 47.376 | dc1-traffic-to-vrrp | 16 pings lost at one ping every 100 ms, traffic stopped for 1.559 to 1.764 s, reply absent at source |
| 47.521 | dc2-traffic-to-vrrp | 9 pings lost at one ping every 100 ms, traffic stopped for 0.83 to 1.034 s, reply absent at source |
| 49.508 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.409 s, reply absent at source |
| 49.643 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.415 s, reply absent at source |
| 49.645 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.415 s, request absent at destination |
| 49.925 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.416 s, reply absent at source |
| 50.059 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.213 s, request absent at destination |
| 50.160 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 50.376 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 50.444 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.314 s, reply absent at source |
| 50.467 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.316 to 0.523 s, reply absent at source |
| 50.581 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 50.757 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.312 s, reply absent at source |
| 50.788 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.312 s, request absent at destination |
| 50.988 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 51.070 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 51.303 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.31 s, request absent at destination |
| 51.375 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 51.400 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.416 s, reply absent at source |
| 51.580 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 51.790 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 51.815 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.31 s, reply absent at source |
| 51.819 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 52.098 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 52.224 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, reply absent at source |
| 52.233 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 52.403 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.312 s, reply absent at source |
| 52.529 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 52.538 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 52.715 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 52.748 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 52.925 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 52.938 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.307 s, reply absent at source |
| 52.959 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.415 s, request absent at destination |
| 53.335 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.309 s, reply absent at source |
| 53.347 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 53.372 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.312 s, request absent at destination |
| 53.657 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 53.683 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.315 s, request absent at destination |
| 53.847 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.312 s, reply absent at source |
| 53.864 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 53.999 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 54.306 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.307 s, request absent at destination |
| 54.365 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 54.572 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 54.673 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 54.712 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 54.780 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.42 to 0.624 s, reply absent at source |
| 54.880 | dc1-traffic-to-vrrp | 5 pings lost at one ping every 100 ms, traffic stopped for 0.416 to 0.622 s, reply absent at source |
| 55.228 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 55.437 | dc2-to-dc1-over-dci | 6 pings lost at one ping every 100 ms, traffic stopped for 0.524 to 0.728 s, request absent at destination |
| 55.500 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.417 s, reply absent at source |
| 55.708 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.311 s, reply absent at source |
| 55.917 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.417 s, reply absent at source |
| 56.020 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.314 s, reply absent at source |
| 56.165 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.314 s, request absent at destination |
| 56.335 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 56.438 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.417 to 0.625 s, reply absent at source |
| 56.478 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.31 s, request absent at destination |
| 56.542 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 56.787 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 56.848 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 56.996 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.311 s, request absent at destination |
| 57.051 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 57.063 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.312 s, reply absent at source |
| 57.260 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 57.308 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 57.375 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.312 s, reply absent at source |
| 57.469 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.415 s, reply absent at source |
| 57.518 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 57.785 | dc1-to-dc2-over-dci | 6 pings lost at one ping every 100 ms, traffic stopped for 0.517 to 0.722 s, reply absent at source |
| 57.884 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.318 to 0.52 s, reply absent at source |
| 58.028 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 58.236 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.311 s, request absent at destination |
| 58.405 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.311 s, reply absent at source |
| 58.547 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 58.717 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.416 s, reply absent at source |
| 58.756 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.11 to 0.313 s, request absent at destination |
| 58.811 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.315 to 0.522 s, reply absent at source |
| 59.069 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 59.278 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 59.336 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 59.539 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.316 to 0.52 s, reply absent at source |
| 59.588 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.419 to 0.628 s, request absent at destination |
| 59.838 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 60.059 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.312 s, reply absent at source |
| 60.315 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 60.346 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.417 s, reply absent at source |
| 60.371 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 60.525 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 60.764 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 60.786 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.307 s, reply absent at source |
| 60.833 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, request absent at destination |
| 60.975 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 61.183 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.311 to 0.52 s, reply absent at source |
| 61.240 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.31 s, request absent at destination |
| 61.298 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 61.504 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 61.548 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 61.702 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 61.811 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.11 to 0.313 s, reply absent at source |
| 61.859 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.316 s, request absent at destination |
| 61.913 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.31 s, reply absent at source |
| 62.172 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 62.219 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 62.228 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.416 s, reply absent at source |
| 62.430 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.311 s, reply absent at source |
| 62.531 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 62.547 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 62.740 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.306 s, reply absent at source |
| 62.745 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.307 s, reply absent at source |
| 62.990 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 63.047 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 63.296 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.307 s, request absent at destination |
| 63.357 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 63.456 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 63.604 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 63.661 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 63.913 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.309 s, request absent at destination |
| 63.971 | dc1-traffic-to-vrrp | 4 pings lost at one ping every 100 ms, traffic stopped for 0.316 to 0.521 s, reply absent at source |
| 63.971 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 64.179 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.314 s, reply absent at source |
| 64.525 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 64.594 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.212 s, reply absent at source |
| 64.693 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 64.807 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 64.834 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.307 s, request absent at destination |
| 64.901 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 65.013 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.311 s, reply absent at source |
| 65.109 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 65.142 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 65.316 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.416 s, reply absent at source |
| 65.426 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.1 to 0.305 s, reply absent at source |
| 65.455 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.31 s, request absent at destination |
| 65.731 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 65.731 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 65.764 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.311 s, request absent at destination |
| 66.041 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.205 to 0.412 s, reply absent at source |
| 66.041 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, reply absent at source |
| 66.278 | dc2-to-dc1-over-dci | 12 pings lost at one ping every 100 ms, traffic stopped for 1.144 to 1.35 s, request absent at destination |
| 66.454 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.31 s, reply absent at source |
| 66.546 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.324 to 0.53 s, reply absent at source |
| 66.767 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.415 s, reply absent at source |
| 67.280 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 67.384 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.416 s, reply absent at source |
| 67.687 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.313 to 0.517 s, reply absent at source |
| 67.796 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 67.935 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.311 s, request absent at destination |
| 68.004 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 68.312 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 68.409 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.312 s, reply absent at source |
| 68.547 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.421 to 0.624 s, request absent at destination |
| 68.619 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 68.819 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 69.130 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.201 s, reply absent at source |
| 69.332 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 69.333 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 69.373 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 69.579 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 69.648 | recovery | full lab state after power restoration of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service: pass |
| 69.891 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.109 to 0.314 s, request absent at destination |
| 69.948 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.312 s, reply absent at source |
| 70.255 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 70.259 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 70.561 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.308 s, reply absent at source |
| 70.568 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 70.608 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.207 to 0.412 s, request absent at destination |
| 70.771 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 71.222 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 71.275 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 71.389 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.311 s, reply absent at source |
| 71.428 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 71.586 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.308 s, reply absent at source |
| 71.803 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.419 s, reply absent at source |
| 71.893 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 71.943 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.309 s, request absent at destination |
| 72.221 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 72.251 | dc2-to-dc1-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.317 to 0.52 s, request absent at destination |
| 72.305 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 72.611 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.314 s, reply absent at source |
| 72.872 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.308 s, request absent at destination |
| 72.941 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.316 to 0.52 s, reply absent at source |
| 73.180 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.312 s, request absent at destination |
| 73.492 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.213 to 0.416 s, request absent at destination |
| 73.539 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.312 s, reply absent at source |
| 73.564 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.42 s, reply absent at source |
| 73.908 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 74.115 | dc2-to-dc1-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.318 to 0.521 s, request absent at destination |
| 74.185 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 74.259 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.11 to 0.316 s, reply absent at source |
| 74.389 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 74.673 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.306 s, reply absent at source |
| 74.740 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.42 to 0.626 s, request absent at destination |
| 74.979 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 75.003 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 75.289 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 75.363 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.312 s, request absent at destination |
| 75.416 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.31 s, reply absent at source |
| 75.495 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 75.704 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 75.724 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.419 to 0.623 s, reply absent at source |
| 75.910 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 75.982 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.414 s, request absent at destination |
| 76.219 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 76.449 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 76.654 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 76.700 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 76.836 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 77.045 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 77.066 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 77.110 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.31 s, request absent at destination |
| 77.252 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.417 s, reply absent at source |
| 77.268 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.21 to 0.416 s, reply absent at source |
| 77.422 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.311 s, request absent at destination |
| 77.667 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 77.889 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 78.035 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.419 s, request absent at destination |
| 78.379 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 78.588 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.109 to 0.313 s, reply absent at source |
| 78.653 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.417 s, request absent at destination |
| 78.907 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 79.106 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.309 s, reply absent at source |
| 79.220 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.108 to 0.314 s, reply absent at source |
| 79.376 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.31 s, request absent at destination |
| 79.411 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.417 s, reply absent at source |
| 79.737 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 79.887 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 0.413 s, request absent at destination |
| 80.032 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 80.144 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 80.405 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 80.450 | dc1-to-dc2-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.415 to 0.624 s, reply absent at source |
| 80.611 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 80.823 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.221 s, request absent at destination |
| 80.954 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.306 s, reply absent at source |
| 81.037 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.202 s, request absent at destination |
| 81.260 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 81.280 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 81.448 | dc2-to-dc1-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.311 to 0.517 s, request absent at destination |
| 81.570 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.102 to 0.306 s, reply absent at source |
| 81.875 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 82.068 | dc2-to-dc1-over-dci | 9 pings lost at one ping every 100 ms, traffic stopped for 0.835 to 1.044 s, request absent at destination |
| 82.098 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 82.300 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, reply absent at source |
| 82.495 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 82.701 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.313 s, reply absent at source |
| 83.113 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.312 s, reply absent at source |
| 83.220 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 83.312 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, request absent at destination |
| 83.521 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 83.522 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.212 to 0.417 s, reply absent at source |
| 83.529 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 83.727 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.414 s, request absent at destination |
| 83.733 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.414 s, reply absent at source |
| 84.140 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, request absent at destination |
| 84.246 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 84.653 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.311 s, reply absent at source |
| 84.654 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 84.656 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 84.860 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, request absent at destination |
| 84.860 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.416 s, reply absent at source |
| 85.065 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.306 s, reply absent at source |
| 85.169 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.311 s, request absent at destination |
| 85.487 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.221 s, reply absent at source |
| 85.492 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.214 s, request absent at destination |
| 85.579 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.419 s, reply absent at source |
| 85.648 | step | Power recovery |
| 85.693 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, reply absent at source |
| 85.695 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 85.902 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.416 s, reply absent at source |
| 85.902 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.209 to 0.418 s, request absent at destination |
| 86.305 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 86.317 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 86.318 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 86.930 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 86.932 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.211 s, request absent at destination |
| 87.134 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 87.141 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.311 s, request absent at destination |
| 87.315 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.306 s, reply absent at source |
| 87.340 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 87.649 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.308 s, reply absent at source |
| 87.654 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.206 s, request absent at destination |
| 87.824 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 87.863 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.312 s, request absent at destination |
| 87.957 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 88.028 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.109 to 0.312 s, reply absent at source |
| 88.273 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.205 to 0.411 s, request absent at destination |
| 88.342 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.105 to 0.312 s, reply absent at source |
| 88.368 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 0.31 s, reply absent at source |
| 88.652 | steps | last step ended |
| 88.652 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 88.679 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.208 s, reply absent at source |
| 88.684 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 89.195 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 89.399 | dc1-to-dc2-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.205 s, reply absent at source |
| 89.510 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.211 to 0.414 s, request absent at destination |
| 89.923 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.107 to 0.314 s, request absent at destination |
| 89.976 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.203 s, reply absent at source |
| 90.314 | dc1-to-dc2-over-dci | 4 pings lost at one ping every 100 ms, traffic stopped for 0.31 to 0.517 s, reply absent at source |
| 90.341 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.106 to 0.312 s, request absent at destination |
| 90.655 | dc2-to-dc1-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.217 to 0.424 s, request absent at destination |
| 90.891 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, reply absent at source |
| 91.078 | dc2-to-dc1-over-dci | 5 pings lost at one ping every 100 ms, traffic stopped for 0.418 to 0.624 s, request absent at destination |
| 91.202 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.204 s, reply absent at source |
| 91.342 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.109 to 0.312 s, reply absent at source |
| 91.610 | dc1-traffic-to-vrrp | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.308 s, reply absent at source |
| 91.700 | dc2-to-dc1-over-dci | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, request absent at destination |
| 91.907 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for 0.101 to 0.305 s, request absent at destination |
| 92.261 | dc1-to-dc2-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for at least 0.107 s, reply absent at source |
| 92.314 | dc2-to-dc1-over-dci | 2 pings lost at one ping every 100 ms, traffic stopped for at least 0.101 s, request absent at destination |
| 92.414 | state | check after the steps: pass |
| 92.414 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 92.414 | state | Every switch runs with spanning tree off. pass |
| 92.414 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 92.414 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 92.414 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 92.414 | state | Both cables of every host are eligible in its LACP bond. pass |
| 92.414 | streams | measurement ended; captures wait for final replies |
| 92.924 | stopped | captures and streams stopped |
| 92.963 | dc1-core1 log | script,info networka site-power-loss end |
| 93.007 | dc1-core2 log | script,info networka site-power-loss end |
| 93.060 | dc1-dist1 log | script,info networka site-power-loss end |
| 93.109 | dc1-dist2 log | script,info networka site-power-loss end |
| 93.172 | dc1-firewall log | script,info networka site-power-loss end |
| 93.205 | dc2-core1 log | script,info networka site-power-loss end |
| 93.242 | dc2-core2 log | script,info networka site-power-loss end |
| 93.290 | dc2-dist1 log | script,info networka site-power-loss end |
| 93.334 | dc2-dist2 log | script,info networka site-power-loss end |
| 93.392 | dc2-firewall log | script,info networka site-power-loss end |
| 93.401 | switch log | marker 'networka site-power-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
