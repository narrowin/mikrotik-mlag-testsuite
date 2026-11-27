# Small MLAG lab with RSTP

This is the [Small lab](../small/README.md) with RSTP on every bridge and the MLAG pair as root bridge. Switch1 and switch2 have priority `0x1000`, and the client bond ports are edge ports.
Both MLAG peers carry the same bridge priority and the same port STP settings, as the MikroTik MLAG manual requires. The switches also send the `stp` log topic to the collector.
The lab has its own name, `small-mlag-rstp`, and management subnet, `172.30.102.0/24`, so it can run next to the base lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `STP_MODE: rstp` and the collector address for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks before and after every test RSTP on both bridges, both peers as root bridge, and every bridge port forwarding with the client ports as edge ports.
Each test in `cases/` is a symbolic link to the base test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the base lab's files in [tests/small/lab](../small/lab).

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/small-rstp NAME=small-mlag-rstp CONFIG=tests/small/lab/devices.yml
```

The tests and their limits are the base lab's, unchanged: see [the Small README](../small/README.md).

## Live verdicts

Run on 27 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`), one run each, with Small RSTP, Medium RSTP and two-pair RSTP running at the same time. Every replay gave byte-identical `result.json` and `report.md`. The verdicts and stops are quoted from each generated `report.md`, at one ping every 100 ms; a stop is the lower to upper bound with the lost pings. Evidence, including the full switch log `switches.log`, is in `test-results/small-rstp.20261127T061300Z/`, not in git.

| Test | Verdict | Step | Stream | Limit | Measured stop |
| --- | --- | --- | --- | --- | --- |
| bond-member-loss | PASS | Cable client1 to switch1 down | client1:bond0 → client2:bond0 | 1 s | 0 s, 0 lost (pass) |
|  |  | Cable client1 to switch1 down | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable client1 to switch1 back | client1:bond0 → client2:bond0 | 4 s | 0 s, 0 lost (pass) |
|  |  | Cable client1 to switch1 back | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable client1 to switch2 down | client1:bond0 → client2:bond0 | 1 s | 0 to 0.208647 s, 1 lost (pass) |
|  |  | Cable client1 to switch2 down | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable client1 to switch2 back | client1:bond0 → client2:bond0 | 4 s | 2.42515 to 2.63643 s, 24 lost (pass) |
|  |  | Cable client1 to switch2 back | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
| cable-delay | PASS | Delay on client1 cable | client1:bond0 → client2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Delay on client1 cable | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable delay cleared | client1:bond0 → client2:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable delay cleared | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
| cable-packet-loss | ERROR | One-way cable loss | client1:bond0 → client2:bond0 | 4 s | at least 22.8157 s (diagnostic); Diagnostic only: 220 pings recorded lost, 220 sent in this step (configured interval 100 ms) (unverified. Sender cadence was invalid in this step.) |
|  |  | One-way cable loss | client2:bond0 → client3:bond0 | 0 s | 0 s, 0 lost (pass) |
|  |  | Cable loss cleared | client1:bond0 → client2:bond0 | 4 s | unverified; Diagnostic only: 0 pings recorded lost, 0 sent in this step (configured interval 100 ms) (unverified. No sender pings were captured in this step.) |
|  |  | Cable loss cleared | client2:bond0 → client3:bond0 | 0 s | unverified; Diagnostic only: 0 pings recorded lost, 143 sent in this step (configured interval 100 ms) (unverified. The step stopped before it completed.) |
| switch-reboot | PASS | Reboot switch1 | client1:bond0 → client2:bond0 | 4 s | 0.31733 to 0.523343 s, 4 lost (pass) |
|  |  | Reboot switch1 | client2:bond0 → client3:bond0 | 4 s | 0.40252 to 0.610744 s, 5 lost (pass) |

The cable-packet-loss ERROR is the same as in the base lab on 26 November 2026 (`test-results/live-0.5.1/canonical-cable-packet-loss.7OqL68`): client1's eth2 was still not eligible in its bond when the 15 s recovery deadline ran out.
