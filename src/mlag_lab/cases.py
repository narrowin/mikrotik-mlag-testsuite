"""What each case does, its phases, the expected behaviour and the pass limits.

The evaluator reads its limits from here and report writers read the expected behaviour, so the
graded limit and the documented expectation cannot drift apart.
"""

from dataclasses import dataclass, replace

MLAG_MANUAL = "https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/"
BOND_FLAGS = "https://manual.mikrotik.com/docs/cli-reference/interface/bonding/monitor-slaves/"
LACP_STANDARD = "https://standards.ieee.org/ieee/802.1AX/6768/"
LAB_TARGET = "lab target"
# Loss limits per phase. MikroTik documents only "brief packet loss" for LACP renegotiation. With
# lacp-rate=1sec the LACP short timeout is 3 s (IEEE 802.1AX), and a Linux 802.3ad client waits 2 s
# (AD_AGGREGATE_WAIT_TIME) before it adds a returning member, so member and LACP changes get 3 s,
# the LACP timeout itself 4 s, and reboots and the peer link 5 s.
# A calibration is valid only when the applied one-way cut lies inside this window.
CALIBRATION_CUT_S = (1.9, 2.3)
# Longest time a unicast stream may reach an unrelated host after a fault: the M1 lab budget of 1 s in
# docs/reference/protocol-cases.md.
FLOOD_LIMIT_S = 1.0
PHASE_KEYS = ("baseline", "calibration", "withdrawal", "restoration")
BRIDGE_MANUAL = "https://manual.mikrotik.com/docs/cli-reference/interface/bridge/"
# M2: unicast flooded to unrelated hosts while the bridge host tables looked right.
FLOODING_REPORT = "https://forum.mikrotik.com/t/strange-traffic-flooding-in-mlag-setup/271419"
# M4: one member of the bond between two MLAG pairs flapped and unrelated MACs moved to the peer port.
FOUR_SWITCH_REPORT = "https://forum.mikrotik.com/t/7-25-1-stable-is-released/274226/22"
# mac-age-relearn: ageing-time while the MAC-move host is silent, the RouterOS default it returns to, a silence of
# more than twice the ageing time, the return window and the relearn target from the host's first frame.
MAC_AGE_TIME, MAC_AGE_DEFAULT = "10s", "5m"
MAC_AGE_SILENCE_S, MAC_AGE_RETURN_S = 25, 5
RELEARN_LIMIT_S = 1.0
# member-flap-repeat: five cycles of 1 s down and 3 s up.
FLAP_CYCLES, FLAP_DOWN_S, FLAP_UP_S = 5, 1, 3


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
    # MikroTik fixes this case checks: (RouterOS version, MikroTik's changelog wording, changelog link).
    # Filled from docs/reference/mlag-fixes.md, rows in state Checked or Indirect only.
    fixes: tuple[tuple[str, str, str], ...] = ()

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

# Campus option 1 in the Medium lab: spanning tree stops at the access switch's uplink.
CORE_OFF_RESET = ("Resets the data bridge on all three CHRs over management SSH: protocol-mode=none and "
                  "forward-reserved-addresses=no on both MLAG peers, protocol-mode=rstp priority=0x0000 on the access "
                  "switch, with edge=yes on its uplink bond and edge=yes, bpdu-guard=yes and loop-protect=on on its "
                  "host port ether4, and reads the access switch port settings back.")
