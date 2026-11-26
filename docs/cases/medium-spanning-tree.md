# Medium lab spanning-tree comparison

![Medium lab with one access switch connected to both cores, which can be made the RSTP root](../diagrams/medium-lab.png)

## What this test checks

The Medium lab has two cores, CHR 1 and CHR 2, which form an MLAG pair. An access switch has one cable to each core, and the two cables form one LACP bond. Traffic host 1 reaches the cores through this access switch. Traffic host 2 has its own bond with one cable to each core. A direct cable between the two hosts bypasses all switches.

The test reboots one core at a time and measures how long traffic between the two hosts stops. It runs the same reboots in three spanning-tree modes on the same wiring.

- Spanning tree is off on all three bridges.
- RSTP is on, and the MLAG pair is the root bridge.
- RSTP is on, and the access switch is the root bridge.

The wiring is in the [Containerlab topology file](../../labs/medium/medium.clab.yml).

## Why it is needed

A comparison only means something if the wiring stays the same and only the spanning-tree mode changes. In this lab the access switch is the only bridge outside the MLAG pair that can become the root. The archived five-CHR lab further down had two separate root bridges, each with a single cable to the pair.

## The test in detail

| | |
| --- | --- |
| Lab | All devices stay connected in all three modes. The cabling and the root configuration do not change during a fault. |
| Before the fault | Each mode must first pass its own baseline. The table below lists what each baseline checks. |
| Order | After the baseline passes, the test measures a 2 s cut on the direct cable. This proves that it measures loss correctly. It then reboots each core in a separate run. |
| Fault | The test reboots one core. |

| Mode | What the baseline checks |
| --- | --- |
| Spanning tree off | All three bridges report `protocol-mode=none`. Both bonds carry traffic. No bridge sends BPDUs. Each broadcast arrives exactly once. |
| RSTP with the MLAG pair as root | Both cores have the same bridge priority. Both report the same root bridge ID. BPDUs reach the access switch. VLAN traffic passes in both directions. |
| RSTP with the access switch as root | The access switch has the best bridge priority. All three bridges report the access switch as root. VLAN traffic passes in both directions. |

A later case takes both cores down. It runs once with core 1 booting first, once with core 2 booting first, and once with both booting together. This case is still planned. The [plan for both cores down](../validation-plan.md#both-dc1-cores-down-and-return) describes it.

The [operator guide](../operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) has the commands for all three modes.

## What must happen

- In each baseline, the two hosts must lose no ping.
- After a core goes down, traffic between the two hosts may stop for at most **5 s** in each direction. The same limit applies after the core comes back.
- The pings on the direct cable must lose no ping.

The [list of cases](README.md#medium-lab) names the case of each mode and step.

## What was measured

### Archived diagnostics

These results come from earlier labs with other wiring. They describe that wiring only.

- In the earlier three-CHR trial, both cores accepted the access switch as root. Neither VLAN direction delivered any of its 62 pings.
- The five-CHR diagnostic lab had two root bridges, each with a single cable to the MLAG pair. With spanning tree off, the reboots of the MLAG primary and of the MLAG secondary passed in two runs each.
- In the same five-CHR lab with RSTP, one baseline run failed because VLAN traffic did not pass. The test then did not reboot any core.
- Earlier five-CHR runs with RSTP had passed their baseline. Their reboots of the MLAG primary and of the MLAG secondary stopped traffic for more than 5 s.

## How to read the evidence

The saved runs of the five-CHR lab stay with the local campaign evidence. They are not published. The section [Read or replay a run](../test-framework.md#read-or-replay-a-run) explains how to score a saved run again.
