# Medium lab · core reboots with and without spanning tree

## Setup

[Editable draw.io](../../docs/diagrams/mlag-scenarios.drawio) · Pages **1 Small**, **2 Medium**, **3 Large**

| Lab | Tests covered | STP disabled everywhere | RSTP enabled |
| --- | --- | --- | --- |
| [Small lab](../../docs/diagrams/small-lab.png) | Reboot each core; calibration, carrier loss, silent LACP, MAC move | Not run | Both reboots passed. Other tests passed 3/4. |
| [Medium lab](../../docs/diagrams/medium-lab.png) | Reboot each core; preferred-root loss; combined core and root loss | All four reboots passed | All four reboots failed. Root-loss tests also failed. |
| [Large lab · both sites](../../docs/diagrams/large-lab.png) | Two-site failover | Pending | Pending |

[RouterOS 7.26beta7](../../labs/campaign-image.txt) · OrbStack VM `mlag-external` · VLAN 110, both directions · Reboot interruption limit **5 s**. [Test procedure](../../docs/cases/medium-spanning-tree.md) · [Topology and port map](../../labs/medium/README.md)

## TL;DR

- **STP off everywhere** — Rebooting each core twice kept all host-to-host traffic gaps within 5 s.
- **RSTP on, same wiring** — Both reboots of each core exceeded 5 s; RSTP blocked the access-switch path.
- **RSTP on, both hosts directly attached** — Both reboots (one per core) met the 5 s limit.

## Results

| Test | What happened to traffic | What the devices showed |
| --- | --- | --- |
| STP off everywhere · **Pass** | Each core rebooted twice. Longest gaps were ≤3.34 s going down and ≤0.312 s coming back. The bypass lost no probes. | No STP frames during scoring. One extra primary reboot was withheld when both root candidates reported unexpected STP state. |
| STP off on cores only · **Baseline failed** | The host path failed before any reboot. | The access switch’s LACP uplink was discarding. |
| RSTP restored on the same wiring · **Baseline failed** | Both VLAN directions delivered 0/44 probes. Both bypass directions delivered 44/44. | Probes entered the secondary on the peer link and never appeared on its port toward the access switch. The cause remains unknown. |
| RSTP, primary reboot · **Failed twice** | Gaps reached 11.88 s going down and 6.86 s coming back. | The surviving core’s bond toward the access switch discarded traffic. On return, the access switch’s own uplink discarded. |
| RSTP, secondary reboot · **Failed twice** | VLAN traffic was still down at capture end, at least 19.15 s after the core returned. | The returning core’s bond toward the access switch was discarding despite eligible LACP members. |
| Disconnect preferred root · **Return failed** | No probe loss when the backup took over. A repeat failed its initial traffic check. | The preferred root’s attachment stayed in the discarding state after reconnection. |
| Lose primary and preferred root attachment · **Failed twice** | Outage upper bounds were 13.155 s and 12.815 s when the primary went down. | The backup root took over in both trials. |
| RSTP, both hosts directly attached · **Both reboots passed** | Zero lost probes on secondary reboot. The longest gap on primary reboot was ≤2.91 s. | Both hosts used LACP bonds to the cores. |
| Direct-client regression tests · **3 of 4 passed** | Calibration, silent LACP and MAC move passed. Restoring a client link interrupted traffic for ≥2.39 s against a 1 s limit. | LACP was renegotiating when the link came back. |

Virtual links kept carrier during guest reboots. Disconnecting a root attachment dropped carrier at both ends. The final RSTP baseline passed after a management reset. [Routed first-hop redundancy](../../docs/reference/topologies.md#smallest-lab-for-each-question) remains untested.

## Reproduce

| Procedure | Check readiness | Run live | Dry run offline |
| --- | --- | --- | --- |
| [Wiring and pass criteria](../../docs/cases/medium-spanning-tree.md) | [Baseline commands](../../docs/operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) · [Measured readiness](../2026-11-24-medium-lab-readiness/README.md) | [External roots](../../docs/operator-guide.md#deploy-the-three-chr-medium-lab) · [Direct clients](../../docs/operator-guide.md#reboot-the-direct-client-pair) | [Replay the four STP-off reboots](../../docs/test-framework.md#replay-the-stp-off-reboots) |

## Evidence

[Per-flow timings](phase-loss.tsv) · [JUnit](junit.xml) · [STP-off JUnit](stp-disabled-junit.xml) · [Checksums](SHA256SUMS)

Capture archives include the configurations and timelines for each trial group.

