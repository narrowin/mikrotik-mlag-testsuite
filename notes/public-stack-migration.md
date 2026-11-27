# Public tc stack qualification — 27 November 2026

All ten maintained topology definitions pin the public CHR image. The shared
launcher selects and checksum-verifies the published containerlab client.
The post-deploy data-bridge workaround is removed.

The reproducible Networka `0.5.2+chr.5` dependency includes tc NIC discovery,
queue cleanup and complete recovery verification within the original deadline.
Small uses strict RouterOS bond eligibility and Linux independent LACP control.

| Existing Small test | Verdict | Evidence |
| --- | --- | --- |
| cable-delay | PASS | [report](qualification/small-arm64/cable-delay/report.md) |
| bond-member-loss | PASS | [report](qualification/small-arm64/bond-member-loss/report.md) |
| switch-reboot | PASS | [report](qualification/small-arm64/switch-reboot/report.md) |
| cable-packet-loss | PASS | [report](qualification/small-arm64/cable-packet-loss/report.md) |

The complete packet-loss test verified recovery at 14.9090 seconds against
its unchanged 15-second requirement. See [the qualification](final-qualification.md)
and [source provenance](../vendor/README.md). All four results replay identically.
The maintained Small lab remains healthy and deployed.

This is the Small ARM64 campaign. Other definitions use the public stack, but
their campaigns were not rerun. Historical reports retain their original
engine versions, configuration and qualification scope.
