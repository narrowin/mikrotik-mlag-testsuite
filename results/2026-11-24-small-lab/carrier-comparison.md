# Carrier asymmetry in the two-CHR virtual lab

**24 November 2026.** The two tests exposed different behavior at the boundary between a Containerlab link and a QEMU guest. The Linux withdrawal left RouterOS with carrier and stale forwarding. A guest-only carrier drop moved the MAC to the peer link, but Linux still waited for LACP to time out. Neither action signaled loss to both endpoint drivers. [Combined timeline](carrier-comparison-timeline.tsv)

## What was measured

Both trials used the same two RouterOS 7.26beta7 CHRs and six numbered ICMP streams at a nominal 100 ms cadence. All streams passed the 61-second baseline. The withdrawn member stayed down for roughly 16 seconds in each trial. Both bonds fully renegotiated before starting the second trial. Client 2 and the bypass control stayed up. The final baseline passed. [Run and recovery procedure](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/operator-guide.md#how-one-fault-turns-into-a-report)

| Virtual fault | What each endpoint saw | Client 1 impact |
| --- | --- | --- |
| **Linux-side administrative withdrawal** | Client 1's `eth1` went down. The peer veth in the CHR container reported `NO-CARRIER`. RouterOS `ether3` stayed `link-ok`. | **19.34 s** between the last and first good replies, including the time the test held the fault and recovery after restoration. The mobile's independent reverse stream missed 181 replies in a row, with a gap bounded by **19.13–19.33 s**. |
| **QEMU guest-only carrier loss** | QEMU `set_link` on `nic2` made RouterOS `ether3` report `no-link`. Client 1's veth retained `UP,LOWER_UP`. | **2.39–2.60 s** of missed replies on withdrawal, then a separate **2.50–2.70 s** on return. |

In the Linux-side trial, 24 sequence numbers in client 1's originating stream had no request at its own capture point. The ping log recorded local unreachable errors. The 19.34 s figure uses successful replies and includes this sender-side stall. The duration shows what the client experienced during this deliberately held trial.

## What the combined timeline shows

Times in this table are relative to completion of the Linux withdrawal or acknowledgment of the relevant QEMU command. Syslog rows use the collector's receipt time. State queries have start and end timestamps, so close events may fall in the same observation interval.

| Phase | Observation |
| --- | --- |
| **Linux withdrawal, first missed probe** | Probe 615 crossed CHR 2 and the peer link to the mobile on CHR 1. The reply left through CHR 1's old client TAP and never reached the client bond. |
| **Linux withdrawal, about +3.13 s** | CHR 1 advertised expired LACP (`0x8f`). It still reported guest carrier, an active member and a local FDB entry for the client on VLAN 110. For about three seconds, the mobile’s outgoing probes to client 1 appeared on neither client TAP. |
| **Linux withdrawal, about +6.38 s** | CHR 1 reported a defaulted member around the time old-port forwarding resumed. During the remaining hold, 87 of the mobile’s requests to client 1 appeared on the withdrawn TAP, and zero appeared on the surviving client TAP. The polling interval brackets the state change. |
| **Guest-only loss, about +0.06 s** | CHR 1 logged that the client MAC moved from `client1` to the peer link `ether2`. RouterOS snapshots confirmed the move, no guest carrier and an inactive member. Client 1 still sent onto the affected leg. Its LACP actor advertised expiry about **2.54 s** after the QEMU acknowledgment. |
| **Guest-only restore, about +0.09 s** | Syslog recorded the client bond's spanning-tree role progressing to `DESIGNATED_FORWARD` and the MAC moving from the peer link back to the local bond. Probe 915’s reply went to that returning leg before both LACP actors advertised collecting and distributing, about **2.75 s** after the QEMU acknowledgment. |

MLAG stayed connected on both peers. The shared root and the sampled topology-change counter held steady. The peer captures contained ICCP traffic. The local spanning-tree role changes on restoration are in syslog. The evidence supports early return to the restored leg relative to LACP eligibility. It leaves the internal RouterOS decision path open.

## What was problematic and what should change

1. **The injection point was different in each trial.** One action cut the Linux veth and its traffic while leaving guest carrier up. The other cut guest carrier while leaving Linux carrier up. Compare the observed signals at the two drivers, and keep these cases under their own labels. Their timings describe those virtual failures.
2. **Add a synchronized virtual cable-loss control.** From the lab host, drop the CHR container’s affected veth end so the Linux client stays administratively up and loses `LOWER_UP`. Also signal carrier down to the matching QEMU guest NIC. Confirm both endpoint observations and record the skew between them. Restore both signals and verify them again. Use the observed carrier transitions and the packet time base when scoring the fault. Keep the healthy leg and management network up throughout.
3. **Keep a separate silent LACP control.** Preserve carrier and payload on both sides while withholding only LACP control frames on the selected lab path. Verify what was suppressed from the capture. This distinguishes LACP expiry from side effects of dropping the whole virtual link. Compare with an ordinary LACP bond on the same veth/TAP adapter if stale local forwarding persists.
4. **Keep debug scoped.** This run enabled broad debug and captured 3,138 SSH debug records out of 3,435 syslog lines. That scope was unnecessary, and the run provides no measured estimate of its impact. Both live peers and the startup file now use bridge, spanning-tree and interface debug rules. Individual LACP flags come from the member monitor and wire packets. [MikroTik logging topics](https://manual.mikrotik.com/docs/diagnostics-monitoring-and-troubleshooting/log/) · [Lab logging rules](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/syslog/README.md)

Run the synchronized control before using this setup to score cable-loss convergence. Score withdrawal and return separately. The two asymmetric cases remain useful for investigating failures in this Containerlab adapter and for checking RouterOS’s behavior when only one side sees loss.

## Reproduce the analysis

The archive contains 20 PCAPs with zero reported kernel drops, 516 complete RouterOS snapshots, Linux link events, QEMU command receipts, ping output and the raw syslog window. The combined TSV uses seconds from the beginning of the measured baseline. Extract the archive and run these commands from its top-level directory.

```sh
(cd run && shasum -a 256 -c pcap.sha256)
uv run --no-project reconstruct.py run
uv run --no-project timeline.py run
```

Archive SHA-256 is `f4f1974d3b1e59da09b62409f3a998cb431a8ded319643308641279a77be1290`. Both lab peers and client bonds were restored after the trial. The two CHRs are running with the scoped diagnostic settings.
