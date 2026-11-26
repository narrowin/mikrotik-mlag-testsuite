# Clean reference setup for Networka lab tests

This is the one document the builders work from: the Small MLAG lab and its bond member loss test, built fresh for Networka.
The live run must prove every point marked "prove live". New files name no file of the old suite, not even as a source.

## 1. Folder

Everything lives in `tests/small/`, and today's files there are replaced, because one folder that stands on its own is the rule.
The repository `.gitignore` gets `tests/*/clab-*/`, because containerlab writes its lab folder next to the topology.

| File | What it holds |
|---|---|
| `topology.clab.yml` | Nodes, cables, images, management network and the binds of the scripts and the collector. |
| `switch.rsc` | Start configuration of both switches, identical because their ports are identical. |
| `client-setup.sh` | Bond, MAC and address of a client, taken from its host name. |
| `client.Dockerfile` | Client image with iproute2 and sshd on a pinned Alpine base. |
| `chr-qemu.sh` | Wrapper that gives the CHR's virtual ports 10G full duplex. |
| `chr-bridges.sh` | Passes LACP and STP frames and turns learning off on the small bridges in a CHR node. |
| `rsyslog.conf` | Collector configuration: one input, one file, one line format. |
| `devices.yml` | Networka device list: names, platforms and credentials, no addresses. |
| `start.sh` | Builds the client image and deploys the lab. |
| `lab.yaml` | Lab file: streams, state checks and the switch log file. |
| `bond-member-loss.yaml` | Test file: four steps, limits and log rules. |
| `README.md` | One page: the lab, the test, the three commands and the result of the live run. |

## 2. Lab

- Lab name `small-mlag`, management network `small-mlag-mgmt` on `172.30.100.0/24`, because the VM already uses 172.17.0.0/16, 172.30.218.0/27 and 172.30.225.0/27, and the old labs keep to 172.30.192.0/18.
- Management addresses are fixed: syslog .10, switch1 .11, switch2 .12, client1 .21, client2 .22, client3 .23, because the switches need a known collector address and fixed addresses keep docker from giving it to another node.
- `switch1` and `switch2` are the CHR MLAG peers on the pinned image `mikrotik/chr:7.26beta7@sha256:b68f34a50544f6464d592cdd07ecc1d08017d6ec6837ac42b7dbe701d3c1ca6a`, the campaign RouterOS.
- `client1`, `client2` and `client3` are Linux clients built the same way, each with one cable to each switch and an LACP bond. Three are needed, because a stream that does not involve client 1 needs two other clients.
- `syslog` is the collector on `rsyslog/rsyslog@sha256:cac80b5513d78de76c301151e4d248547bcf2b5161d9c891a4b10c302f76dd56`, the digest the Medium lab runs today.
- Cables: `switch1:eth1` to `switch2:eth1` is the peer link. `clientN:eth1` goes to `switch1:eth(N+1)` and `clientN:eth2` to `switch2:eth(N+1)`. A CHR's ethN is RouterOS ether(N+1), because ether1 is management, so the peer link is ether2 and clients 1 to 3 are on ether3 to ether5.
- Client N has `10.0.10.N/24` and bond MAC `02:00:00:00:00:0N` on `bond0`. The fixed MAC makes the bond pick the same cable in every run, because containerlab gives veths random MACs.
- `bond0` is `mode 802.3ad miimon 100 lacp_rate fast`. Without the 100 ms link check a client keeps sending on a cut cable, and the fast rate matches the switches. The hash policy stays at its default, because the fixed MACs already decide the cable.
- The client image sets the root password `admin` that devices.yml uses, because the switches' default login is admin with password admin and one password then serves every node.
- One VLAN, 10, is used, because the MLAG manual carries the client VLANs tagged on the peer port, and 10 equals the third octet of the client subnet.
- The client `exec` and binds sit once in a `clients` group, and the switch scripts once in the `mikrotik_chr` kind. The clients wait at stage `create` for both switches to be `healthy`, so the deploy returns only when the switches answer.
- The collector binds `__clabNodeDir__` to `/logs`, so the lab host reads `clab-small-mlag/syslog/switches.log` (prove live). Each line holds the receive time in UTC RFC 3339 with microseconds, the sender's host name, which containerlab sets to the node name, and the topics and text.
- Left out: the client-to-client cable, pinned neighbour entries, frame type filters, bridge priority, edge, path costs, the collector health check and the switches' wait for it.

## 3. Switch start configuration (`switch.rsc`)

