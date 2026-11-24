"""What each case does, its phases, the expected behaviour and the pass limits.

The evaluator reads its limits from here and report writers read the expected behaviour, so the
graded limit and the documented expectation cannot drift apart.
"""

from dataclasses import dataclass

MLAG_MANUAL = "https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/"
BOND_FLAGS = "https://manual.mikrotik.com/docs/cli-reference/interface/bonding/monitor-slaves/"
LACP_STANDARD = "https://standards.ieee.org/ieee/802.1AX/6768/"
LAB_TARGET = "lab target"
# A calibration is valid only when the applied one-way cut lies inside this window.
CALIBRATION_CUT_S = (1.9, 2.3)
PHASE_KEYS = ("baseline", "calibration", "withdrawal", "restoration")


@dataclass(frozen=True)
class Phase:
    key: str
    name: str
    expected: str
    limit_s: float | None
    source: str


@dataclass(frozen=True)
class Case:
    name: str
    lab: str
    title: str
    action: str
    selectors: tuple[str, ...]
    graded_flows: tuple[int, ...]
    control_flows: tuple[int, ...]
    phases: tuple[Phase, ...]

    def limit(self, key):
        return next(phase.limit_s for phase in self.phases if phase.key == key)


STEADY = Phase(
    "baseline", "Steady state",
    "Both MLAG peers show mlag-state connected, one as MLAG primary and one as MLAG secondary, and use the "
    "primary's system ID as the shared system ID. Each client bonds both members and every probe arrives once.",
    0.0, MLAG_MANUAL)
CALIBRATION = Phase(
    "calibration", "2 s one-way cut",
    "Only the bypass stream between the two clients loses probes, and its measured gap contains the applied "
    "1.9–2.3 s cut. The bypass does not cross the MLAG peers, so every other stream loses nothing.",
    None, LAB_TARGET)

SMALL_VLAN = (101, 102, 201, 202, 302)
BYPASS = (301, 303)

