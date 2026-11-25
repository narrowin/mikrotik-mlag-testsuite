# RouterOS 7.26beta7 MLAG: two faults

Checked on 24 November 2026 from saved packet captures and RouterOS state. No lab was run for this report. Updated on 25 November 2026: how often each fault showed, and the loss ranges, now come from the generated [Faults across runs](../../results/README.md#faults-across-runs) table instead of hand counts. That table also shows that some of the MSTP reboots this report first listed as "MLAG pair as root" had the access switch as root of VLAN 110.

This report is written for filing bug reports with MikroTik. We do not plan to file them ourselves. Anyone who wants to may use it.

## Outcome

- Both faults are RouterOS behaviour, not errors of the test checks.
- Fault 1: after a bond member or an MLAG peer returns, an MLAG peer sends frames from the peer port back out a dual-connected MLAG bond. The 7.26beta7 changelog fix "packets looped back to a dual-connected bond" does not fully hold.
- Fault 2: with two MLAG pairs, rebooting one pair's MLAG primary stops traffic for about 20 s. The other pair keeps sending into the rebooting switch.
- Likely common cause: an MLAG bond whose local member has link up but is not LACP-distributing stays a forwarding bridge port.

## Setup

- RouterOS 7.26beta7 CHR, arm64, build time 2026-11-19 12:13:35, in QEMU under Containerlab 0.83.0.
- Bridge: `protocol-mode=none`, `vlan-filtering=yes`, VLAN 110, `mlag-heartbeat=5s`, `mlag-init-delay=1m`, `mlag-lacp-fallback=yes`.
- MLAG bonds: 802.3ad, one member per MLAG peer, `lacp-rate=1sec`, `lacp-strict=no` unless stated.
- Linux hosts: 802.3ad bond with `lacp_rate fast`.
- Ports on each MLAG peer: `ether2` peer port, `ether3` and `ether4` members of MLAG bonds.

## Fault 1: frames sent back out a dual-connected MLAG bond

**Problem.** For up to about 1 s after a bond member or an MLAG peer returns, a frame that arrived on the peer port is sent out a member of a dual-connected MLAG bond. It goes back to the host that sent it, or reaches another host twice.

**Expected.** Frames from the peer port are never sent out an MLAG bond whose other member, on the other MLAG peer, is active.

**What was done and tested.**

- Broadcast and unknown-unicast streams from traffic host 1 were captured on every host interface and every CHR port, during a repeated bond member flap, reboots and power losses. This was the Small lab, mostly with STP off.
- Looped copies were traced frame by frame through the captures in every Small lab run with the fault and in five Medium lab runs.
- RouterOS LACP member flags, bridge port state, bridge host table and syslog were read for the same moments.

**Results.**

- Every copy takes the same path. It leaves the sending host on one bond member, is sent out the peer port by one MLAG peer, and the other MLAG peer sends it out its own member of a dual-connected MLAG bond.
- Example, member flap, broadcast seq 73, 19:53:24.245 UTC:
  1. Host 1 sends the frame on eth2, and CHR 2 receives it on `ether3`.
  2. CHR 2 sends it out the peer port, tagged VLAN 110.
  3. CHR 1 sends it out `ether3`, back to host 1's eth1. That is 2.3 ms after the original.
- At that moment CHR 1's `ether3` had just come back up. Its first LACPDU came 88 ms later, with the member not in sync and not distributing. `/interface bonding monitor` showed `flags="ATG---FE"`, while the bridge port `client1` showed `forwarding: yes`.
- In a reboot, it starts right after the rebooted MLAG peer logs `peer connected`. In [one run](../../results/2026-11-24-forwarding-checks/validation-none-reboot-power/01-secondary-reboot), 10 frames looped within 1 s.
- Host 1's bond dropped its returned copies. Host 2 received duplicates.

- With STP off on the Small lab, it shows in the repeated bond member flap, the MLAG primary and secondary reboot and the MLAG secondary power loss. It did not show in primary power loss, single member loss, peer link loss or MAC move. How often, per case: [Faults across runs](../../results/README.md#faults-across-runs), rows "Flood frame back at its sender or twice at a host".
- On the Medium lab, a unicast request from host 2 comes back to host 2 the same way during MLAG peer reboots with RSTP or MSTP. It shows with the MLAG pair as root and with the access switch as root of VLAN 110 only. It did not show in any Medium reboot with STP off on the MLAG pair. How often, per setup and case: [Faults across runs](../../results/README.md#faults-across-runs), rows "Unicast request sent back to its sender".
- Neither `lacp-strict=yes` nor `mlag-lacp-fallback=no` prevented it on the Medium lab.

**Not verified.**

- The state of a rebooted MLAG peer in its first second back. It could not be sampled.
- Whether CRS switch chips with hardware offload behave the same. CHR forwards in the software bridge.

**Reproduce.**

1. Build two MLAG peers on 7.26beta7 with the setup above. Connect two Linux hosts with 802.3ad bonds to both peers.
2. On host 1, run `ping -b -i 0.1 10.110.0.255`, and capture with `tcpdump -nei eth1 icmp` and `tcpdump -nei eth2 icmp`.
3. Pull the MLAG primary's cable to host 1 for 1 s, five times, 3 s apart. Or reboot the MLAG secondary.
4. Fault: within about 1 s of the return, a request host 1 sent on one member arrives back on its other member, with the same ICMP sequence number.

## Fault 2: two MLAG pairs keep sending into a rebooting switch

**Problem.** When one MLAG pair's primary reboots, the other pair keeps sending traffic out its member toward the rebooting switch for the whole reboot. Traffic between the pairs stops for about 20 s.

**Expected.** Traffic moves over the peer port to the MLAG peer whose member of the same MLAG bond is active, within the 5 s limit.

**What was done and tested.**

- Two MLAG pairs, A (p1, p2) and B (q1, q2), are joined by MLAG bond `interpair`: p1 `ether3` to q1 `ether3`, and p2 `ether3` to q2 `ether3`. STP is off on all four.
- Each pair's MLAG primary and secondary was rebooted twice while 100 ms pings ran between a host on pair A and a host on pair B.
- The first lost probe, frames during the outage and the first good probe were traced through all captures. The LACPDUs on the inter-pair links, the `interpair` member flags, the bridge port state, the host table and the syslog were read for the outage.

**Results.**

- Every primary reboot of either pair lost about 20 s, against 5 s. Runs and loss ranges: [Faults across runs](../../results/README.md#faults-across-runs), Medium lab, STP off, rows "Pair A primary reboot" and "Pair B primary reboot".
- Example, reboot of p1:
  - The last LACPDU from p1 came at 8.89 s.
  - At 12.39 s, q1 marked its member `ether3` expired. It was not collecting or distributing, as expected with `lacp-rate=1sec`.
  - q1 still sent 255 traffic frames out `ether3` into the rebooting p1, until p1 forwarded again at 29.01 s.
- No traffic crossed any peer port during the outage, although q2's member of `interpair` stayed active (`ATGSCD--`).
- During the outage, q1 showed `ether3` as `ATGS---E`, then `ATGS--F-` with no partner. The bridge port `interpair` stayed `forwarding: yes`, and host 2's MAC stayed on `interpair`.
- The surviving peer p2 stayed `mlag-state: connected` and only logged `MLAG: remote heartbeat timeout`.
- Secondary reboots lost nothing, but no test traffic used the secondary's links, so they do not test this path.
- One MLAG pair recovers normally: on the Medium lab with STP off a primary reboot stays within 5 s. There the access switch has a plain LACP bond with a member to each peer.

**Not verified.**

- `lacp-strict=yes` on `interpair`: one saved run still lost about 16.5 s with the same member flags, but that run is invalid for other reasons.
- Power loss on the two-pair lab. There the link goes down, which may avoid the outage.
- Whether hardware shows the same outage on a reboot. A rebooting CHR keeps its link up, and most hardware drops it. Any failure that stops forwarding while the link stays up triggers the behaviour.

**Reproduce.**

1. Build two MLAG pairs on 7.26beta7, cabled as above, STP off.
2. Ping every 100 ms between a host on pair A and a host on pair B.
3. Stop pair A's MLAG primary while its link stays up: `/system reboot` on CHR, or pause the switch.
4. Fault: on pair B's switch, `/interface bonding monitor interpair` shows the member toward the stopped switch as `E`, then `F`, but `/interface bridge port print` still shows `interpair` forwarding. Its tx counter keeps rising, nothing crosses the peer port, and the ping fails until the stopped switch forwards again.

## Next action

- To file a report with MikroTik, send both faults with this report. Ask whether an MLAG bond whose only local member has no LACP partner should stay a forwarding bridge port.

## Evidence

- Run folders: [member flap](../../results/2026-11-24-forwarding-checks/stable-none-plink-macmove-flap/03-member-flap-repeat), [secondary reboot](../../results/2026-11-24-forwarding-checks/validation-none-reboot-power/01-secondary-reboot), [two-pair primary reboot](../../results/2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/01-two-pair-stp-off-reboot-a-primary) and [Medium RSTP secondary reboot](../../results/2026-11-24-medium-search/rstp-pair-root-run2/01-medium-pair-root-reboot-secondary).
- Each folder publishes `result.json`, `timeline.tsv`, the RouterOS configs and the capture checksums in `pcap.sha256`. The timeline merges the RouterOS state samples, LACP frames and syslog quoted here.
- Packet captures and the raw state and syslog files are not published.
