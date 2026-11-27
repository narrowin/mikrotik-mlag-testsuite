# Medium MLAG lab with RSTP

This is the [Medium lab](../medium/README.md) with RSTP on every bridge and the MLAG pair as root bridge. Switch1 and switch2 have priority `0x1000` and the access switch `0x8000`; host ports are edge ports, and the peer link and the uplinks are not.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `medium-mlag-rstp`, and management subnet, `172.30.113.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on all three bridges, both peers as root bridge with root ID `0x1000.02:00:00:21:01:01` (switch1), the access switch on the same root through `uplink`, and every bridge port forwarding with the host ports as edge ports.
Each test in `cases/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/medium/lab](../medium/lab).

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium-rstp NAME=medium-mlag-rstp CONFIG=tests/medium/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the Medium README](../medium/README.md).

## Live verdicts

Run on 27 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`), one run each, with Small RSTP, Medium RSTP and two-pair RSTP running at the same time. Every replay gave byte-identical `result.json` and `report.md`. The verdicts and stops are quoted from each generated `report.md`, at one ping every 100 ms; a stop is the lower to upper bound with the lost pings. Evidence, including the full switch log `switches.log`, is in `test-results/medium-rstp.20261127T061300Z/`, not in git.

| Test | Verdict | Step | Stream | Limit | Measured stop |
| --- | --- | --- | --- | --- | --- |
| baseline | PASS | Steady traffic | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Steady traffic | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| primary-power-loss | FAIL | Baseline | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Baseline | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| | | switch1 power lost | host1:eth1 → host2:bond0 | 5 s | 9.26826 to 10.4905 s (diagnostic); Diagnostic only: 91 pings recorded lost, 191 sent in this step (configured interval 100 ms) (unverified. Sender cadence was invalid in this step.) |
| | | switch1 power lost | host2:bond0 → host1:eth1 | 5 s | 9.8012 to 10.0058 s, 96 lost (fail) |
| | | switch1 power restored | host1:eth1 → host2:bond0 | 5 s | 1.04147 to 1.2454 s, 19 lost (pass) |
| | | switch1 power restored | host2:bond0 → host1:eth1 | 5 s | 1.04 to 1.24813 s, 20 lost (pass) |
| | | Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| primary-reboot | ERROR | Baseline | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Baseline | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| | | Reboot switch1 | host1:eth1 → host2:bond0 | 5 s | 8.53613 to 28.678 s (diagnostic); Diagnostic only: 112 pings recorded lost, 274 sent in this step (configured interval 100 ms) (unverified. Sender cadence was invalid in this step.) |
| | | Reboot switch1 | host2:bond0 → host1:eth1 | 5 s | 28.1015 to 28.3147 s (diagnostic); Diagnostic only: 243 pings recorded lost, 406 sent in this step (configured interval 100 ms) (unverified. Sender cadence was invalid in this step.) |
| | | Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| secondary-power-loss | PASS | Baseline | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Baseline | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| | | switch2 power lost | host1:eth1 → host2:bond0 | 5 s | 0 to 0.202893 s, 1 lost (pass) |
| | | switch2 power lost | host2:bond0 → host1:eth1 | 5 s | 0 s, 0 lost (pass) |
| | | switch2 power restored | host1:eth1 → host2:bond0 | 5 s | 0 s, 0 lost (pass) |
| | | switch2 power restored | host2:bond0 → host1:eth1 | 5 s | 0 to 0.204263 s, 1 lost (pass) |
| | | Power recovery | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Power recovery | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| secondary-reboot | FAIL | Baseline | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Baseline | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |
| | | Reboot switch2 | host1:eth1 → host2:bond0 | 5 s | 2.49547 to 2.70461 s, 46 lost (pass) |
| | | Reboot switch2 | host2:bond0 → host1:eth1 | 5 s | 2.50554 to 2.71188 s, 47 lost (pass) |
| | | Reboot recovery | host1:eth1 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
| | | Reboot recovery | host2:bond0 → host1:eth1 | 0 s | 0 s, 0 lost (pass) |

secondary-reboot failed on its flood probe, not on traffic: for 10.110.0.255 and 10.110.0.99 the report says a probe was seen more than once across the sender's bond members. The base lab passed each of these tests on 26 November 2026.
