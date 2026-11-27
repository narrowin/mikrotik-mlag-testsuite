# MikroTik MLAG test suite

Containerlab labs of RouterOS CHR switches and Linux hosts that measure how long traffic is interrupted when an MLAG pair meets a fault.
The Networka engine runs the tests and judges them; this repository holds the labs, the tests and their limits, and the RouterOS findings they produced.

## Language

### MLAG

**MLAG pair**:
The two **MLAG peers** that share one **peer link** and act as one LACP partner toward every **dual-connected** device.
_Avoid_: stack, chassis pair, the cores (outside the Large lab)

**MLAG peer**:
One RouterOS switch of an **MLAG pair**; the manual also says "peer" and "MLAG node".
_Avoid_: p1, p2, CHR 1, CHR 2, chassis, unit

**MLAG primary**:
The role of the **MLAG peer** with the lower `mlag-priority`, or the lower bridge MAC on a tie, whose LACP system ID the **MLAG pair** presents; the other peer is the **MLAG secondary**.
_Avoid_: MLAG master, owner, active, root, chassis roles

**Peer link**:
The connection between the two **MLAG peers** of a pair. It carries ICCP, flooded traffic, and traffic whose destination is reached only through the other peer. RouterOS logs name it so; the manual names only its ends, the peer port (`mlag-peer-port`).
_Avoid_: peer-link (in prose), link between the two switches, inter-switch link, ISL, IPL

**MLAG bond**:
A bond that both **MLAG peers** give the same `mlag-id`, so the device or pair on the other side sees one LACP aggregation.
_Avoid_: MLAG interface

**Bond member**:
One interface inside a bond, on a switch or a **host**; the RouterOS manual and CLI call it a slave.
_Avoid_: slave (outside quoted config), client link, leg

**Dual-connected**:
Having a **bond member** on each **MLAG peer** of a pair, as every device in these labs is by default.
_Avoid_: dual-attached, dual-homed

**Inter-pair bond**:
The **MLAG bond** that joins two **MLAG pairs**, with one **bond member** between matching peers of each pair. In the Large lab it is called the DCI.
_Avoid_: interpair, inter-pair link, distributed bond

**Host table**:
The bridge table of MAC addresses and the ports they were learned on, which the **MLAG peers** keep in sync over the **peer link**; one row is a host entry.
_Avoid_: FDB, MAC table

**lacp-strict**:
The RouterOS bond setting that, when on, stops a **bond member** without an LACP partner from carrying traffic even while it has carrier.
_Avoid_: strict mode

**STP mode**:
The spanning-tree protocol of every bridge in a lab: spanning tree off, RSTP or MSTP. With RSTP or MSTP the mode also has a root placement: either the **MLAG pair** or a switch outside the pair is spanning-tree root.
_Avoid_: bridge mode, setup

### Labs and devices

**Lab**:
One containerlab topology of CHR switches, **hosts** and a **collector**, with its **startup config**, **state checks** and **tests**.
_Avoid_: setup, environment, scenario, variant (for a lab of its own)

**Lab size**:
Small (one **MLAG pair**, three **hosts**), Medium (one pair with an **access switch**) or Large (two sites, each with a core pair and a distribution pair); most **labs** are one of these sizes in one **STP mode**.
_Avoid_: simple, core lab, two-site lab, external root lab

**Two-pair lab**:
Two **MLAG pairs** joined by an **inter-pair bond**, with one **dual-connected** **host** on each pair; the two-pair strict lab is the same lab with **lacp-strict** on.
_Avoid_: medium two-pair variant, strict variant

**Access switch**:
A RouterOS switch below an **MLAG pair** with one LACP bond to both **MLAG peers**; it is not an **MLAG peer** itself.
_Avoid_: witness, witness switch, leaf, downstream switch

**Host**:
A Linux container that sends and answers the **pings** of the **streams**. In the Large lab hosts have the roles traffic host and service host.
_Avoid_: client, end system, endpoint, c1, c2, probe host

**MAC-move host**:
A **host** with an active-backup bond that keeps the same MAC address on either **bond member**, so the **MLAG pair** must relearn it on another port.
_Avoid_: mobile endpoint, mobile host

**Role name**:
A device name that says what the device is in its **lab**, such as switch1, access-switch, host2 or dc1-core1.
_Avoid_: p1, c1, r1, CHR 1, CHR 2, witness

**Collector**:
The node that receives the log of every switch in a **lab**, so the log is kept with every **run** even while data links are down.
_Avoid_: log server, receiver

**Startup config**:
The RouterOS configuration each CHR boots with, which brings the **lab** into the state its **tests** need; nothing is configured during a **test**.
_Avoid_: running config, start config, intent

**Campaign version**:
The one pinned RouterOS development build that every live **test** runs on.
_Avoid_: latest, test version

### Tests

**Test**:
One named sequence of **steps** run on one **lab**, with a descriptive name such as primary-reboot.
_Avoid_: case, test case, use case, scenario, case intent

**Step**:
One stretch of a **test** with one action or one **cable** change, its hold time, its **limits** and the expected behaviour.
_Avoid_: phase, stage

**Fault**:
The event a **test** injects to see how the **MLAG pair** copes, such as a **reboot**, a **power loss** or a **cable** going down; it is down while in effect and back when it ends.
_Avoid_: scenario, failure, withdrawal and restoration, lost and restored, loss and return

