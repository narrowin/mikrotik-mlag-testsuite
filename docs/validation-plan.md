# MikroTik MLAG validation plan

Compare STP off and RSTP at each of three lab sizes. Within a lab, keep wiring, VLANs, LACP settings, probes and RouterOS image fixed. With RSTP enabled, vary root placement in separate trials.

[Deploy and run the lab](../README.md) · [Choose a case and find its source](case-catalog.md)

| Lab | STP off | RSTP on |
| --- | --- | --- |
| [1. Small lab](#small-lab-bridge-mode-comparison) | Disable STP on both CHRs. The matched run is open. | Original Small lab and direct-client reboots used RSTP. |
| [2. Medium lab](#matched-comparison-on-the-medium-lab) | Disable STP on both cores and the access switch. The matched run is pending. | Compare the core pair and access switch as root on the same wires. The earlier access-root trial failed its packet baseline. |
| [3. Large lab](#large-lab-bridge-mode-comparison) | Run the full Site A/Site B layout after verifying the logical Layer 2 topology is loop-free on each VLAN. Open. | Keep the same wiring and verify the intended root and forwarding ports. Open. |

| Start with | Question | Pass condition |
| --- | --- | --- |
| Timing calibration | Can the probes measure a two-second, one-way cut? | The measured bounds contain the applied cut. The reverse and unrelated flows stay clean. |
| [One bond member](cases/small-client-link.md) | Can the surviving leg carry the traffic, and does restoring the old leg interrupt service? | At most 1 s per phase on the affected path. |
| [Either chassis goes down and returns](#chassis-loss-and-return) | Can the surviving peer carry traffic while CHR 1 or CHR 2 is absent? Does bringing the failed peer back cause a second outage? | At most 5 s per phase in each VLAN direction. Verify forwarding while the target is still absent. The bypass loses zero probes. |
| [Both DC1 cores go down and return](#both-dc1-cores-down-and-return) | Can either core restore service alone, and does the second core’s return interrupt it? | Time the first and stable VLAN delivery after each return. The bypass stays up throughout. |
| [Access, core and two sites](plans/two-site-design.md) | Which local and remote services still have a path after a core or site failure? | Declare each flow as surviving or expected down for the particular wiring. Local controls at the surviving site stay clean. |

The time limits are lab service targets. Report the observed range, including a lower bound when the run ends before recovery. A capture gap or a missed sender interval can make a timing verdict inconclusive.

## Small lab bridge-mode comparison

Keep the original wiring with two CHRs, two directly bonded Linux clients, the MAC-move host and the independent bypass. Run the readiness check in each mode, then repeat both individual CHR reboots and the same carrier, silent LACP, peer-partition and MAC-move cases. Compare delivery, MAC learning and duplicate frames at the same capture points. [Small lab wiring](../labs/small/small.clab.yml)

For the planned whole-pair restart, stop both CHRs while the clients and bypass stay up. Restore CHR 1 first, CHR 2 first and both together in separate runs. Measure first stable delivery and any second gap as the other CHR rejoins. This establishes whether the direct clients can recover through either CHR alone after a cold start.

The original saved startup configs use RSTP. The later direct-client reboot captures read back RSTP on both CHRs, and the current direct-client runner sets `protocol-mode=rstp` before each case. The archived five-CHR STP-off evidence uses different wiring. The Small lab still needs an STP-off readiness check and fault runs on its own wiring. [Original Small lab captures](../results/2026-11-24-small-lab/README.md#verify-the-result) · [Direct-client reboot and regression archives](cases/medium-spanning-tree.md#archived-diagnostics)

## Matched comparison on the Medium lab

Use the same three CHRs, VLAN 110, probe hosts and bypass in all modes. The access switch has one LACP member to each core and is the single external RSTP root candidate. Host 1 uses that access path. Host 2 has its own bond directly to the core pair. [Current wiring](../labs/medium/medium.clab.yml) · [Inventory](../labs/medium/README.md)

1. **STP off.** Set `protocol-mode=none` on both cores and the access switch. Require zero BPDUs and one copy of each broadcast.
2. **RSTP, core pair as root.** Verify the shared core root ID and the access uplink’s operation.
3. **RSTP, access switch as root.** Give the access switch the best priority. Verify the elected root and both directions of VLAN traffic.

Require at least 30 deliveries per direction with zero loss or duplicates during the baseline before injecting a fault. The earlier access-root trial elected the access switch but failed VLAN delivery. STP-off evidence from the five-CHR diagnostic fixture remains archived. The matched comparison on the revised wiring is pending. [Run commands](operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) · [Earlier access-root evidence](cases/medium-spanning-tree.md)

## Chassis loss and return

Test **`dc1-core-mlag2` (`p2`) and `dc1-core-mlag1` (`p1`) separately** in each mode that passes the DC1 baseline. Record the actual MLAG roles and keep a clean baseline between targets. The direct-client and pair-root labs below are controls with their own wiring and evidence.

| Trial | Fault and return | How to run it |
| --- | --- | --- |
| Reboot each DC1 core with STP off | Reboot each core from a clean baseline. Keep both access-switch members wired. | `medium-stp-off-reboot-secondary` and `medium-stp-off-reboot-primary`. [Commands](operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) |
| Reboot each DC1 core with RSTP on | Repeat with each root placement after its packet baseline passes. | `medium-access-root-reboot-secondary` and `medium-access-root-reboot-primary`, or the `medium-pair-root-*` equivalents. [Commands](operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) |
| Reboot each CHR with direct clients | Reboot the secondary and then the primary in separate trials. Keep the virtual cables in place and record the carrier seen by the other ends. Watch the client path while the guest is down and after it boots. | `direct-reboot-secondary` and `direct-reboot-primary`. [Commands](operator-guide.md#reboot-the-direct-client-pair) |
| Reboot each core with an access switch | Reboot each peer while the pair is the RSTP root. Probe through the access switch to see when its uplink and the survivor forward. Compare with the access switch as root on the same wiring. | `reboot-secondary` and `reboot-primary`. [Pair-root commands](operator-guide.md#reboot-the-root-pair) · [External-root variants](cases/medium-spanning-tree.md) |
| Hold a guest down with carrier up | Pause the guest and keep the virtual links up. Hold the stop past peer timeout to see whether the survivor forwards before the guest resumes. | The runner has `primary-sustained-stop` for a hold of at least 35 s. The matching secondary hold is planned. [Existing procedure](operator-guide.md#reboot-the-root-pair) |
| Hold a CHR down with carrier lost | Stop CHR 1, confirm carrier down on every data link facing it, and hold it absent. Boot it again and observe the links and service returning. Repeat from a clean baseline with CHR 2. | Planned CHR comparison. The existing `carrier` case changes one bond member with both guests running. [Member case](cases/small-client-link.md) |
| Remove power from each physical switch | On the isolated bench, remove power from one chassis and verify the peer link and all attached data links go down at their surviving ends. Hold it off long enough to observe steady forwarding through the survivor, then restore power and record its boot and rejoin. Repeat for the other chassis. | Planned physical qualification. Log switch model, RouterOS and RouterBOARD firmware, ports and optics. Keep the survivor, traffic endpoints and capture system powered independently. [Physical test scope](reference/site-cases.md#cases-that-require-physical-devices-or-a-specific-partner) |

For each run, keep 100 ms probes going in both VLAN and both bypass directions. Timestamp the confirmed chassis loss, first and stable delivery while it is still absent, confirmed boot or resume, link and LACP recovery, and any second traffic gap on rejoin. Record MLAG state and spanning-tree port roles on the access switch when RSTP is active. Apply the 5 s budget independently to loss and return. If traffic never recovers during the hold, record that fact and the measured lower bound. [How to score outages](reference/measurement.md#provisional-pass-criteria)

[Saved direct-client reboot measurements](cases/medium-spanning-tree.md#archived-diagnostics) · [Saved pair-root reboot and held-stop measurements](../results/2026-11-24-medium-lab-pair-root/README.md#development-726beta7)

## Both DC1 cores down and return

These cases cover a full restart of the DC1 MLAG pair. Both cores go down while the access switch, both probe hosts, syslog collector and management observer stay running. Verify both cores are absent and record carrier on the surviving link ends. Expect the VLAN path to be unavailable during the overlap and the independent bypass to stay clean. Preserve the cabling and record whether the outage was a guest stop, a guest boot or a verified loss of carrier.

| Restore order | What to measure |
| --- | --- |
| `dc1-core-mlag1` first | Keep `dc1-core-mlag2` absent. Does VLAN service return through MLAG1 alone? Record first and stable delivery in each direction and the active LACP and bridge ports. Then return MLAG2 and measure any second gap. |
| `dc1-core-mlag2` first | Repeat from a clean baseline, keeping MLAG1 absent until MLAG2 has had the same observation window. Measure service on MLAG2 alone and again as MLAG1 rejoins. |
| Both cores together | Start both in the same action window and record actual start and boot times. Measure first and stable VLAN delivery, when both bonds and the peer session are ready, and whether traffic drops again as the pair converges. |

Do all three orders in the all-off mode first, then for both RSTP root placements after their baselines pass. For staggered return, hold the other core down through a recorded window that includes the effective MLAG initialization delay and time to verify steady traffic. Report if forwarding waited for both cores. Time recovery from each start command, note when links and forwarding became eligible, and report the outage while both were absent separately. Verify stable VLAN delivery and both members after full rejoin. The single-core 5 s outage budget is tracked separately from full boot-to-service time.

Status for these three DC1 cases is open. The current CLI has single-core reboot selectors. The two-site catalogue also has the larger [both-core and rejoin cases DC-04 and DC-07](reference/site-cases.md#core-and-data-center-outage-matrix).

## Large lab bridge-mode comparison

Use the Site A/Site B layout with core and distribution pairs, a DCI, and one VRRP-enabled CHR firewall per site. Each firewall has one LACP cable to each local core and the pair shares a VIP on isolated VLAN 390. Bond each service host to both local distribution switches. Probe the access-local Layer 2 path and the firewall VIP independently. When both cores at one site go down, its clients lose the VIP path while the access-local control can stay up. Choose one set of physical members per bond and keep it in both bridge modes. Before the STP-off run, verify each test VLAN is loop-free. Independent same-VLAN Layer 2 uplinks have their own RSTP experiment.

After each mode passes its baseline, repeat the same link, core, firewall, DCI and site faults. Measure VIP delivery through takeover, failback and core rejoin. Check the VRRP owners after DCI isolation and after the shared VLAN is restored. Keep local Layer 2 probes at both sites. Under RSTP, also capture the elected root and port transitions. The complete Large lab setup and both matched runs remain open. [Full layout](plans/two-site-design.md#target--local-distribution-and-firewall-vrrp) · [Site outage matrix](reference/site-cases.md#core-and-data-center-outage-matrix)

## RouterOS version for live tests

Qualify the latest **7.26 development** build first. Other releases follow after this suite and its reporting work end to end. Use **one RouterOS build for each campaign**, across all test cases, controls, repeats and CI jobs. At the start of the campaign, check the latest **development** release from MikroTik. As of 24 November 2026 that is **7.26beta7**. Pin the version and image digest and record what actually ran. A Stable run or a mixed-version upgrade test requires a separate request. Existing results remain available for offline replay. [MikroTik development releases](https://mikrotik.com/download/changelogs?channelFilter=development) · [Deploy the pinned build](operator-guide.md#reboot-the-root-pair)

## Detailed procedures

- [Sources and test methods](reference/research.md)

- [Topology selection](reference/topologies.md)

- [Measurement and acceptance criteria](reference/measurement.md)

- [Protocol and mobility tests](reference/protocol-cases.md)

- [Site outages, hardware and optional services](reference/site-cases.md)
