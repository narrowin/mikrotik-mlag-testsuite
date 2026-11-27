# Small MLAG with a MAC-move host

Both switches run with spanning tree off. Switch1 is configured as MLAG primary and switch2 as secondary. Host1 and host2 have dual LACP links. The MAC-move host, `mac-move-host`, uses an active-backup bond with the same MAC on either link.

## Live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2, after the glossary renames. Each listed test ran once. `mac-age-relearn` ran with the ageing profile. Every replay produced byte-identical `result.json` and `report.md`. The links open the generated reports; full evidence stays in `test-results/live-20261127-glossary/small-mac-move/` and `test-results/live-20261127-glossary/small-mac-move-age/`.

- [PASS — baseline](runs/live-20261127-glossary/baseline/report.md)
- [PASS — bond-member-loss](runs/live-20261127-glossary/bond-member-loss/report.md)
- [FAIL — lacp-timeout](runs/live-20261127-glossary/lacp-timeout/report.md)
- [PASS — mac-age-relearn](runs/live-20261127-glossary/mac-age-relearn/report.md)
- [PASS — mac-move](runs/live-20261127-glossary/mac-move/report.md)
- [PASS — member-flap-repeat](runs/live-20261127-glossary/member-flap-repeat/report.md)
- [PASS — peer-link-loss](runs/live-20261127-glossary/peer-link-loss/report.md)
- [PASS — primary-power-loss](runs/live-20261127-glossary/primary-power-loss/report.md)
- [PASS — primary-reboot](runs/live-20261127-glossary/primary-reboot/report.md)
- [PASS — secondary-power-loss](runs/live-20261127-glossary/secondary-power-loss/report.md)
- [FAIL — secondary-reboot](runs/live-20261127-glossary/secondary-reboot/report.md)

## Run a test

Run the lab as in [Run a lab](../../docs/tests/README.md#run-a-lab), with these values. The MAC-move lab has its own inventory, because its third host is `mac-move-host`.

```sh
LAB=tests/small-mac-move NAME=small-mlag-mac-move CONFIG=tests/small-mac-move/lab/devices.yml
```

Use the default profile for every test except MAC ageing. For `TEST=mac-age-relearn`, start the lab with the `age` argument, which starts both switches at ten seconds of ageing and pins the necessary host neighbours. Remove the lab with the same ageing value it was started with. Teardown discards the profile. The test itself clears both egress filters.

```sh
sudo env "CLAB=$CLAB" tests/shared/start.sh "$LAB" age
sudo env SMALL_MAC_MOVE_AGE=10s "$CLAB" destroy -t "$LAB/lab/topology.clab.yml" --cleanup
```

## Tests

| Test | Traffic and evidence |
| --- | --- |
| [Baseline](tests/baseline.yaml) | Switch forwarding, peer carrier, both host bonds and both directions between host1 and host2. |
| [Single member](tests/bond-member-loss.yaml), [repeated member flaps](tests/member-flap-repeat.yaml) | Host1 cable to switch1, once for eight seconds or five times for one second each. The repeated test samples unrelated bridge host entries on both switches. |
| [Peer link](tests/peer-link-loss.yaml) | Fifteen-second cut at both switches, with MLAG and RouterOS carrier checks. |
| [LACP timeout](tests/lacp-timeout.yaml) | Eight seconds without host1 LACPDUs to switch1, with carrier, local timeout flags and restored partner flags checked. |
| [Primary reboot](tests/primary-reboot.yaml), [secondary reboot](tests/secondary-reboot.yaml) | Checked role and native uptime reset. The secondary reboot test also checks for returned broadcast and unknown-unicast probes on both sender members. |
| [Primary power loss](tests/primary-power-loss.yaml), [secondary power loss](tests/secondary-power-loss.yaml) | Twenty seconds off, neighbour carrier withdrawal and a new boot. |
| [MAC move](tests/mac-move.yaml), [MAC age and relearn](tests/mac-age-relearn.yaml) | Host table state, switch TAP packet evidence and delivery on all five streams. |

## Observation limits

MAC ageing deliberately silences the MAC-move host for 25 s. The retained 26 s combined interruption limit includes that silence; it is not a 26 s relearning allowance. The typed action separately requires delivery and the end of unknown-unicast flooding within the existing 1 s `relearn_s`, measured from the first returning host frame at a switch TAP. The unaffected host1-to-host2 stream and the subsequent recovery step retain their 0 s limits.

Reports show those deliberate interruptions separately from ordinary traffic outages. The results summary excludes them while they remain within their combined limits, and still highlights a confirmed limit breach. The linked MAC-ageing report has been regenerated from the unchanged saved `result.json` with the local Networka reporting change; no new live run or verdict is implied.

The cable tests record switch log events and state samples. Precise guest carrier deadlines, withdrawn member TAP observations and per-port LACP frame histories remain open. The secondary reboot checks baseline flood copies at host2. The historical receiver checks also watched the MAC-move host.
