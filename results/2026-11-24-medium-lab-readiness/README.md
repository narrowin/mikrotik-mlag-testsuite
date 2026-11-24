# Medium lab readiness

## Setup

| Setting | Value |
| --- | --- |
| Deployment | Medium lab on the `mlag-external` OrbStack VM |
| Devices | Five RouterOS 7.26beta7 CHRs, two Linux probe hosts and one syslog collector. [Inventory and link map](../../labs/medium/README.md) |
| Management subnet | `172.30.218.0/27` |
| Test traffic | VLAN 110 and the independent bypass, both directions |
| Pass target | Four-second window with ≥30 deliveries per direction, zero loss and zero duplicates |

## TL;DR

- **STP off passed twice.** Ready in **12.63–12.69 s from reset**, or **21.18–21.68 s for the full command**. The lab finished in this working state.
- **With RSTP on, the two hosts could reach each other only over the bypass.** The baseline failed **10.57 s** after reset. VLAN traffic reached `dc1-mlag2` over the peer link and never appeared on its TAP toward the access switch, despite the port reporting forwarding. The runner withheld the fault.
- **Networka ran the management ping in 1.45 s.** All five CHRs returned 3/3 replies to the probe host’s management address.

## Readiness checks

1. Verify the deployment, named devices, management IPs and pinned CHR image.
2. Reset the bridges over management SSH and confirm guest uptimes advanced.
3. Read back bridge mode, VLANs, MLAG, LACP, neighbors, link carrier, syslog and BPDU behavior.
4. Score a four-second capture window. Require at least 30 deliveries per VLAN and bypass direction with zero loss or duplicates. With STP off, also verify one delivered copy of each broadcast request.

| Stage | STP off, two runs | RSTP |
| --- | ---: | ---: |
| Bridge reset | 2.49–2.51 s | 2.52 s |
| Start observers and settle | 1.22–1.33 s | 2.53 s |
| Probe and read back state | 4.45–4.49 s | 4.56 s |
| Check captures and delivery | 4.37–4.47 s | 0.95 s |

The RSTP baseline delivered **0/44** and **0/43** VLAN probes and **43/43** in each bypass direction. These checks injected no fault.

## Reproduce

[Readiness procedure](../../docs/test-framework.md#time-initial-readiness-on-the-medium-lab) · [Live baseline-only commands](../../docs/operator-guide.md#introduce-rstp-after-the-all-bridges-off-run) · [Networka management ping](../../docs/operator-guide.md#execute-a-command-on-the-medium-lab) · [Offline replay instructions](../../docs/test-framework.md#read-or-replay-a-run)

For this report’s offline replay, extract the archive below and pass `external-all-stp-off-baseline` and `external-baseline` to the evaluator in separate invocations. Expect exit 0 with STP off and exit 1 with RSTP on.

## Evidence

[Raw timings, captures and Networka output](evidence.tar.gz) · [Checksums](SHA256SUMS)

The first Networka group run exited zero after all five host-key checks failed. The verified run checked each device’s actual output after host-key enrollment. Networka also verified all five RouterOS identities in 0.98 s.

These captures used the earlier deployment name `dc1-mlag-external` and access-switch name `dc1-witness-switch`. The current [Medium lab inventory](../../labs/medium/README.md) maps the same roles and management addresses.

## Verification after renaming

| Lab | Case | Mode | Result | Reset to verdict |
| --- | --- | --- | --- | --- |
| Small lab, `mlag-small` | SMALL-01 | RSTP | Passed | 8.28 s |
| Medium lab, `mlag-medium` | MEDIUM-01 | STP disabled on all bridges | Passed | 13.06 s |

Both checks verified MLAG, LACP and loss-free traffic in both VLAN and both bypass directions. All seven CHRs ran the pinned 7.26beta7 image. Device and container names follow the [naming convention](../../docs/lab-naming.md). New JSON and JUnit records include lab names and case IDs.

[Passing checks, configurations, captures and JUnit](renamed-labs-evidence.tar.gz) · [Running deployments](renamed-deployments.txt) · [Checksums](SHA256SUMS)

Replay `naming-small-rstp-ready` and `naming-medium-final` from the extracted archive with the [existing evaluator](../../docs/test-framework.md#read-or-replay-a-run). Expect exit 0 for both. The initial Small lab attempt lacked the permanent neighbor entries required by the documented setup. Applying that setup produced the pass recorded above.
