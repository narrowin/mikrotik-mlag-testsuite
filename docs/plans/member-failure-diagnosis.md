# Two-CHR member failure diagnosis

**Scope.** Stay with the existing OrbStack pair and replay the Linux client 1 leg loss against CHR 1. The question is why the surviving leg kept delivering requests while return traffic failed. The archived packet evidence is scored here. The new RouterOS monitor commands were verified against the live lab in steady state. [Full postmortem and evidence](../../results/2026-11-24-small-lab/postmortem.md)

## What the first run established

Use the completed Linux disable command as time zero. Match client 1's numbered ICMP requests and replies (`icmp.ident == 101`) on both CHR client TAPs, the peer TAPs and the mobile endpoint.

| Interval | Packet and device evidence |
| --- | --- |
| First 3.168 s | The Linux client stopped transmitting LACP on the withdrawn leg. The client sent requests over CHR 2 and the peer link to the mobile on CHR 1. Replies for sequences 852–882 exited CHR 1's old client TAP. |
| 3.168 s after withdrawal | CHR 1 advertised expired LACP state (`0x8f`), with collecting and distributing clear in its actor flags. This was 3.271 s after the last client LACP frame on that link. See frame 5305 in `p1-tap2.pcap`. |
| After expiry | The mobile received and answered sequences 883–914. Neither client-leg TAP saw the 32 replies. CHR 1's aggregate monitor still listed `ether3` as active, and the client's MAC/VID entry still pointed to the local `client1` bond. |
| 6.555 s after withdrawal | Sequence 915 was the first reply to reappear on the old TAP, while the client leg was still down. It was followed by 24 more there before the restore command. No missing reply took the surviving client TAP during the 111-probe gap. |

