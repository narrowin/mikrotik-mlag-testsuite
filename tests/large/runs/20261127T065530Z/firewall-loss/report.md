# PASS — firewall-loss

Withdraw all data links of the dc1 firewall and pause its guest before a cold reset. The dc2 firewall must take over the VRRP address, and dc1 must take it back after power returns. No stream crosses a firewall, so every stream must continue.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Baseline | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Baseline | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power lost | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| dc1-firewall power restored | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:bond0 → dc1-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:bond0 → dc2-service:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc1-traffic:vlan390 → dc2-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Power recovery | dc2-traffic:vlan390 → dc1-traffic:vlan390 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**dc1-firewall power lost state** · pass
- The dc2 firewall owns the VRRP address. · pass

**Power loss of dc1-firewall** · pass

- Data cables lost carrier and the guest was paused for 20.051 s.
- The new boot was detected at +30.847 s, with all lab checks passing at +33.501 s.

**quiet window** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- dc1-traffic:bond0 → dc1-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:bond0 → dc2-service:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc1-traffic:vlan390 → dc2-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- dc2-traffic:vlan390 → dc1-traffic:vlan390 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -6.653 | test | firewall-loss started in lab large-mlag |
| -6.329 | dc1-core1 log | script,info networka firewall-loss start |
| -6.027 | dc1-core2 log | script,info networka firewall-loss start |
| -5.728 | dc1-dist1 log | script,info networka firewall-loss start |
| -5.449 | dc1-dist2 log | script,info networka firewall-loss start |
| -5.139 | dc1-firewall log | script,info networka firewall-loss start |
| -4.844 | dc2-core1 log | script,info networka firewall-loss start |
| -4.549 | dc2-core2 log | script,info networka firewall-loss start |
| -4.262 | dc2-dist1 log | script,info networka firewall-loss start |
| -3.958 | dc2-dist2 log | script,info networka firewall-loss start |
| -3.666 | dc2-firewall log | script,info networka firewall-loss start |
| -3.661 | switch log | marker 'networka firewall-loss start' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
| -0.124 | state | check before the steps: pass |
| -0.124 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| -0.124 | state | Every switch runs with spanning tree off. pass |
| -0.124 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| -0.124 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| -0.124 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| -0.124 | state | Both cables of every host are eligible in its LACP bond. pass |
| -0.115 | capture | started at dc1-service:bond0 |
| -0.115 | capture | started at dc1-traffic:bond0 |
| -0.115 | capture | started at dc1-traffic:vlan390 |
| -0.065 | capture | started at dc2-service:bond0 |
| -0.064 | capture | started at dc2-traffic:bond0 |
| -0.064 | capture | started at dc2-traffic:vlan390 |
| -0.009 | dc1-traffic-to-dc1-service | started from dc1-traffic:bond0 to dc1-service:bond0 at 10.110.0.17 |
| -0.007 | dc2-traffic-to-dc2-service | started from dc2-traffic:bond0 to dc2-service:bond0 at 10.120.0.27 |
| -0.004 | dc1-to-dc2-over-dci | started from dc1-traffic:vlan390 to dc2-traffic:vlan390 at 198.18.40.26 |
| -0.002 | dc2-to-dc1-over-dci | started from dc2-traffic:vlan390 to dc1-traffic:vlan390 at 198.18.40.16 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.009 | quiet window | clean |
| 4.009 | step | Baseline |
| 8.012 | step | dc1-firewall power lost |
| 8.139 | power | withdrawing the data cables of dc1-firewall and stopping its guest |
| 8.224 | dc1-core2 log | interface,info firewall link down |
| 8.235 | dc1-core1 log | interface,info firewall link down |
| 8.326 | power | dc1-firewall guest paused and all data cables down |
| 8.955 | dc1-core1 log | interface,info ether5 link down |
| 9.130 | dc1-core2 log | interface,info ether5 link down |
| 11.149 | dc2-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 28.373 | state | dc1-firewall power lost pass |
| 28.374 | step | dc1-firewall power restored |
| 28.377 | power | resetting and resuming the guest of dc1-firewall |
| 28.571 | dc1-core2 log | interface,info firewall link up |
| 28.585 | dc1-core1 log | interface,info firewall link up |
| 28.593 | power | dc1-firewall guest running and all data cables up |
| 29.015 | dc1-core1 log | interface,info ether5 link up (speed 10G, full duplex) |
| 29.175 | dc1-core2 log | interface,info ether5 link up (speed 10G, full duplex) |
| 60.507 | dc1-firewall log | vrrp,info vrrp390 now MASTER, master down timer |
| 60.516 | dc2-firewall log | vrrp,info vrrp390 now BACKUP, got higher priority 150 from 198.18.40.2 |
| 61.878 | recovery | full lab state after power restoration of dc1-firewall: pass |
| 77.878 | step | Power recovery |
| 80.881 | steps | last step ended |
| 84.058 | state | check after the steps: pass |
| 84.058 | state | All four MLAG pairs are connected with peer 1 as MLAG primary. pass |
| 84.058 | state | Every switch runs with spanning tree off. pass |
| 84.058 | state | Both members of the DCI and of each distribution-to-core trunk are in use. pass |
| 84.058 | state | Both cables of each firewall are in use in its LACP bond to the local cores. pass |
| 84.058 | state | The dc1 firewall owns the VRRP address and the dc2 firewall is backup. pass |
| 84.058 | state | Both cables of every host are eligible in its LACP bond. pass |
| 84.058 | streams | measurement ended; captures wait for final replies |
| 84.565 | stopped | captures and streams stopped |
| 84.593 | dc1-core1 log | script,info networka firewall-loss end |
| 84.620 | dc1-core2 log | script,info networka firewall-loss end |
| 84.652 | dc1-dist1 log | script,info networka firewall-loss end |
| 84.682 | dc1-dist2 log | script,info networka firewall-loss end |
| 84.730 | dc1-firewall log | script,info networka firewall-loss end |
| 84.761 | dc2-core1 log | script,info networka firewall-loss end |
| 84.789 | dc2-core2 log | script,info networka firewall-loss end |
| 84.829 | dc2-dist1 log | script,info networka firewall-loss end |
| 84.864 | dc2-dist2 log | script,info networka firewall-loss end |
| 84.894 | dc2-firewall log | script,info networka firewall-loss end |
| 84.897 | switch log | marker 'networka firewall-loss end' written on dc1-core1, dc1-core2, dc1-dist1, dc1-dist2, dc1-firewall, dc2-core1, dc2-core2, dc2-dist1, dc2-dist2, dc2-firewall |
