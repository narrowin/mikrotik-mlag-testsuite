# MLAG test cases

[Run cases in order by lab and ID](cases/README.md). This catalogue records the protocol coverage and supporting sources.

[Campaign coverage, remaining tests and reporting procedure](status-report.md)

**Start with a measured case.** Each entry gives the setup, fault, acceptance threshold and packet evidence. [Carrier withdrawal](cases/small-client-link.md) · [Primary reboot while the pair is STP root](cases/medium-core-reboot.md)

[Lab overview](../README.md) · [Full procedures and pass criteria](validation-plan.md) · [OrbStack postmortem](../results/2026-11-24-small-lab/postmortem.md)

**Field report** records an observed symptom. **Vendor fix or response** supplies an implementation detail, confirmation or changelog. **Standard** gives expected protocol behavior. **Lab design** identifies a test we derived from the proposed network, including independent controls, deliberate spanning-tree path changes, and site-wide outages. A combined label preserves both the original observation and the variations we added. The test plan names the affected configurations and the evidence needed for a verdict.

The initial discussion began with a four-switch RouterOS regression. Posts 133–137 describe later development builds and encouraging client-lab checks. Follow the exact posts below for the failure observations and the relevant vendor replies. [Original discussion](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137) · [Release context, post 133](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/133) · [Quick lab result, post 134](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/134) · [Scope of the result, post 137](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/137)

The small OrbStack campaign ran the announced single-attachment variant of MOVE-01, the two withdrawal methods in L2, and the guest-side peer-link cut in P1. The report identifies the variants and observed paths for each result. [Measured cases and raw evidence](../results/2026-11-24-small-lab/postmortem.md)

