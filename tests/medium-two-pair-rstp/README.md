# Medium lab with two MLAG pairs and RSTP

This is the [two-pair lab](../medium-two-pair/README.md) with RSTP on every bridge and the MLAG pair as root bridge. Pair A has priority `0x2000` and is the root, pair B `0x4000`. The host ports stay edge ports, and the peer links and the inter-pair bond keep `edge=auto`, as in the old field setup.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `medium-two-pair-rstp`, and management subnet, `172.30.114.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on all four bridges, root ID `0x2000.02:00:00:21:00:11` (switch-a1) on all four, pair A as root bridge, pair B reaching it through `inter-pair`, and every bridge port forwarding with the host ports as edge ports.
Each test in `cases/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/medium-two-pair/lab](../medium-two-pair/lab).

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/medium-two-pair-rstp NAME=medium-two-pair-rstp CONFIG=tests/medium-two-pair/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the two-pair README](../medium-two-pair/README.md).

## Live verdicts

Run on 27 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`), one run each, with Small RSTP, Medium RSTP and two-pair RSTP running at the same time. Every replay gave byte-identical `result.json` and `report.md`. The verdicts and stops are quoted from each generated `report.md`, at one ping every 100 ms; a stop is the lower to upper bound with the lost pings. Evidence, including the full switch log `switches.log`, is in `test-results/medium-two-pair-rstp.20261127T061300Z/`, not in git.

| Test | Verdict | Step | Stream | Limit | Measured stop |
| --- | --- | --- | --- | --- | --- |
| baseline | PASS | Steady traffic | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Steady traffic | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Steady traffic | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Steady traffic | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| calibration | PASS | One-way bypass cut | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | One-way bypass cut | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | One-way bypass cut | host1:eth3 → host2:eth3 | 2.3 s | 1.88026 to 2.08902 s, 19 lost (pass) |
|  |  | One-way bypass cut | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Bypass restored | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Bypass restored | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Bypass restored | host1:eth3 → host2:eth3 | 2.3 s | 0 s, 0 lost (pass) |
|  |  | Bypass restored | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | After calibration | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | After calibration | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | After calibration | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | After calibration | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| inter-pair-member-flap | FAIL | Inter-pair member down | host1:bond0 → host2:bond0 | 3 s | 9.73696 to 9.9402 s, 94 lost (fail) |
|  |  | Inter-pair member down | host2:bond0 → host1:bond0 | 3 s | 9.80149 to 10.0082 s, 95 lost (fail) |
|  |  | Inter-pair member down | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Inter-pair member down | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Inter-pair member back | host1:bond0 → host2:bond0 | 3 s | 9.73696 to 9.9402 s, 100 lost (fail) |
|  |  | Inter-pair member back | host2:bond0 → host1:bond0 | 3 s | 9.80149 to 10.0082 s, 99 lost (fail) |
|  |  | Inter-pair member back | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Inter-pair member back | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Flap recovery | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Flap recovery | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Flap recovery | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Flap recovery | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| reboot-a-primary | FAIL | Baseline | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a1 | host1:bond0 → host2:bond0 | 5 s | 21.453 to 21.6586 s, 207 lost (fail) |
|  |  | Reboot switch-a1 | host2:bond0 → host1:bond0 | 5 s | 21.5399 to 21.7486 s, 208 lost (fail) |
|  |  | Reboot switch-a1 | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a1 | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| reboot-a-secondary | PASS | Baseline | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a2 | host1:bond0 → host2:bond0 | 5 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a2 | host2:bond0 → host1:bond0 | 5 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a2 | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-a2 | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| reboot-b-primary | FAIL | Baseline | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-b1 | host1:bond0 → host2:bond0 | 5 s | 21.089 to 21.2939 s, 203 lost (fail) |
|  |  | Reboot switch-b1 | host2:bond0 → host1:bond0 | 5 s | 21.1646 to 21.3722 s, 204 lost (fail) |
|  |  | Reboot switch-b1 | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-b1 | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
| reboot-b-secondary | PASS | Baseline | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Baseline | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-b2 | host1:bond0 → host2:bond0 | 5 s | 0 to 0.207847 s, 1 lost (pass) |
|  |  | Reboot switch-b2 | host2:bond0 → host1:bond0 | 5 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-b2 | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot switch-b2 | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:bond0 → host2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:bond0 → host1:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host1:eth3 → host2:eth3 | 0 s | 0 s, 0 lost (pass) |
|  |  | Reboot recovery | host2:eth3 → host1:eth3 | 0 s | 0 s, 0 lost (pass) |
