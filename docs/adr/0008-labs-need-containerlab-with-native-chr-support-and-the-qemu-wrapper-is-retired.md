# Labs need containerlab with native CHR support, and the QEMU wrapper is retired

The labs under `tests/` run on a containerlab build with native CHR support, from commit `06ac3ca4d` of srl-labs/containerlab#3636.
Their topologies do not bind-mount a QEMU wrapper or run a bridge startup script.
The two-port container bridges that join each CHR data port to its QEMU tap do not learn MAC addresses: `tests/shared/start.sh` turns learning off on every data bridge after deploy.

## Why

RouterOS gives a bond member an LACP key only when the port reports full duplex.
Containerlab 0.83.0 reports CHR data ports as half duplex, so no LACP bond comes up.
The old labs worked around this: they bind-mounted `qemu-data-link.sh` over the QEMU binary to report 10 Gbit/s full duplex, and a bridge script turned MAC learning off ("wire" mode).
The operator's containerlab change sets 10 Gbit/s full duplex and forwards LACP and LLDP frames natively.
The Small lab qualified it live on 2026-11-26: all 8 data ports came up at 10 Gbit/s full duplex and all six Linux bond members passed their checks.
The operator then approved removing both CHR helper scripts, their mounts and the bridge startup command.
On 2026-11-27 the operator said of the native build: "this is for the public. We need to use this."

The old labs also turned learning off because an audit said a learning bridge dropped replies in a failover.
The native labs first ran with learning on, because that claim cited no raw run and the first Small cable and reboot runs passed.
On 2026-11-27 the Small cable test failed in most runs started on a fresh lab: host1 lost its replies for 7.5 s while its cable to switch2 was down.
Captures in switch2's peer-link container bridge showed the cause. RouterOS sent 48 replies to host1 out of the tap, none left the veth, and the bridge had learned host1's MAC on the tap side.
A learning Linux bridge drops a frame whose destination it learned on the port the frame came in on.
With learning off, the test passed on 4 of 4 fresh deploys, where it had failed 3 of 3 times just before.

## Consequences

Until the pull request is released, users must build containerlab from the pull request branch.
The native launcher does not turn learning off, so `start.sh` does it; a lab deployed without `start.sh` has learning on.
The root `README.md` keeps the old wrapper as a manual fallback for a released containerlab, only until a released containerlab version includes native CHR support; then the fallback is removed from the README.
The published `nw test` results were run on the native build; the frozen old-suite results in `results/` were run with the wrapper on containerlab 0.83.0.
Only the ARM64 build is qualified; on the lab VM its SHA-256 is `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.
