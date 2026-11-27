# Reboot and power loss are separate tests, and a reboot is a real RouterOS reboot

A reboot test runs `/system reboot` on the switch and proves a new boot from its uptime.
A power loss test pauses the CHR guest and withdraws carrier on all its data cables, keeps it off for 20 s, then resets and resumes it and proves a fresh boot.
Medium and small-mobile have both for the MLAG primary and the MLAG secondary, and Small has the reboot.

## Why

MLAG detects a dead peer differently in each.
In a CHR reboot the cables stay up, so the surviving peer must notice the missing MLAG heartbeat, and the partners notice it only through the LACP timeout.
In a power loss every neighbour sees its cable go down at once.
Power loss keeps the switch off for 20 s, well past the 3 s fast LACP timeout, so the survivor has fully taken over before the switch returns. The [bridge CLI reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/) says a peer logs a warning after three missed heartbeat intervals; the labs keep the default interval, which the manual does not state.
Both tests then go through the same rejoin and the default 60 s MLAG initialisation delay.

On 2026-11-25 the operator noticed that a CHR is back about 15 s after `/system reboot` and asked: "So yeah, we should use the power loss case then, not do the reboot at all, right?"
On 2026-11-27 the operator kept both.
The fast CHR reboot is accepted as a test.
A slower hardware reboot only lengthens the time with a single switch, and the power loss gap covers that time.

## Considered options

- **Power loss only.** Rejected: it drops the fault where the switch is gone while its links still show carrier.
- **Hold the guest for 20 s after the reboot's reset**, to imitate a slow hardware reboot. Not needed, since power loss covers a long single-switch period.
- **Freeze the guest when its management address stops answering.** Rejected: the freeze lands while RouterOS still shuts down, which is a hung switch, a different fault.

## Consequences

Both kinds of test allow each switched stream 5 s, three fast LACP intervals plus two for forwarding, and hold 16 s after the switch returns.
A power loss test waits up to 180 s for the cold boot, the SSH cooldown and the 60 s MLAG initialisation; a reboot test waits up to 60 s.
A reboot shorter than the heartbeat timeout means some runs never leave MLAG `connected`; in the old suite 38 of 52 saved Medium reboot runs did not.