**Cable**:
The virtual wire between two lab interfaces that a **step** takes down or brings back; at a bond end it carries one **bond member**.
_Avoid_: connection, carrier withdrawal

**Reboot**:
A restart of RouterOS on one switch from its own command, during which its data links may keep carrier.
_Avoid_: soft reboot, hardware failure, power loss

**Power loss**:
One switch switched off abruptly, with carrier gone on all its data links, and left off for a gap before it boots again.
_Avoid_: reboot, hard reboot, pause, sustained stop

**Baseline**:
Fault-free traffic with a **limit** of 0 on every **stream**, as a **test** of its own that proves the **lab** forwards or as the opening **step** of a test.
_Avoid_: readiness, readiness gate, zero-loss gate, old results

**State check**:
A check of device state, such as MLAG connected with its role, **STP mode** or a **bond member** in use, that runs before a **test**, again at its end, and after a **reboot** or **power loss** before measuring goes on.
_Avoid_: checkpoint, snapshot, gate, readiness, precondition, health check

### Measurement

**Stream**:
One series of **pings** in one direction between two lab interfaces, named by its direction, such as host1-to-host2.
_Avoid_: flow, graded flow, control flow, stream 101

**Ping**:
One ICMP echo of a **stream**; Networka sends one every 100 ms on every stream.
_Avoid_: probe, packet

**Lost ping**:
A **ping** whose reply did not arrive in time. A count of lost pings is always given with the ping interval and the time it stands for.
_Avoid_: drop, packet loss (for pings)

**Outage**:
The measured interruption of one **stream**: consecutive **lost pings**, given as a lower and an upper bound, such as 24 lost pings at one every 100 ms, an outage of 2.4 to 2.6 s.
_Avoid_: stop (as a noun), convergence time, withdrawal bound, restoration bound

**Limit**:
The longest **outage** a **stream** may have in a **step**, written with its reason and source; 0 means no **lost ping**.
_Avoid_: timer, threshold, target, SLA

### Results

**Run**:
One execution of one **test** on a live **lab**, saved with its **evidence**.
_Avoid_: attempt, trial, repeat

**Evidence**:
What a **run** keeps for its **verdict**: the packet-capture slices the **judge** needs to prove it, device state and the switch log; the run folder is compressed when the run ends.
_Avoid_: proof, archive, recordings

**Judge**:
The part of **Networka** that turns **evidence**, **limits** and **state checks** into a **verdict**; plain code, not an AI.
_Avoid_: grader, evaluator, scorer, grading

**Verdict**:
The result of a **step**, **run** or **test**, written in capitals as PASS, FAIL or ERROR. ERROR means the **evidence** cannot decide, and missing evidence is never PASS.
_Avoid_: Unverified, not available, INVALID, inconclusive, unavailable

**Replay**:
Judging the **evidence** of a saved **run** again without a **lab**; it must give the same result and **report** byte for byte.
_Avoid_: offline, re-grade, verify, re-run

**Report**:
The generated account of a **run**: the **verdict** first, then per **step** and **stream** the expected **limit** against the measured **outage**; nothing in it is written by hand.
_Avoid_: timeline

**Finding**:
A RouterOS misbehaviour a **test** proved, such as two **MLAG pairs** sending into a rebooting **MLAG primary**.
_Avoid_: fault (for a misbehaviour), bug, issue

**Networka**:
A general network testing framework, not tied to containerlab or RouterOS, that runs and judges every **test** here; this repository holds only **labs**, **tests** and **limits**.
_Avoid_: runner, Containerlab tests

**Old suite**:
The frozen mlag-lab runner and its results, kept only to compare against until it is removed.
_Avoid_: legacy, previous framework, migration, backward compatibility

## Relationships

- An **MLAG pair** has two **MLAG peers**, one **MLAG primary** and one **MLAG secondary**, joined by one **peer link**.
- A **lab** has one **startup config**, one set of **state checks**, several **streams** and many **tests**.
- A **test** has ordered **steps**; each **step** has at most one action or **cable** change and one **limit** per **stream**.
- A **fault** is down in one **step** and back in a later one; each **step** measures its own **outages**.
- A **run** of a **test** produces **evidence**; the **judge** turns it into one **verdict** and a **report**; a **replay** repeats that from the **evidence** alone.
- A FAIL becomes a **finding** only when the cause lies in RouterOS, not in the **lab** or the measurement.

## Flagged ambiguities

- Bond member vs cable: "member" was used for the interface in a bond ("Member down") and for the wire a test takes down ("the cable test is bond-member-loss"). Resolved: **bond member** is the interface in a bond, **cable** is the wire a **step** takes down or brings back.
- Test vs case: "case" was used for one file in `cases/` ("Run a case") and "test" for the same file ("Tests and their limits", "one test each"). Resolved: **test**, the word of `nw test`; "case" names only the folder.
- Fault vs finding: "fault" was used for the injected event ("before every fault") and for a RouterOS misbehaviour ("Faults across runs", "Fault 2"). Resolved: **fault** is the injected event, **finding** is the RouterOS misbehaviour a test proved.
- Peer link vs peer port: "peer link" was used for the connection (RouterOS logs) and "peer port" for its ends (the MLAG manual, which never says "peer link"). Resolved: **peer link** is the connection, peer port the manual setting at each end.
- Loss: "loss" was used for faults ("power loss", "peer link loss"), for **lost pings**, for netem packet loss on a **cable** and for the old loss phase. Resolved: "loss" appears only in fault names; the others are **lost pings**, **outage** and packet loss.
