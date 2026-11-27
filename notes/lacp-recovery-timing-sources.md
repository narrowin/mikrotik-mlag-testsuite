# Small cable-packet-loss: recovery timing sources

Research date: 27 November 2026. This is a recommendation only; no test, limit,
startup config or engine code changed, and no live test was run for this review.

The existing `recovery_deadline_s: 15` has no demonstrated protocol derivation.
Recommend **40 s as a local recovery and verification budget**, with the existing
4 s affected-stream outage limit and 0 s independent-stream limit retained.
The reason to allow more than 15 s is the reachable slow-periodic LACP state
after partner information defaults, not the fact that recent runs barely pass.
Forty seconds is an explicit policy choice: one nominal 30 s periodic interval
plus 10 s local allowance for reattachment, scheduling and the complete SSH
state verification. Neither IEEE nor MikroTik promises recovery within 40 s.

The original value was introduced as `wait_healthy_s: 15` in commit
`c0a4ae2da3b5c89f094a822a0e1c7dbc1674871d`, at
`tests/small/cable-packet-loss.yaml`, with a generic comment allowing LACP
negotiation time and no formula. Commit
`c91d5998b16ea28fd4ef0274f95bc2bd79430904` renamed the key to
`recovery_deadline_s` and preserved the value and comment. These inspected
commits establish provenance, not a timed requirement.

## What the deadline measures

The [test](../tests/small/tests/cable-packet-loss.yaml) suppresses every frame
leaving `host1:eth2` for 25 s, including LACPDUs, while carrier stays up. Clearing
the impairment does not produce a carrier transition that would restart LACP.
The [host startup config](../tests/small/lab/host-setup.sh) requests fast LACP
and uses `coupled_control off`. The [RouterOS startup config](../tests/small/lab/switch.rsc)
sets `lacp-rate=1sec lacp-strict=yes min-links=1`.

The [lab state](../tests/small/lab/lab.yaml) requires both bond members of every
host to be eligible, both MLAG peers connected, and spanning tree off. Networka's
`TrafficActions.clear` starts its clock before removing the impairment; its
current implementation first reads the affected Linux bond member through its
normal SSH reader, then obtains every declared state check over SSH. The hard deadline includes
that verification, polling and evidence writes. Traffic continuing on the
healthy bond member therefore does not mean full recovery has completed.
See [`lab_faults.py`](../../networka/src/network_toolkit/lab_faults.py) and
[`wait_recovered`](../../networka/src/network_toolkit/lab_reboot.py).

## Verified protocol values

| Timer or setting | Value | Meaning |
| --- | --- | --- |
| Fast periodic | 1 s | Nominal periodic transmission interval when the operational partner requests short timeout |
| Slow periodic | 30 s | Nominal periodic transmission interval when the operational partner uses long timeout |
| Short receive timeout | 3 s | Invalidates received partner information after three fast intervals |
| Long receive timeout | 90 s | Invalidates received partner information after three slow intervals |
| Aggregate wait | 2 s | Hysteresis while waiting to attach a selected bond member |

