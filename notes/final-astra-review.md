# Final review of the CHR startup proposal

**Stop tonight and resume normal lab testing on the qualified branch.** The public prototype works now. The remaining external step is for the operator to send the prepared reply if they want MikroTik to consider it. This review found no defect that requires another lab run before using the branch.

## What MikroTik would maintain

The reply asks for one Alpine package, an empty directory, and seven added lines in the official `/start.sh`. The loop sources optional scripts in filename order after the host-network safeguard and before networking or QEMU starts. With an empty directory, startup continues as before. Another tool can supply a hook at deployment time. The published overlay uses the pinned official image as its base and adds no RouterOS guest disk layer. Its measured package installation layer, including dependencies, is 340 KiB compressed on AMD64 and 349 KiB on ARM64.

I compared the fenced diff in the reply with the patch file and checked its digest against the public release. They match. The reply correctly distinguishes dual-architecture public-kit checks from ARM64 Small lab qualification. Its statement about removing per-port bridges describes containerlab's use of the hook. Standalone CHR with no hook still uses MikroTik’s original networking. The reply is ready to send. [Reply](mikrotik-sup-217550-reply.md) · [Patch](chr-startup-hooks/start.sh.diff) · [Public release](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/tag/chr-startup-hooks-7.26beta7-20261127)

## What the operator uses now

On the lab branch, the normal Small lab start command is `sudo tests/shared/start.sh tests/small` in the lab VM. It selects the published client for that architecture, verifies the binary checksum, and uses the digest-pinned public image. The usual `uv run --locked nw test run` invocation selects the bundled Networka dependency. A clean checkout on that branch needs neither a local CHR/client rebuild nor the sibling Networka checkout. [Run instructions](../docs/tests/README.md#run-a-lab) · [Artifact inventory](chr-public-artifacts.json)

The native `mikrotik_chr` kind mounts its launcher and hook and sets the entrypoint and sysctl internally. Each Linux data interface and its guest-facing TAP have reciprocal `tc` redirects. The management bridge, first-boot provisioning, and suppression of Linux IPv6 on data interfaces remain necessary. There is no fallback to per-port bridges. The ordinary fork branch contains the three-file change. I regenerated its diff in release-file order and obtained the published SHA-256. The generic image has no dependency on that fork. [Containerlab commit](https://github.com/mischadiehm/containerlab/commit/f3733e41ab78f8144982d59973061e51925d36da)

## What actually passed

The saved anonymous public-kit checks cover deployment, management access, startup config, LACP, IPv4/IPv6 forwarding, numbering gaps, 10G full duplex, and restart with stable MACs on ARM64 and AMD64. I checked the release listing and saved evidence. I did not redeploy either lab. [Public-kit results](chr-startup-hooks/PUBLIC-KIT-RESULTS.md)

All four existing Small lab tests passed on ARM64 QEMU TCG with the final `0.5.2+chr.5` package. I compared the four generated reports and four JSON results in `final-commit-small` with their reviewable copies. They match. All four saved replay verdicts passed. In Small `cable-packet-loss`, the affected stream’s longest measured outage during impairment was **3.030148–3.235389 s** against 4 s. The independent stream had zero lost pings. After clearing the impairment, Networka verified full redundancy at **14.909017633 s** against 15 s. Traffic continuity and restoration of both bond members are separate requirements. [Qualification](final-qualification.md) · [Generated result](qualification/small-arm64/cable-packet-loss/result.json) · [Replay](qualification/small-arm64/replay.json)

Small also changed its startup config. RouterOS `lacp-strict=yes min-links=1` withdraws an unusable local host bond. On Linux, `coupled_control off` lets the host stop transmitting on a member when its partner stops collecting. These are substantive changes to what the lab exercises. Compare historical runs with their original startup config. With the earlier config, the original bridge deployment also breached the traffic limit in `bridge-2`, whose whole-run verdict was ERROR. The byte comparisons across TAP and veth cover the captured windows of `bridge-1` and `tc-1`. Together these observations show the reproduced failure could occur without tc. They cannot assign every millisecond of recovery to RouterOS or establish equal timing. [Bridge comparison](bridge-tc-comparison.md) · [Small lab configuration](../tests/small/README.md)

## Independent Networka review

**Standards.** All eight changed paths were inspected. Zero documented-standard breaches. One optional maintainability observation concerns the repeated tc query and JSON decode in the two directions of NIC discovery. Both reads are required.

**Spec.** The final implementation preserves all declared Small lab state checks and traffic limits. The normal SSH reader is used even for the preliminary member check. The historical chr.4 implementation notes describe an earlier path.

**Correctness.** No source defect found that blocks these tests. Networka verifies the reciprocal tc mapping before acting on a QEMU NIC and drains its own delay queue before removal. The preliminary Linux member check uses the ordinary SSH reader. A complete saved state check still has to pass within the original deadline. Reads across devices can overlap, reads on one device stay serial, and cancellation reaches native operations and connection retry waits.

The reviewed engine range was `3bd8c10..8b504ba`, covering `api/execution.py`, `device.py`, `intent.py`, `lab.py`, `lab_faults.py`, `lab_reboot.py`, `transport/cancellation.py` and `transport/scrapli_sync.py`. I checked all eight packaged files against Git and verified the archive SHA-256. The implementation session recorded 119 passing existing tests, Ruff and mypy checks, and cancellation in 0.234 s with a five-second retry delay configured. I did not rerun those checks. [Networka commit](https://github.com/narrowin/networka/commit/8b504ba1b8f12f6d30ce6496d9e8c08816149424) · [Package provenance](../vendor/README.md)

## What remains

- **Test policy.** The final packet-loss run had about 91 ms to spare on full recovery. A 15-second failure in another run deserves examination on its own evidence. The proposed 40 seconds is a local allowance for one nominal 30-second slow LACP interval plus 10 seconds for reattachment, scheduling and SSH verification. It has no status as a protocol guarantee. Decide that policy separately. The qualified branch still enforces 15 seconds and both traffic limits. [Timing review](lacp-recovery-timing-sources.md)
- **Coverage.** Only Small with spanning tree off completed the final four-test set on ARM64. Small RSTP inherits the bond configuration. Its campaign, other lab campaigns, full AMD64 fault qualification and physical hardware remain outside this result. Run other labs in the ordinary course of testing and use their own reports for claims about them.
- **Adoption.** The support reply is prepared and unsent. Continue using the prototype until an official image can be qualified. The current launcher looks for the literal hook-loop form in `/start.sh`. An equivalent implementation with different syntax can be rejected. Check that when switching images. [Launcher](https://github.com/mischadiehm/containerlab/blob/f3733e41ab78f8144982d59973061e51925d36da/nodes/mikrotik_chr/chr-launch.sh#L76-L89)

The review covered the original chat through the request for this assessment, including the later authorizations to patch containerlab and push the work. Lab comparison `f2ccd31..43fe006aec0375536590057ada5af2aea1c5cc33`; fork comparison `ccf5be6..f3733e4`. The three branch tips match their respective origin tracking refs. This review changed only this local assessment. No new fault injection, publication or support message was needed.
