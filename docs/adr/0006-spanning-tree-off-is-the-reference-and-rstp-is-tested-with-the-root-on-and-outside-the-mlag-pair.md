# Spanning tree off is the reference, and RSTP is tested with the root on and outside the MLAG pair

Every lab has a form with spanning tree off: `protocol-mode=none` on every bridge in its startup config, checked as `stp_mode: none` by its lab file before every test.
That form is the reference every other STP mode is compared with.
The MikroTik manual says MLAG works with STP, RSTP and MSTP, so RSTP is tested too, on the same wiring, as separate labs ([ADR 0004](0004-the-startup-config-sets-the-lab-state-and-state-checks-prove-it.md)).

RSTP is tested with two root placements:

1. **The MLAG pair as root.** This is preferred if it works, because the pair is already the failover system of the network.
2. **A switch outside the pair as root.** This is the fallback in case MLAG breaks with the root on the pair.

Only Medium has a switch outside the pair today, its access switch, so the outside-root test runs on Medium first.
Small and the two-pair lab run the pair-root test only.
MSTP and the other old STP modes, such as a split root per VLAN, are not ported.

## Context

The old suite measured several STP modes in the Small and Medium labs on 2026-11-24.
With the MLAG pair as root, an MLAG primary reboot stopped traffic for 10.9 to 13.1 s against a 5 s limit.
RSTP with default settings showed an intermittent blackhole of about 10.6 s.
With the access switch as root, VLAN 110 did not forward at all.
These figures come from the old suite's plans, not from named `nw test` runs.

That morning the operator asked for each lab to run first without and then with spanning tree, on the same wiring: "Let's test and verify from the beginning without spanning tree and see if everything works."
That evening the operator limited live tests to spanning tree off.
On 2026-11-27 the operator approved RSTP labs for Small, Medium and the two-pair lab, and chose the two root placements above.

## Consequences

`tests/small-rstp/`, `tests/medium-rstp/` and `tests/medium-two-pair-rstp/` reuse the startup config and tests of their STP-off lab and set `STP_MODE: rstp` in their topology, which makes the MLAG pair the root.
A Medium lab with the access switch as root is not built yet.
Each RSTP lab counts towards the three labs that may run with tests at once.
The old STP-on results stay in `results/` as the frozen record.
