# MEDIUM-03 and MEDIUM-04 Core reboots with the MLAG pair as root

## What this test checks

Two CHRs, CHR 1 and CHR 2, form an MLAG pair. They act as the two core switches. Together they are the RSTP root bridge, which is the bridge that the spanning tree is built around.

An access switch sits between client A and the two cores. It has one cable to each core, and the two cables form one LACP bond. Client B has its own bond with one cable to each core.

This test reboots one core and measures how long traffic between client A and client B stops. It runs once with the MLAG secondary, CHR 2, and once with the MLAG primary, CHR 1. The reboot of the MLAG secondary is the control.

The wiring is in the [pair-root topology file](../../labs/medium/medium-pair-root.clab.yml). The [Medium lab bridge-mode comparison](medium-spanning-tree.md) runs the same reboots in other spanning-tree modes.

## Why it is needed

An earlier test on a real network rebooted each core of Site A. Rebooting Site A core 1 stopped traffic for **12 s when it went down and 12 s when it came back**. That core was the MLAG primary and the STP root. Rebooting Site A core 2 stopped traffic for **1 to 2 s** each time. The working note of that test blamed spanning tree for the longer stop. The [working note and its origin](../plans/primary-reboot-plan.md#recovered-tests-and-their-limits) are summarised in the test plan.

This lab repeats that reboot with RouterOS CHRs and captures every step.

## The test in detail

| | |
| --- | --- |
| Name | The test runner calls the two cases `reboot-secondary` and `reboot-primary`. |
| Lab | CHR 1 and CHR 2 are the MLAG peers. The peer link, which is the cable between the two MLAG peers, joins them. Both peers use bridge priority `0x1000`. The access switch uses priority `0x8000`. Client A connects to the access switch. Client B has a bond to both cores. A direct cable between client A and client B bypasses all switches. |
| Before the fault | The test checks that both MLAG peers report the same root bridge ID. It checks that CHR 1 is the MLAG primary and CHR 2 the MLAG secondary. It checks that the access switch sees the same root and forwards on its uplink bond. The pings on the direct cable keep running during the whole test. |
| Order | The test first measures a 2 s cut on the direct cable. This proves that it measures loss correctly. It then reboots the MLAG secondary. It waits until the baseline is back and checks it again. It then reboots the MLAG primary with the same wiring, timers and traffic. |
| Fault | The test reboots the selected CHR with `/system reboot`. |

The test measures the stop after the core goes down and the stop after it comes back separately. In the result files the first is the phase `withdrawal`. The second is the phase `restoration`.

## What must happen

- While the rebooted core is away, the other core must carry traffic in both directions.
- Stream 101 from client A to client B and stream 201 in the other direction may each stop for at most **5 s** after the core goes down. Each may stop for at most **5 s** after it comes back.
- The pings on the direct cable between the clients, streams 301 and 303, must lose **no** ping.
- After the rebooted core has joined again, check which peer is the MLAG primary. The report shows the role of each peer.

## What was measured

On RouterOS 7.26beta7, **both reboots of the MLAG primary failed after the primary went down. Both reboots of the MLAG secondary passed.**

In each primary reboot, the clients got traffic back for a short time and then lost it again. In that second stop, traffic from client A to client B was lost for **11.654 to 11.858 s** in the first run and **10.722 to 10.928 s** in the second run. Each range is the shortest and the longest stop that the captured pings allow. After the primary came back, traffic stopped for more than 5 s in the first run only.

The captures of the CHRs show this order of events.

1. Traffic first kept using the bond member toward the rebooted core. LACP still counted that member as usable.
2. Later the bond of the surviving core toward the access switch stopped forwarding. The capture names this bond `witness-bond`.
3. After the primary came back, the bond members became usable again. The `uplink` bond of the access switch still stayed in the discarding state.

The [results of each traffic direction and the port timeline](../../results/2026-11-24-medium-lab-pair-root/README.md#results) are in the pair-root results.

## How to read the evidence

Run this case on the pair-root topology only. After a run, open `01-reboot-primary/result.json` in the suite directory. The file `timeline.tsv` in the same folder lists every event in time order. The JUnit report names each failed check and its phase.

- [Results of each traffic direction and the port timeline](../../results/2026-11-24-medium-lab-pair-root/README.md#results)
- [Commands to deploy the lab and run the case](../operator-guide.md#reboot-the-root-pair)

Use the latest RouterOS development build for new runs. The [version policy](../validation-plan.md#routeros-version-for-live-tests) explains this rule.
