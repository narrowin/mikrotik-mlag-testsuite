# Parts of the new lab tests carried over from the old suite

This audit looked at the Small lab files, the two Small tests with their state file, and the Networka test engine that runs them.
It questioned 89 parts that came from the old suite, and 10 of them were checked on the running lab or in the export.
The result is 19 parts to remove, 35 to simplify, 4 still unclear and 31 that earn their place.

The live checks are in test-results/suite-yaml-verify/prototype/audit-live/. All three live runs passed. The lab mlag-small-i1 is still up and was put back to its earlier settings after each check.

## Remove

| Part | Where (file) | Why it is not needed | What to do |
| --- | --- | --- | --- |
| The whole baseline test | tests/small/baseline.yaml | Every test already checks the state, runs a 5 s baseline that must lose nothing, and refuses to cut a cable otherwise. | Delete the file and its mentions in tests/README.md and the walkthrough. |
| Syslog collector node | labs/small/small.clab.yml | Neither the new tests nor Networka read RouterOS syslog. It also pulls an unpinned rsyslog:latest image on every deploy. | Delete the node, its logs bind and the Small syslog image steps in labs/campaign.sh (lines 149-156). Keep labs/shared/rsyslog.conf, because Medium and Large bind it. |
| CHRs wait for the collector at startup | labs/small/small.clab.yml | It exists only for the collector. | Delete it in the same change as the collector, or the deploy waits on a missing node. |
| Remote logging rules and the startup ready marker | labs/small/small.rsc lines 9-17 | Nothing in the new tests reads them. They are also the only reason campaign.sh rewrites small.rsc per lab instance. | Delete the lines and the small.rsc entry of the address rewrite in campaign.sh. |
| Direct cable between the two clients on eth3 and its 198.51.100.x addresses | labs/small/small.clab.yml, labs/shared/client-network.sh lines 31-36 | It carried the bypass streams, which are gone. No stream, capture or check uses eth3. | Delete the link and lines 31-36 together. The script stops on the first error, so a leftover address line would abort the deploy. Fix the bypass text in labs/small/README.md and labs/README.md. |
| Pinned neighbour entries on client 1 and client 2 | labs/campaign.sh 182-185, labs/small/quickstart.sh 46-49, docs/operator-guide.md 212-215 | They were made for reboot cases. A live run without them passed with the same loss as with them (23 probes on Member back). The unpinned ARP was answered in 1.4 ms. | Delete them. Only the old direct runner's neighbour check needs them. |
| Frame type filter on the bridge and on ether2 | labs/small/small.rsc lines 3-4 | A live run with admit-all passed every state check. The peer link carried no new untagged traffic. MLAG peer traffic (ICCP) is untagged and passed either way. | Delete both settings. Whether the MikroTik manual example uses them was not checked. |
| Stream 201 | tests/small/*.yaml | The reply of stream 101 already takes the same path in the same direction. It reported the same counts as 101. | Delete it and its limit entries. |
| Stream 202 | tests/small/*.yaml | The reply of stream 102 already covers this direction on the same path. | Delete it and its limit entries. |
| Capture of CHR 1 eth2 | tests/small/bond-member-loss.yaml:39 | It holds the same frames as client 1 eth1 on the same cable. No rule reads it. | Delete it. |
| Peer link captures on both CHRs | tests/small/bond-member-loss.yaml:40-41 | No rule reads them. They only served tracing paths by hand. | Delete them and soften the peer link claim at line 47, or add a path check to the engine. |
| Client 1 member captures inside both CHRs | tests/small/bond-member-loss.yaml:42-43 | They duplicate the captures of the same cables at the container interfaces. | Delete them. |
| ether5 captures on both CHRs | tests/small/bond-member-loss.yaml:44-45 | They served the old MAC move and flood checks. Which CHR the third host uses belongs in a state check. | Delete them. |
| Captures on the QEMU tap interfaces and their comment | tests/small/bond-member-loss.yaml:34-35 | In the run the tap held the same frames as the container interface, and 0 frames while the cable was down. | Delete them. The engine keeps the tap layout for setting the guest link down. |
| Explicit address on every stream | tests/small/*.yaml | The engine already pings the one IPv4 address of the destination interface. A written address can drift from the lab. | Delete the address fields. |
| Bond member lists on the CHRs (4 checks) | tests/small/state.yaml | The LACP member check reads the same rows and fails if the member is missing. Membership is startup config that no step changes. | Delete them. |
| Bond member lists on the Linux clients (2 checks) | tests/small/state.yaml | The per-member checks already fail if eth1 or eth2 is not in the bond. | Delete them. |
| Bridge port forwarding checks (4 checks) | tests/small/state.yaml | With spanning tree off there is no blocking state. A running port forwards, and the LACP checks prove the bonds run. | Delete them. Look at it again only if peer link tests are added. |
| Checksum file of the pcaps | Networka lab.py, labtest.py, traffic.py | The engine never deletes captures. The sums sit next to the pcaps and prove nothing about a change to them. | Delete the file and its check. |

## Simplify

| Part | Where (file) | Why it is not needed as it is | What to do |
| --- | --- | --- | --- |
| Campaign wrapper that always runs an old suite case | labs/campaign.sh lines 39, 192-205 | The new tests got their lab by running an unrelated old baseline case in a second uv environment. | Add a deploy-only path that keeps the health wait and the cable mode step. |
| Cable mode (MAC learning off) set after the health wait | labs/shared/forward-control.sh, labs/campaign.sh 178-181, quickstart.sh 42 | The audit called it unclear, but the review found a case where a learning two-port bridge drops replies in this very failover, so learning stays off. | Put --wire into the Small kind exec as Medium and Large do, and drop the separate step from campaign.sh, quickstart.sh and the operator guide. |
| Second leg of the third host to CHR 2 | labs/small/small.clab.yml, client-network.sh | The tests need a host on CHR 1 only. The CHR 2 leg carried no probe. | Use one cable to CHR 1. CHR 2 then has no ether5, and the shared small.rsc would fail at its ether5 lines, so CHR 2 needs a config without ether5. |
| The third host's name and role | tests/small/bond-member-loss.yaml, client-network.sh | It is called the MAC-move host, but here it is a host behind CHR 1 only. Its path depends on which bond member Linux picked. | With one cable it is single-attached by construction. Name and comment it as such. |
| Client endpoint image | labs/shared/client.Dockerfile | iputils is unused, because ping runs from the VM. The /proc/net/bonding comment is out of date. alpine:latest is unpinned. sshd stays until Networka can read the host checks through nsenter. | Drop iputils, pin the base image, fix the comment. |
| Image defaults and pull policy | labs/small/small.clab.yml | Deploying without campaign.sh gives whatever the development tag points to. Pull policy Always on a pinned image only adds a registry round trip. | Default to the campaign-image.txt digest or fail without it. |
| Address rewriting per lab instance | labs/campaign.sh 121-129 | After the logging rules go, small.rsc needs no rewrite. The profile rewrite remains only because the profile hard-codes addresses. | Drop the small.rsc rewrite. Later, let Networka take addresses from topology-data.json. |
| Networka lab profile | labs/networka/small.yml | The third host's entry is used by no check. Host key checking is already off at 3e96460. | Delete the third host's entry and group membership. |
| Stream numbers | tests/small/*.yaml | The numbering scheme is written nowhere a reader sees it. The engine only needs a unique number. | After 201 and 202 go, add one comment per stream or give streams names. |
| Client 1 eth1 and eth2 captures | tests/small/bond-member-loss.yaml:37-38 | The review found that eth1 alone shows whether RouterOS or the Linux bond causes the return outage. eth2 adds nothing. | Keep eth1 with a comment that says why. Drop eth2. |
| Hold 8 s in Member down | tests/small/bond-member-loss.yaml:52 | The value is the old runner's default with no reason. | Keep 8 s and write the reason: longer than the largest allowed outage, and long enough for late LACP effects. |
| Hold 11 s in Member back | tests/small/bond-member-loss.yaml:61-66 | The extra 3 s is the old runner's recovery window, which the engine does not have. | Use 8 s with the same reason. |
| Limit 3 s in Member down | tests/small/bond-member-loss.yaml:55-56 | Its only reason is LACP timing, which does not apply to carrier loss. The export's six runs (streams.tsv at 5929968, Small, bridge none, bond-member-loss) give at most 0.217 s, so 3 s would hide a 14-fold regression. | Add a loss spread row per phase to mlag-lab export first, then set the limit from it with a stated margin. |
| LACP member checks on the CHRs (4 checks) | tests/small/state.yaml | They read the other end of the same LACP exchange that the host side check reads. | Keep the host side check only. |
| Carrier field in the host member checks | tests/small/state.yaml | A live poll showed the member is never eligible without carrier. | Drop the field, or keep it only for its clearer failure message. |
| Comments and sources that name old suite files | tests/small/*.yaml | They say where a thing was copied from, not why it is there. | Replace each with its reason. Point sources to the manual, small.rsc or client-network.sh. |
| "on VLAN 110" in the stream 302 comment | tests/small/*.yaml | Every stream runs on VLAN 110 now. | Delete the phrase. |
| Interface names in the comments | tests/small/bond-member-loss.yaml:2, 47, 50, 60 | Nothing says that client 1 eth1 is cabled to CHR 1 ether3. | Add one mapping line. Give the Member back limit's reason instead of LACP flags. |
| 2 s wait before the baseline | Networka labtest.py | With cold host ARP caches, every stream was answered within 3 ms. | Start the baseline at the first reply of every stream. |
| Baseline window 5 s and the duplicate step | Networka labtest.py, tests/small/baseline.yaml | The old value was 4 s, and nothing explains 5 s. | Derive length and probe count from one stated rule. |
| Baseline needs 30 delivered probes | Networka traffic.py, labtest.py | The no-loss and no-duplicate part is needed. The number 30 follows from nothing. | Derive the count from the window and the interval. |
| Two baseline rules, one from ping text and one from captures | Networka labtest.py, traffic.py, lab.py | The two can disagree. The verdict always comes from the captures. A live read of a pcap still being written works, but lags about 0.6 s. | Keep one rule. |
| Interval read back from the events | Networka labtest.py, lab.py, traffic.py | No rule reads it, and 0.1 is defined twice. | Keep one constant with its reason and drop the read-back. |
| 2 s settle before the second state check | Networka labtest.py | The review found a real need: captures must run at least 0.5 s past the last step, or the last probes count as lost. | Replace the 2 s sleep with a wait derived from the late reply limit. |
| tcpdump options | Networka lab.py | -Z root only changes the file owner. -s 0, -n and -B 4096 have no shown need. Without immediate mode, tcpdump lost the unread tail of its buffer at stop, which the drop check does not see. | Use --immediate-mode, or compare captured with received packets. Drop the options that have no effect. |
| Wait for each capture to start, one at a time | Networka lab.py | 12 captures took about 0.6 s one after the other. | Start all, then wait once. |
| Kernel drop count parsed twice | Networka lab.py, traffic.py | The second regex misses "1 packet dropped". | Keep one parser. |
| tshark decode cache | Networka traffic.py | A run decodes 3 to 5 small pcaps once. The cache lives outside the evidence folder. The 25 s timeout is arbitrary. | Call tshark without a cache. |
| A gap belongs only to the step it starts in | Networka traffic.py, labtest.py | A gap that runs past the restore makes the later step report no outage while its lost count is above 0. The old suite judged such a gap in both steps. | Use one rule for lost count and outage. Fix the docstring that claims the old rules. |
| Meaning of a 0 s limit | Networka labtest.py, docs/lab-tests.md | "No lost or late probe" is hidden in a special case of the bound rule. | State it once in the code and the docs. |
| Carrier confirmation after a cable is set down | Networka lab.py | One confirmed end is the interface the engine set down itself. The 2 s limit differs from the documented 0.5 s, and nothing judges the latency. | Confirm only the far end. Pick one limit and say why. |
| timeline.tsv | Networka labtest.py | It only reformats events and gaps, and replay does not rebuild it. | Produce it on demand. |
| Evidence folder layout | Networka labtest.py, lab.py | Three entries exist only for the parts above. | Keep test.yaml, state, state-before, state-after, captures, streams as diagnostics, events.jsonl and result.json. |
| Extra captures count toward validity | Networka labtest.py, traffic.py | Captures that no rule decodes can still turn a good run into an error. | Capture stream ends by default. Make extra captures diagnostics that cannot change validity. |
| Constants in the engine | Networka labtest.py, lab.py, traffic.py | None of the measurement values has a written reason. Several depend on the interval but are not derived from it. | See the last section. |

## Unclear

| Part | The open question | The check that settles it |
| --- | --- | --- |
| Spanning tree settings at boot (RSTP, priority, costs, edge) | Does MLAG come up cleanly with protocol-mode=none from boot, so the manual STP-off step and its state check can go? | One fresh deploy with protocol-mode=none in small.rsc and no manual step, then the state file passes and the loss matches the earlier runs. |
| Limit 3 s in Member back | Is 3 s right? The export's six runs reach 2.92 s, which leaves 0.08 s of margin, and today's runs reached 2.83 s. | A loss spread row per phase in mlag-lab export, then a decision on the limit. |
| No check of the third host's attachment | Nothing confirms the host uses CHR 1, and that decides whether stream 101 crosses the peer link. | The single cable to CHR 1 settles it by construction. If the second leg stays, set primary eth1 and add a Networka active-backup check, which does not exist yet. |
| Destination capture per stream | The verdict needs only the source capture. The destination capture adds only the direction of loss. | Your decision whether direction of loss is wanted. If not, judge from the source capture only. |

## Keep

| Part | Why it earns its place |
| --- | --- |
| VLAN 110 with VLAN filtering and the peer link tagged | MLAG needs the client VLANs carried on the peer port. A setup without filtering was not tested. |
| lacp-rate=1sec on the RouterOS bonds | It sets the return timing that the limits were measured with. |
| Fast LACP rate on the Linux clients | It matches the RouterOS rate. |
| ether5 port on CHR 1 | Streams 101 and 102 end there. |
| Linux 802.3ad bond with 100 ms link monitoring | Without it the client keeps sending on the cut member. |
| Fixed bond MACs and the layer2+3 hash | They put client 1's streams on the cable the test cuts, every run. |
| Probe addresses set at deploy | Every stream needs them. |
| Forwarding of LACP frames on the CHR container bridges | Without it no LACPDU reaches RouterOS. |
| QEMU wrapper that sets 10G full duplex | Without it the Linux bonds never formed a two-member aggregate. |
| Locks, copy sync and health wait in campaign.sh | Parallel deploys would race, and tests would start on booting CHRs. |
| Rebuild of the endpoint image | It keeps the image equal to the Dockerfile. Pin the base image. |
| Fixed management addresses | The profile needs them until Networka reads topology-data.json. |
| MLAG pair, peer link and the two dual-homed clients | This is the system under test. |
| labs/shared/rsyslog.conf | Medium and Large still bind it. |
| labs/shared/root-client.sh | Only Medium uses it. Question it when Medium gets new tests. |
| Stream 101 | It is the only stream that crosses the peer link during the fault. |
| Stream 302 | It measures the path between two MLAG bonds. |
| Stream 102 as the control | It catches a disturbance of other ports on CHR 1. |
| Limit 0 s for the control stream | A stream off the cut member has no reason to lose anything. |
| Step names | They are plain and say what the step does. |
| MLAG connected on both peers | It is the precondition of every MLAG fault. |
| Spanning tree off check | It catches a missed manual STP-off step until the lab boots with it off. |
| Host side LACP member check | It proves both CHRs present one LACP system to each client. |
| Sender pace limit | A stalled sender hides an outage, and stalls have been seen. |
| Late reply limit | Delivery needs a deadline. |
| Lower and upper bound of an outage | It is the honest reading of sampled probes. |
| Duplicates fail a step | With spanning tree off, a duplicate is the sign of a loop. Fix the doc sentence that says they are not checked. |
| ip link plus QEMU link down for one cable | Each side sees carrier loss only through its own action. |
| Restoring cables on exit | A failed run would leave a cable down for the next test. |
| Wall clock and monotonic time with the clock check | Windows line up with pcap times, so a clock step would distort outages. |
| Refusing a save folder with evidence | A rerun would mix two runs' events. |

## Unexplained numbers

| Value | Name or place | File |
| --- | --- | --- |
| 0.1 s | Probe interval, also the start_stream default | Networka labtest.py, lab.py |
| 2 s | NEIGHBOUR_S, wait before the baseline | Networka labtest.py |
| 5 s | BASELINE_S, baseline window (old suite 4 s) | Networka labtest.py |
| 2 s | SETTLE_S, wait before the second state check | Networka labtest.py |
| 50 ms | CLOCK_LIMIT_NS, clock check | Networka labtest.py |
| 450 ms | SEND_GAP_LIMIT_NS, sender pace limit | Networka traffic.py |
| 500 ms | LATE_REPLY_NS, late reply limit | Networka traffic.py |
| 30 | BASELINE_MIN_DELIVERED, baseline probe count | Networka traffic.py |
| 25 s | tshark timeout, twice | Networka traffic.py |
| 5 s | LISTEN_TIMEOUT_S, capture start wait | Networka lab.py |
| 2 s | CONFIRM_TIMEOUT_S, carrier confirmation (docs say 0.5 s) | Networka lab.py |
| 5 s | STOP_TIMEOUT_S | Networka lab.py |
| 12 s | COMMAND_TIMEOUT_S | Networka lab.py |
| 3 s | QMP socket timeout | Networka lab.py |
| 4096 KiB | tcpdump kernel buffer | Networka lab.py |
| 8 s | Hold in Member down | tests/small/bond-member-loss.yaml |
| 11 s | Hold in Member back | tests/small/bond-member-loss.yaml |
| 3 s | Limit in Member down | tests/small/bond-member-loss.yaml |
| 3 s | Limit in Member back (reason only in old code) | tests/small/bond-member-loss.yaml |
| 110 | VLAN number, arbitrary but harmless | labs/small/small.rsc |
