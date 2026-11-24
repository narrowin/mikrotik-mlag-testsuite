# MEDIUM-03–04 · Core reboots with the MLAG pair as root

This is the pair-root control. Its access switch sits between Client A and the two cores, and the MLAG pair is the RSTP root. [Pair-root wiring](../../labs/medium/medium-pair-root.clab.yml) · [Pair-root measurements](../../results/2026-11-24-medium-lab-pair-root/README.md#development-726beta7) · [Current Medium lab bridge-mode comparison](medium-spanning-tree.md)

| | Case `reboot-primary` · control `reboot-secondary` |
| --- | --- |
| Setup | Two MLAG peers, a downstream RSTP bridge and two clients. Verify the peers report the same root ID, identify the elected primary, and confirm the downstream bridge sees that root. Keep the independent bypass running. |
| Fault | Calibrate, reboot the secondary, then restore and verify the baseline. Reboot the elected primary with the same wiring, timers and traffic. Measure departure and return separately. |
| Expected | The survivor carries bidirectional traffic while the primary is absent. Each VLAN direction has a **5 s** outage budget per phase. The bypass loses **zero** probes. Check which peer holds the primary role after rejoin. |
| Measured | **Both primary reboots failed the withdrawal target on 7.26beta7. Both secondary controls passed.** In each primary run the clients recovered briefly, then lost traffic again. A → B lost **11.654–11.858 s** in that second gap on repeat 1 and **10.722–10.928 s** on repeat 2. Restoration exceeded 5 s on repeat 1 only. |

The original Site A core 1 test recorded **12 s on failure and 12 s on return**. Rebooting Site A core 2 recorded **1–2 s** in each phase. The working note attributed the longer pause to spanning tree. In the captured CHR sequence, traffic initially followed a still-eligible LACP leg toward the rebooted peer. Later the surviving core’s `witness-bond` stopped forwarding. On return, the downstream access switch’s `uplink` stayed discarding after the bond members became eligible. [Working note and provenance](../plans/primary-reboot-plan.md#recovered-tests-and-their-limits)

Use the dedicated root topology for this case. After a run, open `01-reboot-primary/result.json` and its sibling `timeline.tsv` in the suite directory. The JUnit report records the phase-specific failures. [Per-direction results and port timeline](../../results/2026-11-24-medium-lab-pair-root/README.md#development-726beta7) · [Deployment and run commands](../operator-guide.md#reboot-the-root-pair)

Use the latest development build for future runs. [Version policy](../validation-plan.md#routeros-version-for-live-tests) · [Archived Stable comparison](../../results/2026-11-24-medium-lab-pair-root/README.md#stable-7252-reboot-repeats)
