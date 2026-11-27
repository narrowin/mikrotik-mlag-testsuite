# Labs have no bypass cable between hosts

The bypass is a direct cable between two hosts that crosses no switch.
The old suite pinged across it during every test, with a 0 s limit, to show that the measurement itself did not lose pings, and calibration tests cut it for 2 s to show that a known outage is measured correctly.
The bypass cable, its streams and the calibration tests that cut it are removed from every lab.

## Why

On 2026-11-26 the operator decided that the Small lab under `tests/` does not use the bypass.
He said: "In the lab, we have always a management network".
The commit that removed it gives the reason: Networka's own validity checks cover what the bypass was for: a steady sending pace, no dropped captures and a clean quiet window before the first action.
On 2026-11-27 the operator extended the removal to every lab.

## Consequences

Small and its RSTP lab already have no bypass and no calibration test.
The bypass cable, its streams and the calibration tests were removed from every lab under `tests/` on 2026-11-27.
Until then Medium, the two-pair lab, the two-pair strict lab, Large, small-mac-move and the RSTP labs of Medium and the two-pair lab still have a bypass cable and `bypass-*` streams with 0 s limits, and all but Large have calibration tests that cut it.

See also [Networka ADR 0012](https://github.com/narrowin/networka/blob/main/docs/adr/0012-validity-checks-prove-the-measurement.md).
