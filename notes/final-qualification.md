# Final CHR integration qualification

All four existing Small tests pass with the final reviewed Networka `0.5.2+chr.5` artifact, the unchanged public CHR image and published ARM64 containerlab client. No test action, hold, traffic limit, state expectation or recovery deadline changed.

| Small test | Verdict | Generated report |
| --- | --- | --- |
| cable-delay | PASS | [report](qualification/small-arm64/cable-delay/report.md) |
| bond-member-loss | PASS | [report](qualification/small-arm64/bond-member-loss/report.md) |
| switch-reboot | PASS | [report](qualification/small-arm64/switch-reboot/report.md) |
| cable-packet-loss | PASS | [report](qualification/small-arm64/cable-packet-loss/report.md) |

Every run used `uv run --locked nw test run` in `mlag-external`, followed by `nw test replay`. All generated report/result bytes stayed unchanged. [Copied generated evidence](qualification/small-arm64/README.md) and [artifact provenance](../vendor/README.md).

In Small `cable-packet-loss`, run `final-commit-small`, the generated result records complete recovery at **14.909018 s** against the existing 15 s cutoff. Its affected-stream outage was **3.030148–3.235389 s** against 4 s, and the independent stream had no lost pings. These are measurements of this named run, not timing guarantees. The [cutoff review](lacp-recovery-timing-sources.md) recommends a documented 40 s local recovery budget; that recommendation is not implemented.

## What is included

- The generic image proposal adds `iproute2-tc` and seven startup-hook lines; the RouterOS guest disk is unchanged. [Image source](chr-startup-hooks/README.md) and [MikroTik reply](mikrotik-sup-217550-reply.md).
- Containerlab supplies its hook and launcher internally, connects data interfaces through tc, and removes the data-bridge fallback and workarounds. Management provisioning and necessary Linux data-interface IPv6 handling remain. [Committed fork change](https://github.com/mischadiehm/containerlab/commit/f3733e41ab78f8144982d59973061e51925d36da).
- Small uses `lacp-strict=yes min-links=1` on RouterOS host bonds and `coupled_control off` on Linux hosts. These startup-config changes address sustained one-way packet-loss failover.
- Networka identifies tc-backed QEMU NICs, drains owned delay queues, and reads the affected Linux member through its normal SSH intent path before collecting complete recovery state across devices. Native cancellation and connection retry waits share operation cancellation. [Committed engine change](https://github.com/narrowin/networka/commit/8b504ba1b8f12f6d30ce6496d9e8c08816149424).

The final packaged and installed source bytes match all eight reviewed Networka files. Existing checks: **119 passed**; Ruff lint/format and mypy pass. A real native connection configured for three attempts and a five-second retry delay cancelled in 0.234 s. Independent Standards, Spec and Correctness source reviews found no remaining source findings after the corrections. The final live runs above qualify the revised SSH path; earlier namespace-based runs are historical.

## Coverage

The complete final Small test set is qualified on ARM64 CHR under QEMU TCG. [Public-kit anonymous reproduction](chr-startup-hooks/PUBLIC-KIT-RESULTS.md) separately passed deployment, LACP, IPv4/IPv6 forwarding and restart on ARM64 and AMD64. Final Networka fault tests were not repeated on AMD64 or physical hardware. Other maintained topology definitions use the public stack, but their full test sets were not rerun; Small RSTP shares the updated startup config and is not claimed qualified.

The [original bridge comparison](bridge-tc-comparison.md) already reproduced failure without tc. It excludes tc as a necessary cause of that reproduced failure; it does not establish equal recovery timing in every circumstance.

The operator has sent the MikroTik support reply. Upstream adoption remains outstanding. Raw evidence stays local.
