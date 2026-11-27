# PASS — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond, and on the independent bypass. Check that flooded probes reach host1 once.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host1:eth3 → host2:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:eth3 → host1:eth3 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both MLAG bonds on both peers contain their wired bond member and use it for LACP forwarding. · pass
- Both MLAG bond bridge ports are forwarding on both peers and both peer ports have carrier. · pass

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host1:eth3 → host2:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:eth3 → host1:eth3 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Flood probes

**pass**
- host2:bond0 → 10.110.0.255 · 98 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 98 probes at one every 100 ms, 0 returned to the sender, 40 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.838 | test | baseline started in lab medium-mlag |
| -2.223 | access-switch log | script,info networka baseline start |
| -1.613 | switch1 log | script,info networka baseline start |
| -1.013 | switch2 log | script,info networka baseline start |
| -1.007 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| -0.124 | state | check before the steps: pass |
| -0.124 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.124 | state | All three switches run with spanning tree off. pass |
| -0.124 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.124 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.062 | capture | started at host1:eth1 |
| -0.062 | capture | started at host1:eth3 |
| -0.062 | capture | started at host2:bond0 |
| -0.062 | capture | started at host2:eth1 |
| -0.062 | capture | started at host2:eth2 |
| -0.062 | capture | started at host2:eth3 |
| -0.008 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.005 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.003 | bypass-host1-to-host2 | started from host1:eth3 to host2:eth3 at 198.51.100.2 |
| -0.001 | bypass-host2-to-host1 | started from host2:eth3 to host1:eth3 at 198.51.100.1 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 0.000 | flood probe | started from host2:bond0 to 10.110.0.255 |
| 0.003 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 4.136 | quiet window | clean |
| 4.136 | step | Steady traffic |
| 8.981 | state | Steady traffic pass |
| 8.981 | steps | last step ended |
| 10.216 | state | check after the steps: pass |
| 10.216 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 10.216 | state | All three switches run with spanning tree off. pass |
| 10.216 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 10.216 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 10.216 | streams | measurement ended; captures wait for final replies |
| 10.721 | stopped | captures and streams stopped |
| 10.757 | access-switch log | script,info networka baseline end |
| 10.792 | switch1 log | script,info networka baseline end |
| 10.845 | switch2 log | script,info networka baseline end |
| 10.849 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
