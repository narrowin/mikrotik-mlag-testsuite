# Medium lab with two MLAG pairs and lacp-strict

This is the [two-pair lab](../two-pair/README.md) with `lacp-strict=yes` on the inter-pair bond of all four switches, set in the startup config.
With `lacp-strict=yes` a bond member without an LACP partner stops carrying traffic even while its link keeps carrier.
The lab has its own name, `two-pair-strict`, and management subnet, so it can run next to the two-pair lab.

The folder holds only what differs: [topology.clab.yml](lab/topology.clab.yml), which sets `LACP_STRICT` for the shared startup config, and [lab.yaml](lab/lab.yaml), which checks `lacp-strict=yes` before and after every test.
Each test in `tests/` is a symbolic link to the two-pair test of the same name, and Networka resolves its `lab: ../lab/lab.yaml` from the link's folder, so it runs with this lab's `lab.yaml`.
The startup config, host setup and inventory are the two-pair lab's files in [tests/two-pair/lab](../two-pair/lab).

## Live runs

Run on 28 November 2026 with RouterOS 7.26beta7 in our CHR image `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10` and Networka 0.5.2+chr.5. Each listed test ran once. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports, and [image-proof.json](runs/live-20261128-image-dbd8a548/image-proof.json) records the image of every node; full evidence stays in `test-results/live-20261128-image-dbd8a548/two-pair-strict/`.

- [PASS — baseline](runs/live-20261128-image-dbd8a548/baseline/report.md)
- [PASS — inter-pair-member-flap](runs/live-20261128-image-dbd8a548/inter-pair-member-flap/report.md)
- [FAIL — reboot-a-primary](runs/live-20261128-image-dbd8a548/reboot-a-primary/report.md)
- [PASS — reboot-a-secondary](runs/live-20261128-image-dbd8a548/reboot-a-secondary/report.md)
- [FAIL — reboot-b-primary](runs/live-20261128-image-dbd8a548/reboot-b-primary/report.md)
- [PASS — reboot-b-secondary](runs/live-20261128-image-dbd8a548/reboot-b-secondary/report.md)

inter-pair-member-flap passed. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 it failed.

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
| inter-pair-member-flap | No old result | PASS. Down: host1 to host2 0.10558 to 0.309641 s (2 lost), host2 to host1 0 to 0.202416 s (1 lost). Back: host1 to host2 1.15043 to 1.35714 s (15 lost), host2 to host1 1.14592 to 1.34826 s (15 lost) | Not comparable. On 27 November 2026 with the official `mikrotik/chr` image and Networka 0.5.2 it failed. |
| reboot-a-primary | Run 01 INVALID: Pair A primary down 1.912816 to 2.591661 s, back 16.447632 to 16.650563 s; the management TAP showed one closed guest absence | FAIL, 19.1532 to 19.3626 s | No valid old result. The old invalid run also lost about 16.5 s. |
| reboot-a-secondary | Run 01 did not reach evaluation | PASS, 0 lost | No valid old result |
| reboot-b-primary | No old result | FAIL, 18.6762 to 18.9601 s | Not comparable |
| reboot-b-secondary | No old result | PASS, 0 lost | Not comparable |

In one run each, `lacp-strict=yes` changed no verdict: every test has the verdict it has in the two-pair lab. The primary reboot stops of 18.7 to 19.4 s are about 2 to 3 s longer than the two-pair lab's 16.2 to 16.8 s.
