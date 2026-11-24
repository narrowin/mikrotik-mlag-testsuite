# MLAG campaign coverage

**24 November 2026.** The runner covers the Small and three-CHR Medium topologies. The Medium cases compare STP off and both RSTP root placements on the same wiring. Single-homed root runs are archived for replay. Count qualification by catalogue ID, topology and fault variant. [Case catalogue](case-catalog.md) · [Runner selectors](../src/mlag_lab/cli.py)

## Where we are

[Plain-English result of the primary reboot test](../results/2026-11-24-medium-lab-pair-root/README.md#short-answer-on-726beta7)

| Campaign | Saved verdict | Evidence |
| --- | --- | --- |
| Small pair on 7.26beta7 | Eight attempts. Both calibrations passed. The MAC move, member restoration and silent-LACP cases each failed a network assertion twice. Zero evidence errors. A separate exploratory run also cut the peer link. | [Suite results](../results/2026-11-24-small-lab/reports/suite.json) · [Peer-link and member postmortem](../results/2026-11-24-small-lab/postmortem.md) |
| Pair as RSTP root on 7.26beta7 | Both secondary reboots passed. Both primary reboots exceeded the five-second target while the primary was down. The surviving switch blocked traffic first, then the downstream switch blocked the uplink during rejoin. | [Development JUnit](../results/2026-11-24-medium-lab-pair-root/development-junit.xml) · [Timeline and diagnosis](../results/2026-11-24-medium-lab-pair-root/README.md) |
| Primary held stopped and fallback disabled | During separate 35-second stops with carrier up, service recovered briefly and failed again until the primary resumed. Disabling LACP fallback in a separate reboot still exceeded the outage target. | [Root campaign report and archives](../results/2026-11-24-medium-lab-pair-root/README.md) · [Per-flow measurements](../results/2026-11-24-medium-lab-pair-root/phase-loss.tsv) |
| Archived five-CHR external roots on 7.26beta7 | The initial and management-reset baselines passed. Both chassis roles exceeded the five-second target on the access-switch path. | [External campaign](cases/medium-spanning-tree.md#archived-diagnostics) |
| Archived five-CHR bridges off on 7.26beta7 | Both chassis roles passed twice. Reintroducing RSTP on the same wiring reproduced a non-forwarding baseline. | [Matched comparison](cases/medium-spanning-tree.md#archived-diagnostics) |
| Direct-client pair on 7.26beta7 | Both chassis role checks passed with RSTP on the cores. The four original Small lab cases then yielded three passes and one carrier restoration failure. | `final-runs-evidence.tar.gz` (saved campaign bundle) |

## What to do next

Use the [matched all-bridges-off and RSTP comparison](test-framework.md#compare-forwarding-with-and-without-spanning-tree) to qualify chassis forwarding before testing gateway failover and the rest of the matrix.

| Batch | Cases to qualify | Coverage gap |
| --- | --- | --- |
| 1. Finish the small topologies | BASE-01–04, MOVE-01/03/04/06 and applicable M, S, L and P variants | First compare the measured carrier-up primary stop with a sustained primary loss that signals carrier down on all failed chassis links. Verify every surviving neighbor sees the intended link state. Then cover VLAN-scoped learning, old-port forwarding, independent RSTP uplinks and peer partition/rejoin. |
| 2. Add first-hop routing and a second pair | BASE-05/06, G1–G3 and inter-pair M/S/L variants | Check VRRP ownership and routed service in both directions. Keep local controls running through access/core failover and restoration. |
| 3. Add the second site | MOVE-02, cross-site MOVE-06, DC-01–07 | Compare the two- and four-member interconnects. Test individual and crossed core loss, DCI partition, whole-site loss, and return order. Predeclare which local services must survive. |
| 4. Use the required platform or service | MOVE-05, H1–H3, X1–X4 and remaining deployment-specific variants | Use ESXi for live vMotion and physical switches for optics, real carrier propagation, ASIC forwarding and hardware load. Schedule optional services only where deployed. |

## Reporting

Use the [report template](../results/REPORT-TEMPLATE.md) for each campaign. The README leads with setup and the verdicts. Link per-attempt results, JUnit and captures for the measurements by build, repeat, direction and phase. Use the catalogue to track coverage, including withheld, unimplemented and hardware-only cases. [Qualification procedure](reference/measurement.md#procedure-for-every-run)
