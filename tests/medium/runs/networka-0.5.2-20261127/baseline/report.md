# PASS — baseline

Check forwarding in both directions between host1 behind the access switch and host2 on its MLAG bond. Check that flooded probes reach host1 once.

## Traffic

| Step | Stream | Limit | Total lost pings | Longest measured stop | Verdict |
| --- | --- | --- | --- | --- | --- |
| Steady traffic | host1:eth1 → host2:bond0 | 0 s | 0 at one ping every 100 ms | 0 s | pass |
| Steady traffic | host2:bond0 → host1:eth1 | 0 s | 0 at one ping every 100 ms | 0 s | pass |

**Steady traffic state** · pass
- Both MLAG bonds on both peers contain their wired bond member and use it for LACP forwarding. · pass
- Both MLAG bond bridge ports are forwarding on both peers and both peer ports have carrier. · pass

**quiet window** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

**after the steps** · pass

- host1:eth1 → host2:bond0 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates
- host2:bond0 → host1:eth1 · 0 pings lost at one ping every 100 ms, traffic stopped for 0 s · 0 duplicates

## Flood probes

**pass**
- host2:bond0 → 10.110.0.255 · 96 probes at one every 100 ms, 0 returned to the sender, 38 reached the baseline witness host1:eth1 once.
- host2:bond0 → 10.110.0.99 · 96 probes at one every 100 ms, 0 returned to the sender, 38 reached the baseline witness host1:eth1 once.

## Switch log rules

This test declares no switch log rules.

## What happened

Times are relative to the start of the quiet window or, if it never started, the first recorded event.

| Time (s) | Event | Detail |
| --- | --- | --- |
| -2.812 | test | baseline started in lab medium-mlag |
| -2.241 | access-switch log | script,info networka baseline start |
| -1.653 | switch1 log | script,info networka baseline start |
| -1.044 | switch2 log | script,info networka baseline start |
| -1.037 | switch log | marker 'networka baseline start' written on access-switch, switch1, switch2 |
| -0.123 | state | check before the steps: pass |
| -0.123 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| -0.123 | state | All three switches run with spanning tree off. pass |
| -0.123 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| -0.123 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| -0.061 | capture | started at host1:eth1 |
| -0.061 | capture | started at host2:bond0 |
| -0.060 | capture | started at host2:eth1 |
| -0.060 | capture | started at host2:eth2 |
| -0.005 | host1-to-host2 | started from host1:eth1 to host2:bond0 at 10.110.0.12 |
| -0.003 | host2-to-host1 | started from host2:bond0 to host1:eth1 at 10.110.0.11 |
| -0.002 | flood probe | started from host2:bond0 to 10.110.0.255 |
| -0.001 | flood probe | started from host2:bond0 to 10.110.0.99 |
| 0.000 | quiet window | starts at the first reply of every stream |
| 4.037 | quiet window | clean |
| 4.037 | step | Steady traffic |
| 8.832 | state | Steady traffic pass |
| 8.832 | steps | last step ended |
| 10.082 | state | check after the steps: pass |
| 10.082 | state | Switch1 is the connected MLAG primary and switch2 the connected MLAG secondary. pass |
| 10.082 | state | All three switches run with spanning tree off. pass |
| 10.082 | state | Both bond members of the access switch uplink are synchronized, collecting and distributing. pass |
| 10.082 | state | Both bond members of host2 have carrier and are eligible in its LACP bond. pass |
| 10.083 | streams | measurement ended; captures wait for final replies |
| 10.588 | stopped | captures and streams stopped |
| 10.637 | access-switch log | script,info networka baseline end |
| 10.684 | switch1 log | script,info networka baseline end |
| 10.722 | switch2 log | script,info networka baseline end |
| 10.732 | switch log | marker 'networka baseline end' written on access-switch, switch1, switch2 |
