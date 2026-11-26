# Review of the clean Small lab

The identifiers follow the order of the 26 November 2026 review at `a324af6`. The original report is preserved in that commit. [Original findings](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/a324af6/docs/plans/clean-setup-open-findings.md)

The evidence for this review is in `test-results/suite-yaml-verify/clean/phase1-close/`. The static comparison in `03-lab-findings-checks.log` verifies that all ten device checks, both stream directions, the four cable actions, their times and limits, and the port log rules still match the previous run. `03-warning-sources.log` records the warning-text sources.

## Wrong results

| ID | Status | Decision and reason |
| --- | --- | --- |
| W1 | Fixed | During a live interrupt the port-up log arrived before the end markers. The run persisted its evidence and exited 130. Replay gave error (`03-interrupt-repeat.log`). |
| W2 | Fixed | All four steps passed in the live closing-only loss check. From client2 to client3, 6 pings were lost at one ping every 100 ms and traffic stopped for 0.537 to 0.744 s after the steps. Run and replay exited 1 with identical evidence hashes (`03-closing-loss.log`). |
| W3 | Fixed | A missing file starts at byte zero. The live run with no initial collector file and its replay both passed (`03-fresh-collector.log`). |
| W4 | Fixed, checked offline | The production judge used the captured cable log unchanged. With only switch1 expected, it named switch2 as unverified and gave the every-switch log rule error. Declaring the deployed Linux client2 as a target recorded that its platform cannot write a marker. Neither case was induced on the live lab (`04-sol-w4-offline.log`). |
| W5 | Fixed | Only actual marker records are excluded. Rejudging the previous saved log showed that a marker-only text cannot satisfy a required rule or trip a forbidden one. The same text can still match an actual device message (`engine-verdict-offline.console`). |

## Duplicates

| ID | Status | Decision and reason |
| --- | --- | --- |
| D1 | Fixed | Removed the client address and cable table. The topology and the client setup give those values. |
| D2 | Fixed | The README points to the test for its purpose, limits and log rules. |
| D3 | Fixed | The README links to the engine guide for the report format and shows a measured stop from the committed native Small run. |
| D4 | Fixed | Removed the file list and the repeated collector path. |
| D5 | Fixed | Plain YAML aliases share bridge parameters, bond members and expected values. Every physical member remains a distinct precondition in the saved lab file. |
| D6 | Fixed | Removed ten optional check names. Each check still records its device, check, parameters and expected result. |
| D7 | Fixed | The test is the sole source of the MLAG manual reference. |
| D8 | Fixed | Removed the comment repeating the collector field definition. The writer and reader each need their file path. |
| D9 | Fixed | The unaffected stream's limit is an alias and the LACP timeout is explained at its first use. |
| D10 | Fixed | Shortened expected outcomes and shared the return expectation. Explicit step names keep a saved test readable and replayable without the topology. |
| D11 | Fixed | Only one evidenced warning remains, so a list-valued rule would have no use in this test. |
| D12 | Rejected | Replay reads the saved test as `test.yaml`, so a name derived from its filename would change the marker text. |
| D13 | Rejected | Explicit inventory and deployed lab paths identify exactly which instances the operator selected, including deployments outside the test directory. |
| D14 | Fixed | YAML aliases share platform definitions. Explicit node and group membership keeps credential selection and switch coverage independent of runtime topology inference. |
| D15 | Fixed | The client group's required description no longer repeats the image's password comment. |
| D16 | Fixed | A single comment explains containerlab-to-RouterOS port numbering at the topology links. |
| D17 | Fixed | The earlier script discovered data veths and numbered taps. The qualified native launcher now configures those ports. All six bond members were eligible in the isolated trial (`native-chr/04-before-restart.log`). |
| D18 | Rejected | RouterOS and containerlab both need the collector address, Docker and containerlab need the same image tag, and each LACP endpoint sets the rate. |
| D19 | Fixed | The spec links to the startup config, test, topology and README and records the properties that those files must preserve. |
| D20 | Fixed | The engine guide links to the working lab and explains the quiet-window and marker requirements once. |

## Leftovers