CORE_OFF_SOURCE = "https://manual.mikrotik.com/docs/bridging-and-switching/user-guides/spanning-tree-protocol/"

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
              3.0, MLAG_MANUAL),
         Phase('restoration', 'Member back',
              'Carrier returns at both ends and LACP renegotiates ether3 with client 1 at the 1-second LACPDU rate. Each end carries traffic on the member only once its LACP flags show synchronization, collecting and distributing (S, C, D), so the return causes at most brief loss.',
              3.0, BOND_FLAGS),)),
    Case('lacp-timeout', 'Small', 'LACP partner timeout and return',
         "Blocks client 1's LACPDUs towards CHR 1 on ether3 for 8 s while carrier stays up, then lets them through again.",
         ('silent-lacp',), (101, 201, 302), (102, 202, 301, 303),
         (Phase('withdrawal', 'LACPDUs blocked',
              "Carrier stays up, but CHR 1 receives no LACPDUs on ether3. With lacp-rate=1sec, CHR 1's partner information expires after the 3 s short timeout: ether3 shows expired (E) and stops collecting and distributing, and traffic for client 1 moves to its member on CHR 2, crossing the peer port where needed.",
              4.0, LACP_STANDARD),
         Phase('restoration', 'LACPDUs resumed',
              "Client 1's LACPDUs reach CHR 1 again, so ether3 has current partner information and clears the expired (E) and defaulted (F) flags. The member returns to synchronization, collecting and distributing (S, C, D) in the MLAG bond, with brief loss.",
              3.0, BOND_FLAGS),)),
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
         'Resets the bridge on CHR 1 and CHR 2 over management SSH with the bridge mode of the run, picks the MLAG peer that reports mlag-state connected as secondary, and after a loss-free baseline reboots it with `/system reboot` (1 s delay). The runner waits for the guest uptime to reset, then keeps probing for 16 s plus a 3 s recovery window.',
         ('direct-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              'The MLAG primary keeps the shared system ID, so both traffic hosts keep their LACP partner and forward over their bond member to the primary, which delivers locally without the peer port. The virtual links keep carrier, so each host drops its member to the secondary only at the LACP short timeout (3 × 1 s). Only traffic hashed to that member sees brief loss.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'The rejoining secondary keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with the primary (mlag-init-delay, default 1 min), then adds them under the unchanged shared system ID. The MLAG bonds client1 and client2 are edge ports and forward at once, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('primary-reboot', 'Small', 'MLAG primary reboot',
         'Resets the bridge on CHR 1 and CHR 2 over management SSH with the bridge mode of the run, picks the MLAG peer that reports mlag-state connected as primary, and after a loss-free baseline reboots it with `/system reboot` (1 s delay). The runner waits for the guest uptime to reset, then keeps probing for 16 s plus a 3 s recovery window.',
         ('direct-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "The MLAG secondary reverts its MLAG bonds to its own LACP system ID (mlag-lacp-fallback=yes) and both traffic hosts renegotiate LACP, with brief loss. The virtual links keep carrier, so each host drops its member to the primary only at the LACP short timeout (3 × 1 s). The secondary's edge MLAG bonds keep forwarding throughout.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'The rebooted peer keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. Both traffic hosts renegotiate LACP to the shared system ID, with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case('secondary-power-loss', 'Small', 'MLAG secondary power loss',
         "Resets the bridge on CHR 1 and CHR 2 over management SSH with the bridge mode of the run, picks the MLAG peer that reports mlag-state connected as secondary, and after a loss-free baseline emulates its power loss. In one step it takes the container veths behind the secondary's ether2 to ether5 down, sets the other peer's peer-link NIC link-down over QMP and pauses the secondary's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers the secondary on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('direct-power-loss-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary off',
              'Every link to the secondary loses carrier at once, as on a real power loss. The MLAG primary sees its peer port ether2 go down and keeps the shared system ID, so both traffic hosts keep their LACP partner. Each host drops its member to the secondary on carrier loss, without waiting for the LACP short timeout, and forwards over its member to the primary. Only traffic hashed to the lost member sees brief loss.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'Carrier returns while the secondary boots. Its bond members stay out of the 802.3ad bond until the MLAG system ID syncs with the primary (mlag-init-delay, default 1 min), then join under the unchanged shared system ID. The MLAG bonds client1 and client2 are edge ports and forward at once, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('primary-power-loss', 'Small', 'MLAG primary power loss',
         "Resets the bridge on CHR 1 and CHR 2 over management SSH with the bridge mode of the run, picks the MLAG peer that reports mlag-state connected as primary, and after a loss-free baseline emulates its power loss. In one step it takes the container veths behind the primary's ether2 to ether5 down, sets the other peer's peer-link NIC link-down over QMP and pauses the primary's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers the primary on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('direct-power-loss-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary off',
              "Every link to the primary loses carrier at once, as on a real power loss. The MLAG secondary sees its peer port ether2 go down and reverts its MLAG bonds to its own LACP system ID (mlag-lacp-fallback=yes), so both traffic hosts renegotiate LACP, with brief loss. Each host drops its member to the primary on carrier loss, without waiting for the LACP short timeout. The secondary's edge MLAG bonds keep forwarding throughout.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'Carrier returns while the primary boots. It keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. Both traffic hosts renegotiate LACP to the shared system ID, with brief loss.',
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
    Case('medium-stp-off-power-loss-secondary', 'Medium', 'MLAG secondary power loss · Medium lab, all bridges STP off',
         "Resets all three bridges over management SSH with protocol-mode=none. It requires a loss-free probe baseline, zero BPDUs and one copy of each broadcast. It then emulates a power loss of CHR 2 (MLAG secondary, mlag-priority=20): in one step it takes the container veths behind CHR 2's ether2 to ether4 down, sets the facing NICs of CHR 1 and the access switch link-down over QMP and pauses CHR 2's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers CHR 2 on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-stp-off-power-loss-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary off',
              "Every link to CHR 2 loses carrier at once, as on a real power loss. CHR 1 (MLAG primary) sees its peer port ether2 go down and keeps the shared system ID, so the access switch's uplink bond and traffic host 2 keep their LACP partner. They drop their member to CHR 2 on carrier loss, without waiting for the LACP short timeout, and forward over their members to CHR 1. With protocol-mode=none no port changes state and no BPDUs appear.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'Carrier returns while CHR 2 boots. CHR 2 keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with CHR 1 (mlag-init-delay), then adds them under the unchanged shared system ID. The access switch and traffic host 2 re-add the member to the same aggregator, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('medium-stp-off-power-loss-primary', 'Medium', 'MLAG primary power loss · Medium lab, all bridges STP off',
         "Resets all three bridges over management SSH with protocol-mode=none. It requires a loss-free probe baseline, zero BPDUs and one copy of each broadcast. It then emulates a power loss of CHR 1 (MLAG primary, mlag-priority=10): in one step it takes the container veths behind CHR 1's ether2 to ether4 down, sets the facing NICs of CHR 2 and the access switch link-down over QMP and pauses CHR 1's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers CHR 1 on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-stp-off-power-loss-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary off',
              'Every link to CHR 1 loses carrier at once, as on a real power loss. CHR 2 sees its peer port ether2 go down and reverts its MLAG bonds to its own LACP system ID, so the access switch and traffic host 2 renegotiate LACP, with brief loss. They drop their member to CHR 1 on carrier loss, without waiting for the LACP short timeout. With protocol-mode=none no port changes state and no BPDUs appear.',
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              'Carrier returns while CHR 1 boots. CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. The access switch and traffic host 2 renegotiate LACP to the shared system ID, with brief loss.',
              5.0, MLAG_MANUAL),)),
    Case('medium-core-off-baseline', 'Medium', 'Baseline · STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         CORE_OFF_RESET + ' Then run numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions, read back bridge, MLAG, RSTP and LACP state, and send three ARP broadcasts each way. No fault is applied.',
         ('medium-core-off-baseline',), (101, 201), (301, 303),
         (Phase('baseline', 'Baseline',
              "Both MLAG peers run protocol-mode=none with forward-reserved-addresses=no, so they neither send BPDUs nor pass the access switch's BPDUs (STP group address 01:80:C2:00:00:00). The access switch is the only RSTP bridge and, with priority 0x0000, its own root (root ID 0x0000.02:00:00:21:00:13). Its uplink bond is an edge port, so it forwards at once without a proposal/agreement handshake, and its host port ether4 is an edge port with bpdu-guard=yes and loop-protect=on. MLAG is connected, every bond member is synchronized, collecting and distributing, each ARP broadcast arrives once and all four streams deliver with zero loss.",
              0.0, CORE_OFF_SOURCE),)),
    Case('medium-core-off-calibrate', 'Medium', 'One-way calibration · STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         "After the campus option 1 bridge reset and baseline gate, the runner adds a tc ingress filter on host 2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and observes 3 s of settling and a 3 s recovery window.",
         ('medium-core-off-calibrate',), (301,), (101, 201, 303),
         (Phase('calibration', 'One-way bypass cut',
              "The filter drops only stream 301's echo requests at host 2's bypass port, outside the MLAG fabric. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
              None, LAB_TARGET),)),
    Case('medium-core-off-reboot-secondary', 'Medium', 'MLAG secondary reboot · Medium lab, STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         CORE_OFF_RESET + ' It requires a loss-free probe baseline, no BPDU from or through the MLAG pair and one copy of each broadcast. It then reboots CHR 2 (MLAG secondary, mlag-priority=20) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-core-off-reboot-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary down',
              "CHR 1 (MLAG primary) keeps the shared system ID, so the access switch's uplink bond and traffic host 2 keep their LACP partner and forward over their members to CHR 1. The virtual links keep carrier, so they drop the member to CHR 2 only at the LACP short timeout (3 × 1 s). The access switch stays its own RSTP root and its edge uplink keeps forwarding, because a member leaving the bond does not change the bridge port.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'CHR 2 keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with CHR 1 (mlag-init-delay), then adds them under the unchanged shared system ID. The access switch re-adds the member to its uplink bond, which stays a forwarding edge port, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('medium-core-off-reboot-primary', 'Medium', 'MLAG primary reboot · Medium lab, STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         CORE_OFF_RESET + ' It requires a loss-free probe baseline, no BPDU from or through the MLAG pair and one copy of each broadcast. It then reboots CHR 1 (MLAG primary, mlag-priority=10) with `/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.',
         ('medium-core-off-reboot-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary down',
              "CHR 2 reverts its MLAG bonds to its own LACP system ID (mlag-lacp-fallback=yes), so the access switch and traffic host 2 renegotiate LACP, with brief loss. The virtual links keep carrier, so they drop the member to CHR 1 only at the LACP short timeout (3 × 1 s). The access switch's uplink is an edge port, so once LACP has reselected it forwards at once, without RSTP discarding and learning states.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              "CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. The access switch and traffic host 2 renegotiate LACP to the shared system ID with brief loss, and the access switch's edge uplink forwards again at once.",
              5.0, MLAG_MANUAL),)),
    Case('medium-core-off-power-loss-secondary', 'Medium', 'MLAG secondary power loss · Medium lab, STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         CORE_OFF_RESET + " It requires a loss-free probe baseline, no BPDU from or through the MLAG pair and one copy of each broadcast. It then emulates a power loss of CHR 2 (MLAG secondary): in one step it takes the container veths behind CHR 2's ether2 to ether4 down, sets the facing NICs of CHR 1 and the access switch link-down over QMP and pauses CHR 2's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers CHR 2 on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-core-off-power-loss-secondary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Secondary off',
              "Every link to CHR 2 loses carrier at once, as on a real power loss. CHR 1 (MLAG primary) sees its peer port ether2 go down and keeps the shared system ID, so the access switch's uplink bond and traffic host 2 keep their LACP partner. They drop their member to CHR 2 on carrier loss, without waiting for the LACP short timeout. The uplink bond keeps one running member, so the access switch's edge bridge port keeps forwarding.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Secondary back',
              'Carrier returns while CHR 2 boots. CHR 2 keeps its bond members out of the 802.3ad bond until the MLAG system ID syncs with CHR 1 (mlag-init-delay), then adds them under the unchanged shared system ID. The access switch re-adds the member to its forwarding edge uplink, so loss is brief or none.',
              5.0, MLAG_MANUAL),)),
    Case('medium-core-off-power-loss-primary', 'Medium', 'MLAG primary power loss · Medium lab, STP off on the MLAG pair, RSTP on the access switch (campus option 1)',
         CORE_OFF_RESET + " It requires a loss-free probe baseline, no BPDU from or through the MLAG pair and one copy of each broadcast. It then emulates a power loss of CHR 1 (MLAG primary): in one step it takes the container veths behind CHR 1's ether2 to ether4 down, sets the facing NICs of CHR 2 and the access switch link-down over QMP and pauses CHR 1's guest with QMP stop, then confirms carrier loss at every neighbour. After 20 s it powers CHR 1 on with QMP system_reset and cont, brings the links back up, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
         ('medium-core-off-power-loss-primary',), (101, 201), (301, 303),
         (Phase('withdrawal', 'Primary off',
              "Every link to CHR 1 loses carrier at once, as on a real power loss. CHR 2 sees its peer port ether2 go down and reverts its MLAG bonds to its own LACP system ID, so the access switch and traffic host 2 renegotiate LACP, with brief loss. They drop their member to CHR 1 on carrier loss, without waiting for the LACP short timeout. The access switch's uplink is an edge port, so it forwards as soon as LACP has reselected.",
              5.0, MLAG_MANUAL),
         Phase('restoration', 'Primary back',
              "Carrier returns while CHR 1 boots. CHR 1 keeps its bond members out of the bond until the MLAG system ID syncs (mlag-init-delay), rejoins as MLAG primary and restores the shared system ID. The access switch and traffic host 2 renegotiate LACP to the shared system ID with brief loss, and the edge uplink forwards again at once.",
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
    Case("mac-age-relearn", "Small", "Silent host past bridge ageing, then relearn",
         "Sets ageing-time=10s on the bridge of both MLAG peers and reads it back, and pins permanent neighbour "
         "entries between the MAC-move host and both traffic hosts, so no host needs ARP while one side is silent. "
         "After the baseline it drops every frame the MAC-move host sends for 25 s, with a tc filter on egress of "
         "both its bond members, then removes the filter and watches 5 s of return plus a 3 s recovery window. "
         "Afterwards it restores ageing-time=5m, reads it back and removes the pinned neighbour entries.",
         ("silent-mobile",), (101, 102, 201, 202), (301, 302, 303),
         (Phase("withdrawal", "Host silent",
                "Nothing from the MAC-move host reaches either MLAG peer. After the 10 s ageing time both peers "
                "remove the host MAC from the bridge host table: CHR 1 its entry on ether5, CHR 2 its entry on the "
                "peer port ether2. Frames to the host MAC are then unknown unicast, so both peers flood streams 101 "
                "and 102 to the other traffic host as well. This is correct bridge behaviour and is recorded, not "
                "failed. Every stream to or from the host loses probes for the whole silence; that loss is the fault "
                "itself, so the limit is the 25 s silence plus the 1 s relearn target. Stream 302 and both bypass "
                "streams lose nothing.", 26.0, BRIDGE_MANUAL),
          Phase("restoration", "Host sends again",
                "The host's first frame enters CHR 1 on ether5, so CHR 1 learns the host MAC on ether5 and CHR 2 on "
                "the peer port. Lab target, measured from the host's first frame at a CHR TAP: flooding of streams "
                "101 and 102 to the other traffic host stops within 1.0 s, streams 101, 102, 201 and 202 deliver "
                "again within 1.0 s and lose nothing afterwards. The field report saw this flooding continue while "
                "both bridge host tables showed the right port. Stream 302 and both bypass streams lose nothing.",
                RELEARN_LIMIT_S, FLOODING_REPORT))),
    Case("member-flap-repeat", "Small", "Repeated MLAG bond member flap",
         "Takes client 1's bond member to CHR 1 (ether3) down at both ends for 1 s and back up for 3 s, five times, "
         "then watches 8 s of return plus a 3 s recovery window. Both MLAG peers' bridge host table entries for "
         "client 2 and the MAC-move host are sampled every 0.35 s throughout.",
         ("carrier-flap",), (101, 201, 302), (102, 202, 301, 303),
         (Phase("withdrawal", "Five member flaps",
                "Each flap removes ether3 from CHR 1's MLAG bond client1 and adds it back once LACP renegotiates. "
                "While the member is down, CHR 1 forwards traffic for client 1 over the peer link to CHR 2, with "
                "brief loss. This phase runs from the first flap to the fifth return, so it holds four complete flaps "
                "and the fifth down; result.json lists the loss of every flap separately. Each loss of streams 101, "
                "201 and 302 may last at most 3 s, the member limit per flap. Streams 102 and 202 never touch client "
                "1 and lose nothing, and the bridge host table entries for client 2 and the MAC-move host stay on "
                "both MLAG peers. The field report saw unrelated MACs move to the peer port after a member flap.",
                3.0, FOUR_SWITCH_REPORT),
          Phase("restoration", "Member back after the fifth flap",
                "Carrier returns for the last time and LACP renegotiates ether3 with client 1 until it shows "
                "synchronization, collecting and distributing (S, C, D). Loss of streams 101, 201 and 302 lasts at "
                "most 3 s. Streams 102 and 202 and both bypass streams lose nothing, and the host entries for client "
                "2 and the MAC-move host stay present.", 3.0, BOND_FLAGS))),
    # Planned: listed in the case index, not yet runnable.

    Case("primary-pause", "Small", "MLAG primary held stopped with carrier up",
         "Pause the MLAG primary's QEMU guest for at least 35 s while its virtual links keep carrier, then "
         "resume it. Runs today only in the Medium pair-root lab as primary-sustained-stop.", (), (), (), ()),
    Case("primary-reboot-no-fallback", "Small", "MLAG primary reboot with mlag-lacp-fallback=no",
         "Set mlag-lacp-fallback=no on both MLAG peers, reboot the MLAG primary, then restore the setting. "
         "Runs today only in the Medium pair-root lab as reboot-primary-no-fallback.", (), (), (), ()),
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


# MSTP Medium cases mirror the RSTP root placements on the same wiring.
CASES += tuple(
    replace(case, name=case.name.replace("medium-", "medium-mstp-", 1),
            title=case.title.replace("RSTP", "MSTP"),
            action=case.action.replace("protocol-mode=rstp", "protocol-mode=mstp"),
            selectors=tuple(s.replace("medium-", "medium-mstp-", 1) for s in case.selectors))
    for case in CASES if case.name.startswith(("medium-pair-root-", "medium-access-root-")))

# Two MLAG pairs in one Layer 2 domain. Pair A (CHR 1 primary, CHR 2 secondary) is the intended root,
# pair B (CHR 3 primary, CHR 4 secondary) hangs off it on one distributed LACP bond. "equal" puts every
# switch on 0x8000, as in the field report where pairs with the same priority fought over the root.
# "field" is the deployed field design: the same priority inside a pair and a lower value on the root pair.
ROOT_FIGHT_REPORT = "https://forum.mikrotik.com/t/mlag-between-crs326-24s-2q-rm-with-more-than-1-000-hosts-macs/269294"
TWO_PAIR_SETUPS = {
    "equal": ("equal bridge priority 0x8000", "bridge priority 0x8000 on all four CHRs, as in the field report "
              "where every MLAG pair kept the same priority", "0x8000.02:00:00:21:00:11", "0x8000.02:00:00:21:00:12",
              "the lower bridge MAC, because all priorities are equal"),
    "field": ("field priorities, pair A 0x2000, pair B 0x4000", "bridge priority 0x2000 on pair A and 0x4000 on pair B, "
            "the field design with one priority per pair", "0x2000.02:00:00:21:00:11", "0x4000.02:00:00:21:00:12",
            "priority 0x2000 against 0x4000"),
}
TWO_PAIR_WIRING = ("Pair A (CHR 1 MLAG primary, CHR 2 MLAG secondary) and pair B (CHR 3 MLAG primary, CHR 4 MLAG "
                   "secondary) are joined by one distributed LACP bond, mlag-id 11 on pair A and 21 on pair B. "
                   "Host 1 bonds to pair B and host 2 to pair A, so both VLAN 110 streams cross both pairs.")
TWO_PAIR_REBOOTS = {
    "reboot-a-primary": ("p1", "Pair A primary reboot", "CHR 1 (pair A's MLAG primary)",
                         "CHR 2, CHR 3 and CHR 4", "CHR 1 rejoins as MLAG primary and pair A presents {a} again."),
    "reboot-a-secondary": ("p2", "Pair A secondary reboot", "CHR 2 (pair A's MLAG secondary)",
                           "CHR 1, CHR 3 and CHR 4", "CHR 2 rejoins as MLAG secondary under pair A's unchanged ID."),
    "reboot-b-primary": ("q1", "Pair B primary reboot", "CHR 3 (pair B's MLAG primary)",
                         "CHR 1, CHR 2 and CHR 4", "CHR 3 rejoins as MLAG primary and pair B presents {b} again."),
    "reboot-b-secondary": ("q2", "Pair B secondary reboot", "CHR 4 (pair B's MLAG secondary)",
                           "CHR 1, CHR 2 and CHR 3", "CHR 4 rejoins as MLAG secondary under pair B's unchanged ID."),
}
TWO_PAIR_WITHDRAWAL = {
    ("equal", "reboot-a-primary"): (
        "If CHR 2 presents its own bridge ID 0x8000.02:00:00:21:00:14 while CHR 1 is away, pair B's "
        "0x8000.02:00:00:21:00:12 is lower and RSTP moves the root to pair B. That root move, and the topology "
        "change it causes on every switch, is the field failure this setup reproduces.", ROOT_FIGHT_REPORT),
    ("field", "reboot-a-primary"): (
        "Even if CHR 2 presents its own bridge ID 0x2000.02:00:00:21:00:14, it still beats pair B's 0x4000, so "
        "the root stays on pair A. This is what the field per-pair priority is meant to guarantee.", ROOT_FIGHT_REPORT),
    ("equal", "reboot-a-secondary"): ("CHR 1 keeps pair A's bridge ID, so the root does not change.", MLAG_MANUAL),
    ("field", "reboot-a-secondary"): ("CHR 1 keeps pair A's bridge ID, so the root does not change.", MLAG_MANUAL),
    ("equal", "reboot-b-primary"): (
        "Pair B may present CHR 4's bridge ID 0x8000.02:00:00:21:00:13 instead. It is still higher than pair A's, "
        "so the root stays on pair A.", MLAG_MANUAL),
    ("field", "reboot-b-primary"): (
        "Pair B may present CHR 4's bridge ID 0x4000.02:00:00:21:00:13 instead. It is still higher than pair A's, "
        "so the root stays on pair A.", MLAG_MANUAL),
    ("equal", "reboot-b-secondary"): ("CHR 3 keeps pair B's bridge ID, so the root does not change.", MLAG_MANUAL),
    ("field", "reboot-b-secondary"): ("CHR 3 keeps pair B's bridge ID, so the root does not change.", MLAG_MANUAL),
}
# The same wiring with spanning tree off; stp-off-strict also sets lacp-strict=yes on the inter-pair bond.
# The same wiring with spanning tree off on both pairs: no BPDUs, no root, only LACP and MLAG.
_off = ("Resets the data bridge on all four CHRs over management SSH with protocol-mode=none. "
        f"{TWO_PAIR_WIRING}")
CASES += (
    Case("two-pair-stp-off-baseline", "Medium", "Baseline · two MLAG pairs, spanning tree off",
         f"{_off} Then runs numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions and reads back "
         "bridge, MLAG and LACP state on all four CHRs. No fault is applied.",
         ("two-pair-stp-off-baseline",), (101, 201), (301, 303),
         (Phase("baseline", "Baseline",
                "Both pairs are connected, with CHR 1 and CHR 3 as MLAG primaries. With protocol-mode=none no bridge "
                "sends or forwards BPDUs. Every member of the inter-pair bond and both host bonds is synchronized, "
                "collecting and distributing, and all four streams deliver with zero loss.", 0.0, MLAG_MANUAL),)),
    Case("two-pair-stp-off-calibrate", "Medium", "One-way calibration · two MLAG pairs, spanning tree off",
         "After the bridge reset (protocol-mode=none) and baseline gate, the runner adds a tc ingress filter on host "
         "2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and "
         "observes 3 s of settling and a 3 s recovery window.",
         ("two-pair-stp-off-calibrate",), (301,), (101, 201, 303),
         (Phase("calibration", "One-way bypass cut",
                "The filter drops only stream 301's echo requests at host 2's bypass port, outside both MLAG pairs. "
                "Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured "
                "1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
                None, LAB_TARGET),)),
)
for _step, (_target, _title, _who, _others, _back) in TWO_PAIR_REBOOTS.items():
    _primary = _step.endswith("-primary")
    CASES += (Case(
        f"two-pair-stp-off-{_step}", "Medium", f"{_title} · two MLAG pairs, spanning tree off",
        f"{_off} It requires a loss-free baseline and zero BPDUs. It then reboots {_who} with `/system reboot`, waits "
        "for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
        (f"two-pair-stp-off-{_step}",), (101, 201), (301, 303),
        (Phase("withdrawal", f"{_title.split(' reboot')[0]} down",
               ("The surviving peer reverts its MLAG bonds to its own LACP system ID, so the other pair and the host "
                "renegotiate LACP, with brief loss. " if _primary else
                "The surviving peer keeps the shared LACP system ID. ")
               + "The virtual links keep carrier, so partners drop the member to the rebooted switch at the LACP short "
               "timeout (3 × 1 s). No port depends on spanning tree, no BPDUs appear, and each VLAN direction loses "
               "at most 5 s.", 5.0, MLAG_MANUAL),
         Phase("restoration", f"{_title.split(' reboot')[0]} back",
               "The rebooted switch keeps its bond members out of the bond until the MLAG system ID syncs "
               "(mlag-init-delay) and rejoins under the shared system ID. Partners renegotiate LACP with brief loss, "
               "and each VLAN direction loses at most 5 s.", 5.0, MLAG_MANUAL)),
    ),)
# The same wiring with spanning tree off on both pairs: no BPDUs, no root, only LACP and MLAG.
_off = ("Resets the data bridge on all four CHRs over management SSH with protocol-mode=none. It first sets lacp-strict=yes on the inter-pair bond of all four CHRs, so a member whose LACP partner times out stops carrying traffic. "
        f"{TWO_PAIR_WIRING}")
CASES += (
    Case("two-pair-stp-off-strict-baseline", "Medium", "Baseline · two MLAG pairs, spanning tree off, lacp-strict=yes on the inter-pair bond",
         f"{_off} Then runs numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions and reads back "
         "bridge, MLAG and LACP state on all four CHRs. No fault is applied.",
         ("two-pair-stp-off-strict-baseline",), (101, 201), (301, 303),
         (Phase("baseline", "Baseline",
                "Both pairs are connected, with CHR 1 and CHR 3 as MLAG primaries. With protocol-mode=none no bridge "
                "sends or forwards BPDUs. Every member of the inter-pair bond and both host bonds is synchronized, "
                "collecting and distributing, and all four streams deliver with zero loss.", 0.0, MLAG_MANUAL),)),
    Case("two-pair-stp-off-strict-calibrate", "Medium", "One-way calibration · two MLAG pairs, spanning tree off, lacp-strict=yes on the inter-pair bond",
         "After the bridge reset (protocol-mode=none) and baseline gate, the runner adds a tc ingress filter on host "
         "2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and "
         "observes 3 s of settling and a 3 s recovery window.",
         ("two-pair-stp-off-strict-calibrate",), (301,), (101, 201, 303),
         (Phase("calibration", "One-way bypass cut",
                "The filter drops only stream 301's echo requests at host 2's bypass port, outside both MLAG pairs. "
                "Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose the measured "
                "1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose nothing.",
                None, LAB_TARGET),)),
)
for _step, (_target, _title, _who, _others, _back) in TWO_PAIR_REBOOTS.items():
    _primary = _step.endswith("-primary")
    CASES += (Case(
        f"two-pair-stp-off-strict-{_step}", "Medium", f"{_title} · two MLAG pairs, spanning tree off, lacp-strict=yes on the inter-pair bond",
        f"{_off} It requires a loss-free baseline and zero BPDUs. It then reboots {_who} with `/system reboot`, waits "
        "for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery window.",
        (f"two-pair-stp-off-strict-{_step}",), (101, 201), (301, 303),
        (Phase("withdrawal", f"{_title.split(' reboot')[0]} down",
               ("The surviving peer reverts its MLAG bonds to its own LACP system ID, so the other pair and the host "
                "renegotiate LACP, with brief loss. " if _primary else
                "The surviving peer keeps the shared LACP system ID. ")
               + "The virtual links keep carrier, so partners drop the member to the rebooted switch at the LACP short "
               "timeout (3 × 1 s). No port depends on spanning tree, no BPDUs appear, and each VLAN direction loses "
               "at most 5 s.", 5.0, MLAG_MANUAL),
         Phase("restoration", f"{_title.split(' reboot')[0]} back",
               "The rebooted switch keeps its bond members out of the bond until the MLAG system ID syncs "
               "(mlag-init-delay) and rejoins under the shared system ID. Partners renegotiate LACP with brief loss, "
               "and each VLAN direction loses at most 5 s.", 5.0, MLAG_MANUAL)),
    ),)
for _setup, (_label, _priorities, _a, _b, _winner) in TWO_PAIR_SETUPS.items():
    _reset = (f"Resets the data bridge on all four CHRs over management SSH with protocol-mode=rstp and {_priorities}. "
              f"{TWO_PAIR_WIRING}")
    CASES += (
        Case(f"two-pair-{_setup}-baseline", "Medium", f"Baseline · two MLAG pairs, {_label}",
             f"{_reset} Then runs numbered 100 ms pings for 4 s in both VLAN 110 and both bypass directions and reads "
             "back bridge, MLAG, RSTP and LACP state on all four CHRs. No fault is applied.",
             (f"two-pair-{_setup}-baseline",), (101, 201), (301, 303),
             (Phase("baseline", "Baseline",
                    f"Both pairs are connected and each presents its MLAG primary's bridge ID: pair A {_a}, pair B "
                    f"{_b}. All four CHRs report root {_a}; pair A wins on {_winner}. Every member of the inter-pair "
                    "bond and both host bonds is synchronized, collecting and distributing, RSTP BPDUs from the root "
                    "reach pair B, and all four streams deliver with zero loss.", 0.0, MLAG_MANUAL),)),
        Case(f"two-pair-{_setup}-calibrate", "Medium", f"One-way calibration · two MLAG pairs, {_label}",
             f"After the bridge reset ({_priorities}) and baseline gate, the runner adds a tc ingress filter on host "
             "2's eth3 that drops bypass-forward echo requests (stream 301) for 2 s. It then removes the filter and "
             "observes 3 s of settling and a 3 s recovery window.",
             (f"two-pair-{_setup}-calibrate",), (301,), (101, 201, 303),
             (Phase("calibration", "One-way bypass cut",
                    "The filter drops only stream 301's echo requests at host 2's bypass port, outside both MLAG "
                    "pairs. Stream 301 shows exactly one gap, with every request sent, and the gap's bounds enclose "
                    "the measured 1.9–2.3 s filter interval. The reverse bypass and both VLAN 110 directions lose "
                    "nothing.", None, LAB_TARGET),)),
    )
    for _step, (_target, _title, _who, _others, _back) in TWO_PAIR_REBOOTS.items():
        _expected, _source = TWO_PAIR_WITHDRAWAL[_setup, _step]
        CASES += (Case(
            f"two-pair-{_setup}-{_step}", "Medium", f"{_title} · two MLAG pairs, {_label}",
            f"{_reset} It requires a loss-free baseline with root {_a} on all four CHRs. It then reboots {_who} with "
            "`/system reboot`, waits for the guest uptime to reset and keeps probing for 16 s plus a 3 s recovery "
            "window.",
            (f"two-pair-{_setup}-{_step}",), (101, 201), (301, 303),
            (Phase("withdrawal", f"{_title.split(' reboot')[0]} down",
                   f"{_expected} The case passes only if {_others} keep root {_a} while the switch is away and each "
                   "VLAN direction loses at most 5 s.", 5.0, _source),
             Phase("restoration", f"{_title.split(' reboot')[0]} back",
                   f"{_back.format(a=_a, b=_b)} {_others} must keep root {_a} throughout, and each VLAN direction "
                   "loses at most 5 s.", 5.0, MLAG_MANUAL)),
        ),)
# The four-switch report's trigger on every two-pair setup: one inter-pair bond member down and up.
_flap_setups = {
    **{setup: (label, f"protocol-mode=rstp and {priorities}", root)
       for setup, (label, priorities, root, _b, _winner) in TWO_PAIR_SETUPS.items()},
    "stp-off": ("spanning tree off", "protocol-mode=none", None),
    "stp-off-strict": ("spanning tree off, lacp-strict=yes on the inter-pair bond",
                       "protocol-mode=none, after setting lacp-strict=yes on the inter-pair bond of all four CHRs", None),
}
for _setup, (_label, _settings, _root) in _flap_setups.items():
    _kept = (f"The inter-pair bond stays one bridge port on each pair, so all four CHRs keep root {_root}."
             if _root else "No bridge sends or forwards BPDUs.")
    CASES += (Case(
        f"two-pair-{_setup}-interpair-member-flap", "Medium", f"Inter-pair bond member flap · two MLAG pairs, {_label}",
        f"Resets the data bridge on all four CHRs over management SSH with {_settings}. {TWO_PAIR_WIRING} It requires "
        "a loss-free baseline" + (f" with root {_root} on all four CHRs" if _root else "") + ". It then takes the "
        "inter-pair bond member between CHR 1 ether3 and CHR 3 ether3 down at both ends (both container veths and "
        "both QEMU NICs), holds it down for 8 s, brings both ends back up and watches 8 s of return plus a 3 s "
        "recovery window. The bridge host table size and the topology-change counter of every CHR are sampled "
        "throughout.",
        (f"two-pair-{_setup}-interpair-member-flap",), (101, 201), (301, 303),
        (Phase("withdrawal", "Inter-pair member down",
               "CHR 1 and CHR 3 each lose their only member of the inter-pair MLAG bond (mlag-id 11 on pair A, 21 on "
               "pair B). The bond keeps forwarding over its other member between CHR 2 and CHR 4, and traffic that "
               f"reaches CHR 1 or CHR 3 crosses its pair's peer port. Streams 101 and 201 lose at most 3 s. {_kept} "
               "The field report saw unrelated MACs move to the peer port and the host table shrink after this flap; "
               "the host table size and topology-change counter of every CHR are recorded for comparison.",
               3.0, FOUR_SWITCH_REPORT),
         Phase("restoration", "Inter-pair member back",
               "Carrier returns at both ends and LACP adds ether3 back to the inter-pair bond on CHR 1 and CHR 3 "
               "once it shows synchronization, collecting and distributing (S, C, D). Streams 101 and 201 lose at "
               f"most 3 s. {_kept}", 3.0, BOND_FLAGS)),
    ),)

def _changelog(version):
    return f"https://cdn.mikrotik.com/routeros/{version}/CHANGELOG"


def _reboot(name):
    return ("reboot" in name or "power-loss" in name) and "calibrat" not in name


def _baseline(name):
    return name.endswith("-baseline") or name == "baseline"


_STP_REBOOT = ("medium-pair-root-reboot-", "medium-access-root-reboot-", "medium-mstp-pair-root-reboot-",
               "medium-mstp-access-root-reboot-", "reboot-primary", "reboot-secondary", "two-pair-equal-reboot-",
               "two-pair-field-reboot-")
# Each row of docs/reference/mlag-fixes.md in state Checked or Indirect, with the cases that grade it.
FIXES = (
    ("7.25.2", "Dual-bond hosts dropped when an MLAG peer is lost", _reboot),
    ("7.25.2", "Packets looped back to a dual-connected bond", lambda name: True),
    ("7.24.6", "BPDUs leaking to the wrong dual-connected bond (introduced in 7.24)",
     lambda name: not name.startswith("two-pair-") or name.startswith("two-pair-stp-off-")),
    ("7.25.2", "LACP system ID not synchronised when bonds are created before MLAG", lambda name: True),
    ("7.25", "New settings mlag-lacp-fallback and mlag-init-delay",
     lambda name: _reboot(name) or name == "peer-link-loss"),
    ("7.25", "MLAG peer stuck in the disabled state after config changes", _baseline),
    ("7.26beta4", "New setting lacp-strict for 802.3ad bonds", lambda name: name.startswith("two-pair-stp-off-strict-")),
    ("7.24", "STP, BPDU and topology-change handling with MLAG; dual-connected port STP state in sync with the "
     "MLAG peer", lambda name: name.startswith(_STP_REBOOT)),
    ("7.24", "MLAG MAC address handling for ageing, flushing and moving", lambda name: name == "mac-move"),
    ("7.22", "MAC moving between regular ports and bonds", lambda name: name == "mac-move"),
    ("7.22", "MLAG state permanently disabled after changing bridge settings", _baseline),
    ("7.18", "mlag-heartbeat; no peer port reset on heartbeat timeout, a warning is logged",
     lambda name: name in ("peer-link-loss", "primary-sustained-stop")),
    ("7.14", "MLAG connection after a peer link flap (introduced in 7.13)", lambda name: name == "peer-link-loss"),
    ("7.14", "MLAG with MSTP: support and stability", lambda name: name.startswith("medium-mstp-")),
    ("7.17", "Priority setting to elect the MLAG primary", _baseline),
)
# The BPDU fix only on the Medium lab and the two-pair deployment: the Small lab has no BPDU check on a bond.
CASES = tuple(replace(case, fixes=tuple(
    (version, wording, _changelog(version)) for version, wording, applies in FIXES
    if case.selectors and applies(case.name)
    and not (wording.startswith("BPDUs leaking") and case.lab != "Medium"))) for case in CASES)


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
        split = flow["phase_gaps_s"].get(key, [])
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in split]
        # A split outage has exact time bounds per phase but no per-phase probe count.
        probes = None
    else:
        spans = [(gap["lower_s"], gap["upper_s"]) for gap in gaps]
        probes = sum(gap["failed_probes"] for gap in gaps)
    if not spans:
        return None
    return {"lower_s": max(lower for lower, _ in spans),
            "upper_s": None if any(upper is None for _, upper in spans) else max(upper for _, upper in spans),
            "lost_probes": probes,
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
    A single-phase case takes every check as its own. A check tagged with a phase the case lacks, such as a
    baseline flood in a fault case, counts against every phase, even one whose fault was withheld.
    """
    single = len(spec.phases) == 1
    executed = result.get("fault_executed", True)
    flows = result.get("flows", {})
    run_error = any(not c["ok"] and c["level"] in ("error", "inconclusive") and "phase" not in c for c in checks)
    keys = {phase.key for phase in spec.phases}
    stray = [c for c in checks if not c["ok"] and "phase" in c and c["phase"] not in keys]
    summary = []
    for phase in spec.phases:
        own = checks if single else [c for c in checks if c.get("phase") == phase.key] + stray
        failed = {c["level"] for c in own if not c["ok"]}
        if phase.key != "baseline" and not executed and not stray:
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
                              "lost_probes": max((v["lost_probes"] for v in loss.values()
                                                  if v["lost_probes"] is not None), default=None),
                              "spans_both_phases": any(v["spans_both_phases"] for v in loss.values())}
                             if loss else None),
            "loss_s": loss,
            "control_loss_s": _loss(flows, spec.control_flows, phase.key, single),
            "failed_checks": [c["detail"] for c in own if not c["ok"]],
        })
    return summary