The bridge stayed peered and the sampled RSTP root and topology counters stayed unchanged. This rules out a simple explanation that the outage was the fast LACP timeout or an observed STP reconvergence. The wire shows LACP expiry, then a period with no reply on either leg, then resumed delivery to the disabled leg. The first report described the stale path but did not distinguish these phases. A MikroTik forum operator also reported different results for client-side and switch-side withdrawal. [Original evidence](../../results/2026-11-24-small-lab/postmortem.md) · [Comparable field report](https://forum.mikrotik.com/t/mlag-client-lacp-failover-handling/272065)

## What we still need to see

- **Carrier on three surfaces.** Time-stamp `ip -ts monitor link` in the client namespace and CHR container namespace. In RouterOS read the guest's `ether3` carrier. The installed Containerlab launcher bridges the veth to a TAP. Its link watcher attaches a missing veth when it appears. The watcher does not mirror administrative state or carrier changes into QEMU. We still need to observe live whether Linux `LOWER_UP` drops while the guest continues to see `link-ok`. This distinguishes the virtual failure mechanism from a direct cable cut. [Containerlab CHR kind](https://containerlab.dev/manual/kinds/mikrotik_chr/) · [QEMU guest link control](https://www.qemu.org/docs/master/interop/qemu-qmp-ref.html)
- **RouterOS per-member LACP state on both peers.** The aggregate's active list obscured the transition. Collect local and partner flags, key, selected partner and port state. Check for expired and defaulted states and when collecting/distributing returns. The command below worked on 7.26beta7, with one-shot and continuous output. Both lab peers currently show `lacp-rate=1sec`, `link-monitoring=mii` and `lacp-strict=no` on this bond. [RouterOS member monitor and flags](https://manual.mikrotik.com/docs/cli-reference/interface/bonding/monitor-slaves/)
- **Match the forwarding decision to those signals.** Keep the authoritative captures at the client, both client TAPs, the peer link and the mobile. Poll the FDB for the client's MAC and VLAN 110 on both peers, plus bridge state. Use the common Linux host clock for captures, Linux notifications, collector receipt times and fault markers. Bracket snapshots with command start/end times. If the internal forwarding decision is still ambiguous, the evidence is enough to ask MikroTik what happened between the documented state and the observed transmit port.

Verified RouterOS commands:

```routeros
/interface/bonding/monitor-slaves bond=client1
/interface/bonding/monitor-slaves bond=client1 once=yes
/interface/ethernet/monitor ether3 once
/interface/bridge/host/print detail where mac-address=02:00:00:11:00:11
```

## Options for telemetry

**Classification.** Two-way door for temporary collection on the lab.

**Problem.** The first run could see protocol expiry and wrong-port packets. It could not align those observations with changes in guest carrier and the individual member.

**Desired outcome.** Put carrier, member state, MAC egress and observed delivery on one clock across the entire fault and restoration.

| Option | What it contributes | What to verify |
| --- | --- | --- |
| Linux link events, continuous RouterOS CLI monitors over persistent SSH, and PCAPs | Native event timestamps on Linux, RouterOS per-member and guest link samples, and actual protocol and payload on the wire. Add targeted FDB/bridge snapshots on a separate session. | The member command already streams over one SSH session. Measure cadence and observer CPU on both peers before injecting a fault. Preserve raw output and tag it with the source and capture clock. Each CLI monitor samples state, so packets and Linux link events provide the finer timing. |
| Native RouterOS API on a persistent session | The native API returned structured bond-member, guest Ethernet and bridge monitor samples on both CHRs. It also returned the targeted MAC/VID entry on request. | Both `/interface/listen` and `/interface/bridge/host/listen` were quiet during the steady-state check. Verify their notifications during a known change before relying on them. REST is request/response with a 60-second limit on a request. [RouterOS API](https://manual.mikrotik.com/docs/developer-guides/api/) · [REST limits](https://manual.mikrotik.com/docs/developer-guides/rest-api/) |
| Remote syslog | The lab already sends RouterOS logs through the management VRF. A syslog record can corroborate an event independently of the monitor session. | Keep collector receipt times alongside device timestamps. Check both peers' markers around each measured event. [Verified lab syslog](../syslog/README.md) |
| SNMP interface traps | RouterOS documents `linkDown` and `linkUp` traps for changes of interface state. These can corroborate guest-visible carrier and feed an existing network management system. | These traps expose an interface index and event, without the LACP member flags or FDB forwarding decision needed here. Carrier can stay up during partner expiry. SNMP remained disabled on both lab CHRs during this evaluation. [RouterOS SNMP traps](https://manual.mikrotik.com/docs/diagnostics-monitoring-and-troubleshooting/snmp/) |

| Collection choice | Impact | Confidence | Ease | ICE |
| --- | --- | --- | --- | ---: |
| Extend persistent CLI collection with Linux link events and packet captures | 9 because it covers both missing observations | 9 because the saved run validates the baseline and the live member monitor returned repeated samples | 9 because the lab already has the sessions and capture points | 729 |
| Build around a persistent RouterOS API connection immediately | 8 because structured streams simplify parsing | 7 because steady-state monitor coverage was verified and notification behavior under fault remains open | 6 because it requires a new collection path | 336 |

**API check on 7.26beta7.** Each peer returned five samples for each of `/interface/bonding/monitor-slaves`, `/interface/ethernet/monitor` and `/interface/bridge/monitor` over one 4.4-second management session. The samples were about one second apart and contained the expected actor and partner flags, `link-ok` on the guest port and the connected MLAG state. The FDB read returned VLAN 110 and egress `client1`. This verifies structured periodic streaming in steady state. The listener check produced no event to score. [RouterOS LACP flags](https://manual.mikrotik.com/docs/cli-reference/interface/bonding/monitor-slaves/)

Start with the first option for the fault replay. The existing collector, syslog, Linux link events and per-port captures cover the questions the next run needs to answer. Use the API streams if structured fields will simplify a later repeat. Retain packet timestamps for timing below the monitor interval. SNMP is an optional separate check when instrumentation must demonstrate trap delivery to a network management system. NUTS remains useful for steady-state reachability checks.

Both live CHRs now send routine UDP syslog through the management VRF to one receiver. Add its time-bounded export to each run. Focused debug can be enabled for a single event and is disabled between runs. [Verified configuration and sample records](../syslog/README.md)

## How to isolate and fix it

Run one change at a time on the existing pair. Apply the same six streams and the same packet-to-port verdict each time. Keep the leg withdrawn for at least 15 seconds in this diagnostic run, or long enough to capture any expiry-to-defaulted transition and 10 consecutive successful replies if the surviving path recovers. Record return separately. Restore the prior configuration between variants.

1. **Repeat the Linux-side withdrawal with the new collectors.** Confirm whether guest carrier stays up and whether `defaulted`, the active-member list or the FDB changes before old-port forwarding restarts.
2. **Give only the affected QEMU NIC an explicit guest-visible link loss.** Verify that RouterOS sees the carrier drop and compare convergence on the same VLAN and flows. If this removes the prolonged outage, use verified guest-visible carrier for the lab's cable-pull test. Keep the original Linux-side withdrawal as its own LACP-silence case. A physical cable pull on a matched bench can validate the deployment behavior. [QEMU monitor schema](https://raw.githubusercontent.com/qemu/qemu/master/qapi/net.json)
3. **Compare strict LACP on the same build.** With full duplex still verified, change only `lacp-strict` consistently on the affected distributed bond on both peers. Verify the wire and the service before scoring a fix. This is a configuration hypothesis prompted by the expired-to-old-port behavior and the observed `lacp-strict=no` setting. Record effects on startup, loss and failback. The bridge setting `mlag-lacp-fallback` controls the system ID on *peer-link loss*. The peer stayed connected in this experiment. [RouterOS bridge settings](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/)
4. **Run the ordinary LACP control on the same build.** On one CHR, reproduce the same silent member loss with an ordinary two-member bond and local responder. If it repeats there, the implicated path is shared with ordinary bonding or the adapter. If the control passes and the MLAG pair continues using the expired or defaulted member, preserve the before/during/after evidence for a scoped MikroTik report. Use the campaign's pinned development build for both setups.

A candidate fix passes when the inactive member stops receiving client unicast after convergence, the surviving member actually delivers, and both failure and restoration are within the declared budget. Preserve the separate result if an explicitly guest-signaled cable cut works while a silent partner or Linux veth withdrawal still fails.
