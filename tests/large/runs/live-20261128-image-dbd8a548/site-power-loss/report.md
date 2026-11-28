# PASS — site-power-loss

Cut power to the whole dc1 site at once: both cores, both distribution switches, the firewall and both hosts. dc2 must keep forwarding inside its site, and the dc2 firewall must take over the VRRP address. After power returns, dc1 must boot, rejoin the DCI and take the VRRP address back.

## Forwarding and failover during power loss

**dc1 power lost**

Expected: The dc2 cores see both DCI members go down, dc2 keeps forwarding its site VLAN and the dc2 firewall becomes VRRP master.

| Stream | Measured outage | Limit | Lost pings | Verdict |
| --- | --- | --- | --- | --- |
| dc2-traffic-to-dc2-service | 0 s | 0 s | 0 | pass |
| dc2-traffic-to-vrrp | 3.50964 to 3.71585 s | 4 s | 34 | pass |

## Traffic details

| Step | Stream | Limit | Total lost pings | Longest measured outage | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 34 at one ping every 100 ms | 3.50964 to 3.71585 s | pass |
| dc1 power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → 198.18.40.1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

## Intentional interruptions

These measured interruptions include deliberate host silence or power loss at a host. The combined interruption limits remain in force; they are not failover limits for a path that should stay available. Recovery is checked separately below.

| Step | Stream | Cause | Combined limit | Total lost pings | Longest measured interruption | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| dc1 power lost | dc1-traffic:bond0 → dc1-service:bond0 | Host power loss | 216 s | 231 at one ping every 100 ms | 44.915 to 45.1211 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | Host power loss | 216 s | 235 at one ping every 100 ms | 45.3894 to 45.5957 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | Host power loss | 216 s | 435 at one ping every 100 ms | 45.3582 to 45.5636 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → 198.18.40.1 | Host power loss | 216 s | 242 at one ping every 100 ms | 46.1061 to 46.3085 s | pass |
| dc1 power restored | dc1-traffic:bond0 → dc1-service:bond0 | Host power loss | 216 s | 233 at one ping every 100 ms | 44.915 to 45.1211 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | Host power loss | 216 s | 235 at one ping every 100 ms | 45.3894 to 45.5957 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | Host power loss | 216 s | 435 at one ping every 100 ms | 45.3582 to 45.5636 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → 198.18.40.1 | Host power loss | 216 s | 243 at one ping every 100 ms | 46.1061 to 46.3085 s | pass |

## State checks

**dc1 power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

## Restart and rejoin after power returns

Boot and rejoin times start at power-on dispatch.

**Power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service** · pass