| ID | Status | Decision and reason |
| --- | --- | --- |
| L1 | Fixed | The topology explains subnet isolation without referring to another suite. |
| L2 | Fixed | Replaced the unmeasured example with the first cable run on the committed native Small lab (`08-native-main-matrix.log`). |
| L3 | Fixed | Removed the fabricated example and defined the outage bounds from observed timestamps. |
| L4 | Fixed | The lab API's example uses the Small lab endpoint naming convention. |
| L5 | Rejected | `restore_errors` identifies a failed cleanup in saved runs. Renaming it would break readers of those events, and the report explains the failure in words. |
| L6 | Fixed | Current JSON names traffic stops `outages`. The reader keeps the older saved shape for historical replays. |
| L7 | Fixed | Current outage records include `not_sent` only when a sequence number was absent at the source. These are distinct from requests sent and lost. |
| L8 | Fixed | Both guide and code explain the 10% sender scheduling allowance and the one boundary ping. |
| L9 | Fixed | The sender pause limit is the late-reply allowance less half a ping interval, preserving the 450 ms validity limit. |
| L10 | Fixed | The engine guide explains the ping interval, quiet window, carrier and marker deadlines, late reply allowance, sender pause and wall-clock drift limits. |
| L11 | Fixed | The guide explains that a lost ping makes a stop longer than its lower bound, so equality at the limit fails. |
| L12 | Fixed | Polling intervals are derived from ping cadence where appropriate and the carrier poll documents its confirmation deadline. |
| L13 | Fixed | Ordinary namespace commands share the five-second local-process guard. QEMU monitor exchanges and offline capture decoding have separate deadlines. |
| L14 | Fixed | The link definition explains the one-port offset introduced by RouterOS management. |
| L15 | Fixed | Kept the collector at .10 and documented its RouterOS dependency. The two deployments received different dynamic addresses for the other nodes and both tests passed (`03-run-a.log`, `03-run-b-with-tag.log`). |
| L16 | Fixed | The startup configuration explains why the client VLAN must be tagged on the peer link and how its number was chosen. |
| L17 | Fixed | The switch configuration identifies the topics for port changes and markers and the severity rules that capture MLAG problems across topics. |
| L18 | Fixed | The native launcher discovers the data ports. The bridges had spanning tree off, which Linux uses to forward bridge-group BPDUs (`native-chr/04-before-restart.log`). |
| L19 | Fixed | The older audit reported dropped replies with learning enabled and cited no raw run for this Small lab. The native trial passed both cable runs and the reboot with normal bridge learning. The operator approved retiring the extra no-learning setting (`native-chr/10-sol-matrix-review.log`). |
| L20 | Fixed | The native launcher defaults the data ports to 10 Gbit/s full duplex, as measured on RouterOS. Its source includes both QEMU architectures. The ARM64 ports were checked live (`native-chr/03-source-and-runner.log`, `native-chr/04-before-restart.log`). |
| L21 | Fixed | The lab and test prose use the actual node names. |
| L22 | Fixed | Kept the observed RouterOS heartbeat warning. Neither the cited manual nor the saved raw logs supported the two sync-warning strings. |
| L23 | Fixed | The README links to the per-step reasons alongside their limits. |
| L24 | Fixed | The README identifies the host prerequisites, working directory, required uv version and Networka checkout. |

## Unneeded lines

| ID | Status | Decision and reason |
| --- | --- | --- |
| U1 | Fixed | Removed the legacy subnet reference. |
| U2 | Fixed | The switches still delivered port and marker messages on the default destination port (`03-run-a.log`). |
| U3 | Rejected | The pinned rsyslog rejects an imudp input without its port and restarts repeatedly. Restoring `port="514"` restores collection (`03-imudp-diagnostic.log`). |
| U4 | Fixed | Removed both explicit RouterOS format options after the default preserved switch name and topics. Kept the rsyslog tag because removing it lost topics and left the markers unproven (`03-run-a.log`, `03-run-b.log`). |
| U5 | Fixed | With the pinned collector image using its local timezone, the lines remained in UTC after removing the template override (`03-run-a.log`). |
| U6 | Fixed | Removed the extra mask. Native bridge ports pass LACP. Linux also forwards the bridge-group BPDU when host bridge STP is off, as in the trial. Direct BPDU capture was outside this trial (`native-chr/04-before-restart.log`). |
| U7 | Fixed | The client image starts sshd without sending its diagnostics to stderr. SSH state checks and the cable case passed (`03-run-a.log`). |
| U8 | Fixed | Removed both QEMU wrapper binds. The pinned launcher supplies the speed and duplex in both QEMU architecture paths. Only ARM64 execution was verified (`native-chr/03-source-and-runner.log`, `native-chr/04-before-restart.log`). |
| U9 | Fixed | Removed five static management addresses. The engine found all five devices from the current deployment in both passing runs (`03-run-a.log`, `03-run-b-with-tag.log`). |
| U10 | Fixed | Removed the duplicate README file list. |
| U11 | Fixed | Removed the table and the repeated limits. The topology explains the port names used in log rules. |
| U12 | Fixed | The README uses the saved native cable-return measurement, with its ping interval and bounds (`08-native-main-matrix.log`). |
| U13 | Fixed | The unaffected stream's limit and its reason occur once in the test. |
| U14 | Fixed | Removed both statement-level copies of the manual URL. |
| U15 | Fixed | Current result files keep each window and interval once. Legacy evidence uses the recorded representation for equality checks. |
| U16 | Rejected | `link_start` preserves the attempted cable action when an interrupt prevents the later `link_applied` event. |
| U17 | Fixed | The capture command keeps `LC_ALL=C` because the engine parses tcpdump's readiness and drop messages. Removed the timezone override. On the C.UTF-8 VM, tcpdump 4.99.5 started each capture and reported zero kernel drops. TShark 4.4.19 decoded the captures and replay matched (`03-locale-runtime.log`, `03-run-b-with-tag.log` and the run's capture logs). |
| U18 | Fixed | Local process and namespace commands use a common five-second timeout. Retained separate deadlines for QEMU/socket commands and offline tshark decoding. |
| U19 | Fixed | Removed the unused capture path and expose capture diagnostics on error. Retained sequences, pause and clock timestamps that locate failures or allow recomputation. |
| U20 | Rejected | Removing the documented multi-file CLI, interactive credentials, explicit hosts, log-free tests or ordinary Linux cables would break supported uses beyond the reference lab. |
| U21 | Fixed | The engine guide links to the working Small lab and keeps only a generic CLI invocation. |