```
/interface bonding add name=client1 mode=802.3ad mlag-id=1 slaves=ether3 lacp-rate=1sec
/interface bonding add name=client2 mode=802.3ad mlag-id=2 slaves=ether4 lacp-rate=1sec
/interface bonding add name=client3 mode=802.3ad mlag-id=3 slaves=ether5 lacp-rate=1sec
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=client1 pvid=10
/interface bridge port add bridge=bridge interface=client2 pvid=10
/interface bridge port add bridge=bridge interface=client3 pvid=10
/interface bridge vlan add bridge=bridge tagged=ether2 vlan-ids=10
/system logging action add name=collector target=remote remote=172.30.100.10 remote-port=514 vrf=mgmt
/system logging add action=collector topics=interface
/system logging add action=collector topics=script
/system logging add action=collector topics=warning
/system logging add action=collector topics=error
/system logging add action=collector topics=critical
```

- The mlag-id is the client number, because both switches must give a client's bond the same ID. `lacp-rate=1sec` makes a returning cable join within seconds instead of 30 to 90 s at the slow rate.
- `protocol-mode=none` from boot is the STP-off state, so no manual step exists (prove live). The pvid ports join VLAN 10 untagged by themselves, so the VLAN entry names only the peer port (prove live).
- `vrf=mgmt` sends from the management port, which the CHR kind puts in that VRF (prove live).
- `interface` carries the port link lines that the log rules read. `script` carries the engine's markers, which `:log info` writes with that topic.
- `warning`, `error` and `critical` carry MLAG problems, whose topic no source names, so the severity topics catch them.
- The collector address is the one fact written twice, here and in the topology, because RouterOS needs a literal address and containerlab fills no values into a start configuration.

## 4. CHR workarounds until containerlab fixes them

- `chr-qemu.sh` adds `speed=10000,duplex=full` to each virtio-net NIC, because without it the Linux bonds never formed a two-member aggregate.
- `chr-bridges.sh` sets `group_fwd_mask` to 5 (STP and LACP) and `learning` to 0 on eth1 to eth4 and tap1 to tap4, because a Linux bridge drops LACP frames and a learning two-port bridge drops replies in this failover. STP frames pass so that a switch that sends BPDUs by mistake shows it at its peer. LLDP no longer passes, because no check reads it. The script waits up to 60 s for each tap, because QEMU creates them within seconds.

## 5. Lab file and test file

`lab.yaml` fields: `streams`, `state`, `switch_log`.

- `streams`: each has `name`, `from` and `to` as node:interface. The engine assigns the ICMP identifier and pings the IPv4 address of the `to` interface.
- `client1-to-client2`: from `client1:bond0` to `client2:bond0`. Pings leave client 1 on the cable its bond chose, cross switch1 or switch2 and the peer link when needed, and reach client 2. Replies take the way back into client 1. It proves client 1's traffic recovers in both directions. No third stream is needed, because this reply already enters client 1 over each cable in turn.
- `client2-to-client3`: from `client2:bond0` to `client3:bond0`, through the switches in both directions. It proves traffic that does not involve client 1 is not disturbed.
- `state`: statements with `statement`, `source` and `checks`, run before the first step and after the last step.
- `mlag` connected on switch1 and switch2, because it is the precondition of every MLAG fault. `stp_mode` none on both, because the test claims spanning tree off.
- `bond_member` eligible for eth1 and eth2 of each client (six checks), because it proves both switches present one LACP system to that client.
- Dropped as redundant: bond member lists, bridge port forwarding, LACP member checks on the switches and the carrier field.
- `switch_log: syslog/switches.log`, the collector file inside the containerlab lab folder. No `captures` field, because no rule needs more than the engine's own captures.

`bond-member-loss.yaml` fields: `name`, `purpose`, `source`, `lab`, `log`, `steps`.

- Each step has `name`, `cable` (one end as node:interface), `state` (down or up), `hold_s`, `max_outage_s` (stream name to seconds), `expected` and an optional `log`.
- A `log` holds `must` and `must_not`, each a list of `switch` (a name or `every`) and `text`. `text` matches part of a line ignoring case, because the source texts are lower case.
- A step's rules apply from its start to its end. The test's rules apply from the start marker to the end marker.

| Step | cable, state | hold_s | client1-to-client2 | client2-to-client3 | log must |
|---|---|---|---|---|---|
| Cable client1 to switch1 down | client1:eth1 down | 5 | 1 | 0 | switch1 `ether3 link down` |
| Cable client1 to switch1 back | client1:eth1 up | 7 | 4 | 0 | switch1 `ether3 link up` |
| Cable client1 to switch2 down | client1:eth2 down | 5 | 1 | 0 | switch2 `ether3 link down` |
| Cable client1 to switch2 back | client1:eth2 up | 7 | 4 | 0 | switch2 `ether3 link up` |

