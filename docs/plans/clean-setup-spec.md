# Small MLAG reference setup

The [Small lab](../../tests/small/README.md) boots two RouterOS MLAG peers with spanning tree off. Three dual-attached Linux clients support two independent measurements. One stream involves the client whose cable changes. The other runs between the two unaffected clients. A separate syslog node records what each switch saw.

## Lab contract

- The [topology](../../tests/small/lab/topology.clab.yml) declares the images, links, management network and mounts. The [switch startup configuration](../../tests/small/lab/switch.rsc) sets up MLAG, the client VLAN and remote logging before testing begins.
- Each [client](../../tests/small/lab/host-setup.sh) has a stable bond MAC so the choice of cable is reproducible across deployments.
- The qualified Containerlab launcher defaults the CHR data ports to 10 Gbit/s full duplex and passes LACP through its standard Linux bridges. These bridges learn MAC addresses. Host bridge STP is off, allowing accidental BPDUs to reach the peer. [Native CHR evidence](implementation-plan.md#native-containerlab-chr-qualification)
- Three values span separate programs. RouterOS needs the collector address declared in the topology, Docker builds the client image tag that containerlab deploys, and both ends of the bond need the fast LACP rate.
- Switch logs must keep the UTC receive time, sender, topics and message. The engine must be able to distinguish an absent warning from a silent switch. [Collector](../../tests/shared/rsyslog.conf)

## Test contract

- The [lab file](../../tests/small/lab/lab.yaml) defines each stream's direction and the state required before and after the test.
- The [test file](../../tests/small/cases/bond-member-loss.yaml) defines the cable changes, hold times, per-stream limits and switch log rules. A passing test independently demonstrates traffic recovery and the expected port log for each step.
- The run must retain enough evidence for offline replay to regenerate the same verdict and human-readable report. Both must show each lost-ping count with the interval and the measured stop.
- The start, run, replay and removal commands belong in the [lab README](../../tests/small/README.md). The [implementation plan](implementation-plan.md) defines the live acceptance checks.
