# Medium lab with two MLAG pairs and lacp-strict

This is the [two-pair lab](../two-pair/README.md) with `lacp-strict=yes` on the inter-pair bond of all four switches, set in the startup config.
With `lacp-strict=yes` a bond member without an LACP partner stops carrying traffic even while its link keeps carrier.
The lab has its own name, `two-pair-strict`, and management subnet, so it can run next to the two-pair lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `LACP_STRICT` for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks `lacp-strict=yes` before and after every test.
Each test in `tests/` is a symbolic link to the two-pair test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the two-pair lab's files in [tests/two-pair/lab](../two-pair/lab).

## Networka 0.5.2 live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links below open the generated reports; full evidence stays in `test-results/networka-0.5.2-20261127/medium-two-pair-strict/`. Earlier measurements below remain historical.

- [PASS — baseline](runs/networka-0.5.2-20261127/baseline/report.md)
- [FAIL — inter-pair-member-flap](runs/networka-0.5.2-20261127/inter-pair-member-flap/report.md)
- [FAIL — reboot-a-primary](runs/networka-0.5.2-20261127/reboot-a-primary/report.md)
- [PASS — reboot-a-secondary](runs/networka-0.5.2-20261127/reboot-a-secondary/report.md)
- [FAIL — reboot-b-primary](runs/networka-0.5.2-20261127/reboot-b-primary/report.md)
- [PASS — reboot-b-secondary](runs/networka-0.5.2-20261127/reboot-b-secondary/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/two-pair-strict NAME=two-pair-strict CONFIG=tests/two-pair/lab/devices.yml
```

The limits are the two-pair ones. The `two-pair-stp-off-strict-*` cases of the old catalogue give the same limits and holds.

## Live verdicts

Run on 27 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1 and the qualified Containerlab build (SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`). Every attempt replayed with byte-identical `result.json` and `report.md`. The verdict and the measured stops are quoted from each generated `report.md`, at one ping every 100 ms. Evidence is under `test-results/medium-two-pair/r3/4c/`, not in git.

| Test | Verdict | Longest measured stop of the host streams |
| --- | --- | --- |
| baseline | PASS | 0 lost |
| inter-pair-member-flap | FAIL | Member down: host1 to host2 lost 78, 8.05368 to 8.26084 s; host2 to host1 lost 79, 8.12048 to 8.33055 s. The same outage runs into the member back step. |
| reboot-a-primary | FAIL | host1 to host2 lost 175, 18.1305 to 18.337 s; host2 to host1 lost 175, 18.1369 to 18.345 s |
| reboot-a-secondary | PASS | 0 lost |
| reboot-b-primary | FAIL | host1 to host2 lost 160, 16.5593 to 16.766 s; host2 to host1 lost 160, 16.5463 to 16.7493 s |
| reboot-b-secondary | PASS | 0 lost |

After the runs host1 had sent 5009 packets on `eth1` and 428 on `eth2`, host2 4971 on `eth1` and 448 on `eth2`, so the host traffic used the primaries (`test-results/medium-two-pair/r3/09-4c-counters-destroy.log`).

## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8` (`results/index/phases.jsonl`) and `results/2026-11-24-two-pair/README.md`, Medium lab, STP off, cases `two-pair-stp-off-strict-*`. The only old suite is `2026-11-24-two-pair/stp-off-strict`.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | Run 01 pass, no loss | PASS, no loss | Same |
| inter-pair-member-flap | No old result | FAIL, the whole 8 s down hold | Not comparable. The same unexplained stop as in the two-pair lab: requests reach switch-b1 and nothing leaves it on any port, the peer link included, although host2's entry is on the peer port within about 2 s. |
| reboot-a-primary | Run 01 INVALID: Pair A primary down 1.912816 to 2.591661 s, back 16.447632 to 16.650563 s; the management TAP showed one closed guest absence | FAIL, 18.1369 to 18.345 s | No valid old result. The old invalid run also lost about 16.5 s. |
| reboot-a-secondary | Run 01 did not reach evaluation | PASS, 0 lost | No valid old result |
| reboot-b-primary | No old result | FAIL, 16.5463 to 16.766 s | Not comparable |
| reboot-b-secondary | No old result | PASS, 0 lost | Not comparable |

`lacp-strict=yes` changed no verdict. The primary reboot stops of 16.5 to 18.3 s fall in the range of the two-pair lab's 16.4 to 18.1 s, in one run each.
