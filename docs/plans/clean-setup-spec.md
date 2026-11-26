# Small MLAG reference setup

The [Small lab](../../tests/small/README.md) boots two RouterOS MLAG peers with spanning tree off. Three dual-attached Linux clients support two independent measurements. One stream involves the client whose cable changes. The other runs between the two unaffected clients. A separate syslog node records what each switch saw.

## Lab contract

- The [topology](../../tests/small/topology.clab.yml) declares the images, links, management network and mounts. The [switch startup configuration](../../tests/small/switch.rsc) sets up MLAG, the client VLAN and remote logging before testing begins.
- Each [client](../../tests/small/client-setup.sh) has a stable bond MAC so the choice of cable is reproducible across deployments.
- The CHR virtual ports need equal speed and full duplex. Their host-side bridges must pass LACP and any accidental BPDU to the peer and forward data like a cable. [QEMU wrapper](../../tests/small/chr-qemu.sh) · [Bridge setup](../../tests/small/chr-bridges.sh)
- Three values span separate programs. RouterOS needs the collector address declared in the topology, Docker builds the client image tag that containerlab deploys, and both ends of the bond need the fast LACP rate.
- Switch logs must keep the UTC receive time, sender, topics and message. The engine must be able to distinguish an absent warning from a silent switch. [Collector](../../tests/small/rsyslog.conf)

## Test contract

- The [lab file](../../tests/small/lab.yaml) defines each stream's direction and the state required before and after the test.
- The [test file](../../tests/small/bond-member-loss.yaml) defines the cable changes, hold times, per-stream limits and switch log rules. A passing test independently demonstrates traffic recovery and the expected port log for each step.
- The run must retain enough evidence for offline replay to regenerate the same verdict and human-readable report. Both must show each lost-ping count with the interval and the measured stop.
- The start, run, replay and removal commands belong in the [lab README](../../tests/small/README.md). The [implementation plan](implementation-plan.md) defines the live acceptance checks.
