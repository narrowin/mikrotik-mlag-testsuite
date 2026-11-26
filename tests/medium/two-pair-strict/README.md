# Medium lab with two MLAG pairs and lacp-strict

This is the [two-pair lab](../two-pair/README.md) with `lacp-strict=yes` on the inter-pair bond of all four switches, set in the startup config.
With `lacp-strict=yes` a bond member without an LACP partner stops carrying traffic even while its link keeps carrier.
The lab has its own name, `medium-two-pair-strict`, and management subnet, so it can run next to the two-pair lab.

The folder holds only what differs: [topology.clab.yml](topology.clab.yml), which sets `LACP_STRICT` for the shared startup config, and [lab.yaml](lab.yaml), which checks `lacp-strict=yes` before and after every test.
The test files are links to the two-pair tests. Networka reads a test's `lab` file relative to the path it is given, so each linked test runs with this folder's `lab.yaml`.
The startup config, host setup and inventory are the two-pair lab's files.

## Commands

Prepare the shell as in the two-pair lab and start the lab from the repository root.

```sh
sudo env "CLAB=$CLAB" tests/medium/two-pair/start.sh strict
```

Run a test and replay it.

```sh
CASE=baseline
mkdir -p test-results/medium
RUN=$(mktemp -d test-results/medium/two-pair-strict.XXXXXX)
lab_nw test run "tests/medium/two-pair-strict/$CASE.yaml" \
  --lab tests/medium/two-pair-strict/clab-medium-two-pair-strict --config tests/medium/two-pair/devices.yml --save "$RUN"
lab_nw test replay "$RUN/$CASE"
```

Remove the lab when finished.

```sh
sudo "$CLAB" destroy -t tests/medium/two-pair-strict/topology.clab.yml --cleanup
```

The limits are the two-pair ones. The `two-pair-stp-off-strict-*` cases of the old catalogue give the same limits and holds.

## Live verdicts

Run on 26 November 2026 on RouterOS 7.26beta7 with Networka 0.5.1. Every attempt replayed with byte-identical `result.json` and `report.md`. The verdict and the measured stops are quoted from each generated `report.md`. Evidence is under `test-results/medium-two-pair/4c/`, not in git.

| Test | Verdict | Measured stop of the host streams |
| --- | --- | --- |
| baseline | PASS | 0 lost |
| calibration | PASS | Bypass lost 19 at one ping every 100 ms, 1.87121 to 2.08247 s |
| inter-pair-member-flap | PASS | 0 lost; both host MACs stayed in the host table of all four switches |
| reboot-a-primary | PASS | host1 to host2 lost 4 at one ping every 100 ms, 0.316485 to 0.525407 s. host2 to host1 lost 5, 0.403122 to 0.609865 s. |
| reboot-a-secondary | FAIL | host1 to host2 lost 211 at one ping every 100 ms, 21.8908 to 22.096 s. host2 to host1 lost 211, 21.8999 to 22.1054 s. |
| reboot-b-primary | PASS | host1 to host2 lost 4 at one ping every 100 ms, 0.316284 to 0.520742 s. host2 to host1 lost 3, 0.206444 to 0.412918 s. |
| reboot-b-secondary | FAIL | host2 to host1 lost 206 at one ping every 100 ms, 21.3416 to 21.5461 s. host1 to host2 is unverified: sender cadence was invalid in this step. |

## Comparison with the old suite

Old values are quoted from the results index at commit `3af4cd8` (`results/index/phases.jsonl`) and `results/2026-11-24-two-pair/README.md`, Medium lab, STP off, cases `two-pair-stp-off-strict-*`. The only old suite is `2026-11-24-two-pair/stp-off-strict`.

| Test | Old verdict and loss | New verdict and loss | Reason for the difference |
| --- | --- | --- | --- |
| baseline | Run 01 pass, no loss | PASS, no loss | Same result |
| calibration | No old result | PASS, 1.87121 to 2.08247 s | Not comparable |
| inter-pair-member-flap | No old result | PASS, 0 lost | Not comparable |
| reboot-a-primary | Run 01 INVALID: Pair A primary down 1.912816 to 2.591661 s, back 16.447632 to 16.650563 s; the management TAP showed one closed guest absence | PASS, at most 0.609865 s | The old run is invalid. Here no host traffic passes switch-a1, as in the two-pair lab. |
| reboot-a-secondary | Run 01 did not reach evaluation | FAIL, 21.8999 to 22.1054 s (host2 to host1) | No valid old result. The host traffic passes switch-a2. |
| reboot-b-primary | No old result | PASS, at most 0.520742 s | Not comparable |
| reboot-b-secondary | No old result | FAIL, 21.3416 to 21.5461 s; host1 to host2 unverified | Not comparable |

The host traffic takes the secondaries' cables here too. Host1 `eth2` sent 5795 packets and `eth1` 494, host2 `eth2` 5721 and `eth1` 559 (`test-results/medium-two-pair/09-4c-summary.log`). The reason is in the two-pair README.
`lacp-strict=yes` did not prevent the secondary reboot outage. It lasted 21.3 to 22.1 s here against 18.2 to 18.8 s without it, in one run each.
The primary reboots lost 0.2 to 0.6 s here and nothing without it, although no host traffic passes the primary. The cause is not verified. A likely one is that strict mode stops the secondary's inter-pair member while LACP renegotiates under the secondary's own system ID.