- Every data cable of these nodes lost carrier for 20.096 s, and their RouterOS guests were paused.
- dc1-core1 showed a new boot at +47.389 s.
- dc1-core2 showed a new boot at +47.913 s.
- dc1-dist1 showed a new boot at +48.412 s.
- dc1-dist2 showed a new boot at +49.034 s.
- dc1-firewall showed a new boot at +41.883 s.
- All lab checks passed at +52.673 s after power-on dispatch, against a 180 s recovery deadline.

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
| -7.277 | test | site-power-loss started in lab large-mlag |
| -6.950 | dc1-core1 log | script,info networka site-power-loss start |
| -6.586 | dc1-core2 log | script,info networka site-power-loss start |
| -6.194 | dc1-dist1 log | script,info networka site-power-loss start |
| -5.863 | dc1-dist2 log | script,info networka site-power-loss start |
| -5.494 | dc1-firewall log | script,info networka site-power-loss start |
| -5.157 | dc2-core1 log | script,info networka site-power-loss start |
| -4.802 | dc2-core2 log | script,info networka site-power-loss start |
| -4.450 | dc2-dist1 log | script,info networka site-power-loss start |
| -4.111 | dc2-dist2 log | script,info networka site-power-loss start |
| -3.803 | dc2-firewall log | script,info networka site-power-loss start |
| -3.797 | switch log | marker 'networka site-power-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.128 | state | check before the steps: pass |
| -0.128 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.128 | state | Every switch runs with spanning tree off. pass |
| -0.128 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.128 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.128 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.128 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.121 | capture | started at dc1-service:bond0 |
| -0.120 | capture | started at dc1-traffic:bond0 |
| -0.120 | capture | started at dc1-traffic:vlan390 |
| -0.069 | capture | started at dc2-service:bond0 |
| -0.068 | capture | started at dc2-traffic:bond0 |
| -0.068 | capture | started at dc2-traffic:vlan390 |
| -0.015 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.012 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.009 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.006 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.005 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.004 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.123 | quiet window | clean |
| 4.124 | step | Baseline |
| 8.124 | step | dc1 power lost |
| 8.643 | power | taking down the data cables of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) and stopping the RouterOS guests |
| 8.664 | dc2-to-dc1-over-dci | 435 pings lost at one ping every 100 ms, traffic stopped for 45.358 to 45.564 s, request absent at destination |
| 8.712 | dc2-traffic-to-vrrp | 34 pings lost at one ping every 100 ms, traffic stopped for 3.51 to 3.716 s, reply absent at source |
| 8.713 | dc1-to-dc2-over-dci | 235 pings lost at one ping every 100 ms, traffic stopped for 45.389 to 45.596 s, request absent at destination |
| 8.718 | dc1-traffic-to-vrrp | 242 pings lost at one ping every 100 ms, traffic stopped for 46.106 to 46.309 s, reply absent at source |
| 8.884 | dc1-traffic-to-dc1-service | 231 pings lost at one ping every 100 ms, traffic stopped for 44.915 to 45.121 s, request absent at destination |
| 8.943 | dc2-core2 log | interface,info dci link down |
| 9.006 | dc2-core1 log | interface,info dci link down |
| 9.107 | dc2-core2 log | interface,info ether4 link down |
| 9.140 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests paused and all data cables down |
| 9.764 | dc2-core1 log | interface,info ether4 link down |
| 12.222 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 29.227 | state | dc1 power lost pass |
| 29.228 | step | dc1 power restored |
| 29.236 | power | resetting and resuming the RouterOS guests of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) |
| 29.944 | dc2-core2 log | interface,info dci link up |
| 30.034 | dc2-core1 log | interface,info dci link up |
| 30.153 | dc2-core2 log | interface,info ether4 link up (speed 10G, full duplex) |
| 30.346 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests running and all data cables up |
| 30.848 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 54.311 | dc1-traffic-to-dc1-service | 2 pings lost at one ping every 100 ms, traffic stopped for 0.103 to 0.318 s, reply absent at source |
| 62.109 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 62.128 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 62.131 | dc1-traffic-to-vrrp | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.209 s, reply absent at source |
| 81.910 | recovery | full lab state after the power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service: pass |
| 97.913 | step | Power recovery |
| 100.922 | steps | last step ended |
| 105.349 | state | check after the steps: pass |
| 105.349 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 105.349 | state | Every switch runs with spanning tree off. pass |
| 105.349 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 105.349 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 105.349 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 105.349 | state | Both cables of every host are eligible in its LACP bond. pass |
| 105.349 | streams | measurement ended; captures wait for final replies |
| 105.870 | stopped | captures and streams stopped |
| 105.916 | dc1-core1 log | script,info networka site-power-loss end |
| 105.985 | dc1-core2 log | script,info networka site-power-loss end |
| 106.073 | dc1-dist1 log | script,info networka site-power-loss end |
| 106.265 | dc1-dist2 log | script,info networka site-power-loss end |
| 106.335 | dc1-firewall log | script,info networka site-power-loss end |
| 106.388 | dc2-core1 log | script,info networka site-power-loss end |
| 106.467 | dc2-core2 log | script,info networka site-power-loss end |
| 106.533 | dc2-dist1 log | script,info networka site-power-loss end |
| 106.601 | dc2-dist2 log | script,info networka site-power-loss end |
| 106.649 | dc2-firewall log | script,info networka site-power-loss end |
| 106.664 | switch log | marker 'networka site-power-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
