# Small MLAG lab and its bond member loss test

This folder holds one containerlab lab and one Networka lab test for it.
The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux clients, `client1` to `client3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

| Client | Address | Cable to switch1 | Cable to switch2 |
|---|---|---|---|
| client1 | 10.0.10.1 | eth1 to ether3 | eth2 to ether3 |
| client2 | 10.0.10.2 | eth1 to ether4 | eth2 to ether4 |
| client3 | 10.0.10.3 | eth1 to ether5 | eth2 to ether5 |

## Files

- `topology.clab.yml`: nodes, cables, images and management network.
- `switch.rsc`: start configuration of both switches.
- `client-setup.sh`, `client.Dockerfile`: the clients' bond and image.
- `chr-qemu.sh`, `chr-bridges.sh`: make LACP work on the CHR's virtual ports.
- `rsyslog.conf`: the collector, which writes `clab-small-mlag/syslog/switches.log`.
- `devices.yml`: Networka's device names, platforms and logins.
- `lab.yaml`: the streams, the state checks and the switch log file.
- `bond-member-loss.yaml`: the test.

## Commands

Run them as root in the lab VM from the repository root, with `NETWORKA` set to a Networka checkout.

```sh
sudo tests/small/start.sh
sudo env "PATH=$PATH" uv run --project "$NETWORKA" nw test run tests/small/bond-member-loss.yaml \
  --lab tests/small/clab-small-mlag --config tests/small/devices.yml --save test-results/small
sudo containerlab destroy -t tests/small/topology.clab.yml --cleanup
```

## What the test proves

Two streams send one ping every 100 ms: `client1-to-client2` and `client2-to-client3`, both through the switches.
The test first checks that MLAG is connected, spanning tree is off and every client cable is in its bond.
A 3 s quiet window follows, in which no ping may be lost.
Then client 1's cable to switch1 goes down and comes back, and then its cable to switch2 does the same.
Client 1's traffic may stop for up to 1 s when a cable goes down and up to 4 s when it comes back.
`client2-to-client3` may lose no ping.
The switch at the cable's end must log the port down and up, and no switch may log an MLAG sync or heartbeat warning.

## How to read the result

`nw test run` prints the verdict per step and stream, for example "24 pings lost at one ping every 100 ms, traffic stopped for 2.4 to 2.6 s".
The saved folder holds `result.json` with every check and rule, and `timeline.tsv` with every event and switch log line in time order.
`nw test replay` builds both again from the saved folder.
