# Findings

These pages record what the tests showed about RouterOS 7.26beta7 MLAG on CHR.
Each number on them comes from a generated report or index, named with its lab, test and run.
They cover RouterOS in the software bridge of CHR, not CRS switch hardware, as [ADR 0007](../adr/0007-the-labs-run-routeros-chr-in-containerlab-and-do-not-test-switch-hardware.md) says.

| Page | What it shows |
| --- | --- |
| [An MLAG bond without an LACP partner keeps forwarding](mlag-bond-without-lacp-partner-keeps-forwarding.md) | Frames loop back to their sender after a return, and two MLAG pairs keep sending into a rebooting MLAG primary. Written for reports to MikroTik. |
| [A silent bond member](silent-bond-member.md) | With 100 % packet loss on one cable, or a bond member taken down on the host side, the MLAG peer keeps sending to that bond member. |
| [Spanning tree with MLAG](spanning-tree-with-mlag.md) | Only spanning tree off passed every Medium run; with RSTP or MSTP and the MLAG pair as root, the MLAG primary reboot went over 5 s. |
| [Reboot and power loss timing](reboot-and-power-loss-timing.md) | A CHR reboot is about as short as the MLAG heartbeat timeout, and it costs more traffic than a power loss. |
| [Two-site design](two-site-design.md) | Two straight DCI links leave no path when opposite cores fail, and MikroTik documents no design for two joined MLAG pairs. |

The current results of every lab are in the [README results table](../../README.md#results).
The old suite's frozen results are in [results/](../../results/README.md).
