"""Decode root-pair packet and state evidence on the host clock."""

from collections import defaultdict
from datetime import datetime
import json
import re

from .evidence import capture_hashes, load_jsonl, packets
from .legacy import NS
from .measure import seconds, within
from .root_state import linux_members, router_members, router_state
from .root_topology import MANAGEMENT_PROBES, ROOT_FLOWS, ROOT_ID, ROOT_NODES

FRAME = ("icmp.ident", "icmp.type", "icmp.seq", "eth.src", "eth.dst", "eth.type", "vlan.id")
ARP = ("arp.opcode", "arp.src.proto_ipv4", "arp.dst.proto_ipv4")
LACP = ("lacp.actor.sysid", "lacp.actor.port", "lacp.actor.state",
        "lacp.partner.sysid", "lacp.partner.port", "lacp.partner.state")
STP = ("stp.version", "stp.type", "stp.flags", "stp.flags.port_role", "stp.root.prio", "stp.root.ext",
       "stp.root.hw", "stp.root.cost", "stp.bridge.prio", "stp.bridge.ext", "stp.bridge.hw",
       "stp.port", "stp.msg_age", "stp.max_age", "stp.hello", "stp.forward")
ROOT_FIELDS = ("frame.time_epoch", *FRAME, *LACP, *STP, *ARP)


def read_root_packets(path, captures, start, down, check, timeline, *, reference_root=True,
                      probes=MANAGEMENT_PROBES):
    manifest = (path / "pcap.sha256").read_text()
    if manifest != capture_hashes(path, captures):
        raise ValueError("PCAP hashes differ from saved manifest")
    icmp, frames, iccp = {}, defaultdict(list), defaultdict(list)
    root_legs = set()
    for cap in captures:
        data = defaultdict(list)
        icmp[cap] = data
        pcap = path / "captures" / f"{cap}.pcap"
        log = pcap.with_suffix(".log").read_text()
        check("error", re.search(r"^0 packets dropped by kernel$", log, re.M),
              f"{cap} captured with zero kernel drops")
        last_lacp = {}
        for stamp, row in packets(pcap, ROOT_FIELDS, "icmp || arp || lacp || stp || eth.type == 0x88b5"):
            fields = dict(zip(ROOT_FIELDS[1:], row, strict=True))
            ident = fields["icmp.ident"]
            if ident and int(ident) in ROOT_FLOWS:
                key = (int(ident), int(fields["icmp.type"]), int(fields["icmp.seq"]))
                data[key].append(stamp)
                frames[key].append({
                    "time_s": seconds(stamp - start), "point": cap,
                    "src": fields["eth.src"], "dst": fields["eth.dst"],
                    "tagged_vid": int(fields["vlan.id"]) if fields["vlan.id"] else None,
                })
            elif ident and int(ident) in probes.values():
                data[int(ident), int(fields["icmp.type"]), int(fields["icmp.seq"])].append(stamp)
            if fields["stp.version"]:
                bpdu = {field: fields[field] for field in (*STP, "eth.src")}
                timeline.append((stamp, f"bpdu-{cap}", json.dumps(bpdu, sort_keys=True)))
                if fields["stp.root.prio"] and fields["stp.root.ext"]:
                    priority = int(fields["stp.root.prio"], 0) + int(fields["stp.root.ext"], 0)
                    root = f"{priority:#06x}.{fields['stp.root.hw']}"
                    if (cap in ("witness-tap1", "witness-tap2") and within(stamp, start, down)
                            and fields["stp.version"] == "2" and root == ROOT_ID
                            and fields["stp.bridge.hw"] != "02:00:00:21:00:13"):
                        root_legs.add(cap)
            if actor := fields["lacp.actor.sysid"]:
                lacp = {field: fields[field] for field in (*LACP, "eth.src")}
                sender = fields["eth.src"], fields["lacp.actor.port"]
                if last_lacp.get(sender) != lacp:
                    timeline.append((stamp, f"lacp-{cap}", json.dumps(lacp, sort_keys=True)))
                    last_lacp[sender] = lacp
            if fields["eth.type"] == "0x88b5":
                iccp[cap, fields["eth.src"]].append(stamp)
                timeline.append((stamp, f"iccp-{cap}", f"{fields['eth.src']} -> {fields['eth.dst']}"))
            if fields["arp.opcode"]:
                arp = {field: fields[field] for field in (*ARP, "eth.src", "eth.dst", "vlan.id")}
                timeline.append((stamp, f"arp-{cap}", json.dumps(arp, sort_keys=True)))
    if reference_root:
        check("error", bool(root_legs), "Witness received RSTP BPDUs for the shared root before actuation")
    return icmp, frames, sorted(root_legs), iccp


