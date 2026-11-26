# SMALL-03 · Client link loss and return

![Small lab wiring and scenarios, with c1 eth1 to p1 ether3 marked as the member under test](../diagrams/small-lab.png)

[Editable drawing · Small lab tab](../diagrams/mlag-scenarios.drawio) · [Carrier verdict and packet timeline](../diagrams/README.md#small-lab-evidence)

| | Case `carrier` · catalogue L2 |
| --- | --- |
| Setup | Two CHRs, two dual-homed clients, the Linux MAC-move host and an independent bypass. The host stays on one attachment for this trial and exchanges probes with both clients. Verify both client bonds carry traffic. |
| Fault | Withdraw client 1’s link to CHR 1 on both the Linux interface and the QEMU NIC. Restore it with the probes still running. |
| Expected | Both drivers confirm each change within 0.5 s. Graded streams 101, 201 and 302 each lose at most **3 s** on withdrawal and **3 s** on restoration. Control streams 102 and 202 between client 2 and the MAC-move host, and bypass streams 301 and 303, lose zero probes. Zero probes addressed to client 1 should leave on the confirmed withdrawn leg. |
| Measured | **Fail on restoration**, both repeats on RouterOS 7.26beta7. These archived runs were graded against an earlier 1 s limit per phase. The catalogue now sets 3 s per phase. Withdrawal recovered within 0.22 s. Restoration loss bounds across affected flows ranged from **2.18 to 2.52 s**. Client 2 and the bypass stayed clean. |

Open the timeline beside the verdict. Compare the first packet on the restored member with both partners’ collecting and distributing flags. The time a link gains carrier and the time a client receives replies are separate observations. [First verdict](../../results/2026-11-24-small-lab/reports/01-carrier/result.json) · [First timeline](../../results/2026-11-24-small-lab/reports/01-carrier/timeline.tsv) · [Second verdict](../../results/2026-11-24-small-lab/reports/02-carrier/result.json)

[Run this case](../../labs/small/README.md#deploy) · [Original member-loss reports](../case-catalog.md#spanning-tree-and-lacp)
