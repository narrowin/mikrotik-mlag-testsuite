# Original bridge image versus tc — 27 November 2026

The original image and original bridge client also fail the packet-loss test.
The failure therefore does not require the new tc forwarding, image startup
hook or published client changes. This control corrects the earlier premature
attribution based only on captures from the tc lab. It does not independently
rule out factors shared by both deployments: the engine, Linux bonding, QEMU,
the lab configuration and RouterOS.

## Controlled comparison

On `mlag-external` (ARM64, QEMU TCG), deployed an isolated copy of Small as
`forwarding-ab-small`, then replaced only that disposable deployment with its
tc counterpart. Pre-existing labs were left running. Both used Networka
`0.5.2+chr.2` and the exact same test, startup config, host setup, lab file and
inventory bytes. Checksums are recorded in `input-checksums.json`.

Both deployments had the same explicit management addresses, guest MACs,
MLAG role assignment, 288 MiB guest memory, one guest CPU and 10G/full-duplex
data NIC settings. Runtime proof is in `runtime-comparison.json`. The topology
files differ only in the CHR image reference; each used its corresponding
qualified launcher/client.

The original control used `mikrotik/chr:7.26beta7` at digest
`b68f34a50544f6464d592cdd07ecc1d08017d6ec6837ac42b7dbe701d3c1ca6a`
and the pre-tc bridge client with verified SHA-256
`feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.
Its original launcher was taken from this repository's HEAD. Each switch had
br0 plus br1–br4; data-port learning was verified off. This is the original
native containerlab bridge workflow, which supplies `/chr-launch.sh`, rather
than a standalone invocation of the image's default entrypoint.

The tc comparison used the currently pinned public image and published ARM64
client. Each switch had only management br0; reciprocal ingress redirects
joined data interfaces to TAPs. Both images contain the identical RouterOS
7.26beta7 guest disk, SHA-256
`c814fa30498964f9c8cfa586bd01aea1b0cc0c8b753b2e8956ef923d6a4cb467`.
Full references are in `image-and-client-proof.json`.

The test still drops 100% of frames leaving host1:eth2 for 25 seconds. The
four-second affected-stream limit, zero-loss independent-stream limit and
15-second recovery deadline are unchanged. Initial state checks passed in
all named runs.

## Generated results

| Run | Affected-stream impairment result | Whole run |
| --- | --- | --- |
| Original bridges, bridge-1 | Unqualified duration: sender cadence invalid | ERROR |
| Original bridges, bridge-2 | FAIL: outage at least 31.7841 s against 4 s | ERROR: recovery deadline exceeded; cleared step also has invalid sender cadence |
| tc, tc-1 | FAIL: outage 39.56–39.7683 s against 4 s | ERROR: recovery deadline exceeded |
| tc, tc-2 | FAIL: outage 39.2003–39.4108 s against 4 s | FAIL: recovery and closing state complete |

Durations and verdicts above come from each named `nw test` run's generated
`report.md` and `result.json`. The valid bridge-2 impairment result establishes
that the original forwarding path breaches the traffic limit; its whole-run
ERROR is retained. The independent host2-to-host3 stream has no lost pings in
these runs. No error is counted as a successful complete run and no limit was
relaxed to obtain a result.

## Packet evidence and scope

Both methods show partner expiry/defaulting and delayed LACP renegotiation.
During each recorded test window (`test_started` through `stopped`), complete
LACP frame bytes match between switch2's guest-facing tap2 and container eth2.
There are no unmatched frames in either direction in either method. The
comparison excludes the extra capture startup/shutdown tails; one tc tail
frame falls after the other capture has ended. This is packet evidence that
the new tc redirects are not suppressing or changing LACP during the test.
See `forwarding-frame-proof.json`, `lacp-comparison.json` and the local pcaps.

This excludes the new tc stack as a necessary cause of this reproduced
failure. It does not establish equal performance in every circumstance or
identify an internal RouterOS source-code defect. The original bridge
workflow already exhibits the failure under the same stated requirement.

All four saved runs replay with byte-identical results, including the ERROR
verdicts (`replay-proof.json`). The temporary comparison lab was destroyed
using its own topology file. The test-owned qdisc was restored to `noqueue`.
Raw evidence remains local under `test-results/bridge-tc-ab/`.

[Original bridge report](qualification/bridge-tc-ab/bridge-2/report.md)
· [Matched tc report](qualification/bridge-tc-ab/tc-2/report.md)
