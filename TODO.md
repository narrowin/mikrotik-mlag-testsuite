# To do

Open work after the Medium and Large labs moved to Networka, as of 27 November 2026.

## Networka

- `nw test summary` ranks a lab's worst stop by the largest measured stop, even when it is within its limit. The front page shows Large's expected 39.9 s dc1 outage in site power loss instead of the failing DCI stop. Rank by stops that break their limit.
- A powered-off Linux host keeps its bond and neighbour state, and streams from it show lower bounds near 0 because their pings were never sent. Decide whether those streams count as unverified.

## Results of the live runs of 27 November after the renames

Every lab ran once on `live-20261127-glossary`; the lab READMEs link the reports.

- Medium RSTP with the access switch as root: every test stops at the state check before the test, because the access switch `uplink` never forwards. Both MLAG peers put their port to it back into the proposed root role every 2 s. Find whether RouterOS or the lab causes it ([tests/medium-rstp-access-root/README.md](tests/medium-rstp-access-root/README.md)).
- Two-pair inter-pair member flap passes without the bypass cable (2.5 to 2.8 s against 3 s); with it, traffic stopped for the whole 8 s down hold. Two-pair strict still fails it with 5.4 to 5.6 s, and two-pair RSTP now fails it.
- New FAILs against the earlier Networka 0.5.2 run, one run each: Medium secondary reboot stops 7.8 s against 5 s; the MAC-move lab's lacp-timeout stops 5.2 to 5.4 s against 4 s and its secondary reboot returns one flood probe. Small and Small RSTP cable-delay now pass.
- The saved runs were recorded with Networka 0.5.2. With the pinned Networka `03f61c3` they load and summarize, but replay is not byte-identical, because 0.5.2 used older names in `evidence.json`, `result.json` and `report.md`. The next live runs restore byte-identical replay.
- The run folders before `live-20261127-glossary` under `tests/*/runs/` are superseded; the findings pages still link the `networka-0.5.2-20261127` runs. Decide which to keep.

## Large

- In the dc1-dist2 reboot, the dc1 stream to the VRRP address is ERROR again (89 lost at 9.17 to 19.82 s), because its sender lost its 100 ms cadence.
- Core and distribution reboots fail with about 17 to 22 s on the DCI streams against 5 s. This is the known reboot fault, kept as a finding.

## Decisions for the operator

- The two-pair and strict labs share their tests by symlink; the strict `lab.yaml` repeats the two-pair one to change one value.

## After the glossary and ADRs (27 November)

- Capture slices and run compression (Networka ADR 0008) are not built in Networka; it still keeps full captures.
- A check that fails on `_Avoid_` words from GLOSSARY.md, once the glossary has settled.

## Clean-up seen in review

- The remote logging tail and `refresh-collector` scheduler are copied into every startup config, and the bond loop into three `host-setup.sh` files, which already differ.
- Large hardcodes its collector address in `tests/large/lab/routeros.rsc`; the other labs take it from `COLLECTOR`.
- MAC prefixes overlap across labs: the two-pair `admin-mac` `02:00:00:21:00:11` equals the Medium host1 MAC.
- `tests/shared/start.sh` carries the `age` profile that only the MAC-move lab uses.

## Containerlab

- Remove the learning step from `tests/shared/start.sh` once the labs run a Containerlab build whose CHR launcher creates the data bridges with learning off. `start.sh` then prints "The CHR data bridges already have learning off". Update the pinned build in [docs/tests/README.md](docs/tests/README.md) and [ADR 0008](docs/adr/0008-labs-need-containerlab-with-native-chr-support-and-the-qemu-wrapper-is-retired.md) in the same change.
