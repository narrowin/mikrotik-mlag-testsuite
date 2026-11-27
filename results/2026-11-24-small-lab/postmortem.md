# Two-CHR OrbStack campaign and postmortem

**24 November 2026.** The evidence was sufficient to reconstruct the failures and restoration. The timing calibration and announced MAC moves passed. Single-member withdrawal and restoration missed the one-second lab target even though the MLAG session stayed connected. A peer-link cut interrupted both clients. The five lab nodes were left healthy in OrbStack’s `debian-clab` VM. [Test plan](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/validation-plan.md)

## Topology and run

Two RouterOS 7.26beta7 CHRs on Containerlab 0.83.0 ran with two dual-homed Linux clients and a mobile Linux endpoint in VLAN 110. CHR 2 was the MLAG primary. CHR 1 initially hosted the mobile endpoint. The isolated virtual adapters used the previously verified full-duplex settings. [Wiring and virtual NIC settings](dual-homed.md)

Six numbered Linux ICMP streams ran at a nominal 100 ms cadence. Each client probed the mobile, the mobile independently probed both clients, and two client-to-client controls used the test VLAN and a dedicated bypass cable. The 61-second baseline had zero loss across all six streams. Traffic continued through two calibration drops, both MAC moves, and withdrawal and restoration of the Linux member, the RouterOS member, and the peer link. The recovery gate checked MLAG, both negotiated members on each client and ten consecutive replies per client. For MAC moves it also verified both learned egress ports.

## Measurements

The outage ranges use send timestamps around each run of missed replies. A receive gap measures the interval between successful replies and includes a probe interval. The independent cable had zero misses throughout.

