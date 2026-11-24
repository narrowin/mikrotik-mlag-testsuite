# Measurement and acceptance criteria

[Validation plan](../validation-plan.md) · [Case catalogue](../case-catalog.md)

## Measure a failure while it happens

**Problem statement.** A five-packet ping before and after a fault misses transient outages, failures on one hash path, and traffic delivered to a bystander. Periodic ARP can even repair the condition being measured.

**Use NUTS for reachability assertions.** Its Linux and RouterOS YAML checks cover positive and negative reachability. Allocate two real CHRs per modeled MLAG pair and use the RouterOS 7.22+ per-bridge MLAG settings. Check the rendered export on each peer if an existing playbook still uses the old `/interface bridge mlag` menu. [Upstream NUTS](https://github.com/network-unit-testing-system/nuts)

The Linux client image needs `ping`, `iperf3`, `tcpdump`, `tshark` and `arping`. Verify which image and services actually run. For silent-host cases, use a quiet client or stop periodic announcements for that run and prove silence on capture.

**Lab setup.** Use an isolated Containerlab host. Record its version, CPU budget, acceleration, image tags/digests and CHR license. On current Containerlab the native `mikrotik_chr` kind accepts the official CHR image. The existing `mikrotik_ros` kind remains an option with a version-matched vrnetlab build. Start well below measured capacity. Free CHR licenses limit upload to 1 Mbit/s per interface. A saturated VM, license cap, or full capture buffer invalidates a loss measurement. [Native CHR kind](https://containerlab.dev/manual/kinds/mikrotik_chr/) · [Containerlab current release](https://github.com/srl-labs/containerlab/releases/latest) · [CHR licensing](https://manual.mikrotik.com/docs/getting-started/routeros-licensing/chr/chr-licensing/)

**OrbStack preflight.** On ARM64 `debian-clab`, inspect `/interface ethernet monitor ether3 once` on each CHR. A usable virtual Ethernet link for this test reported a rate and full duplex. The tested setup passed link-local protocols across the CHR adapter ports and advertised `speed=10000,duplex=full` on the QEMU data NICs. Before measuring a fault, verify both Linux bond members and the actor and partner collecting/distributing bits. [Working two-CHR configuration and packet evidence](../../results/2026-11-24-small-lab/dual-homed.md)

### Capture and inspect the data plane

Use NUTS for repeatable reachability and isolation assertions before and after each case. During the event, keep independently numbered Linux pings running at 100 ms for each direction and a control path. Use tcpdump at the endpoints and relevant forwarding ports. Read the saved captures with TShark. These tools reproduced two known drops and traced a reply across the correct peer link and out the wrong client leg. The archived Python reader consumes TShark output and uses the standard library. [Small-lab postmortem](../../results/2026-11-24-small-lab/postmortem.md)

For a MAC move, capture both attachments and the independent witness. Verify each observer sees a frame it should receive before scoring absence. Match the sequence number across captures and check the intended destination as well as the old port. Use a timed read-only session per CHR. Check that it sustains the intended cadence before applying the first fault. A failed query or missing capture makes the affected evidence inconclusive.

### Distributed probes and outage timing

**Problem statement.** If an access client loses the remote service for two seconds, the measure of interest is the time that *client and direction* lost service. Another client, or the reverse path, may still work. A poll of the core cannot measure that interval.

Use the documented Linux ICMP streams for small Layer 2 runs. Where a case calls for sequenced UDP between Linux endpoints, use the current **IRTT** release. It produces per-packet JSON and uses a server receipt window to help identify direction. Keep ICMP for a VIP that cannot run an IRTT server, and use an actual TCP request for application availability. Preserve endpoint captures for one-way loss, delayed packets and cases where IRTT reports an unknown loss direction. [IRTT client and result fields](https://github.com/heistp/irtt/blob/master/doc/irtt-client.md) · [IRTT releases](https://github.com/heistp/irtt/releases/latest) · [IETF one-way loss metric](https://www.rfc-editor.org/rfc/rfc7680.html)

| Clients to place | Concurrent traffic | What the comparison reveals |
| --- | --- | --- |
| A1-side and A2-side single-attached clients, plus a dual-homed client | Each single-attached client exchanges data with the dual-homed client. Run both initiation directions. | Loss specific to one ingress peer, a forced peer-port path, or one LACP member. In T1 reuse existing hosts and give single-attached probes separate network namespaces or containers and actual data ports. |
| One access client and one access-local routed service **per site** | A client ↔ A service, B client ↔ B service, A client ↔ B service, B client ↔ A service. Both sites also probe their own VIP. | A local failure, an inter-site partition and an off-path remote rejoin have distinct signatures. Mark a stream that crosses the VIP separately from a stream that ends on it. |
| A stationary sender in each site and a mobile endpoint on the stretched test VLAN | Both stationary senders target the mobile endpoint. For an active move it sends independent traffic back to both. Capture the old port, new port and an unrelated same-VLAN witness. | Which site relearns first, whether a frame still goes to the old location, and whether flooding hides a missing FDB entry. |

The collector reaches agents through out-of-band management. Each agent sends through its **data** address. Keep per-flow results in a host-mounted directory and capture on the surviving side from outside the endpoint lifecycle. An abruptly stopped IRTT client may never write its final JSON. For a site-stop or long soak, continuously write rotating PCAPs to the collector and retain the fault window before it rolls over. Map each stream to its source, destination, VID, direction, five-tuple and expected path before the fault. If a client dies with its site, record the remote observer's evidence and the end of that client's observation window. Continue every surviving stream through failback.

**Example for one routed flow.** Start the server on the service in B and the client on the access host in A. Use a fresh filename per run and verify the data route on each endpoint. For the reciprocal stream, start a server on A and a client on B. Start the other flows concurrently from their own clients. Extend the duration past the planned recovery window. [IRTT server bind syntax](https://github.com/heistp/irtt/blob/master/doc/irtt-server.md) · [Client options](https://github.com/heistp/irtt/blob/master/doc/irtt-client.md)

```sh
# Service in B
irtt server -b 10.220.0.11:2112

# Client in A
irtt client --local=10.110.0.11 --stats=both -i 100ms -d 10m -l 96 -o A-to-B-01.json 10.220.0.11:2112
```

#### How to report seconds blocked

1. Send **one probe every 100 ms per active flow**. Record actual send times. For each direction, keep captures of transmitted and received data on the endpoint interfaces. Match the same datagram by flow and sequence, or by UDP payload across the two captures. Use unique flow IDs for separate sessions. Keep delayed, reordered and duplicate arrivals. Mark a packet as late after a declared delivery deadline (initial lab value **1 s**), and as missing from the capture only after its observation window closes. Allow a drain interval after the last probe.
2. For each contiguous burst of missed deadlines, report the last timely good probe, the first and last missed probes, and the first timely good probe afterward. For regularly spaced transmissions, **missed slots × 0.1 s** estimates unavailable time. With irregular spacing, use the actual transmit timestamps and give bounds. For a single contiguous interruption, the first-to-last missed send times give the lower bound and the surrounding good sends the upper bound on the sampled service gap. A late recovered packet and a packet never delivered are different counts.
3. **Worked example, illustrative.** Sequence 480 succeeds at send time 48.0 s. Sequences 481–500 miss their deadlines. Sequence 501, sent at 50.1 s, succeeds. Report **20 missed slots, estimated 2.0 s, bounded by 1.9–2.1 s** for that direction. Report fault-to-first-recovery separately. Ten successive timely probes qualify stable recovery, dated to the first of those ten. Emit a separate row for every later outage, including rejoin. An outage still in progress at the end is reported as “at least N seconds.”
4. Keep all durations per flow and direction before summarizing the worst surviving path. A 2.0 s round-trip gap establishes an end-to-end interruption. To attribute A→B loss, locate the request at A's egress and B's ingress. To attribute B→A loss, trace B's reply back to A. Independent reverse-originated probes add coverage of different hash paths. Call it **STP blocking** only when port evidence and BPDUs support that cause.
5. For captures on one Containerlab host, use the common host clock. On separate physical hosts record clock offset/uncertainty before and after, and use a monotonic clock for local durations. If cross-host uncertainty exceeds the 100 ms sampling interval, report source-local round-trip durations and directional sequence evidence. Only score a one-way deadline when the time bases support it. For a budget close to the measured interval, use the bounds: upper bound within budget passes, lower bound above budget fails, and a boundary-straddling result needs finer sampling. Record sender stalls, capture drops, endpoint CPU overload and observations cut short by a site failure.

**Calibration before accepting a timing result.** On T0, run the affected stream plus a control on two data interfaces that bypass the test link. Attach an extra stationary endpoint or give the clients a separate, verified control path for this calibration. On the disposable data interface apply a measured **2 s one-way drop**, keeping the return direction and control path open. Record fault-on and fault-off at the injection point, using observed start/end times. Repeat in the opposite direction, then apply two short interruptions separated by a healthy interval. At 10 probes/s a clean 2.0 s interruption should lose about 20 transmissions, within one slot for healthy pacing. Require the measured bounds to contain the actual fault duration within the recorded clock/actuation uncertainty, both interruptions to appear separately, and zero loss on the unaffected control. If the sender missed its cadence or the observer lost capture data, fix the measurement and repeat before scoring MLAG. [Containerlab directional impairments](https://containerlab.dev/manual/impairments/)

### Collect RouterOS state with Networka

Start with the tested checkpoint in the small lab. Current RouterOS exposes MLAG peer state in the **bridge monitor**. The lab sequence also reads STP port roles, guest carrier, member LACP flags and the FDB entry for client 1. Save the checkpoint before the fault and after recovery. For a sustained fault, take an extra checkpoint or query the operational field of interest on all affected peers. Use the continuous collector for transitions you expect to occur between checkpoints. [Small lab installation and checkpoint](../operator-guide.md#collect-a-networka-checkpoint) · [RouterOS bridge reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/)

From the repository root, after following the installation and authentication steps, one group read can focus on the STP state while a fault is held. Use a unique results directory for each case, repeat and phase.

```sh
uv run --locked --extra checkpoints nw --inventory-prefer config run \
  --config labs/networka/small.yml --interactive-auth --store-results \
  --results-dir networka-results/S1/01/fault mlag-peers '/interface/bridge/port/monitor [find] once'
```

| Fault | First read while broken | Cross-check |
| --- | --- | --- |
| S1–S3, unexpected STP block | Port monitor on both ends of the suspect uplink. Follow immediately with `/interface/bridge/monitor [find] once` for root ID, root port, topology changes and MLAG peer state. | BPDU and payload captures establish the transition order. A later snapshot can already show a healthy tree. |
| M1/M4, stale or flushed MAC | `/interface/bridge/host/print detail where mac-address=02:00:00:00:01:01` on every peer along the path. Substitute the moving MAC, compare its VID and egress, then take a full FDB snapshot once. | First source frame on new ingress, first correct return frame and any copy on old egress. |
| L1/G2, core return and VRRP | On switches read `/interface/bonding/monitor-slaves bond=<bond> once=yes` and the bridge monitor. On the gateway group read `/interface/vrrp/print detail`. | Correlate LACP partner ID, VRRP advertisements at both routers, and continuity of the unaffected local flow. |

**Calibrate on T1.** Time ten group reads of the same bridge-port command from the collector. Record start and finish for each sweep, worst duration, missing device results and CPU with probes running. Place a known member-down and member-up event between two marked samples, holding the down state long enough for a sweep, then repeat with a brief fault. Per-device reads run concurrently. Commands within a sequence and result write times still have skew. Use continuously captured packets for subsecond outage timing. Preserve raw command output when diffing counters and topology-change timestamps.

**When a coordinator would help.** If manual fault and rejoin markers cannot be aligned with the probes, use the existing timed state and capture workflow to measure the gap. A coordinator could timestamp fault actions on that same host to reduce manual alignment. Verify the change against the T1 calibration.

#### Reusable investigation prompt

> Analyze the saved Networka results and packet captures for this case. Identify the case ID, intended root, intended gateway owner and the path that should have survived. Align fault and rejoin timestamps with the last good and first recovered probe in each direction. Find the first device, port, or MAC/VID whose observed state disagrees with that path. Cite the device, command output and packet sequence or timestamp. If the transition falls between reads, give the time bounds and name the single read or capture that would distinguish STP delay, LACP renegotiation and stale MAC forwarding on the next run.

### Procedure for every run

1. **Declare the fault and prediction.** Record build, case ID, wiring variant, root and backup, elected MLAG primary, VIP owner, timers and port roles. List flows that must continue, those physically isolated by the fault, and ports forbidden to receive each flow. Capture both the failure and the return to service as separate events.
2. **Warm and verify.** Run the existing reachability/denial pattern. For at least 60 seconds, record a loss-free baseline on each continuous flow. Check sender, receiver and observer captures. Send one deliberate witness packet to confirm the observer can see traffic on its port. Vary MAC/IP pairs and transport ports until captures or member counters prove that **every intended member** carries tagged test traffic. A single iperf stream cannot establish that.
3. **Keep probes running.** In each direction run numbered ICMP or low-rate sequenced UDP on the same VLAN, to the VIP, through the VIP to a routed service, and across sites where applicable. Keep one established TCP stream alive and repeatedly start short new TCP connections. Include one unrelated same-site flow per site. Ping each switch's in-band management IP separately from the out-of-band collector. Example for a Linux data interface: `ping -n -D -O -i 0.1 -I bond0.110 10.110.0.1`. Give each stream its own ID and sample interval.
4. **Timestamp the event.** Capture on the host-side data veths for both peers, the client legs, the service and an unrelated access port. Use one host clock for injection markers and captures where possible. Export bridge/FDB, LACP, VRRP, logs and CPU before, during the fault, immediately after return, and once stable. For a cable test verify guest carrier at both ends. For silent loss keep carrier up and confirm frames disappear in the intended direction. Containerlab netem supports directional interface impairments. For abrupt power loss suspend/stop the isolated VM and verify whether carrier fell. Restart with a method that restores its lab links. A stopped process with carrier up tests a different failure. [Capture](https://containerlab.dev/cmd/capture/) · [Impairments](https://containerlab.dev/manual/impairments/) · [CHR restart semantics](https://containerlab.dev/manual/kinds/mikrotik_chr/)
5. **Preserve the broken state.** Keep the initiating fault in place long enough to judge the surviving path. If forwarding stalls, save both peers' host tables by MAC **and VID**, captures, bond members, STP state, neighbor caches and resource history before intervention. If a reboot, ARP flush, FDB edit, or port bounce restores service, record it as a workaround after marking the case failed. Capture a support output file on the affected devices if the issue will be escalated. Retain it locally for review.
6. **Restore and repeat.** Remove only the injected fault. Verify all members return, both traffic directions work, the standby path can carry traffic again, roles settle, and the unrelated flows stay healthy. Keep recording for at least two configured bridge ageing intervals on MAC cases. Repeat each critical fault and restoration at least five times in each role orientation. Report the worst run and the number of failures.

| Evidence | Collect on both peers and on the partner where applicable |
| --- | --- |
| Bridge and spanning tree | `/interface/bridge/monitor [find] once`, `/interface/bridge/port/monitor [find] once`, effective VLAN membership. Record root ID/port, cost, topology changes, role, learning, forwarding and BPDU counters. For MSTP include each relevant instance. |
| LACP and peer state | `/interface/bonding/monitor <bond> once`, `/interface/bonding/monitor-slaves bond=<bond> once=yes`, bridge MLAG state/role. On Linux save `/proc/net/bonding/bond0`. Correlate partner system ID, key, selected aggregator, collecting/distributing and first valid payload. [Two-CHR member diagnostics](../plans/member-failure-diagnosis.md) |
| FDB and first hop | `/interface/bridge/host/print detail`, `/interface/bridge/vlan/print detail`, `/interface/vrrp/print detail`, `/ip/arp/print detail`, IPv6 neighbors if enabled. Track local, static, peer and dynamic entries separately. Record the host's IP-to-MAC neighbor entry independently of each bridge's MAC/VID-to-port mapping. |
| Packets and resources | PCAP with VLAN headers, both directions and capture-drop counts. Decode LACP, ICCP, BPDUs, VRRP adverts, GARP/ND and numbered payload. Save `/system/resource/print`, bounded CPU profile samples, link counters and logs. Confirm suspected wrong-port delivery at an independent receiver. The same frame at two serial observation points is one delivery. |

### Provisional pass criteria

| Flow or event | Rule for this campaign |
| --- | --- |
| Unaffected path | Zero missing probes, duplicate deliveries or TCP resets at the declared sample rate during fault **and rejoin**. A remote reboot disrupting a purely local path fails this rule. |
| Redundant path switching | Initial service targets: at most **1 s** for a directly signaled single member loss and **5 s** for a fast-LACP chassis loss or 1 s-advertisement VRRP takeover. Apply separately on failback. Record fast/slow LACP, carrier, VRRP timers and configured minimum links. For deliberate slow-timer variants record protocol behavior and separately mark any service-target miss. |
| Complete partition | Mark an impossible path **expected down** and verify it really stops. Apply the unaffected rule to surviving local services. On repair, mark when the path first becomes eligible and measure recovery to sustained delivery. |
| Forwarding correctness | Zero test frames in a forbidden VLAN, persistent known-unicast flooding, reflected test frames or duplicate application deliveries. A connected VRRP domain has one master per VRID after convergence. Affected hosts must relearn on valid source traffic, without operator intervention. Record expected transient unknown-unicast flooding separately. |
| Calculating loss | Use the distributed-probe method above. Report every outage in seconds per client, direction and phase, its sampling bounds, longest gap, and separate late, missing, duplicate and reordered counts. Record first recovery, stable recovery and application outcome. |

## How to iterate and record a result

**Problem statement.** A result such as “7.26 works” loses the topology, the recovery order, and the class of traffic that was actually observed.

1. **First session.** Calibrate timing on T0 with the known one-way interruption. On T1 run the applicable BASE checks and MOVE-01 in both directions, then build T2 and run §4/M4 on the same pinned development build. Keep the local control running during fault and rejoin.
2. **Second session.** On the smallest applicable topology run S1, S2, S3, L1, L2, G1 and P1, plus MOVE-03/04 and the local MOVE-06 variant. Check which event consumed the outage budget. Time spent waiting for client LACP expiry, waiting for STP forwarding and forwarding to a stale MAC call for different fixes.
3. **Two-site session.** Add the second local gateway and independent witnesses. Run BASE-06, G2, MOVE-02, the cross-site MOVE-06 variant and DC-01 through DC-07 before a long soak. Schedule MOVE-05 on the ESXi bench. Finish the remaining catalogue on the relevant topologies. Replay intermittent cases with the same inputs and compare the new evidence with the last recorded passing run.
4. **Result entry.** Retain one row per run, stream, direction, phase and distinct loss interval. Attach the resolved build, calibration, capture-drop counts and timing uncertainty. A run with no detected outage records 0 missed probes at the stated cadence. Use **pass**, **fail**, **inconclusive** (missing evidence or inadequate probe capacity), **expected down** for a specific flow, or **not run**. A hardware-only subcase stays pending until tested on that platform.

| Case / run / build | Stream, event and phase | Expected path and budget | Measured outage in seconds (bounds) and counts | First / stable recovery, TCP outcome | Evidence and verdict |
| --- | --- | --- | --- | --- | --- |
| M4 / 01 / current development CHR / T2 two-wire | A stationary client → A local service, client-member down | Unaffected / 0 missed probes at 10/s | Pending | Pending | Not run |
| MOVE-02 / 01 / current development CHR / T3 | B stationary client → mobile VM, first new ingress in A | Stretched VLAN / 1 s after first valid source frame | Pending | Pending | Not run |

Alongside each row, identify the last good, first missed, last missed and first good sequence/timestamp. Keep the reverse and control rows even when they have zero misses. Report both the clocked interval of any confirmed STP discard and the measured interruption to the service. These intervals can start and end at different times.

For a failing run, keep the topology revision, image digest, sanitized exports from **both** peers, partner config/timers, before/during/after snapshots, UTC event log and the smallest PCAPs showing the first wrong decision. Record the first bad frame's sequence, MAC, VID, expected and observed egress, and whether recovery required intervention. Repeat that case on the campaign's pinned build when confirmation is needed.
