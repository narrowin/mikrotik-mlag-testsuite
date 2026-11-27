# PASS — site-power-loss

Cut power to the whole dc1 site at once: both cores, both distribution switches, the firewall and both hosts. dc2 must keep forwarding inside its site, and the dc2 firewall must take over the VRRP address. After power returns, dc1 must boot, rejoin the DCI and take the VRRP address back.

## Forwarding and failover during power loss

**dc1 power lost**

Expected: The dc2 cores see both DCI members go down, dc2 keeps forwarding its site VLAN and the dc2 firewall becomes VRRP master.

| Stream | Measured outage | Limit | Lost pings | Verdict |
| --- | --- | --- | --- | --- |
| dc2-traffic-to-dc2-service | 0 s | 0 s | 0 | pass |
| dc2-traffic-to-vrrp | 3.02886 to 3.23489 s | 4 s | 30 | pass |

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
| dc1 power lost | dc2-traffic:vlan390 → 198.18.40.1 | 4 s | 30 at one ping every 100 ms | 3.02886 to 3.23489 s | pass |
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
| dc1 power lost | dc1-traffic:bond0 → dc1-service:bond0 | Host power loss | 216 s | 2 at one ping every 100 ms | 0.104128 to 40.6992 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | Host power loss | 216 s | 3 at one ping every 100 ms | 0.219082 to 40.996 s | pass |
| dc1 power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | Host power loss | 216 s | 393 at one ping every 100 ms | 40.9326 to 41.1381 s | pass |
| dc1 power lost | dc1-traffic:vlan390 → 198.18.40.1 | Host power loss | 216 s | 3 at one ping every 100 ms | 0.207691 to 42.8146 s | pass |
| dc1 power restored | dc1-traffic:bond0 → dc1-service:bond0 | Host power loss | 216 s | 2 at one ping every 100 ms | 0 to 40.4914 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | Host power loss | 216 s | 0 at one ping every 100 ms | 0 to 40.6757 s | pass |
| dc1 power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | Host power loss | 216 s | 393 at one ping every 100 ms | 40.9326 to 41.1381 s | pass |
| dc1 power restored | dc1-traffic:vlan390 → 198.18.40.1 | Host power loss | 216 s | 0 at one ping every 100 ms | 0 to 42.5059 s | pass |

## State checks

**dc1 power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

## Restart and rejoin after power returns

Boot and rejoin times start at power-on dispatch.

**Power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service** · pass