| Event | Client 1 → mobile | Client 2 → mobile | What the traces show |
| --- | --- | --- | --- |
| Calibration pulse 1 | 19 misses, 1.870–2.079 s | 19, 1.874–2.079 s | The kernel cut lasted 2.002–2.005 s. All independently numbered reverse requests reached their clients. |
| Calibration pulse 2 | 19 misses, 1.870–2.079 s | 19, 1.870–2.080 s | The kernel cut lasted 2.010–2.013 s. It produced a distinct gap in the same direction. |
| MAC move to CHR 2 and back | 0 misses | 0 misses | Zero unicast to the old attachment after either announcement at both capture points. The first replies after an announcement arrived in 35.8–96.2 ms. |
| Linux client 1 withdraws its CHR 1 leg | 111 misses, 11.463–11.676 s across withdrawal and return | 0 misses | The leg stayed down for about 9.13 s. Requests arrived over the surviving leg. Replies went to the disabled attachment, disappeared from both client TAPs after LACP expiry, then resumed on the disabled leg. [Member timeline](../../docs/findings/silent-bond-member.md#linux-side-takes-a-bond-member-down) |
| RouterOS withdraws the corresponding client port | 26 misses, 2.602–2.809 s | 0 misses | The Linux bond initially kept sending to the affected leg. CHR 1 learned the client via the peer after forwarding switched. |
| RouterOS restores that port | 22 misses, 2.197–2.408 s | 0 misses | A separate return-path gap occurred while the restored member negotiated. |
| CHR 1 disables and restores the peer link | 13.258 s between good replies | 12.351 s between good replies | Client 1 had nine sequence numbers with no request at its own capture point. Client 2’s sampled outage bounds were 11.081–12.351 s. |

During the peer-link outage client 1 had no captured transmission for sequences 1256–1264. The ping log attributes eight of them to local “Destination Host Unreachable” errors. The reverse round trips from the mobile had receive gaps of **13.160 s** to client 1 and **12.416 s** to client 2. The shared-VLAN client-to-client control lost two packets at peer-link withdrawal and three at restoration. All six streams were healthy at the end. Interruptions shorter than a probe interval could fall between samples.

## Reconstructing the events

**Client-side withdrawal.** Filter for `icmp.ident == 101 && icmp.seq == 852`. The request appears in frame 328 on CHR 2’s client TAP, crosses its peer TAP in frame 689, and reaches the mobile on CHR 1. The reply appears in frame 5210 on CHR 1’s TAP toward the disabled client leg. Client 1's bond never receives it. In the paired `client_down` snapshots, Linux marks the leg down and selects one active member. CHR 1 still lists `ether3` as active and the client's VLAN-110 MAC on its local bond. MLAG stayed connected and the RSTP root and topology-change counters held steady. The traces locate stale local-leg forwarding. The reason the CHR retained that member needs separate testing. [Comparable MikroTik field report](https://forum.mikrotik.com/t/mlag-client-lacp-failover-handling/272065)

**RouterOS-side withdrawal and return.** During withdrawal, sequence 1020 reaches CHR 1’s client TAP and goes no farther. The client then advertises the affected member as expired. RouterOS lists it inactive and learns the client via the peer. During restoration, sequence 1109 reaches the mobile, then its reply exits CHR 1’s returning member while the client is still negotiating it. The two stages interrupt different directions.

**Peer-link partition.** CHR 1 reported `peer port not running` and advertised its own bridge and LACP system IDs. CHR 2 still showed `connected` in the paired samples during the cut. Its log records disconnect and reconnect in the same second at restoration. Both CHRs returned to the shared RSTP root and incremented their bridge topology-change counters from one to two. A longer partition, opposite role orientation, or physical carrier loss can produce different behavior.

## Evidence quality and test precedents

| Practice | Evidence from this run |
| --- | --- |
| Measure failover and reversion independently with packet sequence numbers and timestamps. [RFC 6414, §3.6](https://www.rfc-editor.org/rfc/rfc6414.html#section-3.6) | Each calibration bounds the measured kernel cut. Restoring the RouterOS member produced a second outage. |
| Send traffic during the fault, identify gaps and duplicates, and verify switch roles. [SONiC link-failure tests](https://github.com/sonic-net/sonic-mgmt/blob/master/tests/dualtor_io/test_link_failure.py) · [SONiC packet analysis](https://github.com/sonic-net/sonic-mgmt/blob/master/tests/common/dualtor/dual_tor_io.py) | Sender, receiver and old-port captures distinguished absent sends, misdirected replies and an unaffected bypass. The six measured streams had no duplicate deliveries. |
| Verify member and role selection before switching and again after clearing the forced state. [Nokia 7750 MC-LAG worked example](https://documentation.nokia.com/acg/25-3-2/books/interface-configuration-classic/c008-mc-lag.html) | Paired snapshots retain bridge roles, RSTP, MLAG, bonds, the FDB by VID, VLAN membership and CPU. Linux snapshots add link counters, bond state and neighbors. |
| Preserve raw evidence on a common time base. | All 19 captures reported zero kernel drops. All 334 scheduled RouterOS snapshots were complete, 167 per peer. Median poll spacing was 0.889 s and the maximum was 0.985 s. Each query has start and end timestamps on the capture host. |

The first attempt opened a fresh password-authenticated SSH connection for each poll. Authentication became intermittent and the resulting gaps are preserved in `collection-preflight/`. The scored rerun reused one authenticated connection per CHR and retained every sample. A probe-stop error extended the ping logs beyond the capture window. The offline reader uses the recorded observation window, and final connectivity and two-member LACP were independently verified after the probes stopped.

This run qualifies the evidence workflow and the announced mobility case for this role orientation. It records failures against the member service target. Stable RouterOS, additional orientations, hardware, actual VM migration and gateway failover have independent cases.

## Inspect the archive

The archive includes the topology and CHR configuration, captures and checksums, timed state snapshots, logs, and an offline reader. `evidence/postmortem.json` includes the first and last missed sequences, wire positions of the first missing packets, LACP transitions and timing bounds. Its relative clock starts at the beginning of the 61-second baseline.

```sh
(cd evidence && shasum -a 256 -c pcap.sha256)
uv run --no-project reconstruct.py evidence
tshark -n -r evidence/captures/p1-tap2.pcap -Y 'icmp.ident == 101 && icmp.seq == 852'
```

The archive SHA-256 is `20f239fe09903643dbed07744bdbd52b3ce2ba9fa88040e37e2f226bd95c2c3c`. The live topology is `nwfull1124` at `/tmp/nwmlag-full1124/full.clab.yml` inside `debian-clab`.
