# RouterOS syslog on the management network

The small lab topology runs both CHRs and their rsyslog receiver together. Each CHR imports the complete RouterOS startup file from Containerlab, including its remote logging rules. The rules send traditional BSD syslog over **UDP port 1514** using the `mgmt` VRF on `ether1`. The unprivileged port is internal to the lab management network, with no host port published. Containerlab waits for the UDP listener and writable log directory before it creates either CHR. [Deploy the small lab](../../labs/small/README.md#deploy) · [Containerlab dependencies](https://containerlab.dev/manual/nodes/#wait-for) · [RouterOS remote logging](https://manual.mikrotik.com/docs/diagnostics-monitoring-and-troubleshooting/log/)

| Device | Management address | Role |
| --- | --- | --- |
| CHR 1 | `172.30.215.11` | Syslog sender |
| CHR 2 | `172.30.215.12` | Syslog sender |
| `clab-mlag-small-dc1-syslog-collector` | `172.30.215.20:1514/udp` | Receiver on `mlag-small-mgmt` |

The small lab writes to `labs/small/logs/routeros.jsonl` on the Linux lab host. Its directory is bind-mounted, so stopping or recreating the receiver leaves that file on the host. Each row contains the collector's UTC receive timestamp, the source management IP and the original syslog message. The message retains the router identity, severity and RouterOS topics. [Topology](../../labs/small/small.clab.yml) · [RouterOS startup config](../../labs/small/small.rsc) · [rsyslog UDP input](https://docs.rsyslog.com/doc/configuration/modules/imudp.html)

The shared receiver config accepts senders from the small, root and external lab management subnets (`172.30.215.0/27`, `172.30.216.0/27` and `172.30.217.0/27`). A new device on one of those networks only needs to point its syslog sender at that lab's collector. Update the receiver's subnet filter when adding or changing a lab management subnet. [Receiver config](../../labs/shared/rsyslog.conf)

## Check collection

After both CHRs are healthy, look for an `mlag-lab-startup-config-ready` event from each management IP. The startup file generates those markers only after it adds the logging rules. The routine configuration forwards `info`, `warning`, `error` and `critical`, with exclusions to keep a combined-severity event from matching twice. Local RouterOS memory and console rules continue to operate.

**OrbStack verification, 24 November 2026.** A fresh deployment on RouterOS 7.26beta7 and rsyslog 8.2610.0 recorded the startup marker once from each peer. Both client bonds had two collecting and distributing members and both clients reached the mobile endpoint. The receiver ran as the deploying user with no host port mappings. Restarting just the receiver preserved the existing log and both peers appended a new marker without any RouterOS configuration changes.

The earlier live retrofit used the `172.30.214.0/27` network. Its receiver captured 18 UDP datagrams per CHR with zero kernel drops. The eight tagged events arrived once each, and the two debug markers sent outside the enabled window from each CHR were absent. Keep these sample records separate from the new topology’s startup markers. [Earlier log samples](verification.jsonl) · [Earlier RouterOS retrofit fragment](remote-logging.rsc)

## Collect a debug window

The measurement lab starts with three scoped debug rules. Keep `bridge,debug,!packet` for the MAC and MLAG events RouterOS emits, `stp,debug,!bridge,!packet` for spanning-tree changes, and `interface,debug,!bridge,!stp,!packet` for link events. The exclusions route each message through at most one rule. [MikroTik logging topics and matching rules](https://manual.mikrotik.com/docs/diagnostics-monitoring-and-troubleshooting/log/)

On RouterOS 7.26beta7, the topic parser accepted `bridge`, `stp`, `interface`, and `packet`. It rejected `mlag`, `iccp`, `lacp`, `bonding`, `ethernet`, `rstp`, and `switch`. Both peers have the three scoped debug rules enabled. Keep protocol-specific evidence in the state collector and capture files. [RouterOS bridge reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/) · [RouterOS member monitor](https://manual.mikrotik.com/docs/cli-reference/interface/bonding/monitor-slaves/)

| Question | Evidence to collect |
| --- | --- |
| Did MLAG change peer state, or did a MAC stay on the old egress? | Bridge debug, each peer’s bridge monitor and FDB, and the peer-link capture for ICCP and payload. |
| Did LACP expire, default or resume forwarding? | Member-monitor actor and partner flags, wire LACPDUs on the client legs, and payload on those same legs. |
| Did RSTP block a port, or did the virtual link lose carrier? | STP and interface debug, BPDUs and bridge-port roles, plus independent Linux and RouterOS link observations. |

```routeros
/system/logging/print detail where action="mlagLabSyslog"
```

Record the start and end on the collector host. Check a marker from both routers on either side of the run and export the matching section of the log. UDP provides delivery without acknowledgments, and RouterOS only forwards events it emits. Use packet captures and continuous per-member monitors for subsecond forwarding and LACP state transitions. [Member-failure evidence plan](../plans/member-failure-diagnosis.md)
