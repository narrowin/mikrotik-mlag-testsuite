# To do

Open work after the Medium and Large labs moved to Networka, as of 27 November 2026.

## Networka

- `nw test summary` ranks a lab's worst stop by the largest measured stop, even when it is within its limit. The front page shows Large's expected 39.9 s dc1 outage in site power loss instead of the failing DCI stop. Rank by stops that break their limit.
- A powered-off Linux host keeps its bond and neighbour state, and streams from it show lower bounds near 0 because their pings were never sent. Decide whether those streams count as unverified.

## Unexplained differences from the old suite

- Medium primary power loss: 3 of 8 runs lost 0.21 to 0.52 s right at power off, where the old runs lost nothing. Networka pauses the guest before it withdraws the cables; the old runner did the reverse. Not tested ([tests/medium/README.md](tests/medium/README.md)).
- Two-pair inter-pair member flap: traffic stops for the whole 8 s down hold, where the old suite lost 0.1 to 0.5 s on the same RouterOS. Every lab difference tested so far is ruled out ([tests/two-pair/README.md](tests/two-pair/README.md)).
- Two-pair primary reboots stop 2 to 7 s shorter than in the old suite. A faster native CHR restart is a guess, not verified.

## Large

- In the dc1-dist2 reboot, the dc1 stream to the VRRP address is unverified because its sender lost its 100 ms cadence.
- Core and distribution reboots fail with about 15 to 18 s on the DCI streams against 5 s. This is the known reboot fault, kept as a finding.

## Decisions for the operator

- Proposed ADRs 0020 (no bypass cable) and 0021 (no separate baseline test) would remove the bypass streams, calibration tests and baselines from Medium, both two-pair labs, Large, Small mobile and the RSTP labs.
- The two-pair and strict labs share their tests by symlink; the strict `lab.yaml` repeats the two-pair one to change one value.

## Clean-up seen in review

- The remote logging tail and `refresh-collector` scheduler are copied into every startup config, and the bond loop into three `host-setup.sh` files, which already differ.
- Large hardcodes its collector address in `tests/large/lab/routeros.rsc`; the other labs take it from `COLLECTOR`.
- MAC prefixes overlap across labs: the two-pair `admin-mac` `02:00:00:21:00:11` equals the Medium host1 MAC.
- `tests/shared/start.sh` carries the `age` profile that only the MAC-move lab uses.