def summarize_router(raw):
    bridge, ports = router_state(raw)
    carriers = dict(re.findall(r"^\s*name:\s*(ether\d+)\s*\n\s*status:\s*(\S+)", raw, re.M))
    hosts = [
        {"mac": mac.lower(), "vid": int(vid), "interface": interface, "on_interface": actual}
        for mac, vid, interface, actual in re.findall(
            r"mac-address=(02:00:00:11:00:(?:11|12)) vid=(\d+) interface=(\S+)"
            r"\s+bridge=\S+\s+on-interface=(\S+)", raw, re.I
        )
    ]
    return {"bridge": bridge, "ports": ports, "carrier": carriers,
            "lacp": router_members(raw), "fdb": hosts}


def read_root_state(path, start, end, target, check, timeline, *, nodes=None):
    nodes = nodes or dict.fromkeys(ROOT_NODES, 3)
    summary = {}
    for node in (*nodes, "host"):
        samples = load_jsonl(path / f"state-{node}.jsonl")
        usable, incomplete = [], []
        previous = None
        for sample in samples:
            raw = sample.get("raw")
            if raw is not None:
                if node == "host":
                    state = {"carrier": raw["links"], "lacp": linux_members(raw["bond"])}
                    if "virtual_cable_fdb" in raw:
                        state["virtual_cable_fdb"] = raw["virtual_cable_fdb"]
                    complete = all(node in raw["links"] for node in (*nodes, "c1", "c2"))
                else:
                    state = summarize_router(raw)
                    complete = bool(state["bridge"] and state["ports"] and len(state["carrier"]) == nodes[node]
                                    and re.search(r"^uptime-ns=\d+", raw, re.M))
            else:
                state = {"error": sample.get("stderr") or sample.get("error")}
                complete = False
            if state != previous:
                observed = {"query_start_s": seconds(sample["started_ns"] - start), **state}
                timeline.append((sample["done_ns"], node, json.dumps(observed, sort_keys=True)))
                previous = state
            if complete:
                usable.append(sample)
            else:
                incomplete.append(sample)
        cadence = [b["started_ns"] - a["started_ns"] for a, b in zip(usable, usable[1:])]
        summary[node] = {"complete": len(usable), "incomplete": len(incomplete),
                         "max_start_interval_s": seconds(max(cadence, default=0)),
                         "max_poll_duration_s": seconds(max(
                             (s["done_ns"] - s["started_ns"] for s in samples), default=0))}
        covered = bool(usable and usable[0]["started_ns"] <= start and usable[-1]["done_ns"] >= end)
        check("error", covered, f"{node} state samples cover both ends of the scoring window")
        if node != target:
            check("error", not incomplete and max(cadence, default=0) <= 1.5 * NS,
                  f"{node} independent observer had complete state at intervals within 1.5 s")
    return summary


def read_root_syslog(path, target, check, timeline, *, nodes=ROOT_NODES, label="mlag-root"):
    logs = load_jsonl(path / "syslog.jsonl")
    received = {}
    for phase in ("begin", "end"):
        marker = f"{label}-{path.name}-{phase}"
        sources = {log["source_ip"] for log in logs if marker in log["raw"]}
        expected = set(nodes.values())
        if target and phase == "end":
            expected.remove(nodes[target])
        check("error", expected <= sources, f"Management UDP syslog {phase} markers from required observers")
        received[phase] = sorted(sources)
    for log in logs:
        stamp = int(datetime.fromisoformat(log["received_at"]).timestamp() * NS)
        timeline.append((stamp, f"syslog-{log['source_ip']}", log["raw"]))
    if target:
        received["target_end_received"] = nodes[target] in received["end"]
        received["target_after_rebind_received"] = any(
            log["source_ip"] == nodes[target] and f"{label}-{path.name}-after-rebind" in log["raw"]
            for log in logs
        )
    return received