- Every data cable of these nodes lost carrier for 20.060 s, and their RouterOS guests were paused.
- dc1-core1 showed a new boot at +46.846 s.
- dc1-core2 showed a new boot at +47.323 s.
- dc1-dist1 showed a new boot at +47.820 s.
- dc1-dist2 showed a new boot at +40.833 s.
- dc1-firewall showed a new boot at +41.368 s.
- All lab checks passed at +50.623 s after power-on dispatch, against a 180 s recovery deadline.

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
| -6.865 | test | site-power-loss started in lab large-mlag |
| -6.547 | dc1-core1 log | script,info networka site-power-loss start |
| -6.249 | dc1-core2 log | script,info networka site-power-loss start |
| -5.942 | dc1-dist1 log | script,info networka site-power-loss start |
| -5.625 | dc1-dist2 log | script,info networka site-power-loss start |
| -5.308 | dc1-firewall log | script,info networka site-power-loss start |
| -5.015 | dc2-core1 log | script,info networka site-power-loss start |
| -4.721 | dc2-core2 log | script,info networka site-power-loss start |
| -4.426 | dc2-dist1 log | script,info networka site-power-loss start |
| -4.133 | dc2-dist2 log | script,info networka site-power-loss start |
| -3.836 | dc2-firewall log | script,info networka site-power-loss start |
| -3.834 | switch log | marker 'networka site-power-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.161 | state | check before the steps: pass |
| -0.161 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.161 | state | Every switch runs with spanning tree off. pass |
| -0.161 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.161 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.161 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.161 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.141 | capture | started at dc1-service:bond0 |
| -0.140 | capture | started at dc1-traffic:bond0 |
| -0.139 | capture | started at dc1-traffic:vlan390 |
| -0.087 | capture | started at dc2-service:bond0 |
| -0.087 | capture | started at dc2-traffic:bond0 |
| -0.087 | capture | started at dc2-traffic:vlan390 |
| -0.030 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.026 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.019 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.012 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| -0.010 | dc1-traffic-to-vrrp | started from dc1-traffic:vlan390 to 198.18.40.1 |
| -0.008 | dc2-traffic-to-vrrp | started from dc2-traffic:vlan390 to 198.18.40.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.150 | quiet window | clean |
| 4.151 | step | Baseline |
| 8.154 | step | dc1 power lost |
| 8.543 | dc2-to-dc1-over-dci | 393 pings lost at one ping every 100 ms, traffic stopped for 40.933 to 41.138 s, reply absent at destination, reply absent at source, request absent at destination |
| 8.544 | power | taking down the data cables of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) and stopping the RouterOS guests |
| 8.623 | dc2-traffic-to-vrrp | 30 pings lost at one ping every 100 ms, traffic stopped for 3.029 to 3.235 s, reply absent at source |
| 8.626 | dc1-to-dc2-over-dci | 3 pings lost at one ping every 100 ms, traffic stopped for 0.219 to 40.996 s, request absent at destination |
| 8.637 | dc1-traffic-to-vrrp | 3 pings lost at one ping every 100 ms, traffic stopped for 0.208 to 42.815 s, reply absent at source |
| 8.717 | dc1-traffic-to-dc1-service | 2 pings lost at one ping every 100 ms, traffic stopped for 0.104 to 40.699 s, request absent at destination |
| 8.865 | dc2-core2 log | interface,info dci link down |
| 8.881 | dc2-core1 log | interface,info dci link down |
| 8.971 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests paused and all data cables down |
| 8.987 | dc2-core1 log | interface,info ether4 link down |
| 9.431 | dc2-core2 log | interface,info ether4 link down |
| 11.732 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 29.028 | state | dc1 power lost pass |
| 29.028 | step | dc1 power restored |
| 29.031 | power | resetting and resuming the RouterOS guests of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) |
| 29.654 | dc2-core2 log | interface,info dci link up |
| 29.672 | dc2-core1 log | interface,info dci link up |
| 29.788 | power | dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service (dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service) RouterOS guests running and all data cables up |
| 30.037 | dc2-core1 log | interface,info ether4 link up (speed 10G, full duplex) |
| 30.443 | dc2-core2 log | interface,info ether4 link up (speed 10G, full duplex) |
| 49.170 | dc1-core2 log | interface,info dci link down |
| 49.186 | dc1-core2 log | interface,info dci link up |
| 49.483 | dc1-dist2 log | interface,info traffic link down |
| 49.498 | dc1-dist2 log | interface,info traffic link up |
| 49.518 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.21 s, request absent at destination |
| 49.561 | dc1-dist2 log | interface,info service link down |
| 49.572 | dc1-dist2 log | interface,info service link up |
| 50.351 | dc1-traffic-to-dc1-service | 1 ping lost at one ping every 100 ms, traffic stopped for 0 to 0.207 s, reply absent at source |
| 63.178 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 63.189 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 79.654 | recovery | full lab state after the power loss of dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc1-traffic, dc1-service: pass |
| 95.655 | step | Power recovery |
| 98.657 | steps | last step ended |
| 102.010 | state | check after the steps: pass |
| 102.010 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 102.010 | state | Every switch runs with spanning tree off. pass |
| 102.010 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 102.010 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 102.010 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 102.010 | state | Both cables of every host are eligible in its LACP bond. pass |
| 102.010 | streams | measurement ended; captures wait for final replies |
| 102.520 | stopped | captures and streams stopped |
| 102.556 | dc1-core1 log | script,info networka site-power-loss end |
| 102.592 | dc1-core2 log | script,info networka site-power-loss end |
| 102.624 | dc1-dist1 log | script,info networka site-power-loss end |
| 102.657 | dc1-dist2 log | script,info networka site-power-loss end |
| 102.710 | dc1-firewall log | script,info networka site-power-loss end |
| 102.752 | dc2-core1 log | script,info networka site-power-loss end |
| 102.791 | dc2-core2 log | script,info networka site-power-loss end |
| 102.835 | dc2-dist1 log | script,info networka site-power-loss end |
| 102.887 | dc2-dist2 log | script,info networka site-power-loss end |
| 102.933 | dc2-firewall log | script,info networka site-power-loss end |
| 102.939 | switch log | marker 'networka site-power-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
