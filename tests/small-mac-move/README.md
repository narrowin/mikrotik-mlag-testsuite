# Small MLAG with a MAC-move host

Both switches run with spanning tree off. Switch1 is configured as MLAG primary and switch2 as secondary. Host1 and host2 have dual LACP links. The MAC-move host, `mac-move-host`, uses an active-backup bond with the same MAC on either link.

## Networka 0.5.2 live runs

Run on 27 November 2026 with RouterOS 7.26beta7 and Networka 0.5.2. Each listed test ran once; `mac-age-relearn` used the required ageing profile. Every replay produced byte-identical `result.json` and `report.md`. These links open the generated reports. Full evidence stays in `test-results/networka-0.5.2-20261127/small-mobile/` and `small-mobile-age/`.

- [PASS — baseline](runs/networka-0.5.2-20261127/baseline/report.md)
- [PASS — bond-member-loss](runs/networka-0.5.2-20261127/bond-member-loss/report.md)
- [PASS — lacp-timeout](runs/networka-0.5.2-20261127/lacp-timeout/report.md)
- [PASS — mac-age-relearn](runs/networka-0.5.2-20261127/mac-age-relearn/report.md)
- [PASS — mac-move](runs/networka-0.5.2-20261127/mac-move/report.md)
- [PASS — member-flap-repeat](runs/networka-0.5.2-20261127/member-flap-repeat/report.md)
- [PASS — peer-link-loss](runs/networka-0.5.2-20261127/peer-link-loss/report.md)
- [PASS — primary-power-loss](runs/networka-0.5.2-20261127/primary-power-loss/report.md)
- [PASS — primary-reboot](runs/networka-0.5.2-20261127/primary-reboot/report.md)
- [PASS — secondary-power-loss](runs/networka-0.5.2-20261127/secondary-power-loss/report.md)
- [PASS — secondary-reboot](runs/networka-0.5.2-20261127/secondary-reboot/report.md)

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

The cable tests record switch log events and state samples. Precise guest carrier deadlines, withdrawn member TAP observations and per-port LACP frame histories remain open. The secondary reboot checks baseline flood copies at host2. The historical receiver checks also watched the MAC-move host.
