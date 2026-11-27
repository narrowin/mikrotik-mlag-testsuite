# Medium lab with two MLAG pairs and lacp-strict

This is the [two-pair lab](../two-pair/README.md) with `lacp-strict=yes` on the inter-pair bond of all four switches, set in the startup config.
With `lacp-strict=yes` a bond member without an LACP partner stops carrying traffic even while its link keeps carrier.
The lab has its own name, `two-pair-strict`, and management subnet, so it can run next to the two-pair lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `LACP_STRICT` for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks `lacp-strict=yes` before and after every test.
Each test in `tests/` is a symbolic link to the two-pair test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the two-pair lab's files in [tests/two-pair/lab](../two-pair/lab).

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/two-pair-strict/`.

- [PASS — baseline](runs/live-20261127-glossary/baseline/report.md)
- [FAIL — inter-pair-member-flap](runs/live-20261127-glossary/inter-pair-member-flap/report.md)
- [FAIL — reboot-a-primary](runs/live-20261127-glossary/reboot-a-primary/report.md)
- [PASS — reboot-a-secondary](runs/live-20261127-glossary/reboot-a-secondary/report.md)
- [FAIL — reboot-b-primary](runs/live-20261127-glossary/reboot-b-primary/report.md)
- [PASS — reboot-b-secondary](runs/live-20261127-glossary/reboot-b-secondary/report.md)

## Commands

Start, run, replay and remove the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values.

```sh
LAB=tests/two-pair-strict NAME=two-pair-strict CONFIG=tests/two-pair/lab/devices.yml
```

The limits are the two-pair ones. The `two-pair-stp-off-strict-*` cases of the old catalogue give the same limits and holds.


## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8` (`results/index/phases.jsonl`) and `results/2026-11-24-two-pair/README.md`, Medium lab, STP off, cases `two-pair-stp-off-strict-*`. The only old suite is `2026-11-24-two-pair/stp-off-strict`.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | Run 01 pass, no loss | PASS, no loss | Same |
| inter-pair-member-flap | No old result | FAIL. Down: host1 to host2 5.40884 to 5.61424 s (53 lost), host2 to host1 5.41469 to 5.62633 s (53 lost), against 3 s. Back: 0.318171 to 0.523095 s and 0.419289 to 0.621454 s | Not comparable. Shorter than the whole 8 s down hold of the runs recorded with the bypass cable; the two-pair lab without `lacp-strict` passes this test. |
| reboot-a-primary | Run 01 INVALID: Pair A primary down 1.912816 to 2.591661 s, back 16.447632 to 16.650563 s; the management TAP showed one closed guest absence | FAIL, 17.796 to 18.1021 s | No valid old result. The old invalid run also lost about 16.5 s. |
| reboot-a-secondary | Run 01 did not reach evaluation | PASS, 0 lost | No valid old result |
| reboot-b-primary | No old result | FAIL, 23.38 to 23.7188 s | Not comparable |
| reboot-b-secondary | No old result | PASS, 0 lost | Not comparable |

In one run each, `lacp-strict=yes` changed one verdict: the inter-pair member flap fails here and passes in the two-pair lab. The primary reboot stops of 17.8 to 23.7 s are close to the two-pair lab's 19.1 to 24.3 s.
