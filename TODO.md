# To do

Open work after the Medium and Large labs moved to Networka, as of 28 November 2026.

## Networka

- A powered-off Linux host keeps its bond and neighbour state, and streams from it show lower bounds near 0 because their pings were never sent. Decide whether those streams count as unverified.

## Results of the live runs of 28 November on our image

Every lab ran once on `live-20261128-image-dbd8a548`, with our CHR image by digest and Networka 0.5.2+chr.5; Small and Small strict ran five fresh-deploy rounds. The lab READMEs link the reports, and every replay was byte-identical.

- Medium RSTP with the access switch as root remains blocked by RouterOS 7.26beta7 RSTP/MLAG agreement handling; every test is ERROR because the access switch `uplink` port does not forward before the test. A fresh deployment with default peer-port settings still blocks; timer-based forwarding passes the existing baseline, but changes the intended rapid RSTP behaviour. No lab correction was retained. The [investigation and generated reports](tests/medium-rstp-access-root/README.md#rstp-agreement-investigation-27-november-2026) are ready for a RouterOS follow-up.
- Two-pair and two-pair strict pass the inter-pair member flap; two-pair RSTP fails it.
- Small cable-packet-loss is ERROR in all five rounds. Small strict cable-packet-loss missed its 15 s recovery deadline in 2 of 5 rounds while its outage passed.
- Changed from the 27 November runs on the official image with Networka 0.5.2: Small and Small RSTP bond-member-loss, Medium secondary reboot and two-pair strict inter-pair member flap now pass; the MAC-move lab's lacp-timeout is ERROR instead of FAIL.
- The run folders before `live-20261128-image-dbd8a548` under `tests/*/runs/` are superseded; the findings pages still link the `networka-0.5.2-20261127` runs. Decide which to keep.

## Large

- Core and distribution reboots fail with about 16 to 20 s on the DCI streams against 5 s. This is the known reboot fault, kept as a finding. The dc1-dist2 reboot also fails on the dc1 VRRP stream.

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
