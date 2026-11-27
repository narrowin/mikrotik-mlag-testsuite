# The labs run RouterOS CHR in containerlab and do not test switch hardware

Every switch in every lab is a MikroTik CHR from the official `mikrotik/chr` image, run by containerlab's `mikrotik_chr` kind.
Containerlab is the only lab technology the suite supports.
No hardware bench belongs to this repository.

## Why

The CHR runs the full RouterOS in QEMU, so the tests exercise RouterOS's own bridge, LACP and MLAG code.
Anyone can rerun a lab from the committed files without buying switches.
The actions that make a test, such as cutting a cable, rebooting or powering off a switch, capturing at both ends of a stream and adding netem loss, need control of the lab host.
On 2026-11-26 the operator tied those actions to containerlab, the only lab tool in use.
Supporting another lab tool would mean a second implementation of every action.

Networka itself is not limited to containerlab or RouterOS.
The operator said the same day: "It's not only tests for [containerlab]. It's just a testing framework".
Against a production network only its state, ping and path checks apply.

## Consequences

A pass covers RouterOS on CHR, where forwarding happens in the software bridge.
It does not cover the switch chip offload of CRS hardware or real loss of signal on optics.
Fixes that only matter on hardware are marked as hardware only.
The operator's own results on CRS326 and CCR2004 switches are cited, not reproduced, when a reader objects that CHR results do not hold on hardware.

See also [Networka ADR 0004](https://narrowin.github.io/networka/adr/0004-lab-actions-run-on-containerlab-only/).
