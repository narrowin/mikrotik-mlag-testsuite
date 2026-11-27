# Every device on an MLAG pair is dual-connected

Every host, access switch, firewall and distribution pair that connects to an MLAG pair has one cable to each MLAG peer.
Most use an LACP bond; the MAC-move host `client3` of small-mac-move uses an active-backup bond with the same MAC on either link.
No device is attached to only one peer.
A single-homed device is a future test, `FUT-01` in the [old case index](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/tests/README.md), not a current one.

## Why

On 2026-11-24 a draft topology had hosts and spanning tree root routers attached to one peer only.
The operator rejected it: "Everything is dual attached, also in the large lab".
His reason: a single-homed device makes the pair asymmetric, and that asymmetry is not what the current tests ask about.
He extended the rule to the Large lab, where the local service hosts are also dual-connected.
The two single-homed root routers built that day for diagnosis were dropped.

## Consequences

Real networks often have single-homed devices, and the suite does not yet say how MLAG treats them during a peer link loss or a peer reboot.
A test that needs one would add a new lab, not change an existing lab.
