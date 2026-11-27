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

**Lab size**:
Small (one **MLAG pair**, three **hosts**), Medium (one pair with an **access switch**) or Large (two sites, each with a core pair and a distribution pair); most **labs** are one of these sizes in one **STP mode**.
_Avoid_: simple, core lab, two-site lab, external root lab

**Two-pair lab**:
Two **MLAG pairs** joined by an **inter-pair bond**, with one **dual-connected** **host** on each pair; the two-pair strict lab is the same lab with **lacp-strict** on.
_Avoid_: medium two-pair variant, strict variant

**Access switch**:
A RouterOS switch below an **MLAG pair** with one LACP bond to both **MLAG peers**; it is not an **MLAG peer** itself.
_Avoid_: witness, witness switch, leaf, downstream switch

**MAC-move host**:
A **host** with an active-backup bond that keeps the same MAC address on either **bond member**, so the **MLAG pair** must relearn it on another port.
_Avoid_: mobile endpoint, mobile host

**Role name**:
A device name that says what the device is in its **lab**, such as switch1, access-switch, host2 or dc1-core1.
_Avoid_: p1, c1, r1, CHR 1, CHR 2, witness

**Startup config**:
The RouterOS configuration each CHR boots with, which brings the **lab** into the state its **tests** need; nothing is configured during a **test**.
_Avoid_: running config, start config, intent

**Campaign version**:
The one pinned RouterOS development build that every live **test** runs on.
_Avoid_: latest, test version

### Results

**Finding**:
A RouterOS misbehaviour a **test** proved, such as two **MLAG pairs** sending into a rebooting **MLAG primary**.
_Avoid_: fault (for a misbehaviour), bug, issue

**Old suite**:
The frozen mlag-lab runner and its results, kept only to compare against until it is removed.
_Avoid_: legacy, previous framework, migration, backward compatibility

### Engine terms

[Networka's GLOSSARY.md](https://narrowin.github.io/networka/glossary/) defines these words, and this repository uses them in that sense:
**lab**, **host**, **collector**, **test**, **step**, **fault**, **cable**, **reboot**, **power loss**, **baseline**, **state check**, **stream**, **ping**, **lost ping**, **outage**, **limit**, **run**, **evidence**, **judge**, **verdict**, **replay**, **report** and **Networka**.
In the Large lab, hosts have the roles traffic host and service host.
At a bond end a **cable** carries one **bond member**.

## Relationships

- An **MLAG pair** has two **MLAG peers**, one **MLAG primary** and one **MLAG secondary**, joined by one **peer link**.
- A **lab** has one **startup config**.
- A FAIL becomes a **finding** only when the cause lies in RouterOS, not in the **lab** or the measurement.

## Flagged ambiguities

- Bond member vs cable: "member" was used for the interface in a bond ("Member down") and for the wire a test takes down ("the cable test is bond-member-loss"). Resolved: **bond member** is the interface in a bond, **cable** is the wire a **step** takes down or brings back.
- Test vs case: "case" was used for one file in `cases/` ("Run a case") and "test" for the same file ("Tests and their limits", "one test each"). Resolved: **test**, the word of `nw test`; the folder is `tests/<lab>/tests/` since 27 November 2026.
- Fault vs finding: "fault" was used for the injected event ("before every fault") and for a RouterOS misbehaviour ("Faults across runs", "Fault 2"). Resolved: **fault** is the injected event, **finding** is the RouterOS misbehaviour a test proved.
- Peer link vs peer port: "peer link" was used for the connection (RouterOS logs) and "peer port" for its ends (the MLAG manual, which never says "peer link"). Resolved: **peer link** is the connection, peer port the manual setting at each end.
- Loss: "loss" was used for faults ("power loss", "peer link loss"), for **lost pings**, for netem packet loss on a **cable** and for the old loss phase. Resolved: "loss" appears only in fault names; the others are **lost pings**, **outage** and **impairment**.
