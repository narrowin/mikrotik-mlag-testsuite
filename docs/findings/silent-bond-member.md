# A silent bond member: RouterOS keeps sending to it

When a host's bond member stops sending but its cable keeps carrier, the MLAG peer keeps sending traffic to that bond member.
With every frame from `host1` on one cable lost, the current Small lab lost every ping from `host1` for the whole step and did not recover.
The old suite traced the same behaviour frame by frame when the Linux side took a bond member down.
Both match [Finding 1 and Finding 2](mlag-bond-without-lacp-partner-keeps-forwarding.md): an MLAG bond keeps forwarding into a bond member that has no LACP partner.

## 100 % packet loss on one cable

- The Small lab test [cable-packet-loss](../../tests/small/tests/cable-packet-loss.yaml) drops every frame leaving `host1` on its cable to switch2, LACPDUs included, for 25 s. The cable keeps carrier.
- Run `tests/small/runs/networka-0.5.2-20261127/cable-packet-loss`, spanning tree off: ERROR.
- In that run the stream `host1` to `host2` lost 379 pings at one ping every 100 ms, an outage of at least 39.4227 s against 4 s.
- The stream `host2` to `host3` lost no ping.
- That saved report still names the hosts `client1` to `client3`, as the lab did before the hosts were renamed.
- The run stopped because the lab did not recover within the deadline after the loss was cleared.
- Run `tests/small-rstp/runs/networka-0.5.2-20261127/cable-packet-loss`, RSTP: ERROR, because the sender cadence was invalid in the loss step; its outage is diagnostic only.
- The limit of 4 s is one fast LACP timeout of 3 s plus one LACPDU interval; the switch should have stopped using the bond member by then.
- The behaviour was first seen while the packet loss action was built; that run was not saved, so its figures are not quoted.

## Linux side takes a bond member down

The old suite took the Small lab bond member of `host1` toward switch1 down on the Linux side on 24 November 2026.
The sequence comes from the [postmortem](../../results/2026-11-24-small-lab/postmortem.md) of that run.
Its counts and times are written by hand there and are not quoted here.

1. `host1` stopped sending LACPDUs on the bond member and sent its requests over switch2 and the peer link.
2. switch1 still sent the replies out the old bond member toward `host1`.
3. After the fast LACP timeout, switch1 advertised the expired LACP state, with collecting and distributing clear.
4. After that, the replies reached neither bond member of `host1`.
5. Later, replies again left switch1 on the old bond member, while it was still down at `host1`.

- During all of it switch1 listed `ether3` as active in the bond and kept the host entry of `host1` on its local bond.
- MLAG stayed connected, and the RSTP root and topology-change counters did not change.
- So the outage was neither the LACP timeout alone nor an RSTP reconvergence.
- When RouterOS took the same port down instead, switch1 learned `host1` over the peer link after forwarding switched, and the outage was far shorter.
- A MikroTik forum report also saw different results when the host or the switch took the bond member down: [MLAG client LACP failover handling](https://forum.mikrotik.com/t/mlag-client-lacp-failover-handling/272065).

### Not verified

- Whether RouterOS saw carrier drop on `ether3`. The containerlab CHR launcher of that time attached a veth to its TAP but did not pass administrative state or carrier changes into QEMU; that was read from its code, not observed live.
- Whether `lacp-strict=yes` changes the behaviour on this path.

## LACPDUs blocked while the cable carries data

- When only the LACPDUs of `host1` were blocked, RouterOS dropped the bond member after the fast LACP timeout.
- Old suite, Small, spanning tree off, `2026-11-24-small-search/none-default-l2`, test `01-lacp-timeout`: PASS, an outage of 3.23 to 3.44 s while LACPDUs were blocked and 0.21 to 0.42 s after they resumed, against 4 s and 3 s.

## RouterOS commands that showed the state

These worked on 7.26beta7, once and as a continuous monitor. `client1` is the bond name in the old suite's startup config:

```routeros
/interface/bonding/monitor-slaves bond=client1
/interface/bonding/monitor-slaves bond=client1 once=yes
/interface/ethernet/monitor ether3 once
/interface/bridge/host/print detail where mac-address=02:00:00:11:00:11
```

- `monitor-slaves` gives the actor and partner flags of each bond member, which the bond's active list hides.
- The RouterOS API returned the same bond member, Ethernet and bridge monitor samples about once per second over one session.
- `/interface/listen` and `/interface/bridge/host/listen` sent no event in steady state; whether they report a change during a fault was not checked.
