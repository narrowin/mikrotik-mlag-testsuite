"""Read and verify the saved packet and management evidence."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import re
import subprocess

from .legacy import CAPTURES, CLIENT_MAC, FLOWS, MOBILE_MAC, NS
from .measure import seconds, within

FIELDS = (
    "frame.time_epoch", "icmp.ident", "icmp.type", "icmp.seq", "eth.src", "eth.dst",
    "arp.src.proto_ipv4", "arp.dst.proto_ipv4", "lacp.actor.sysid", "lacp.actor.state", "lacp.partner.state",
)


@dataclass
class PacketEvidence:
    icmp: dict
    lpdus: dict
    garps: dict
    mobile_unicast: dict
    client_icmp: dict


def capture_hashes(path, captures):
    checksums = []
    for cap in captures:
        pcap = path / "captures" / f"{cap}.pcap"
        with pcap.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        checksums.append(f"{digest}  captures/{pcap.name}\n")
    return "".join(checksums)


def seal_captures(path, captures=CAPTURES):
    with (path / "pcap.sha256").open("x") as manifest:
        manifest.write(capture_hashes(path, captures))


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def packets(path, fields=FIELDS, display_filter="icmp || arp || lacp"):
    args = ["tshark", "-n", "-r", str(path), "-Y", display_filter,
            "-T", "fields", "-E", "occurrence=f"]
    for field in fields:
        args.extend(("-e", field))
    for line in subprocess.check_output(args, text=True, stderr=subprocess.PIPE, timeout=25).splitlines():
        stamp, *fields = line.split("\t")
        yield int(Decimal(stamp) * NS), fields


def read_legacy_packets(path, check, timeline, captures=CAPTURES):
    manifest = (path / "pcap.sha256").read_text()
    icmp = {}
    lpdus = defaultdict(list)
    garps = defaultdict(list)
    mobile_unicast = defaultdict(list)
    client_icmp = defaultdict(list)
    for cap in captures:
        data = defaultdict(list)
        icmp[cap] = data
        pcap = path / "captures" / f"{cap}.pcap"
        log = pcap.with_suffix(".log").read_text()
        check("error", re.search(r"^0 packets dropped by kernel$", log, re.M), f"{cap} captured with zero kernel drops")
        actors = {}
        for stamp, (ident, kind, seq, src, dst, arp_src, arp_dst, actor, actor_state, partner_state) in packets(pcap):
            if ident and int(ident) in FLOWS:
                data[int(ident), int(kind), int(seq)].append(stamp)
                if dst == CLIENT_MAC:
                    client_icmp[cap].append(stamp)
            if dst == MOBILE_MAC:
                mobile_unicast[cap].append(stamp)
            if src == MOBILE_MAC and arp_src == arp_dst == "10.110.0.50":
                garps[cap].append(stamp)
                timeline.append((stamp, cap, "Mobile gratuitous ARP"))
            if actor:
                lpdus[cap].append((stamp, actor, int(actor_state, 0)))
                key = (actor_state, partner_state)
                if actors.get((src, actor)) != key:
                    timeline.append((stamp, cap, f"LACP {src} system={actor} actor={key[0]} partner={key[1]}"))
                    actors[src, actor] = key
    check("error", manifest == capture_hashes(path, captures), "PCAP hashes match the saved manifest")
    return PacketEvidence(icmp, lpdus, garps, mobile_unicast, client_icmp)


def read_legacy_state(path, name, marks, start, down, up, check, timeline):

    link_events = defaultdict(list)
    for path_link in sorted((path / "links").glob("*.txt")):
        for line in path_link.read_text().splitlines():
            if match := re.match(r"^\[([^]]+)\]\s*(.*)$", line):
                stamp = int(datetime.fromisoformat(match[1] + "+00:00").timestamp() * NS)
                timeline.append((stamp, f"link-{path_link.stem}", match[2]))
                if flags := re.search(r"<([^>]+)>", match[2]):
                    link_events[path_link.stem].append((stamp, set(flags[1].split(","))))
    manifest = path / "attempt.json"
    mode = json.loads(manifest.read_text()).get("bridge_mode", "rstp") if manifest.exists() else "rstp"
    # With protocol-mode=none the bridge monitor prints no root bridge or topology-change fields.
    required = ("status:", "partner-flags=", "mlag-state:", "forwarding:", "mac-address=") + (
        () if mode == "none" else ("root-bridge-id:", "topology-changes:"))
    for peer in ("p1", "p2"):
        samples = load_jsonl(path / f"state-{peer}.jsonl")
        previous = None
        complete = []
        for sample in samples:
            raw = sample.get("raw", "")
            if all(field in raw for field in required):
                complete.append(sample["started_ns"])
                fields = tuple(line.strip() for line in raw.splitlines()
                               if re.search(r"(status:|port=ether|partner-flags=|^\s*role:|mlag-state:|"
                                            r"root-bridge-id:|topology-changes:|forwarding:|on-interface=)", line))
                if fields != previous:
                    timeline.append((sample["done_ns"], peer,
                                     f"query start +{seconds(sample['started_ns'] - start)} s | " + " | ".join(fields)))
                    previous = fields
        cadence = [b - a for a, b in zip(complete, complete[1:])]
        check("error", len(complete) == len(samples) and len(complete) >= 8
              and max(cadence, default=0) <= 1.5 * NS, f"{peer} complete state samples no more than 1.5 s apart")
        if name == "silent-lacp" and peer == "p1":
            during = [s for s in samples if within(s["started_ns"], down, up)]
            check("error", bool(during) and all("status: link-ok" in s.get("raw", "") for s in during),
                  "p1 guest carrier stayed up during LACP suppression")

    logs = load_jsonl(path / "syslog.jsonl")
    for phase in ("begin", "end"):
        marker = f"mlag-suite-{path.name}-{phase}"
        sources = {log["source_ip"] for log in logs if marker in log["raw"]}
        check("error", sources == {"172.30.215.11", "172.30.215.12"}, f"Syslog {phase} markers from both peers")
    for log in logs:
        stamp = int(datetime.fromisoformat(log["received_at"]).timestamp() * NS)
        timeline.append((stamp, f"syslog-{log['source_ip']}", log["raw"]))
    return link_events