The Site A/Site B designs come from the two supplied sketches. The comparison of straight and crossed circuits is a lab design for DC-02, DC-03 and DC-06. The four-switch forwarding and packet-loss concerns have a direct operator precedent, including the observation that a member change alone could disrupt unrelated flows. [Site A/Site B designs and test order](plans/two-site-design.md) · [Four-switch CRS326 operator report](https://forum.mikrotik.com/t/two-interconnected-mlag-pairs-on-crs326-which-routeros-versions-are-stable/274258) · [Larsa’s interconnect advice, post 2](https://forum.mikrotik.com/t/two-interconnected-mlag-pairs-on-crs326-which-routeros-versions-are-stable/274258/2)

The last column tracks qualification on the active 7.26 build. **Open** means the catalogue variant still needs a dedicated verdict. **Partial** identifies narrower evidence. A measured failure is a completed observation.

## Baseline and protocol behavior

[Procedures and pass conditions](reference/protocol-cases.md#normal-forwarding-and-protocol-checks)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| BASE-01 | LACP startup and both legs carrying traffic | Standard | [Link aggregation](https://standards.ieee.org/ieee/802.1AX/6768/) | Partial · bond readiness [small suite](../results/2026-11-24-small-lab/reports/suite.json) |
| BASE-02 | VLAN-scoped MAC learning and isolation | Standard | [VLAN bridges](https://standards.ieee.org/ieee/802.1q/10323/) | Open |
| BASE-03 | Local forwarding, peer fallback and duplicate suppression | Vendor behavior | [RouterOS forwarding rules](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) | Open |
| BASE-04 | RSTP alternate path, logical LAG and MSTP roles | Standard and lab design | [Bridged networks](https://standards.ieee.org/ieee/802.1q/10323/) · [RouterOS MLAG and STP](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) | Partial · access switch as root [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |
| BASE-05 | VRRP elections and actual first-hop service | Standard and lab design | [VRRPv3 RFC 9568, sections 6.1 and 6.4](https://www.rfc-editor.org/rfc/rfc9568.html) · [RouterOS VRRP](https://manual.mikrotik.com/docs/cli-reference/interface/vrrp/) | Open |
| BASE-06 | End-to-end access, core and DCI acceptance | Lab design | Designed for this lab. | Open |

## MAC and IP mobility

[Procedures and pass conditions](reference/protocol-cases.md#vmotion-ip-and-mac-mobility)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| MOVE-01 | Same MAC/IP/VID moves across peers or bonds | Field report and lab variants | [Reported GARP and stale port](https://forum.mikrotik.com/t/mac-move-detection/271620) | Partial · announced move failed [small suite](../results/2026-11-24-small-lab/reports/suite.json) |
| MOVE-02 | Cross-site MAC move, silent and announced | Field report and lab variants | [Inter-pair move reports](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137?page=6) | Open |
| MOVE-03 | Service IP transfers to a different MAC | Standard and lab design | [IPv4 announcements](https://www.rfc-editor.org/rfc/rfc5227.html#section-2.3) · [IPv6 neighbor updates](https://www.rfc-editor.org/rfc/rfc4861.html#section-7.2.5) | Open |
| MOVE-04 | Renumbering versus moving a MAC to another VLAN | Lab design | Designed for this lab. | Open |
| MOVE-05 | Live vMotion and RARP on ESXi | Vendor procedure and field report | [Broadcom Notify Switches and RARP](https://knowledge.broadcom.com/external/article/343401/ip-to-mac-mapping-garp-rarp-and-notify-s.html) · [Broadcom capture and stale physical-switch mapping](https://knowledge.broadcom.com/external/article/318873/a-virtual-machine-loses-network-connecti.html) | Open |
| MOVE-06 | Repeated move, failed leg or remote peer rejoin | Field reports and lab variants | [Repeated migration field observations](https://forum.mikrotik.com/t/mac-move-detection/271620) · [Remote rejoin case](https://forum.mikrotik.com/t/mlag-what-happens-when-member-interface-joins/263166) | Open |

## MAC learning, peer forwarding and VLAN behavior

[Procedures and pass conditions](reference/protocol-cases.md#mac-learning-peer-forwarding-and-vlans)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| M1 | Stale MAC after GARP or migration | Field reports | [Proxmox MAC move](https://forum.mikrotik.com/t/mac-move-detection/271620) · [Inter-pair move](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137?page=6) | Partial · old-port unicast [small suite](../results/2026-11-24-small-lab/reports/suite.json) |
| M2 | Unicast floods while a moved VM still answers | Field reports | [Hyper-V migration and captures](https://forum.mikrotik.com/t/crs317-mlag-hyper-v-set-vm-connectivity-failures-after-migration-and-pfsense-carp-events/273728) · [Flooding with apparently correct FDB](https://forum.mikrotik.com/t/strange-traffic-flooding-in-mlag-setup/271419) | Open |
| M3 | Reboot leaves a stale peer-port entry | Field reports | [Post-reboot observation](https://forum.mikrotik.com/t/mlag-transmit-hash-policy/274432/8) · [SUP-228131 and SUP-228515](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/129) | Open |
| M4 | Unrelated FDB flush and CPU load after a member flap | Field reports | [Four-switch report](https://forum.mikrotik.com/t/7-25-1-stable-is-released/274226/22) · [Unrelated port](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/48) | Open |
| M5 | VLAN-specific loss, peer membership or broadcast setting | Field reports | [Per-VLAN observation](https://forum.mikrotik.com/t/bridging-hosts-not-forwarding/270143) · [Operator correction](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/115) · [7.25 changes](https://forum.mikrotik.com/t/7-25-stable-is-released/273987/1) | Open |
| M6 | Peer loss drops a dual-attached host or reflects traffic | Vendor fix and field report | [7.25.2 fixes](https://forum.mikrotik.com/t/7-25-2-stable-is-released/274638) · [Reflection follow-up](https://forum.mikrotik.com/t/solved-mlag-problem-packets-occasionally-reflected-back/160701) | Open |
| M7 | Long-running FDB notification pressure and watchdog | Field reports and vendor response | [CRS326 report and staff reply](https://forum.mikrotik.com/t/mlag-fdb-host-table-duplication/269518) · [Long-running degradation](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/77) | Open |

## Spanning tree and LACP

[Procedures and pass conditions](reference/protocol-cases.md#spanning-tree-and-lacp)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| S1 | Distant reboot disturbs forwarding between MLAG pairs | Field report with support reproduction | [Three-pair case](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/85) · [7.24.4 case](https://forum.mikrotik.com/t/mikrotik-m-lag/273578) | Open |
| S2 | BPDUs sent on the wrong bond or guard triggers | Vendor fix and field reports | [Guarded host report](https://forum.mikrotik.com/t/secondary-mlag-switch-sending-bpdus-on-edge-lacp-bond/273756) · [VLAN 1 follow-up](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/131) | Open |
| S3 | Unexpected root cost, blocked peer path or loop | Vendor fix and field reports | [Root observation](https://forum.mikrotik.com/t/mlag-and-spanning-tree-observation/265862) · [Peer-link reconvergence](https://forum.mikrotik.com/t/stp-on-mlag-peerlink/263388) · [Loop after reboot](https://forum.mikrotik.com/t/crs326-24s-2q-7-24-6-l2-loop-for-5-minutes-after-reboot-rstp-did-not-block-alternate-uplink/274427) | Open |
| S4 | RSTP/MSTP with independent uplinks and multiple instances | Field reports and lab variants | [MSTP field report](https://forum.mikrotik.com/t/mlag-mstp-take-down-entire-network-redundant-links-without-loops/182671) · [Separate inter-rack bonds](https://forum.mikrotik.com/t/mlag-vlan-filtering-rstp-breaks-everything/269081) | Open |
| L1 | LACP system-ID change and partner timeout at reboot | Vendor behavior and field reports | [System ID and staff response](https://forum.mikrotik.com/t/mlag-issue-mlag-functionality-flaps-lacp-system-id-of-secondary-when-primary-reboots/157426) · [Timer follow-up](https://forum.mikrotik.com/t/mlag-failover-2-minutes/273498) · [Catalyst behavior](https://forum.mikrotik.com/t/mlag-configuration-for-v7-22-1/269918) · [Fallback and initialization](https://manual.mikrotik.com/changelog/changelog-2026-10-22/) | Partial · primary reboot [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |
| L2 | Client-side versus switch-side loss of a member · [Carrier procedure and verdict](cases/small-client-link.md) | Field reports | [Existing CHR experiment](https://forum.mikrotik.com/t/mlag-client-lacp-failover-handling/272065) · [Cable outage](https://forum.mikrotik.com/t/mlag-the-traffic-can-no-longer-be-rerouted-after-the-cable-outage/266644) | Partial · member failure [small suite](../results/2026-11-24-small-lab/reports/suite.json) |
| L3 | Bond creation order and primary rejoin | Vendor fix and field report | [7.25.2 changes](https://forum.mikrotik.com/t/7-25-2-stable-is-released/274638) · [Failback field report](https://forum.mikrotik.com/t/mikrotik-mlag-saga/183339) | Open |
| L4 | Hash-specific loss, passive LACP or loss with carrier up | Field reports and lab variants | [Four-link report and passive-mode control](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137?page=4) · [Partner removed while carrier remained](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/43) | Open |

## Bridge modes by lab size

| Lab | Covered | Open |
| --- | --- | --- |
| Small lab | Original direct-client tests with RSTP. | STP disabled on both CHRs with the same wiring and faults. [Small lab plan](validation-plan.md#small-lab-bridge-mode-comparison) |
| Medium lab | Earlier three-CHR core-root and access-root evidence. | Matched STP-off and both RSTP root placements using the same dual-attached access switch. [Medium lab plan](validation-plan.md#matched-comparison-on-the-medium-lab) |
| Large lab | Full target layout and cases specified. | STP off on the verified loop-free layout, then RSTP with the same wiring. [Large lab plan](validation-plan.md#large-lab-bridge-mode-comparison) |

## Archived single-homed root experiments

| Case | Coverage | 7.26 qualification |
| --- | --- | --- |
| Medium lab baseline, STP off then RSTP | The historical test kept two single-homed root candidates connected in both modes. | Both all-off baselines passed. The named RSTP baseline failed and the runner withheld the fault. [DC1 readiness evidence](cases/medium-spanning-tree.md#archived-diagnostics) |
| External RSTP chassis reboots | Keep the preferred root on the survivor. Reboot each role after the RSTP baseline passes. | Earlier external-root trials failed for both roles on passing baselines. See the port, packet and timing evidence. |
| External root withdrawal and combined loss | Change the preferred attachment with both cores up, then combine withdrawal with a primary reboot. | Root-only fail on restoration state with no client loss. Both combined trials exceeded the withdrawal target. |
| Core-only STP disabled | Disable STP on the cores while the access switch and leaves retain RSTP. | Baseline failed on the access switch uplink. |
| All bridges STP disabled | Verify an all-off baseline and compare chassis recovery before introducing RSTP on the same wiring. | Both chassis roles passed both repeats. RSTP introduction subsequently reproduced a failed forwarding baseline. |

[Current three-CHR comparison](cases/medium-spanning-tree.md) · [Archived 7.26beta7 results](cases/medium-spanning-tree.md#archived-diagnostics)

## Whole-pair restart in DC1

Use the same DC1 links and probe hosts. Take both cores down, then run each restore order with STP off and with RSTP once its baseline passes. [Detailed procedure and scoring](validation-plan.md#both-dc1-cores-down-and-return)

| Case | What it checks | Status |
| --- | --- | --- |
| MLAG1 returns first | Can VLAN traffic resume with MLAG1 alone? Does MLAG2 rejoining cause another loss? | Open |
| MLAG2 returns first | Can VLAN traffic resume with MLAG2 alone? Does MLAG1 rejoining cause another loss? | Open |
| Both cores return together | When do stable forwarding, the peer session and both LACP members become ready? Does service drop again during convergence? | Open |

## Root-pair chassis cases

| Case | Coverage | Origin | 7.26 qualification |
| --- | --- | --- | --- |
| `reboot-secondary` | Reboot the observed secondary while the pair is root and compare both client directions. | [Historical Site A core 2 control](plans/primary-reboot-plan.md#recovered-tests-and-their-limits) | Pass · [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |
| `reboot-primary` | Reboot the observed primary and align BPDU, port, LACP and client transitions. | [Case procedure and measured result](cases/medium-core-reboot.md) | Fail · [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |
| `primary-sustained-stop` | Hold the guest stopped with virtual carrier up. Check the survivor after peer timeout and before resuming the primary. | [Chassis isolation decision](plans/primary-reboot-plan.md#how-to-interpret-the-evidence) | Fail · [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |
| `reboot-primary-no-fallback` | Run a paired reboot with `mlag-lacp-fallback=no`. | [RouterOS fallback behavior](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) | Fail · [root campaign](../results/2026-11-24-medium-lab-pair-root/README.md) |

[Runner and evidence](operator-guide.md#reboot-the-root-pair)

## First-hop redundancy, peer loss and edits

[Procedures and pass conditions](reference/protocol-cases.md#first-hop-split-brain-and-configuration-changes)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| G1 | VRRP master returns but VIP traffic fails | Field reports | [RB4011 failback and captures](https://forum.mikrotik.com/t/mlag-vrrp-failback-issue-vrrp-master-does-not-process-vip-traffic-after-recovery-rb4011-ros-7-22-1/269687) · [Partial application outage](https://forum.mikrotik.com/t/mlag-vrrp-not-functioning-together/184156) | Open |
| G2 | Remote core rejoins and interrupts a local gateway | Field report and replication design | [Two-site topology and second observation](https://forum.mikrotik.com/t/mlag-what-happens-when-member-interface-joins/263166) | Open |
| G3 | Passive firewall receives frames for the VRRP MAC | Field report with controlled comparison | [Reported traffic and controlled comparison](https://forum.mikrotik.com/t/mlag-frames-destined-for-vrrp-mac-are-received-by-the-passive-firewall/274190) | Open |
| P1 | Peer-link partition while both switches are up | Vendor response and lab variants | [MikroTik response on split-brain](https://forum.mikrotik.com/t/mlag-issue-mlag-functionality-flaps-lacp-system-id-of-secondary-when-primary-reboots/157426/8) | Partial · guest-side peer-link cut [postmortem](../results/2026-11-24-small-lab/postmortem.md) |
| P2 | Missed heartbeats and FDB sync log floods | Vendor fix and field reports | [7.25 log report](https://forum.mikrotik.com/t/7-25-stable-is-released/273987/36) · [SUP-228588](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/130) | Open |
| P3 | Bridge edits, peer restart and MTU mismatch | Vendor fixes and field reports | [7.24 release history](https://mikrotik.com/download/changelogs?channelFilter=stable&versionFilter=7.24) · [7.25 changes](https://forum.mikrotik.com/t/7-25-stable-is-released/273987/1) · [Jumbo-frame report](https://forum.mikrotik.com/t/2x-crs317-in-mlag-jumbo-frames-not-work/175282) | Open |

## Core and whole-site outage

[Procedures and pass conditions](reference/site-cases.md#core-and-data-center-outage-matrix)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| DC-01 | One access switch fails | Lab design | Designed for this lab. | Open |
| DC-02 | One core switch fails | Lab design | [Reported dependency on the failed core returning](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/100) | Open |
| DC-03 | One DCI member, then entire DCI, fails | Lab design | Designed for this lab. | Open |
| DC-04 | Both cores at one site fail | Lab design | Designed for this lab. | Open |
| DC-05 | An entire site fails and returns | Lab design | Designed for this lab. | Open |
| DC-06 | Crossed core failures under two DCI wirings | Lab design | Designed for this lab. | Open |
| DC-07 | Different rejoin orders and rolling update | Lab design | Designed for this lab. | Open |

## Physical hardware and deployment-specific cases

[Procedures and pass conditions](reference/site-cases.md#cases-that-require-physical-devices-or-a-specific-partner)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| H1 | CRS reflection and hardware offload changes | Vendor fix and field reports | [CRS8xx fix](https://forum.mikrotik.com/t/7-24-6-long-term-is-released/274207) · [Offload restart fix](https://forum.mikrotik.com/t/7-25-2-stable-is-released/274638) · [Solved throughput case](https://forum.mikrotik.com/t/solved-extremely-low-bandwidth-in-sfp28-mlag-setup/165580) | Open |
| H2 | FDB and CPU pressure on real hardware | Field report and lab controls | [CRS326 case](https://forum.mikrotik.com/t/mlag-fdb-host-table-duplication/269518) · [CRS317 storage-traffic report](https://forum.mikrotik.com/t/crs317-1g-16s-on-ros-7-22-2-heavy-cpu-after-mlag-bonding-for-proxmox-server/270148) | Open |
| H3 | Partner interoperability and in-band management | Field reports | [Catalyst case](https://forum.mikrotik.com/t/mlag-configuration-for-v7-22-1/269918) · [HP stack management loss](https://forum.mikrotik.com/t/mlag-issue-with-lacp-ports-on-hp-5130-stack/165500) · [Hyper-V SET/CARP](https://forum.mikrotik.com/t/crs317-mlag-hyper-v-set-vm-connectivity-failures-after-migration-and-pfsense-carp-events/273728) | Open |

## Optional service cases

[Procedures and pass conditions](reference/site-cases.md#additional-tests-when-the-service-uses-these-features)

| Case | Coverage | Origin | Direct evidence | 7.26 qualification |
| --- | --- | --- | --- | --- |
| X1 | IGMP snooping and receiver placement | Field report and lab design | [Snooping report](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/11) | Open |
| X2 | MVRP registration across MLAG bonds | Vendor release and lab design | [7.25 release](https://forum.mikrotik.com/t/7-25-stable-is-released/273987/1) | Open |
| X3 | Stacked VLAN PPPoE discovery return path | Field report | [Stacked-tag report](https://forum.mikrotik.com/t/crs326-with-mlag-and-bridge-vlan-filtering-with-qinqinq/174002) | Open |
| X4 | RPC replication fails despite ping and iperf | Field report | [RPC field report](https://forum.mikrotik.com/t/routeros-7-11-2-mlag-with-2-crs317-1g-16s-rpc-errors/170599) | Open |

## Additional MikroTik forum references

These posts provide context, alternative configurations, vendor follow-ups or corroboration used in the plan. The case rows above link to the evidence closest to the test trigger.

- [Larsa’s release context](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/133)
- [Quick lab result](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/134)
- [Linked reply](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/137)
- [Development release notes](https://forum.mikrotik.com/t/7-26beta-development-is-released/273582)
- [Starting discussion](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137)
- [Independent multi-pair discussion](https://forum.mikrotik.com/t/multiple-mlag-pairs/273236)
- [Four-device report, SUP-115519](https://forum.mikrotik.com/t/mlag-bridge-not-work-in-ros-7-7-7-8-7-9-ok-in-ros-7-6/166477)
- [Two-device comparison](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/2)
- [Support acknowledgement relayed by the reporter](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/4)
- [Passive/active control](https://forum.mikrotik.com/t/mlag-hopelessly-broken/167137/66)