- The port texts come from real lines of this fault on these switches (results/2026-11-24-small-lab/reports/01-carrier/timeline.tsv).
- Test `log.must_not` for `every` switch: `failed to sync`, `attempting to resync`, `heartbeat timeout`, the MLAG warnings that src/mlag_lab/forwarding_checks.py looks for. The test file cites the MLAG manual as its source and names no file. No rule covers a bond member's LACP state or the bond's own link line, because the port line already proves the switch saw the fault.

## 6. Numbers

- Ping interval 100 ms: an outage is resolved to 0.1 s, which is ten times finer than the smallest limit. Unchanged.
- Quiet window 3 s, starting at the first reply of every stream: three LACP messages at the fast rate, so a bond still settling loses pings here and not in a step. Was 5 s after a 2 s wait.
- Limit down 1 s: both ends see the carrier loss within one 100 ms link check, and an LACP timeout of 3 s would exceed it. Was 3 s. Hold down 5 s: longer than the 3 s LACP timeout, so a loss from a late timeout falls inside the step. Was 8 s.
- Limit back 4 s: a cable joins after up to three LACP messages at one per second, and 1 s more covers one late message. Was 3 s, which left 0.08 s of margin. Hold back 7 s: the 4 s limit plus one 3 s LACP timeout, so a slow return ends inside the step and is measured. Was 11 s.
- Limit 0 s on `client2-to-client3`: it crosses no failing cable, so it may lose no ping.

## 7. Engine changes in Networka

1. Streams have `name` only, the engine numbers ICMP identifiers in file order, and logs are `streams/<name>.log`. `id`, `address`, `interval_ms` and the interval read-back go, and one 100 ms constant stays.
2. Quiet window replaces the baseline: no 2 s wait, start at the first reply of every stream, 3 s, no lost and no duplicate ping, the count derived from window and interval, one rule from the captures, used live and in replay. The word is "ping" in code, output, result.json and docs.
3. Every lost count carries the interval and the time: `24 pings lost at one ping every 100 ms, traffic stopped for 2.4 to 2.6 s`, in `nw test run`, `nw test replay`, result.json and timeline.tsv.
4. A gap counts in every step it overlaps, with one rule for lost count and outage. A 0 s limit means no lost and no late ping, stated once in code and docs.
5. Captures: both ends of each stream and of each action cable. The `captures` field goes. Cable captures are diagnostics that cannot change validity.
6. tcpdump runs with `-U --immediate-mode` only, all captures start before one wait, one drop parser also reads "1 packet dropped", tshark runs without a cache, and pcap.sha256 goes.
7. A cable change confirms carrier at the far end only, within 1 s, because a veth changes carrier within milliseconds. The 2 s settle becomes the late reply limit of 500 ms plus one interval, so the last pings can still be answered. Every engine constant gets its reason in one sentence or is derived from the interval.
8. Device addresses come from topology-data.json of `--lab`, so devices.yml holds none.
9. Switch logs: the RouterOS platform module offers `log_marker(text)`, which runs `:log info "<text>"`. At the start the engine notes the size of `switch_log` and writes `networka <test> start` on every RouterOS device. After the last step it writes `networka <test> end`, waits up to 1 s for both markers, because UDP on the management bridge arrives within milliseconds, and copies the added lines to `syslog.log`. A missing marker or file makes the verdict error. result.json lists log lines per switch, not judged.
10. Log rules: `must` and `must_not` per step and per test, judged from syslog.log in run and replay. A broken rule fails the step, and result.json shows each rule with its matching lines.
11. timeline.tsv is rebuilt by `nw test replay`. Columns are seconds from the start of the quiet window, what, and a detail in words, for example `cable client1:eth1 down at both ends`. Syslog lines appear as `switch1 log` with their text. No JSON.
12. Evidence folder: test.yaml, lab.yaml, state-before, state-after, captures, streams, events.jsonl, syslog.log, result.json, timeline.tsv.

## 8. Commands

- Start the lab: `sudo tests/small/start.sh`.
- Run the test: `sudo env "PATH=$PATH" uv run --project "$NETWORKA" nw test run tests/small/bond-member-loss.yaml --lab tests/small/clab-small-mlag --config tests/small/devices.yml --save test-results/small`.
- Remove the lab: `sudo containerlab destroy -t tests/small/topology.clab.yml --cleanup`.