# Test order: the Small lab first, then Medium, then Large.
CASES = (
    Case('baseline', 'Small', 'Baseline readiness',
         'Applies the bridge mode on both MLAG peers, waits for MLAG and LACP to settle, checks MLAG, LACP and the virtual links, and sends numbered pings for 4 s without a fault.',
         ('direct-baseline',), (101, 201), (301, 303),
         (STEADY,)),
    Case('calibration', 'Small', 'Calibration',
         'Drops the forward bypass pings at client 2 for 2 s with a tc filter while seven numbered ping streams run, then removes the filter.',
         ('calibrate',), (301,), (101, 102, 201, 202, 302, 303),
         (CALIBRATION,)),
    Case('bond-member-loss', 'Small', 'MLAG bond member loss and return',
         "Takes client 1's bond member to CHR 1 (ether3) down at both ends, holds it down for 8 s, then brings both ends back up.",
         ('carrier',), (101, 201, 302), (102, 202, 301, 303),
         (Phase('withdrawal', 'Member down',
              "Carrier drops at both ends, so CHR 1's MLAG bond client1 (mlag-id=11) stops using ether3 and client 1 sends only on its member to CHR 2. CHR 1 forwards traffic for client 1 over the peer link (mlag-peer-port ether2) to CHR 2, which delivers it on its member of the same MLAG bond, with brief loss.",
              1.0, MLAG_MANUAL),
         Phase('restoration', 'Member back',
              'Carrier returns at both ends and LACP renegotiates ether3 with client 1 at the 1-second LACPDU rate. Each end carries traffic on the member only once its LACP flags show synchronization, collecting and distributing (S, C, D), so the return causes at most brief loss.',
              1.0, BOND_FLAGS),)),
    Case('lacp-timeout', 'Small', 'LACP partner timeout and return',
         "Blocks client 1's LACPDUs towards CHR 1 on ether3 for 8 s while carrier stays up, then lets them through again.",
         ('silent-lacp',), (101, 201, 302), (102, 202, 301, 303),
         (Phase('withdrawal', 'LACPDUs blocked',
              "Carrier stays up, but CHR 1 receives no LACPDUs on ether3. With lacp-rate=1sec, CHR 1's partner information expires after the 3 s short timeout: ether3 shows expired (E) and stops collecting and distributing, and traffic for client 1 moves to its member on CHR 2, crossing the peer port where needed.",
              4.0, LACP_STANDARD),
         Phase('restoration', 'LACPDUs resumed',
              "Client 1's LACPDUs reach CHR 1 again, so ether3 has current partner information and clears the expired (E) and defaulted (F) flags. The member returns to synchronization, collecting and distributing (S, C, D) in the MLAG bond, with brief loss.",
              1.0, BOND_FLAGS),)),
    Case('mac-move', 'Small', 'MAC move between MLAG peers and back',
         "Switches the MAC-move host's active-backup bond from its link to CHR 1 to its link to CHR 2, keeping the same MAC and IP address, then switches it back after 4 s.",
         ('mobile-move',), (101, 102, 201, 202), (301, 302, 303),
         (Phase('withdrawal', 'Move to CHR 2',
              "The host's gratuitous ARP enters CHR 2 on ether5, a regular bridge port without mlag-id. CHR 2 moves the host MAC to ether5 in its bridge host table and floods the broadcast to its local ports and over the peer port; CHR 1 floods it only to its regular port ether5 and moves the MAC to the peer port ether2. Lab target: no probe to or from the host is lost, and once the gratuitous ARP reaches CHR 2, no frame addressed to the host MAC leaves CHR 1 on ether5.",
              0.0, LAB_TARGET),
         Phase('restoration', 'Move back to CHR 1',
              "The host's gratuitous ARP enters CHR 1 on ether5. CHR 1 moves the host MAC back to ether5 and floods the broadcast to its local ports and over the peer port; CHR 2 floods it only to its regular port ether5 and moves the MAC to the peer port ether2. Lab target: no probe to or from the host is lost, and from the moment the gratuitous ARP reaches CHR 1 to the end of the recovery window, no frame addressed to the host MAC leaves CHR 2 on ether5.",
              0.0, LAB_TARGET),)),
    Case('reboot-calibration', 'Small', 'Calibration before reboots',
         'Runs the baseline check, then drops the forward bypass pings at client 2 for 2 s with a tc filter while four numbered ping streams run.',
         ('direct-calibrate',), (301,), (101, 201, 303),
         (CALIBRATION,)),
    Case('secondary-reboot', 'Small', 'MLAG secondary reboot',
         'Resets the bridge on CHR 1 and CHR 2 over management SSH with protocol-mode=rstp, picks the MLAG peer that reports mlag-state connected as secondary, and after a loss-free baseline reboots it with `/system reboot` (1 s delay). The runner waits for the guest uptime to reset, then keeps probing for 16 s plus a 3 s recovery window.',
         ('direct-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'The MLAG primary keeps the shared system ID, so both traffic hosts keep their LACP partner and forward over their bond member to the primary, which delivers locally without the peer port. The virtual links keep carrier, so each host drops its member to the secondary only at the LACP short timeout (3 × 1 s). Only traffic hashed to that member sees brief loss.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'The rejoining secondary keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with the primary (mlag-init-delay, default 1 min), then adds them under the unchanged shared system ID. The MLAG bonds client1 and client2 are edge ports and forward at once, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('primary-reboot', 'Small', 'MLAG primary reboot',
         'Resets the bridge on CHR 1 and CHR 2 over management SSH with protocol-mode=rstp, picks the MLAG peer that reports mlag-state connected as primary, and after a loss-free baseline reboots it with `/system reboot` (1 s delay). The runner waits for the guest uptime to reset, then keeps probing for 16 s plus a 3 s recovery window.',
         ('direct-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "The MLAG secondary reverts its MLAG bonds to its own LACP system ID (mlag-lacp-fallback=yes) and both traffic hosts renegotiate LACP, with brief loss. The virtual links keep carrier, so each host drops its member to the primary only at the LACP short timeout (3 × 1 s). The secondary's edge MLAG bonds keep forwarding throughout.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'The rebooted peer keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. Both traffic hosts renegotiate LACP to the shared system ID, with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case('medium-stp-off-baseline', 'Medium', 'Baseline · all bridges STP off',
         'Reset the data bridge on all three CHRs over management SSH with protocol-mode=none (priority 0x1000 on both MLAG peers, 0x8000 on the access switch). Then run numbered 100 ms pings for 4 s in both VLAN 110 directions and both bypass directions, read back bridge, MLAG and LACP state, and send three ARP broadcasts each way. No fault is applied.',
         ('medium-stp-off-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              'Both MLAG peers show mlag-state connected once ICCP is established, with CHR 1 as MLAG primary (lower mlag-priority) and CHR 2 as MLAG secondary. Every bond member of the MLAG bonds and of the access switch uplink is synchronized, collecting and distributing. With protocol-mode=none no bridge sends or forwards BPDUs, each ARP broadcast arrives exactly once, and all four streams deliver with zero loss.',
              0.0, 'https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/#mlag-settings-and-monitoring'),)),
    Case('medium-pair-root-baseline', 'Medium', 'Baseline · RSTP, MLAG pair as root',
         'Reset the data bridge on all three CHRs over management SSH with protocol-mode=rstp, priority 0x1000 on both MLAG peers and 0x8000 on the access switch. Then run numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions and read back bridge, MLAG, RSTP and LACP state. No fault is applied.',
         ('medium-pair-root-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              "Both MLAG peers are connected and use the MLAG primary's system ID as the shared RSTP bridge ID, so both show as root bridge with root ID 0x1000.02:00:00:21:00:11. The access switch picks its non-edge uplink bond as root port and all VLAN 110 ports forward. RSTP BPDUs from that root reach the access switch, and all four streams deliver with zero loss.",
              0.0, MLAG_MANUAL),)),
    Case('medium-access-root-baseline', 'Medium', 'Baseline · RSTP, access switch as root',
         'Reset the data bridge on all three CHRs over management SSH with protocol-mode=rstp, priority 0x1000 on both MLAG peers and 0x0000 on the access switch. Then run numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions and read back bridge, MLAG, RSTP and LACP state. No fault is applied.',
         ('medium-access-root-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              'The access switch has the lowest bridge priority (0x0000), so every bridge elects it as RSTP root with root ID 0x0000.02:00:00:21:00:13. The connected MLAG peers present one shared bridge ID toward it. The non-edge MLAG bond access-uplink and all VLAN 110 ports forward, and all four streams deliver with zero loss.',
              0.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/user-guides/spanning-tree-protocol/#election-process'),)),
    Case('external-baseline', 'Medium', 'Baseline · RSTP, external root r2 (archived five-CHR)',
         'Archived five-CHR run, replay only. The runner reset all five bridges over management SSH with protocol-mode=rstp, priority 0x0000 on r2 and 0x1000 on r1, then ran the 4 s numbered-ping window in both VLAN 110 and both bypass directions and read back bridge, MLAG, RSTP and LACP state. No fault is applied.',
         ('external-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              'Every bridge elects the preferred external root r2, which has the lowest priority (root ID 0x0000.02:00:00:21:00:15). r1 runs as backup with bridge ID 0x1000.02:00:00:21:00:14. CHR 2 uses ether5 as root port, CHR 1 uses the peer port ether2 and the access switch uses its uplink bond. MLAG is connected, all VLAN 110 ports forward and all four streams deliver with zero loss.',
              0.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/user-guides/spanning-tree-protocol/#election-process'),)),
    Case('external-no-stp-baseline', 'Medium', 'Baseline · STP off on MLAG peers only (archived five-CHR)',
         'Archived five-CHR run, replay only. The runner reset all five bridges over management SSH with protocol-mode=none on both MLAG peers and rstp on the access switch, r1 and r2 (r2 0x0000, r1 0x1000). It then ran the 4 s numbered-ping window, read back state and sent three ARP broadcasts each way. No fault is applied.',
         ('external-no-stp-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              'With protocol-mode=none and forward-reserved-addresses=no, the MLAG peers neither send BPDUs nor pass the BPDUs of r1, r2 or the access switch, while r1 and r2 keep sending their own. MLAG is connected and all LACP bond members are synchronized, collecting and distributing. Each ARP broadcast arrives once and all four streams deliver with zero loss.',
              0.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/#bridge-interface-setup'),)),
    Case('external-all-stp-off-baseline', 'Medium', 'Baseline · all bridges STP off (archived five-CHR)',
         'Archived five-CHR run, replay only. The runner reset all five bridges over management SSH with protocol-mode=none, then ran the 4 s numbered-ping window in both VLAN 110 and both bypass directions, read back state and sent three ARP broadcasts each way. No fault is applied.',
         ('external-all-stp-off-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              'With protocol-mode=none on all five bridges, no BPDU appears on any captured port. MLAG is connected and the bond members of both MLAG bonds are synchronized, collecting and distributing. Each ARP broadcast arrives exactly once, so the dual-attached access switch bond forms no loop, and all four streams deliver with zero loss.',
              0.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/#bridge-interface-setup'),)),
    Case('root-calibrate', 'Medium', 'One-way calibration · RSTP, MLAG pair as root (pair-root deployment)',
         "On the dedicated pair-root deployment, which keeps its startup RSTP config with no bridge reset, the runner verifies the baseline. It then adds a tc ingress filter on host 2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s, removes it, and observes 3 s of settling and a 3 s recovery window.",
         ('root-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('medium-stp-off-calibrate', 'Medium', 'One-way calibration · all bridges STP off',
         "After the protocol-mode=none bridge reset and baseline gate, the runner adds a tc ingress filter on host 2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and observes 3 s of settling and a 3 s recovery window.",
         ('medium-stp-off-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('medium-pair-root-calibrate', 'Medium', 'One-way calibration · RSTP, MLAG pair as root',
         "After the RSTP pair-root bridge reset and baseline gate, the runner adds a tc ingress filter on host 2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and observes 3 s of settling and a 3 s recovery window.",
         ('medium-pair-root-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('medium-access-root-calibrate', 'Medium', 'One-way calibration · RSTP, access switch as root',
         "After the RSTP access-root bridge reset and baseline gate, the runner adds a tc ingress filter on host 2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and observes 3 s of settling and a 3 s recovery window.",
         ('medium-access-root-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('external-calibrate', 'Medium', 'One-way calibration · RSTP, external root r2 (archived five-CHR)',
         "Archived five-CHR run, replay only. After the RSTP bridge reset (r2 preferred root) and baseline gate, the runner dropped bypass-forward echo requests (stream 301) at host 2's eth3 ingress with a tc filter for 2 s. It then removed the filter and observed 3 s of settling and a 3 s recovery window.",
         ('external-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('external-no-stp-calibrate', 'Medium', 'One-way calibration · STP off on MLAG peers only (archived five-CHR)',
         "Archived five-CHR selector, replay only. After the bridge reset (protocol-mode=none on the MLAG peers, rstp elsewhere) and baseline gate, the runner drops bypass-forward echo requests (stream 301) at host 2's eth3 ingress with a tc filter for 2 s. It then removes the filter and observes 3 s of settling and a 3 s recovery window.",
         ('external-no-stp-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('external-all-stp-off-calibrate', 'Medium', 'One-way calibration · all bridges STP off (archived five-CHR)',
         "Archived five-CHR run, replay only. After the protocol-mode=none reset of all five bridges and the baseline gate, the runner dropped bypass-forward echo requests (stream 301) at host 2's eth3 ingress with a tc filter for 2 s. It then removed the filter and observed 3 s of settling and a 3 s recovery window.",
         ('external-all-stp-off-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('external-root-loss', 'Medium', 'Preferred STP root attachment loss and return · RSTP, r2 on CHR 2 (archived five-CHR)',
         "Archived five-CHR run, replay only. With both MLAG peers up, the runner took the preferred root r2's attachment to CHR 2 ether5 down at both ends (r2's Linux eth1 plus the QEMU NIC link on both guests) and held it down for 35 s. It then brought the attachment up and observed 16 s plus a 3 s recovery window.",
         ('external-root-loss',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Root attachment down',
              'CHR 2 loses carrier on ether5 and, with it, its root port. RSTP elects the backup root r1, next-lowest priority (0x1000.02:00:00:21:00:14), on r1, both MLAG peers and the access switch, while both MLAG peers stay up. VLAN 110 traffic between the hosts does not cross r1 or r2, so it sees at most brief loss.',
              5.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/user-guides/spanning-tree-protocol/#stp-example'),
         Phase('restoration', 'Root attachment back',
              "Carrier returns on r2 ether2 and CHR 2 ether5. r2's superior BPDUs (priority 0x0000) make every bridge re-elect r2 as root, and RSTP returns the point-to-point non-edge ports to forwarding within seconds. By the end of the recovery window every baseline port, including r2 ether2, forwards again.",
              5.0, 'https://manual.mikrotik.com/docs/bridging-and-switching/user-guides/spanning-tree-protocol/#stp-and-rstp'),)),
    Case('external-combined-loss', 'Medium', 'MLAG primary reboot with preferred root attachment loss · RSTP, r1 on CHR 1 (archived five-CHR)',
         "Archived five-CHR run, replay only. The runner took the preferred root r1's attachment to CHR 1 ether5 down at both ends, then rebooted CHR 1 (MLAG primary) with /system reboot. When CHR 1's uptime reset was first observed it brought the attachment back up, then observed 16 s plus a 3 s recovery window.",
         ('external-combined-loss',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary and root attachment down',
              'The MLAG secondary CHR 2 loses ICCP and, with mlag-lacp-fallback=yes, reverts its MLAG bonds to its own LACP system ID. The access switch and host 2 renegotiate LACP with brief loss. RSTP elects the backup root r2 (0x1000.02:00:00:21:00:15), attached to CHR 2 ether5, on CHR 2, r2 and the access switch.',
              5.0, 'https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/#mlag-settings-and-monitoring'),
         Phase('restoration', 'Primary and root attachment back',
              "CHR 1's dual-connected bond members stay out of the MLAG bonds until the MLAG system ID syncs (mlag-init-delay=1m). CHR 1 then rejoins as MLAG primary, the shared system ID is restored and the LACP partners renegotiate with brief loss. r1's superior BPDUs return on CHR 1 ether5 and every bridge re-elects r1 as root.",
              5.0, 'https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/#mlag-settings-and-monitoring'),)),
    Case('medium-stp-off-reboot-secondary', 'Medium', 'MLAG secondary reboot · Medium lab, all bridges STP off',
         'Resets all three bridges over management SSH with protocol-mode=none. It requires a loss-free probe baseline, zero BPDUs and one copy of each broadcast. It then reboots CHR 2 (MLAG secondary, mlag-priority=20) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-stp-off-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              "CHR 1 (MLAG primary) keeps the shared system ID, so the access switch's uplink bond and traffic host 2 keep their LACP partner and forward over their members to CHR 1. The virtual links keep carrier, so each partner drops its member to CHR 2 only at the LACP short timeout (3 × 1 s). With protocol-mode=none no port changes state and no BPDUs appear.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'CHR 2 keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with CHR 1 (mlag-init-delay), then adds them under the unchanged shared system ID. The access switch and traffic host 2 re-add the member to the same aggregator, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('medium-pair-root-reboot-secondary', 'Medium', 'MLAG secondary reboot · Medium lab, RSTP, MLAG pair as root',
         "Resets all three bridges over management SSH with protocol-mode=rstp, priority 0x1000 on CHR 1 and CHR 2 and 0x8000 on the access switch. It requires a loss-free baseline with root ID 0x1000.02:00:00:21:00:11 in the access switch's BPDUs. It then reboots CHR 2 (MLAG secondary) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-pair-root-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'CHR 1 keeps the shared system ID, which is both the RSTP bridge ID and the LACP system ID, so the access switch still sees root 0x1000.02:00:00:21:00:11 and its uplink stays the forwarding root port. The virtual links keep carrier, so the access switch and traffic host 2 drop their member to CHR 2 at the LACP short timeout (3 × 1 s). Only traffic hashed to that member sees brief loss.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              "CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. The root ID and the access switch's forwarding uplink do not change, so loss is brief or none.",
              5.0, MLAG_MANUAL),)),
    Case('medium-access-root-reboot-secondary', 'Medium', 'MLAG secondary reboot · Medium lab, RSTP, access switch as root',
         'Resets all three bridges over management SSH with protocol-mode=rstp, priority 0x1000 on CHR 1 and CHR 2 and 0x0000 on the access switch. It requires a loss-free baseline with the access switch as root (0x0000.02:00:00:21:00:13). It then reboots CHR 2 (MLAG secondary) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-access-root-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'CHR 1 keeps the shared system ID, so the access switch keeps its LACP partner and stays RSTP root. The MLAG pair keeps access-uplink as its forwarding root port. The virtual links keep carrier, so the access switch and traffic host 2 drop their member to CHR 2 at the LACP short timeout (3 × 1 s), with brief loss on traffic hashed to it.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              "CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. The access switch stays root, and CHR 2's non-edge access-uplink must reach forwarding without a further outage.",
              5.0, MLAG_MANUAL),)),
    Case('reboot-secondary', 'Medium', 'MLAG secondary reboot · RSTP, MLAG pair as root, pair-root control topology',
         "Uses the pair-root deployment (medium-pair-root.clab.yml) with its startup configuration and no bridge reset. It verifies CHR 1 as MLAG primary and CHR 2 as MLAG secondary, both as RSTP root 0x1000.02:00:00:21:00:11, and the access switch's uplink as forwarding root port. It then reboots CHR 2 with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'CHR 1 keeps the shared system ID, which is both the RSTP bridge ID and the LACP system ID, so the access switch still sees root 0x1000.02:00:00:21:00:11 and its uplink stays the forwarding root port. The virtual links keep carrier, so the access switch and traffic host 2 drop their member to CHR 2 at the LACP short timeout (3 × 1 s). Only traffic hashed to that member sees brief loss.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              "CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. The root ID and the access switch's forwarding uplink do not change, so loss is brief or none.",
              5.0, MLAG_MANUAL),)),
    Case('external-reboot-secondary', 'Medium', 'MLAG secondary reboot · archived five-CHR lab, RSTP, single-homed roots r1/r2',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner reset all bridges with protocol-mode=rstp, root bridge r1 (priority 0x0000) on CHR 1 ether5 and backup r2 (0x1000) on CHR 2 ether5. It then rebooted CHR 2 (MLAG secondary) with `/system reboot` and probed for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'CHR 1 keeps the shared system ID, so the access switch and traffic host 2 keep their LACP partner and drop the member to CHR 2 at the LACP short timeout (3 × 1 s). Root bridge r1 is attached to the surviving CHR 1, and CHR 1, the access switch and r1 must keep r1 as RSTP root throughout the absence.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. r1 stays RSTP root, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('external-no-stp-reboot-secondary', 'Medium', 'MLAG secondary reboot · archived five-CHR lab, STP off on the MLAG peers only',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner set protocol-mode=none on CHR 1 and CHR 2 and rstp on the access switch, r1 and r2 (r2 preferred, priority 0x0000). It would then reboot CHR 2 (MLAG secondary) with `/system reboot` and probe for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-no-stp-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              "CHR 1 keeps the shared system ID, so the access switch and traffic host 2 keep their LACP partner and drop the member to CHR 2 at the LACP short timeout (3 × 1 s). The MLAG peers run protocol-mode=none and pass no BPDUs, so the access switch's RSTP uplink must keep forwarding.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. Loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('external-all-stp-off-reboot-secondary', 'Medium', 'MLAG secondary reboot · archived five-CHR lab, all bridges STP off',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner reset all five bridges with protocol-mode=none, then rebooted CHR 2 (MLAG secondary) with `/system reboot` and probed for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-all-stp-off-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'CHR 1 keeps the shared system ID, so the access switch and traffic host 2 keep their LACP partner and drop the member to CHR 2 at the LACP short timeout (3 × 1 s). All five bridges run protocol-mode=none, so no port changes state and no BPDUs appear.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'CHR 2 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), then adds them under the unchanged shared system ID. Loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('medium-stp-off-reboot-primary', 'Medium', 'MLAG primary reboot · Medium lab, all bridges STP off',
         'Resets all three bridges over management SSH with protocol-mode=none. It requires a loss-free probe baseline, zero BPDUs and one copy of each broadcast. It then reboots CHR 1 (MLAG primary, mlag-priority=10) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-stp-off-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              'CHR 2 reverts its MLAG bonds to its own LACP system ID, so the access switch and traffic host 2 renegotiate LACP, with brief loss. The virtual links keep carrier, so they drop the member to CHR 1 only at the LACP short timeout (3 × 1 s). With protocol-mode=none no port changes state and no BPDUs appear.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. The access switch and traffic host 2 renegotiate LACP to the shared system ID, with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case('medium-pair-root-reboot-primary', 'Medium', 'MLAG primary reboot · Medium lab, RSTP, MLAG pair as root',
         "Resets all three bridges over management SSH with protocol-mode=rstp, priority 0x1000 on CHR 1 and CHR 2 and 0x8000 on the access switch. It requires a loss-free baseline with root ID 0x1000.02:00:00:21:00:11 in the access switch's BPDUs. It then reboots CHR 1 (MLAG primary) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-pair-root-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. The MLAG pair must stay RSTP root (0x1000 against 0x8000), and CHR 2's access-uplink and the access switch's uplink must keep forwarding.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay). It rejoins as MLAG primary and restores the shared system ID as LACP system ID and RSTP bridge ID, and partners renegotiate LACP with brief loss. The access switch must again see root 0x1000.02:00:00:21:00:11 with its uplink forwarding.',
              5.0, MLAG_MANUAL),)),
    Case('medium-access-root-reboot-primary', 'Medium', 'MLAG primary reboot · Medium lab, RSTP, access switch as root',
         'Resets all three bridges over management SSH with protocol-mode=rstp, priority 0x1000 on CHR 1 and CHR 2 and 0x0000 on the access switch. It requires a loss-free baseline with the access switch as root (0x0000.02:00:00:21:00:13). It then reboots CHR 1 (MLAG primary) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-access-root-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. The access switch must stay RSTP root, and CHR 2's access-uplink must keep forwarding as root port.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID, and partners renegotiate LACP with brief loss. The access switch stays root, and access-uplink must return to forwarding on both MLAG peers.',
              5.0, MLAG_MANUAL),)),
    Case('reboot-primary', 'Medium', 'MLAG primary reboot · RSTP, MLAG pair as root, pair-root control topology',
         "Uses the pair-root deployment (medium-pair-root.clab.yml) with its startup configuration and no bridge reset. It verifies CHR 1 as MLAG primary and CHR 2 as MLAG secondary, both as RSTP root 0x1000.02:00:00:21:00:11, and the access switch's uplink as forwarding root port. It then reboots CHR 1 with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. The MLAG pair must stay RSTP root (0x1000 against 0x8000), and CHR 2's access-uplink and the access switch's uplink must keep forwarding.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay). It rejoins as MLAG primary and restores the shared system ID as LACP system ID and RSTP bridge ID, and partners renegotiate LACP with brief loss. The access switch must again see root 0x1000.02:00:00:21:00:11 with its uplink forwarding.',
              5.0, MLAG_MANUAL),)),
    Case('primary-sustained-stop', 'Medium', 'MLAG primary paused 35 s with carrier up · RSTP, MLAG pair as root, pair-root control topology',
         "On the pair-root deployment, pauses CHR 1's QEMU vCPUs with QMP stop, confirms the paused status and holds for 35 s while every virtual link keeps carrier. It then resumes CHR 1 with QMP cont and keeps probing for 16 s plus a 3 s recovery window.",
         ('primary-sustained-stop',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary paused',
              'The access switch and traffic host 2 drop their member to the paused CHR 1 at the LACP short timeout (3 × 1 s). CHR 2 must detect the lost MLAG peer over ICCP while the peer port keeps carrier, take over with its own LACP system ID and keep VLAN 110 forwarding before CHR 1 resumes.',
              5.0, LAB_TARGET),
         Phase('restoration', 'Primary resumed',
              'CHR 1 resumes without a reboot, so mlag-init-delay does not apply. ICCP must return to connected with CHR 1 as MLAG primary and the shared system ID, with at most brief loss while partners re-add or renegotiate the member.',
              5.0, LAB_TARGET),)),
    Case('reboot-primary-no-fallback', 'Medium', 'MLAG primary reboot with mlag-lacp-fallback=no · RSTP, MLAG pair as root, pair-root control topology',
         'On the pair-root deployment, verifies mlag-lacp-fallback=yes on both MLAG peers, sets it to no on both and waits for the pair-root baseline. It then reboots CHR 1 (MLAG primary) with `/system reboot` and keeps probing for 16 s after the uptime reset plus a 3 s recovery window. Afterward it restores mlag-lacp-fallback=yes.',
         ('reboot-primary-no-fallback',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              'With mlag-lacp-fallback=no, CHR 2 keeps the shared MLAG system ID, so the access switch and traffic host 2 do not renegotiate LACP. The virtual links keep carrier, so they drop the member to CHR 1 at the LACP short timeout (3 × 1 s) and continue over CHR 2.',
              5.0, 'https://manual.mikrotik.com/docs/cli-reference/interface/bridge/'),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay) and rejoins as MLAG primary. The shared system ID never changed, so partners re-add the member without renegotiation and loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('external-reboot-primary', 'Medium', 'MLAG primary reboot · archived five-CHR lab, RSTP, single-homed roots r1/r2',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner reset all bridges with protocol-mode=rstp, root bridge r2 (priority 0x0000) on CHR 2 ether5 and backup r1 (0x1000) on CHR 1 ether5. It then rebooted CHR 1 (MLAG primary) with `/system reboot` and probed for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              'CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. Root bridge r2 is attached to the surviving CHR 2, and CHR 2, the access switch and r2 must keep r2 as RSTP root throughout the absence.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID, and partners renegotiate LACP with brief loss. r2 stays RSTP root.',
              5.0, MLAG_MANUAL),)),
    Case('external-no-stp-reboot-primary', 'Medium', 'MLAG primary reboot · archived five-CHR lab, STP off on the MLAG peers only',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner set protocol-mode=none on CHR 1 and CHR 2 and rstp on the access switch, r1 and r2 (r2 preferred, priority 0x0000). It would then reboot CHR 1 (MLAG primary) with `/system reboot` and probe for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-no-stp-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. The MLAG peers run protocol-mode=none and pass no BPDUs, so the access switch's RSTP uplink must keep forwarding through the renegotiation.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. Partners renegotiate LACP with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case('external-all-stp-off-reboot-primary', 'Medium', 'MLAG primary reboot · archived five-CHR lab, all bridges STP off',
         'Archived replay only, because the current runner rejects external-* selectors. The retired five-CHR runner reset all five bridges with protocol-mode=none, then rebooted CHR 1 (MLAG primary) with `/system reboot` and probed for 16 s after the uptime reset plus a 3 s recovery window.',
         ('external-all-stp-off-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              'CHR 2 reverts its MLAG bonds to its own LACP system ID and the access switch and traffic host 2 renegotiate LACP, with brief loss. All five bridges run protocol-mode=none, so no port changes state and no BPDUs appear.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. Partners renegotiate LACP with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case("peer-link-loss", "Small", "Peer link loss and return",
         "Cuts the peer link (ether2) at both MLAG peers, holds it down for 15 s, restores it and watches 65 s of "
         "return.",
         ("peer-link-loss",), SMALL_VLAN, BYPASS,
         (Phase("withdrawal", "Peer link down",
                "Both MLAG peers lose ICCP and leave mlag-state connected. With mlag-lacp-fallback=yes the MLAG "
                "secondary stops using the shared system ID, so the clients renegotiate LACP and keep their member "
                "to the primary, with brief loss.", 5.0, MLAG_MANUAL),
          Phase("restoration", "Peer link back",
                "ICCP returns to mlag-state connected on both peers and the secondary takes the shared system ID "
                "again. The clients renegotiate LACP with brief loss.", 5.0, MLAG_MANUAL))),
    # Planned: listed in the case index, not yet runnable.

    Case("primary-pause", "Small", "MLAG primary held stopped with carrier up",
         "Pause the MLAG primary's QEMU guest for at least 35 s while its virtual links keep carrier, then "
         "resume it. Runs today only in the Medium pair-root lab as primary-sustained-stop.", (), (), (), ()),
    Case("primary-reboot-no-fallback", "Small", "MLAG primary reboot with mlag-lacp-fallback=no",
         "Set mlag-lacp-fallback=no on both MLAG peers, reboot the MLAG primary, then restore the setting. "
         "Runs today only in the Medium pair-root lab as reboot-primary-no-fallback.", (), (), (), ()),
    Case("peer-down-carrier-lost", "Small", "MLAG peer held down with carrier lost",
         "Stop CHR 1, confirm carrier is down on every data link facing it, hold it absent, then boot it. "
         "Repeat with CHR 2.", (), (), (), ()),
    Case("both-peers-down", "Small", "Both MLAG peers down and return",
         "Stop both CHRs, then restore CHR 1 first, CHR 2 first, or both together in separate runs. "
         "Measure service on one peer alone and again when the second peer rejoins.", (), (), (), ()),
    Case("iccp-loss", "Small", "ICCP loss with the peer link up",
         "Drop only ICCP frames (EtherType 0x88b5) on the peer link while tagged VLAN traffic still crosses it, "
         "then allow them again.", (), (), (), ()),
    Case("medium-both-peers-down", "Medium", "Both MLAG peers down and return with the access switch",
         "Stop both cores while the access switch, hosts and observers keep running. Restore core 1 first, "
         "core 2 first, or both together in separate runs, in each bridge mode.", (), (), (), ()),
    Case("large-baseline", "Large", "Two-site baseline and calibration",
         "Verify forwarding at both sites and across the interconnect, then calibrate the probes with a 2 s cut. "
         "Catalogue BASE-06.", (), (), (), ()),
    Case("large-interconnect-member-loss", "Large", "Interconnect member loss and return",
         "Remove one member of the inter-site MLAG bond, then restore it. Catalogue L2.", (), (), (), ()),
    Case("large-chassis-loss", "Large", "Access or core chassis loss, including crossed failures",
         "Lose one access or core chassis at a time, then crossed pairs across the sites. "
         "Catalogue DC-01, DC-02 and DC-06.", (), (), (), ()),
    Case("large-site-cores-down", "Large", "Both cores at one site down and return",
         "Stop both core MLAG peers at one site, then restore them in each order. Catalogue DC-04 and DC-07.",
         (), (), (), ()),
    Case("large-interconnect-partition", "Large", "Interconnect partition and restoration",
         "Cut every inter-site member while all local peer links stay up, then restore them. Catalogue DC-03.",
         (), (), (), ()),
    Case("large-site-loss", "Large", "Whole-site loss and restoration",
         "Stop every device at one site while the other keeps running, then restore it core first and, on a "
         "fresh run, access first. Catalogue DC-05.", (), (), (), ()),
)


def _index(cases):
    index = {}
    for case in cases:
        keys = tuple(phase.key for phase in case.phases)
        if not case.selectors and not keys:
            continue  # Planned case: listed in the index, not yet runnable.
        if keys not in (("baseline",), ("calibration",), ("withdrawal", "restoration")):
            raise ValueError(f"{case.name}: unsupported phases {keys}")
        if set(case.graded_flows) & set(case.control_flows):
            raise ValueError(f"{case.name}: a flow is both graded and a control")
        for selector in {case.name, *case.selectors}:
            if selector in index:
                raise ValueError(f"Selector {selector} appears in more than one case")
            index[selector] = case
    return index


BY_SELECTOR = _index(CASES)
BY_NAME = {case.name: case for case in CASES}


def case_spec(selector):
    """The case for a descriptive name or an internal runner selector."""
    try:
        return BY_SELECTOR[selector]
    except KeyError:
        raise ValueError(f"No case specification for {selector!r}") from None


def _flow_loss(flow, key, single):
    gaps = [gap for gap in flow["gaps"] if single or key in gap["phases"]]
    if not single and "phase_gaps_s" in flow:
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in flow["phase_gaps_s"].get(key, [])]
    else:
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in gaps]
    if not spans:
        return None
    return {"lower_s": max(lower for lower, _ in spans),
            "upper_s": None if any(upper is None for _, upper in spans) else max(upper for _, upper in spans),
            "lost_probes": sum(gap["failed_probes"] for gap in gaps),
            # Without split bounds, an outage crossing the restore is reported whole in both phases.
            "spans_both_phases": not single and "phase_gaps_s" not in flow
                                 and any(len(gap["phases"]) > 1 for gap in gaps)}


def _loss(flows, idents, key, single):
    loss = {}
    for ident in idents:
        flow = flows.get(ident) or flows.get(str(ident))
        if flow and (measured := _flow_loss(flow, key, single)):
            loss[str(ident)] = measured
    return loss


def phase_results(spec, result, checks):
    """Measured loss and a verdict for each phase of one attempt.

    A phase fails on a failed check tagged with it; any untagged evidence error invalidates every phase.
    A single-phase case takes every check as its own.
    """
    single = len(spec.phases) == 1
    executed = result.get("fault_executed", True)
    flows = result.get("flows", {})
    run_error = any(not c["ok"] and c["level"] in ("error", "inconclusive") and "phase" not in c for c in checks)
    summary = []
    for phase in spec.phases:
        own = checks if single else [c for c in checks if c.get("phase") == phase.key]
        failed = {c["level"] for c in own if not c["ok"]}
        if phase.key != "baseline" and not executed:
            verdict = "skipped"
        elif run_error or failed & {"error", "inconclusive"}:
            verdict = "error"
        elif "fail" in failed:
            verdict = "fail"
        else:
            verdict = "pass"
        loss = _loss(flows, spec.graded_flows, phase.key, single)
        summary.append({
            "key": phase.key, "name": phase.name, "expected": phase.expected, "source": phase.source,
            "limit_s": phase.limit_s, "window_s": None if single else result.get("phases_s", {}).get(phase.key),
            "verdict": verdict,
            "worst_loss_s": ({"lower_s": max(v["lower_s"] for v in loss.values()),
                              "upper_s": None if any(v["upper_s"] is None for v in loss.values())
                              else max(v["upper_s"] for v in loss.values()),
                              "lost_probes": max(v["lost_probes"] for v in loss.values()),
                              "spans_both_phases": any(v["spans_both_phases"] for v in loss.values())}
                             if loss else None),
            "loss_s": loss,
            "control_loss_s": _loss(flows, spec.control_flows, phase.key, single),
            "failed_checks": [c["detail"] for c in own if not c["ok"]],
        })
    return summary
