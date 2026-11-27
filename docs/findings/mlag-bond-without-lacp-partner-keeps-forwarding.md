# RouterOS 7.26beta7 MLAG: an MLAG bond without an LACP partner keeps forwarding

Two findings show that an MLAG bond keeps forwarding while its local bond member has carrier but is not LACP-distributing.
Finding 1 sends frames from the peer link back out a dual-connected MLAG bond.
Finding 2 keeps one MLAG pair sending into the rebooting MLAG primary of another pair.

This page is written for reporting both findings to MikroTik.
We do not plan to file them ourselves.
Anyone who wants to may use it.

The traces were read on 24 November 2026 from the saved captures and RouterOS state of the old suite; no lab was run for this page.
How often each finding showed, and its outage ranges, come from the generated [Faults across runs](../../results/README.md#faults-across-runs) table of the old suite at commit `95c7482`.
That table also shows that some MSTP reboots first listed here as "MLAG pair as root" had the access switch as root of VLAN 110.

## Outcome

- Both findings are RouterOS behaviour, not errors of the test checks.
- Finding 1: after a bond member or an MLAG peer returns, an MLAG peer sends frames from the peer link back out a dual-connected MLAG bond. The 7.26beta7 changelog fix "packets looped back to a dual-connected bond" does not fully hold.
- Finding 2: with two MLAG pairs, rebooting one pair's MLAG primary stops traffic between the pairs far beyond the 5 s limit. The other pair keeps sending into the rebooting switch.
- Likely common cause: an MLAG bond whose local bond member has link up but is not LACP-distributing stays a forwarding bridge port.

## Configuration

- RouterOS 7.26beta7 CHR, arm64, build time 2026-11-19 12:13:35, in QEMU under containerlab 0.83.0.
- Bridge: `protocol-mode=none`, `vlan-filtering=yes`, VLAN 110, `mlag-heartbeat=5s`, `mlag-init-delay=1m`, `mlag-lacp-fallback=yes`.
- MLAG bonds: 802.3ad, one bond member per MLAG peer, `lacp-rate=1sec`, `lacp-strict=no` unless stated.
- Linux hosts: 802.3ad bond with `lacp_rate fast`.
- Ports on each MLAG peer: `ether2` is the peer port, `ether3` and `ether4` are bond members of MLAG bonds.
- This page uses the role names of the current labs. The old suite named the switches `p1` and `p2` (Small and Medium) and `q1` and `q2` (the second pair); its result folders and config files keep those names.

## Finding 1: frames sent back out a dual-connected MLAG bond

**Problem.** For up to about 1 s after a bond member or an MLAG peer returns, a frame that arrived on the peer link is sent out a bond member of a dual-connected MLAG bond.
It goes back to the host that sent it, or reaches another host twice.

**Expected.** Frames from the peer link are never sent out an MLAG bond whose other bond member, on the other MLAG peer, is active.

**What was done and tested.**

- Broadcast and unknown-unicast streams from `client1` were captured on every host interface and every CHR port during a repeated bond member flap, reboots and power losses. This was the Small lab, mostly with spanning tree off.
- Looped copies were traced frame by frame through the captures in every Small lab run with the finding and in five Medium lab runs.
- RouterOS LACP bond member flags, bridge port state, the host table and syslog were read for the same moments.

**Results.**

- Every copy takes the same path. It leaves the sending host on one bond member, one MLAG peer sends it out the peer port, and the other MLAG peer sends it out its own bond member of a dual-connected MLAG bond.
- Example, bond member flap, broadcast seq 73, 19:53:24.245 UTC:
  1. `client1` sends the frame on `eth2`, and switch2 receives it on `ether3`.
  2. switch2 sends it out the peer port, tagged VLAN 110.
  3. switch1 sends it out `ether3`, back to `eth1` of `client1`, 2.3 ms after the original.
- At that moment `ether3` of switch1 had just come back up. Its first LACPDU came 88 ms later, with the bond member not in sync and not distributing.
- `/interface bonding monitor` showed `flags="ATG---FE"`, while the bridge port `client1` showed `forwarding: yes`.
- In a reboot, the looping starts right after the rebooted MLAG peer logs `peer connected`, as in [one MLAG secondary reboot run](../../results/2026-11-24-forwarding-checks/validation-none-reboot-power/01-secondary-reboot).
- The bond of `client1` dropped its returned copies. `client2` received duplicates.
- With spanning tree off on the Small lab, it shows in the repeated bond member flap, the MLAG primary and secondary reboot and the MLAG secondary power loss.
- It did not show in the MLAG primary power loss, a single bond member loss, peer link loss or the MAC move.
- How often, per test: [Faults across runs](../../results/README.md#faults-across-runs), rows "Flood frame back at its sender or twice at a host".
- On the Medium lab, a unicast request from host2 comes back to host2 the same way during MLAG peer reboots with RSTP or MSTP.
- It shows with the MLAG pair as root and with the access switch as root of VLAN 110 only.
- It did not show in any Medium reboot with spanning tree off.
- How often, per STP mode and test: [Faults across runs](../../results/README.md#faults-across-runs), rows "Unicast request sent back to its sender".
- Neither `lacp-strict=yes` nor `mlag-lacp-fallback=no` prevented it on the Medium lab.

**Not verified.**

- The state of a rebooted MLAG peer in its first second back. It could not be sampled.
- Whether CRS switch chips with hardware offload behave the same. CHR forwards in the software bridge.

**Reproduce.**

1. Build two MLAG peers on 7.26beta7 with the configuration above. Connect two Linux hosts with 802.3ad bonds to both MLAG peers.
2. On `client1`, run `ping -b -i 0.1 10.110.0.255`, and capture with `tcpdump -nei eth1 icmp` and `tcpdump -nei eth2 icmp`.
3. Take the MLAG primary's cable to `client1` down for 1 s, five times, 3 s apart. Or reboot the MLAG secondary.
4. Finding: within about 1 s of the return, a request `client1` sent on one bond member arrives back on its other bond member, with the same ICMP sequence number.

## Finding 2: two MLAG pairs keep sending into a rebooting switch

**Problem.** When one MLAG pair's MLAG primary reboots, the other pair keeps sending traffic out its bond member toward the rebooting switch for the whole reboot.
Traffic between the pairs stops until the rebooted switch forwards again.

**Expected.** Traffic moves over the peer link to the MLAG peer whose bond member of the same MLAG bond is active, within the 5 s limit.

**What was done and tested.**

- Two MLAG pairs, A (switch-a1, switch-a2) and B (switch-b1, switch-b2), are joined by the inter-pair bond `interpair`: switch-a1 `ether3` to switch-b1 `ether3`, and switch-a2 `ether3` to switch-b2 `ether3`. Spanning tree is off on all four.
- Each pair's MLAG primary and MLAG secondary was rebooted twice while pings every 100 ms ran between a host on pair A and a host on pair B.
- The first lost ping, the frames during the outage and the first answered ping were traced through all captures.
- The LACPDUs on the inter-pair bond, the `interpair` bond member flags, the bridge port state, the host table and the syslog were read for the outage.

**Results.**

- Every MLAG primary reboot of either pair went over the 5 s limit. Old suite, Medium lab, spanning tree off, from [Faults across runs](../../results/README.md#faults-across-runs):
  - Pair A primary reboot: 3 of 3 runs, outages of 19.668 to 23.344 s.
  - Pair B primary reboot: 2 of 2 runs, outages of 20.664 to 22.177 s.
- Example, reboot of switch-a1:
  - The last LACPDU from switch-a1 came at 8.89 s.
  - At 12.39 s, switch-b1 marked its bond member `ether3` expired. It was not collecting or distributing, as expected with `lacp-rate=1sec`.
  - switch-b1 still sent traffic frames out `ether3` into the rebooting switch-a1 until switch-a1 forwarded again at 29.01 s.
- No traffic crossed either peer link during the outage, although the `interpair` bond member of switch-b2 stayed active (`ATGSCD--`).
- During the outage, switch-b1 showed `ether3` as `ATGS---E`, then `ATGS--F-` with no partner.
- The bridge port `interpair` stayed `forwarding: yes`, and the MAC address of host2 stayed on `interpair`.
- The surviving MLAG peer switch-a2 stayed `mlag-state: connected` and only logged `MLAG: remote heartbeat timeout`.
- MLAG secondary reboots lost no ping, but no test traffic used the MLAG secondary's links, so they do not test this path.
- One MLAG pair recovers normally: on the Medium lab with spanning tree off an MLAG primary reboot stays within 5 s. There the access switch has a plain LACP bond with a bond member to each MLAG peer.
- Networka reproduces it on the current two-pair labs, runs `networka-0.5.2-20261127`, one ping every 100 ms against 5 s:
  - [Two-pair lab](../../tests/two-pair/README.md), reboot-a-primary: FAIL, an outage of 18.9537 to 19.1575 s on host1 to host2.
  - Two-pair lab, reboot-b-primary: FAIL, an outage of 18.0634 to 18.2708 s on host1 to host2.
  - [Two-pair strict lab](../../tests/two-pair-strict/README.md), reboot-a-primary: FAIL, an outage of 19.4467 to 19.6514 s on host1 to host2.
  - [Two-pair RSTP lab](../../tests/two-pair-rstp/README.md), reboot-a-primary: FAIL, an outage of 25.7228 to 25.9308 s on host1 to host2.

**Not verified.**

- Whether `lacp-strict=yes` on `interpair` changes the cause. The one old-suite run, `results/2026-11-24-two-pair/stp-off-strict`, ended in ERROR with an outage of 16.45 to 16.65 s and the same bond member flags. The current two-pair strict lab fails as shown above.
- Power loss on the two-pair lab. There the link goes down, which may avoid the outage.
- Whether hardware shows the same outage on a reboot. A rebooting CHR keeps its link up, and most hardware drops it. Any fault that stops forwarding while the link stays up triggers the behaviour.

**Reproduce.**

1. Build two MLAG pairs on 7.26beta7, cabled as above, spanning tree off.
2. Ping every 100 ms between a host on pair A and a host on pair B.
3. Stop pair A's MLAG primary while its link stays up: `/system reboot` on CHR, or freeze the CHR guest in QEMU.
4. Finding: on switch-b1, `/interface bonding monitor interpair` shows the bond member toward the stopped switch as `E`, then `F`, but `/interface bridge port print` still shows `interpair` forwarding. Its tx counter keeps rising, nothing crosses the peer link, and the pings fail until the stopped switch forwards again.

## Next action

- To file a report with MikroTik, send both findings with this page. Ask whether an MLAG bond whose only local bond member has no LACP partner should stay a forwarding bridge port.

## Evidence

- Old-suite run folders: [bond member flap](../../results/2026-11-24-forwarding-checks/stable-none-plink-macmove-flap/03-member-flap-repeat), [MLAG secondary reboot](../../results/2026-11-24-forwarding-checks/validation-none-reboot-power/01-secondary-reboot), [two-pair MLAG primary reboot](../../results/2026-11-24-forwarding-checks/debian-two-pair-stp-off-suite/01-two-pair-stp-off-reboot-a-primary) and [Medium RSTP MLAG secondary reboot](../../results/2026-11-24-medium-search/rstp-pair-root-run2/01-medium-pair-root-reboot-secondary).
- Each folder publishes `result.json`, `timeline.tsv`, the RouterOS configs and the capture checksums in `pcap.sha256`. That file merges the RouterOS state samples, LACP frames and syslog quoted here.
- Packet captures and the raw state and syslog files are not published.
- Current runs: the `report.md` of each test under `tests/<lab>/runs/networka-0.5.2-20261127/`.
