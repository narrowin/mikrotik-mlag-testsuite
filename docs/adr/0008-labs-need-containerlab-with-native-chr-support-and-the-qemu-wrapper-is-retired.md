# Labs need containerlab with native CHR support, and the QEMU wrapper is retired

The labs under `tests/` run on a containerlab build with native CHR support, from commit `06ac3ca4d` of srl-labs/containerlab#3636.
Their topologies do not bind-mount a QEMU wrapper or run a bridge startup script.
The container bridges of each CHR use standard Linux MAC learning.

## Why

RouterOS gives a bond member an LACP key only when the port reports full duplex.
Containerlab 0.83.0 reports CHR data ports as half duplex, so no LACP bond comes up.
The old labs worked around this: they bind-mounted `qemu-data-link.sh` over the QEMU binary to report 10 Gbit/s full duplex, and a bridge script turned MAC learning off ("wire" mode).
The operator's containerlab change sets 10 Gbit/s full duplex and forwards LACP and LLDP frames natively.
The Small lab qualified it live on 2026-11-26: all 8 data ports came up at 10 Gbit/s full duplex and all six Linux bond members passed their checks.
The operator then approved removing both CHR helper scripts, their mounts and the bridge startup command.
On 2026-11-27 he said of the native build: "this is for the public. We need to use this."

The no-learning mode was kept in the old labs because an audit said a learning bridge dropped replies in a failover.
That claim cited no raw run, the native launcher has no learning setting, and the Small cable and reboot tests passed with learning on.

## Consequences

Until the pull request is released, users must build containerlab from the pull request branch.
The root `README.md` keeps the old wrapper as a manual fallback for a released containerlab, only until a released containerlab version includes native CHR support; then the fallback is removed from the README.
The published `nw test` results were run on the native build; the frozen old-suite results in `results/` were run with the wrapper on containerlab 0.83.0.
Only the ARM64 build is qualified; on the lab VM its SHA-256 is `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.