These constants appear in the public [IEEE P802.1AX-REV D4.54 draft, section
6.4.4, printed page 58](https://datatracker.ietf.org/documents/LIAISON/liaison-2014-11-08-ieee-8021-rtg-completion-of-8021ax-rev-link-aggregation-to-ietf-routing-area-and-routing-area-wg-attachment-2.pdf#page=58).
That document is an **unapproved 2014 draft**, publicly supplied through an IEEE
liaison to the IETF; it is useful state-machine evidence, not a claim of
conformance to the final standard. It specifies ±250 ms timer tolerance.
The [IEEE listing for 802.1AX-2020](https://standards.ieee.org/ieee/802.1AX/6768/)
identifies the final standard; its full normative text was not used here.
The same constants are directly inspectable in the [Linux v6.12 implementation,
lines 27–32](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L27-L32).

The official [Linux bonding documentation](https://docs.kernel.org/networking/bonding.html)
defines `lacp_rate` as the rate **requested from the partner**, with fast=1 s
and slow=30 s. It also documents independent collecting/distributing control
and `min_links` as a carrier threshold. These settings do not establish a
complete lab-state recovery deadline. This distinction matters: configuring
fast receive timeout is not an instruction to transmit every second in every
subsequent operational state.

MikroTik's [official frozen Bonding reference](https://help.mikrotik.com/docs/spaces/ROS/pages/8323193/Bonding)
documents 1 s/30 s `lacp-rate`, active/passive LACP, and the minimum active
bond-member threshold. It says MII only observes local link state and cannot
prove that frames pass. Its general statement about taking a few seconds to
establish connectivity is not a numerical recovery guarantee. The current
[MLAG guide](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/)
recommends 1 s LACP to speed establishment but gives no universal rejoin bound.
The official [October 27 documentation changelog](https://manual.mikrotik.com/changelog/changelog-2026-10-27/)
records `lacp-strict` being added to the CLI reference, without supplying a
recovery timer.

## Why a sustained one-way impairment can reach slow periodic transmission

The draft's receive machine (6.4.12, printed pages 67–68) enters EXPIRED after
the receive timeout, clears partner synchronization, requests fast transmission
temporarily, and runs another short timeout. With no received LACPDU it enters
DEFAULTED and replaces operational partner information with locally administered
defaults. Its periodic machine (6.4.13, printed pages 69–70) uses that operational
partner's timeout selection. Defaulting does not itself mean that a negotiated
bond member is forwarding.

Linux v6.12 shows the mechanism concretely:

- [`ad_rx_machine`, lines 1292–1312](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L1292-L1312) performs EXPIRED and DEFAULTED transitions; [`__record_default`, lines 578–588](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L578-L588) copies the administrative partner information.
- [`ad_initialize_port`, lines 1949–1982](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L1949-L1982) initializes the partner state to `1`: activity set, short-timeout bit clear. Enabling fast LACP changes the local actor timeout bit, not this partner default.
- [`ad_periodic_machine`, lines 1436–1484](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L1436-L1484) chooses fast or slow transmission from `partner_oper.port_state`.

Inference for this fault: RouterOS receives none of host1's LACPDUs and can
default its partner information. If its resulting transmissions become slow,
Linux can also exhaust its short receive timeout, default its partner and send
slowly. Once both ends are in that condition, clearing a queue does not
necessarily trigger an immediate exchange; the next periodic LACPDU can be
needed. Fast configuration at both ends consequently does not exclude a wait
approaching a slow interval. Linux source corroborates the state mechanism; it
is not RouterOS source, nor proof of the exact kernel revision running in the
VM. The saved lab captures are needed to identify the actual RouterOS path.

## Which intervals overlap

Do not derive a deadline by adding `3 + 3 + 30 + 2 + 2`:

- Initial short-timeout detection and the further short timeout to DEFAULTED
  take place during the 25 s impairment hold. They are not fresh waits that
  must start when the impairment clears.
- LACP partners and bond members run their machines concurrently. Two periodic
  transmitters do not require two serial 30 s waits. Receiving a new LACPDU can
  trigger further transmissions before their periodic timers expire.
- Linux starts its 2 s wait on entering MUX WAITING after selection, not every
  time any frame arrives. It can already be over during the hold; changed
  partner identity on return can cause reselection. See [`ad_mux_machine`,
  lines 1004–1042 and 1147–1149](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/net/bonding/bond_3ad.c#L1004-L1042).
- The 90 s receive timeout applies when the local actor uses long timeout; a
  slow sender does not automatically change the configured local fast receive
  timeout to 90 s. The 60 s churn timer is diagnostic, not an obligatory
  reattachment wait.
- SSH verification and scheduler latency are observer/implementation costs; IEEE LACP
  timer constants do not bound them.

## Recommendation and uncertainty

The Small `cable-packet-loss` run
[`rejoin-final-small`](qualification/rejoin-chr4/final/result.json)
records full recovery in **14.820498463 s**. Its
[report](qualification/rejoin-chr4/final/report.md) passes
both the separate traffic limits and final state. The earlier
[`rejoin-parallel-proof/run`](qualification/rejoin-chr4/parallel/result.json)
records full recovery in **14.941006208 s**. These named runs are not a repeated
homogeneous timing distribution. Near-15 s passes establish that these runs
met 15 s; they do not establish a safe bound over timer phases, CPU scheduling
or repeated runs.

The diagnostic LACP capture stored locally at
`test-results/failover-cause-candidate/cpus2-2/lacp.pcap`
also shows a RouterOS actor with defaulted partner information before and
after a long transmission gap. Those packets occur 18.610 s before and
15.019 s after the recorded `fault_clearing` event: an approximately 33.629 s
gap. These are packet timestamps, not a measured traffic outage or full
recovery result. The corresponding generated [run result](qualification/diagnostic-cpus2/result.json)
is ERROR. This diagnostic supports allowing VM scheduling margin above a
nominal 30 s timer, but does not establish a worst-case margin.

Change the recovery deadline to 40 s **when implementing this recommendation**,
explicitly identifying it as a bounded local allowance for all declared state
and its verification. Thirty seconds accounts for a reachable nominal slow periodic
exchange; the additional ten seconds is a chosen local margin, not a documented
protocol sum or a statistically qualified bound. A 30 s total deadline would
leave no allowance for reattachment and SSH if the first usable LACPDU arrived
near its end. An unbounded wait would hide a stuck bond member. Keeping 15 s
would be defensible only as an explicitly chosen stricter recovery requirement,
which has not been supplied here.

Retain 4 s and 0 s as the stream outage criteria so that a larger recovery
budget cannot excuse poor failover. No finite deadline is guaranteed by the
sources under arbitrary scheduling or repeated negotiation failure. The
specific 40 s budget still needs qualification against the actual automation;
this review does not claim that qualification or alter any generated verdict.
