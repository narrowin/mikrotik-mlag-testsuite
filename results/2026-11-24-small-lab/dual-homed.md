# Dual-homed MAC mobility on OrbStack

**24 November 2026.** Both dual-homed clients received **290/290 replies** while the mobile endpoint moved from CHR 1 to CHR 2 and back. No unicast addressed to the mobile MAC reached either old port after its announcement. The run used two RouterOS 7.26beta7 CHRs and Containerlab 0.83.0 in OrbStack’s ARM64 `debian-clab` VM. [Captures, device state, topology and analysis](dual-homed-evidence.tar.gz)

## Why LACP now works in this lab

The two clients each had a Linux 802.3ad bond with one link to each CHR. In the initial deployment, RouterOS reported `link-ok`, no rate and `full-duplex: no` for its client-facing virtual NICs. The MLAG peer session was connected, but the clients had no usable two-member aggregate. The first run had already shown that changing LACP timers was insufficient. [First run](README.md) · [Linux bonding requirements for 802.3ad](https://docs.kernel.org/networking/bonding.html)

For the comparison, the CHR image, RouterOS configuration, client bonds, wiring and fast LACP timers stayed the same. Both runs enabled link-local protocol forwarding on the disposable CHR data adapters. The second deployment added `speed=10000,duplex=full` to the QEMU virtio data NICs. RouterOS then reported **10 Gbit/s, full duplex** on both peers. This describes the advertised virtual link properties. The experiment ran at low packet rates.

Both clients selected two members. On every leg the actor and partner state was `0x3f`, including synchronization, collecting and distributing. The state held before and after calibration, on the remote attachment and after the move back. The wire captures confirm payload delivery on both members of each client bond. For each client's 290 mobile replies, 219 arrived on the CHR 1 leg and 71 on the CHR 2 leg. The mobile was attached to CHR 2 for those 71 replies. The fixed outbound client flows used the CHR 1 leg. These counts establish the actual paths for this run.

## One-way timing calibration

Each stationary client sent numbered ICMP requests to the mobile at a nominal 100 ms interval. The mobile sent independent streams back. Two more client-to-client streams provided controls, one over the test VLAN and one over a separate cable. A two-second egress drop on CHR 1's private link to the mobile affected both clients. Monotonic timestamps around the kernel operations bound the applied cut to **2.010–2.016 s**.

| Measured request direction | Received | Consecutive misses | Outage bounds from actual send times |
| --- | ---: | --- | ---: |
| Client 1 → mobile | 150/170 | 40–59 inclusive | 1.976–2.190 s |
| Client 2 → mobile | 150/170 | 40–59 inclusive | 1.976–2.190 s |
| Mobile → client 1 and mobile → client 2 | 170/170 each | 0 | No forward loss detected |
| Client-to-client controls | 170/170 each | 0 | No loss detected |

The two reverse pings each lost 20 replies on their return path. Comparing **requests** at their sender and receiver identified the one-way failure.

## Consecutive MAC moves

The mobile kept IP `10.110.0.50`, MAC `02:00:00:11:00:50` and VLAN 110. The active attachment changed while both physical links remained up. Six streams continued through both moves. Before moving back, each client completed ten additional pings, both peers showed the expected MAC location, and all client bond members still collected and distributed.

| Move | Observer | Missed probes | First reply after the new-port GARP | Frames addressed to mobile MAC at old port after GARP |
| --- | --- | ---: | ---: | ---: |
| CHR 1 → CHR 2 | Client 1 | 0 | 22.4 ms | 0 |
| CHR 1 → CHR 2 | Client 2 | 0 | 22.5 ms | 0 |
| CHR 2 → CHR 1 | Client 1 | 0 | 24.4 ms | 0 |
| CHR 2 → CHR 1 | Client 2 | 0 | 48.8 ms | 0 |

**Outage resolution.** The longest gaps between consecutive replies anywhere in the sequence were **111.8 ms for client 1** and **112.1 ms for client 2**. Both received every numbered reply. A shorter interruption could fall between probes. All six streams had zero late deliveries at the one-second deadline, duplicates or missing probes.

**Old-port traffic.** At the CHR guest-facing TAP and on the mobile’s inactive leg, the first old port saw five frames after the move, one broadcast ARP and four IPv6 multicast frames. The other old port saw ten after the return, consisting of ARP, IPv6 multicast and discovery traffic. Neither captured unicast addressed to the mobile MAC between the move command and the first announcement, or after the announcement. All 19 observers in each phase reported zero kernel capture drops.

**Switch state.** CHR 1’s MAC/VID entry changed from local `ether5` to peer `ether2` and back. CHR 2 showed the inverse. Both peers retained the same RSTP root ID, MLAG roles and bridge topology-change counter across the snapshots. State came from direct RouterOS SSH queries. Networka integration, actual VM migration and failover after losing a client member have separate acceptance checks.

## Reuse the setup and verify the measurements

The archive includes the original comparison topology (`small.clab.yml`), the working topology (`full.clab.yml`), the ARM64 QEMU option wrapper, the RouterOS configuration, and the Linux endpoint setup commands actually used. The client and mobile bonds, test VLAN and peer links are all isolated inside the lab. For a future campaign, resolve the current CHR image and record its digest. The archived topology identifies the build that produced these results.

The before-and-after NIC readings and client state are in `ev/`. Each measurement phase includes per-port PCAPs, kernel drop counts, event timestamps, device snapshots, ping logs and computed metrics. From the extracted archive root, verify the captures and recompute the sequence analysis with:

```sh
shasum -a 256 -c calibration/pcap.sha256
shasum -a 256 -c mobility/pcap.sha256
uv run --no-project readcaptures.py calibration
uv run --no-project readcaptures.py mobility
```

Archive SHA-256 is `a12a2c69dd466ae1d2ca47a3c38b87220328d5ad55545460ea5428f7a46c13a0`.
