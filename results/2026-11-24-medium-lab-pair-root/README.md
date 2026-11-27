# Medium lab · core reboots with the MLAG pair as RSTP root

## Setup

| Setting | Value |
| --- | --- |
| Build | RouterOS 7.26beta7 |
| Host | ARM64 OrbStack VM |
| Wiring | The MLAG pair is the shared RSTP root. Client A connects through an access switch with an LACP uplink to both cores. Client B bonds directly to both cores. [Topology](../../labs/medium/medium-pair-root.clab.yml) |
| Traffic | VLAN 110 probes in both directions and an independent bypass |
| Pass target | ≤5 s per direction and phase. [Run commands](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/operator-guide.md#reboot-the-root-pair) |

## TL;DR

- **Traffic between the two clients recovered within five seconds in both secondary reboots.** The longest gap was at most **3.23 s** when the secondary went down. No probes were lost when it rejoined.
- **Traffic took longer than five seconds to recover in both primary reboots.** The surviving core’s bond toward the access switch discarded traffic while the primary was down. The access switch’s uplink discarded on rejoin even though LACP was eligible.
- **When the access switch was elected RSTP root, its uplink stayed in the discarding state.** Neither client received any VLAN 110 probes before a reboot could be tested.

## Results

The two-second calibration passed in both repeats. The bypass lost zero probes during every reboot.

| 7.26beta7 test | Verdict | Measurement or observed reason |
| --- | --- | --- |
| Secondary reboot, two repeats | Pass | Withdrawal upper bounds of 3.228 s and 3.012 s. |
| Primary reboot, two repeats | Fail | Worst withdrawal bound 11.86 s. Restoration bounds reached 1.25 s and 6.87 s. |
| Primary paused for 35 s with carrier up | Fail | Traffic briefly recovered, then went down until resume. The longer gap reached 32.36 s. |
| Primary reboot with LACP fallback off | Fail | Withdrawal reached 13.20 s and restoration reached 6.99 s. |
| Primary reboot with transparent virtual cables | Fail | Withdrawal reached 12.36 s. Restoration bounds straddled 5 s. |

### Access switch as root

Neither VLAN direction delivered any of its 62 probes. Both bypass directions delivered all 62. Captures showed proposals from the access switch without a core reply during the sample. Restoring the original priority restored forwarding. [External roots and STP-off follow-up](../2026-11-24-medium-lab/README.md)

## Reproduce

[Case procedure](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/cases/medium-core-reboot.md) · [Deploy, calibrate, and run](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/operator-guide.md#reboot-the-root-pair)

The packet captures behind this report stay local. Rerun the case with the commands above to get your own captures and verdicts.

## Evidence

[Per-flow phase bounds](phase-loss.tsv) · [Development JUnit](development-junit.xml) · [Capture checksums](SHA256SUMS)
