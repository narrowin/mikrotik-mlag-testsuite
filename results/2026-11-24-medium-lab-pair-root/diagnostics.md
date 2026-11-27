# Pair-root reboot diagnostics

[Campaign summary](README.md) · [Per-direction loss bounds](phase-loss.tsv)

## Primary reboot

RouterOS uptime confirmed the reboot. The surviving peer, virtual TAPs and downstream interfaces retained carrier. The first loss followed traffic sent to the unavailable primary until LACP stopped selecting it. Both directions briefly recovered through the secondary.

| Time from reboot request | Transparent-cable trace |
| --- | --- |
| 1.209 s | The access switch received its last BPDU from the original root on the primary-facing member. |
| 6.293–6.296 s | The access switch elected itself. The survivor received the announcement and logged `DESIGNATED_DISCARD`. Both directions began dropping again. |
| 15.547 s | The survivor logged a heartbeat timeout while still reporting connected secondary and carrier up. |
| 17.710–17.849 s | ICCP and survivor BPDUs returned. The access switch logged `ROOT_DISCARD` on its uplink. |
| 23.425 s | The access switch logged `ROOT_FORWARD`. Both client directions resumed within about 0.05 s. |

The access switch kept the earlier proposal from the survivor, which advertised port ID `0x8001`. The returning primary advertised `0x8003` with the same root, bridge ID and path cost. The access switch treated those proposals as inferior until expiry. The port ID ordering was reversed in the shorter repeat. This could explain the different return times. The selection of port IDs inside RouterOS remains unresolved.

For the 35 s pause, ARP resolution stopped the host from emitting management probes. The initial phase split was inconclusive. QMP’s recorded resume bounded the return and confirmed the loss persisted until resume.

The captures establish forwarding behavior and virtual carrier for these CHRs. Physical carrier and the blocked port in the original Site A/Site B incident remain unverified. [Historical results](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/plans/primary-reboot-plan.md#recovered-tests-and-their-limits) · [Checksums](SHA256SUMS)
