"""Run repeatable faults against the deployed mlag-small topology."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
from threading import Event
import time
from datetime import datetime, timezone

from network_toolkit import InteractiveCredentials, NetworkaClient, NetworkToolkitError

from .cases import FLAP_CYCLES, FLAP_DOWN_S, FLAP_UP_S, MAC_AGE_DEFAULT, MAC_AGE_RETURN_S, MAC_AGE_SILENCE_S, MAC_AGE_TIME
from .cases import case_spec
from .direct_topology import DIRECT_CASES, DIRECT_NODES as PEERS
from .evaluate import analyze
from .proof import keep_proof
from .qmp import QMP_PORT
from .evidence import seal_captures
from .external_topology import EXTERNAL_CASES
from .legacy import CASES, CAPTURES, FLOWS, PEER_LINK_PORTS, case_captures, case_name
from .legacy import FLOOD_FLOWS, FLOOD_NEIGHBOUR
from .legacy import CLIENT_MAC, MOBILE_MAC
from .networka import INSTANCE, PROFILES, lab_name, reads, shift
from .report import write_suite
from .root_state import uptime
from .root_topology import MEDIUM_TARGETS, ROOT_CASES
from .small_06 import SMALL_06_PATH
from .two_pair_topology import TWO_PAIR_TARGETS

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LAB_FOLDERS = {"small": "small", "medium": "medium", "medium-pair-root": "medium", "medium-two-pair": "medium"}
PORTS = {"p1": "eth2", "c1": "eth1"}
UV = os.environ.get("UV", "uv")
HOST_TOOLS = (UV, "docker", "nsenter", "ip", "tc", "ping", "tcpdump", "tshark", "ssh", "containerlab")
BRIDGE_MODES = ("rstp", "none", "mstp")
STATE = ";".join(reads("mlag_small_state"))
# The peer-link case also polls the peer port and each MLAG bond's LACP system ID.
PEER_LINK_STATE = ";".join((
    STATE,
    "/interface/ethernet/monitor ether2 once",
    "/interface/bonding/monitor client1 once",
    "/interface/bonding/monitor client2 once",
))
# The repeated member flap also polls client 2's bridge host table entry on both MLAG peers.
FLAP_STATE = ";".join((
    STATE,
    "/interface/bridge/host/print detail without-paging where mac-address=02:00:00:11:00:12",
))
# Permanent neighbour entries for the MAC-move host's silence, so no host falls back to ARP while it lasts.
PINNED_NEIGHBOURS = (("c1", "10.110.0.50", MOBILE_MAC), ("c2", "10.110.0.50", MOBILE_MAC),
                     ("mobile", "10.110.0.11", CLIENT_MAC), ("mobile", "10.110.0.12", "02:00:00:11:00:12"))
# Three 5 s mlag-heartbeat intervals, the manual's threshold for reporting missed heartbeats.
PEER_LINK_HOLD_S = 15
# mlag-init-delay (default 1 min) bounds how long MLAG bond members stay out of the bond on rejoin.
# Add 3 s for the LACP timeout at lacp-rate=1sec and 2 s margin.
PEER_LINK_RECOVERY_S = 65
UPTIME = ':put ("uptime-ns=" . [:tonsec [/system resource get uptime]])'
CONFIG = ";".join((
    "/interface bridge print detail without-paging",
    "/interface bridge port print detail without-paging",
    "/interface bridge vlan print detail without-paging",
    "/interface bridge msti print detail without-paging",
    "/interface bonding print detail without-paging",
    "/system logging action print detail without-paging where name=mlagLabSyslog",
    ':put ("peer-link-mac=" . [/interface ethernet get ether2 mac-address])',
))
SET_BRIDGE = "/interface bridge set bridge "


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, timeout=12, check=True, **kwargs).stdout


class Lab:
    name = lab_name("mlag-small")
    nodes = ("p1", "p2", "c1", "c2", "mobile", "syslog")
    peers = PEERS
    bridge_mode = "rstp"
    device_names = {
        "p1": "dc1-core-mlag1",
        "p2": "dc1-core-mlag2",
        "c1": "dc1-traffic-host1",
        "c2": "dc1-traffic-host2",
        "mobile": "dc1-mac-move-host",
        "syslog": "dc1-syslog-collector",
    }

    def __init__(self, topology, runtime, username, password):
        self.topology = topology
        self.runtime = runtime
        self.profile = PROFILES / f"{topology.name.removesuffix('.clab.yml')}.yml"
        self.credentials = InteractiveCredentials(username, password)
        self.client = self.networka()
        self.containers = {}
        inspections = json.loads(run(["docker", "inspect", *[self.container_name(n) for n in self.nodes]]))
        for node, cfg in zip(self.nodes, inspections, strict=True):
            labels = cfg["Config"]["Labels"]
            device = self.device_name(node)
            if (labels.get("containerlab") != self.name or labels.get("clab-node-name") != device
                    or Path(labels.get("clab-topo-file", "")).resolve() != topology):
                raise RuntimeError(f"{device} is outside the selected Containerlab deployment")
            address = cfg["NetworkSettings"]["Networks"][f"{self.name}-mgmt"]["IPAddress"]
            if node in self.peers and address != self.peers[node]:
                raise RuntimeError(f"{device} has an unexpected management address")
            self.containers[node] = cfg
        self.validate_links()

    def networka(self):
        """A Networka client for the lab's profile at this instance's addresses, with strict host key checking off."""
        client = NetworkaClient(self.profile)
        client.config.general.ssh_strict_host_key_checking = False
        for device in client.devices.values():
            device.host = shift(device.host)
        return client

    def device_name(self, node):
        return self.device_names.get(node, node)

    def container_name(self, node):
        return f"clab-{self.name}-{self.device_name(node)}"

    def verify_veth(self, a, b):
        left, right = self.link(*a), self.link(*b)
        if left.get("link_index") != right["ifindex"] or right.get("link_index") != left["ifindex"]:
            raise RuntimeError(f"Expected {a} and {b} to be opposite veth endpoints")

    def validate_links(self):
        self.verify_veth(("p1", "eth2"), ("c1", "eth1"))
        self.verify_veth(("p1", "eth1"), ("p2", "eth1"))
        # The carrier case cuts NIC 2 (ether3) on p1; the peer-link case cuts NIC 1 (ether2) on both peers.
        for peer, nics in (("p1", (1, 2)), ("p2", (1,))):
            self.verify_qemu(peer, nics)

    def verify_qemu(self, peer, nics=()):
        """Confirm the QMP socket and that QEMU NIC N drives tapN, so a QMP link change hits the intended cable."""
        pid = self.containers[peer]["State"]["Pid"]
        procs = run(["docker", "exec", self.container_name(peer), "ps", "-o", "args"])
        if not any("qemu-system-" in line and f"127.0.0.1:{QMP_PORT}" in line
                   and all(f"id=nic{nic},netdev=d{nic}" in line and f"id=d{nic},ifname=tap{nic}" in line
                           for nic in nics)
                   for line in procs.splitlines()):
            raise RuntimeError(f"QEMU TAP/NIC or socket layout changed on {peer} (PID {pid})")

    def ns(self, node, *command):
        return ["nsenter", "-t", str(self.containers[node]["State"]["Pid"]), "-n", *command]

    def link(self, node, port):
        return json.loads(run(self.ns(node, "ip", "-j", "-d", "link", "show", "dev", port)))[0]

    def ros(self, peer, command):
        return self.ros_peers(command, (peer,))[peer]

    def ros_peers(self, command, peers=None, client=None):
        """Send one command line to each CHR, all CHRs of a group in one Networka run, and return each reply."""
        peers = peers or tuple(self.peers)
        devices = {self.device_name(peer): peer for peer in peers}
        try:
            results = (client or self.client).run(",".join(devices), command,
                                                  interactive_creds=self.credentials).command_results
        except NetworkToolkitError as error:
            raise RuntimeError(f"{', '.join(peers)}: {error.message}") from error
        replies = {devices[result.device]: result for result in results}
        for peer in peers:
            if peer not in replies or replies[peer].error:
                error = replies[peer].error if peer in replies else "no result"
                raise RuntimeError(f"{peer}: {command} failed: {error}")
        return {peer: replies[peer].output for peer in peers}

    def check_logins(self, timeout=30):
        """Log in afresh to every CHR with the lab credential: a lasting session would hide a rejected password."""
        with self.networka() as fresh:
            for peer in self.peers:
                deadline = time.monotonic() + timeout
                while True:
                    try:
                        if "login-ok" in self.ros_peers(":put login-ok", (peer,), fresh)[peer]:
                            break
                        error = "no login-ok reply"
                    except RuntimeError as failure:
                        error = str(failure)
                    if time.monotonic() >= deadline:
                        raise RuntimeError(f"{peer} did not accept a fresh lab SSH login within {timeout} s: {error}")
                    time.sleep(2)

    def wait_ready(self):
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            try:
                for peer in PEERS:
                    result = self.ros(peer, STATE)
                    if ("mlag-state: connected" not in result
                            or result.count(' flags="ATGSCD--"') < 2
                            or result.count('partner-flags="ATGSCD--"') < 2):
                        raise RuntimeError(f"{peer} MLAG or LACP still settling")
                if "LOWER_UP" in self.link("c1", "eth1")["flags"]:
                    return
            except (RuntimeError, subprocess.SubprocessError):
                pass
            time.sleep(1)
        raise RuntimeError("Both peers did not reach connected MLAG and active LACP within 90 s")

    def close(self):
        self.client.close()

    def snapshot(self, peer, command=STATE):
        start = time.time_ns()
        raw = self.ros(peer, command)
        return {"peer": peer, "started_ns": start, "done_ns": time.time_ns(), "raw": raw}

    def qmp(self, up):
        return self.qmp_action("p1", "up" if up else "down")

    def qmp_action(self, target, action, nic=None):
        command = self.ns(target, UV, "run", "--no-sync", "--project", str(PROJECT),
                          "python", "-m", "mlag_lab.qmp", "_qmp", action, *((nic,) if nic else ()))
        return json.loads(run(command))

    def reset_bridges(self, settings, extra=None):
        """Set each bridge while all bridges are disabled; extra adds per-node commands to the same step."""
        started_ns = time.monotonic_ns()
        def execute(commands):
            with ThreadPoolExecutor(max_workers=len(commands)) as workers:
                pending = {node: workers.submit(self.ros, node, command) for node, command in commands.items()}
                replies = {node: job.result() for node, job in pending.items()}
            for node, reply in replies.items():
                if re.search(r"failure:|syntax error|expected end|does not match", reply, re.I):
                    raise RuntimeError(f"{node}: {commands[node]} returned {reply.strip()}")
            return replies

        read_uptime = dict.fromkeys(self.peers, UPTIME)
        before = {node: uptime(raw) for node, raw in execute(read_uptime).items()}
        try:
            execute(dict.fromkeys(self.peers, "/interface bridge disable bridge"))
            commands = {node: SET_BRIDGE + setting + (f";{extra[node]}" if extra and node in extra else "")
                        for node, setting in settings.items()}
            replies = execute(commands)
            time.sleep(2)
        finally:
            execute(dict.fromkeys(self.peers, "/interface bridge enable bridge"))
        after = {node: uptime(raw) for node, raw in execute(read_uptime).items()}
        if any(before[node] is None or after[node] is None or after[node] <= before[node] for node in self.peers):
            raise RuntimeError(f"Management reset did not prove continuous guest uptime: {before}, {after}")
        return {
            "settings": settings, "replies": replies, "uptime_before_ns": before, "uptime_after_ns": after,
            "started_mono_ns": started_ns, "completed_mono_ns": time.monotonic_ns(),
        }

    def apply_bridge_mode(self, mode):
        """Reset both small-lab bridges to one protocol-mode and read the running value back."""
        reset = self.reset_bridges(dict.fromkeys(self.peers, f"protocol-mode={mode}"))
        readback = {}
        for peer in self.peers:
            raw = self.ros(peer, "/interface bridge print detail without-paging where name=bridge")
            match = re.search(r"\bprotocol-mode=(\w+)", raw)
            readback[peer] = match[1] if match else None
        if any(value != mode for value in readback.values()):
            raise RuntimeError(f"Bridges did not read back protocol-mode={mode}: {readback}")
        return {"bridge_mode": mode, **reset, "readback": readback}

    def versions(self):
        return {
            "platform": os.uname().machine,
            "containerlab": run(["containerlab", "version"]).strip(),
            "tshark": run(["tshark", "--version"]).splitlines()[0],
            "images": {node: {"reference": cfg["Config"]["Image"], "id": cfg["Image"]}
                       for node, cfg in self.containers.items()},
            "routeros": self.ros_peers("/system/resource/print"),
        }


class Capture:
    def __init__(self, lab, path):
        self.lab, self.path = lab, path
        self.processes = []
        self.start_clock = (time.time_ns(), time.monotonic_ns())
        for subdir in ("captures", "probes", "links"):
            (path / subdir).mkdir()

    def mark(self, name, **data):
        event = {"name": name, "epoch_ns": time.time_ns(), "mono_ns": time.monotonic_ns(), **data}
        with (self.path / "events.jsonl").open("a") as file:
            file.write(json.dumps(event) + "\n")
        return event

    def launch(self, command, log):
        with log.open("wb") as stream:
            child = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True,
                                     env={**os.environ, "LC_ALL": "C", "TZ": "UTC"})
        self.processes.append((child, log))
        return child

    def observe(self, captures=CAPTURES, links=tuple(PORTS.items()), flows=FLOWS, *, named_ports=False,
                immediate=False):
        capture_mode = ("--immediate-mode",) if immediate else ()
        for point in captures:
            node, port = point.split("-", 1)
            pcap = self.path / "captures" / f"{point}.pcap"
            self.launch(self.lab.ns(node, "tcpdump", "-n", "-U", *capture_mode, "-s", "0", "-B", "4096", "-Z", "root",
                                    "-i", port, "-w", str(pcap)), pcap.with_suffix(".log"))
        deadline = time.monotonic() + 5
        while any("listening on" not in log.read_text() for _, log in self.processes):
            if time.monotonic() > deadline or any(child.poll() is not None for child, _ in self.processes):
                raise RuntimeError("One or more packet captures did not start. See captures/*.log")
            time.sleep(0.05)
        for node, port in links:
            label = f"{node}-{port}" if named_ports else node
            self.launch(self.lab.ns(node, "ip", "-ts", "monitor", "link", "dev", port),
                        self.path / "links" / f"{label}.txt")
        for ident, (source, _, dest, _) in flows.items():
            node, port = source.split("-", 1)
            self.launch(self.lab.ns(node, "ping", "-n", "-D", "-O", "-i", "0.1", "-e", str(ident),
                                   "-I", port, dest), self.path / "probes" / f"{ident}.log")

    def stop(self):
        early_exits = [log.name for child, log in self.processes if child.poll() is not None]
        for child, _ in self.processes:
            if child.poll() is None:
                child.send_signal(signal.SIGINT)
        for child, _ in self.processes:
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
        epoch, mono = self.start_clock
        self.mark("collectors_stopped", early_exits=early_exits,
                  clock_delta_ns=(time.time_ns() - epoch) - (time.monotonic_ns() - mono))


def poll_peer(lab, peer, path, stop, command=STATE):
    with path.open("w", buffering=1) as file:
        while not stop.is_set():
            start = time.monotonic()
            try:
                sample = lab.snapshot(peer, command)
            except (RuntimeError, subprocess.SubprocessError) as error:
                sample = {"peer": peer, "started_ns": time.time_ns(), "error": str(error)}
            file.write(json.dumps(sample) + "\n")
            stop.wait(max(0.0, 0.35 - (time.monotonic() - start)))


def sample_loop(reader, path, stop, queue=None, period=0.35):
    with path.open("w", buffering=1) as file:
        while not stop.is_set():
            started = time.time_ns()
            tick = time.monotonic()
            try:
                observation = {"raw": reader()}
            except (RuntimeError, OSError, subprocess.SubprocessError) as error:
                observation = {"error": str(error), "stderr": getattr(error, "stderr", None)}
            sample = {"started_ns": started, "done_ns": time.time_ns(), **observation}
            file.write(json.dumps(sample) + "\n")
            if queue is not None:
                queue.put(sample)
            stop.wait(max(0, period - (time.monotonic() - tick)))


def carrier(capture, up):
    lab = capture.lab
    phase = "up" if up else "down"
    start = capture.mark(f"{phase}_start")
    with ThreadPoolExecutor(max_workers=2) as jobs:
        linux = jobs.submit(run, lab.ns("p1", "ip", "link", "set", "dev", "eth2", phase))
        guest = jobs.submit(lab.qmp, up)
        linux.result()
        qmp = guest.result()
    capture.mark(f"{phase}_applied", qmp=qmp)
    hits = {}
    deadline = time.monotonic() + 2
    while len(hits) < 2 and time.monotonic() < deadline:
        with ThreadPoolExecutor(max_workers=2) as jobs:
            checks = {"linux": jobs.submit(lab.link, "c1", "eth1"),
                      "guest": jobs.submit(lab.ros, "p1", "/interface/ethernet/monitor ether3 once")}
            flags = checks["linux"].result()["flags"]
            if "UP" in flags and ("LOWER_UP" in flags) == up:
                hits.setdefault("linux", time.monotonic_ns())
            status = checks["guest"].result()
            if f"status: {'link-ok' if up else 'no-link'}" in status:
                hits.setdefault("guest", time.monotonic_ns())
        if len(hits) != 2:
            time.sleep(0.03)
    capture.mark(f"{phase}_observed", linux_flags=flags, routeros_status=status.strip(),
                 confirmed=list(sorted(hits)),
                 max_latency_s=(max(hits.values()) - start["mono_ns"]) / 1e9 if len(hits) == 2 else None)


def peer_link(capture, up):
    """Cut or restore the peer link at both MLAG peers: container eth1 and the QEMU NIC behind ether2."""
    lab = capture.lab
    phase = "up" if up else "down"
    start = capture.mark(f"{phase}_start")
    with ThreadPoolExecutor(max_workers=2 * len(PEERS)) as jobs:
        # Submit all four actions before waiting, so a failed restore on one end still restores the other.
        linux = [jobs.submit(run, lab.ns(peer, "ip", "link", "set", "dev", "eth1", phase)) for peer in PEERS]
        guest = {peer: jobs.submit(lab.qmp_action, peer, phase, "nic1") for peer in PEERS}
        for job in linux:
            job.result()
        qmp = {peer: job.result() for peer, job in guest.items()}
    capture.mark(f"{phase}_applied", qmp=qmp)
    hits, flags, status = {}, {}, {}
    expected = 2 * len(PEERS)
    deadline = time.monotonic() + 2
    while len(hits) < expected and time.monotonic() < deadline:
        with ThreadPoolExecutor(max_workers=expected) as jobs:
            links = {peer: jobs.submit(lab.link, peer, "eth1") for peer in PEERS}
            guests = {peer: jobs.submit(lab.ros, peer, "/interface ethernet monitor ether2 once") for peer in PEERS}
            for peer in PEERS:
                flags[peer] = links[peer].result()["flags"]
                if ("UP" in flags[peer]) == up and ("LOWER_UP" in flags[peer]) == up:
                    hits.setdefault(f"{peer}-linux", time.monotonic_ns())
                status[peer] = guests[peer].result().strip()
                if f"status: {'link-ok' if up else 'no-link'}" in status[peer]:
                    hits.setdefault(f"{peer}-guest", time.monotonic_ns())
        if len(hits) != expected:
            time.sleep(0.03)
    capture.mark(f"{phase}_observed", linux_flags=flags, routeros_status=status, confirmed=sorted(hits),
                 max_latency_s=(max(hits.values()) - start["mono_ns"]) / 1e9 if len(hits) == expected else None)


@contextmanager
def owned_filter(lab, node, port, filter_args):
    tc = lab.ns(node, "tc")
    qdiscs = json.loads(run([*tc, "-j", "qdisc", "show", "dev", port]))
    if any(q["kind"] in ("clsact", "ingress") for q in qdiscs):
        raise RuntimeError(f"Existing classifier on {node}:{port}; use a clean lab")
    run([*tc, "qdisc", "add", "dev", port, "clsact"])
    try:
        yield tc, ["dev", port, *filter_args]
    finally:
        run([*tc, "qdisc", "del", "dev", port, "clsact"])


def filter_fault(capture, silent):
    filters = ("egress", "protocol", "0x8809", "pref", "43", "flower",
               "dst_mac", "01:80:c2:00:00:02", "action", "drop") if silent else (
               "ingress", "protocol", "ip", "pref", "43", "flower",
               "src_ip", "198.51.100.1", "dst_ip", "198.51.100.2", "ip_proto", "icmp", "type", "8",
               "action", "drop")
    node, port = ("c1", "eth1") if silent else ("c2", "eth3")
    with owned_filter(capture.lab, node, port, filters) as (tc, rule):
        capture.mark("down_start")
        run([*tc, "filter", "add", *rule])
        capture.mark("down_applied")
        time.sleep(8 if silent else 2)
        if silent:
            capture.mark("silent_carrier", flags=capture.lab.link("c1", "eth1")["flags"],
                         routeros_status=capture.lab.ros("p1", "/interface/ethernet/monitor ether3 once"))
        stats = run([*tc, "-s", "filter", "show", "dev", port, filters[0]])
        capture.mark("up_start", counters=stats)
    capture.mark("up_applied")


def move_mobile(capture):
    lab = capture.lab
    before = lab.link("mobile", "bond0")["linkinfo"]["info_data"]["active_slave"]
    if before != "eth1":
        raise RuntimeError("Expected mobile on eth1. Restore the baseline before starting.")
    def select(port):
        run(lab.ns("mobile", "ip", "link", "set", "dev", "bond0", "type", "bond", "active_slave", port))
        data = lab.link("mobile", "bond0")["linkinfo"]["info_data"]
        if data["active_slave"] != port:
            raise RuntimeError(f"Mobile active member did not switch to {port}")
    capture.mark("down_start")
    try:
        select("eth2")
        capture.mark("down_applied")
        time.sleep(4)
    finally:
        capture.mark("up_start")
        select("eth1")
        capture.mark("up_applied")


def flap_member(capture):
    """Flap client 1's member to CHR 1 FLAP_CYCLES times; every down is followed by an up, also on an error."""
    for cycle in range(FLAP_CYCLES):
        if cycle:
            time.sleep(FLAP_UP_S)
        try:
            carrier(capture, up=False)
            time.sleep(FLAP_DOWN_S)
        finally:
            carrier(capture, up=True)


def bridge_ageing(capture, value, label):
    """Set ageing-time on both MLAG peers' bridges and read it back; a failure on one peer does not skip the other."""
    lab = capture.lab
    replies, readback = {}, {}
    for peer in PEERS:
        try:
            replies[peer] = lab.ros(peer, f"{SET_BRIDGE}ageing-time={value}")
            raw = lab.ros(peer, "/interface bridge print detail without-paging where name=bridge")
            match = re.search(r"\bageing-time=(\S+)", raw)
            readback[peer] = match[1] if match else None
        except (RuntimeError, OSError, subprocess.SubprocessError) as error:
            replies[peer], readback[peer] = f"error: {error}", None
    capture.mark(label, value=value, replies=replies, readback=readback)
    if any(found != value for found in readback.values()):
        raise RuntimeError(f"Bridges did not read back ageing-time={value}: {readback}")


def pin_neighbours(capture):
    lab = capture.lab
    entries = {}
    for node, address, mac in PINNED_NEIGHBOURS:
        run(lab.ns(node, "ip", "neigh", "replace", address, "lladdr", mac, "nud", "permanent", "dev", "bond0"))
        entries[f"{node}:{address}"] = run(lab.ns(node, "ip", "neigh", "show", address, "dev", "bond0")).strip()
    capture.mark("neighbours_pinned", entries=entries)


def restore_mac_age(capture):
    """Restore the default ageing-time and remove the pinned neighbour entries; each step runs even if one fails."""
    try:
        bridge_ageing(capture, MAC_AGE_DEFAULT, "bridge_ageing_restored")
    finally:
        removed = {}
        for node, address, _ in PINNED_NEIGHBOURS:
            try:
                done = subprocess.run(capture.lab.ns(node, "ip", "neigh", "del", address, "dev", "bond0"),
                                      capture_output=True, text=True, timeout=12)
                removed[f"{node}:{address}"] = {"returncode": done.returncode, "stderr": done.stderr.strip()}
            except (OSError, subprocess.SubprocessError) as error:
                removed[f"{node}:{address}"] = {"error": str(error)}
        capture.mark("neighbours_unpinned", entries=removed)


def silence_mobile(capture):
    """Drop every frame the MAC-move host sends, on egress of both bond members.

    The filter sits on the members, not on bond0: tc egress on bond0 would drop frames before the bond0 capture
    sees them, and the probe scoring needs every request the host sends.
    """
    lab = capture.lab
    rule = ("egress", "protocol", "all", "pref", "43", "flower", "action", "drop")
    with owned_filter(lab, "mobile", "eth1", rule) as (tc, first), owned_filter(lab, "mobile", "eth2", rule) as (_, second):
        capture.mark("down_start")
        run([*tc, "filter", "add", *first])
        run([*tc, "filter", "add", *second])
        capture.mark("down_applied")
        time.sleep(MAC_AGE_SILENCE_S)
        counters = {port: run([*tc, "-s", "filter", "show", "dev", port, "egress"]) for port in ("eth1", "eth2")}
        capture.mark("up_start", counters=counters)
    capture.mark("up_applied")


def start_floods(capture, floods=FLOOD_FLOWS):
    """Start the flood streams from traffic host 1 after a permanent neighbour entry for the unknown-unicast target."""
    lab = capture.lab
    address, mac = FLOOD_NEIGHBOUR
    # replace is idempotent, so a lab deployed before the flood streams needs no redeploy.
    run(lab.ns("c1", "ip", "neigh", "replace", address, "lladdr", mac, "nud", "permanent", "dev", "bond0"))
    capture.mark("flood_neighbour_set", address=address, mac=mac,
                 readback=run(lab.ns("c1", "ip", "neigh", "show", address, "dev", "bond0")).strip())
    for ident, (source, dest, _) in floods.items():
        node, port = source.split("-", 1)
        broadcast = ("-b",) if dest == "10.110.0.255" else ()
        capture.launch(lab.ns(node, "ping", "-n", "-D", "-O", *broadcast, "-i", "0.1", "-e", str(ident),
                              "-I", port, dest), capture.path / "probes" / f"{ident}.log")


def remove_flood_neighbour(capture):
    """Remove the neighbour entry once the flood streams have stopped; a missing entry is recorded, not raised."""
    address, _ = FLOOD_NEIGHBOUR
    try:
        removed = subprocess.run(capture.lab.ns("c1", "ip", "neigh", "del", address, "dev", "bond0"),
                                 capture_output=True, text=True, timeout=12)
        capture.mark("flood_neighbour_removed", address=address, returncode=removed.returncode,
                     stderr=removed.stderr.strip())
    except (OSError, subprocess.SubprocessError) as error:
        capture.mark("flood_neighbour_removed", address=address, error=str(error))


def run_case(lab, path, name, changes, hold=8):
    path.mkdir()
    manifest = {"case": name, "name": case_name(name), "bridge_mode": changes["bridge_mode"], "instance": INSTANCE}
    (path / "attempt.json").write_text(json.dumps(manifest, indent=2) + "\n")
    capture = Capture(lab, path)
    capture.mark("configuration_applied", replies=changes)
    captures = case_captures(name)
    peer_case = name == "peer-link-loss"
    mac_age = name == "silent-mobile"
    syslog = lab.topology.parent / "logs" / "routeros.jsonl"
    with syslog.open() as feed:
        feed.seek(0, os.SEEK_END)
        stop = Event()
        try:
            if peer_case:
                capture.observe(captures, PEER_LINK_PORTS, named_ports=True)
            else:
                capture.observe()
            start_floods(capture)
            with ThreadPoolExecutor(max_workers=3) as workers:
                for peer in PEERS:
                    workers.submit(poll_peer, lab, peer, path / f"state-{peer}.jsonl", stop,
                                   PEER_LINK_STATE if peer_case else FLAP_STATE if name == "carrier-flap" else STATE)
                if peer_case:
                    def bonds():
                        return {node: run(lab.ns(node, "cat", "/proc/net/bonding/bond0")) for node in ("c1", "c2")}
                    workers.submit(sample_loop, bonds, path / "state-host.jsonl", stop)
                try:
                    for peer in PEERS:
                        lab.ros(peer, f':log info "mlag-suite-{path.name}-begin"')
                    if mac_age:
                        pin_neighbours(capture)
                        bridge_ageing(capture, MAC_AGE_TIME, "bridge_ageing_set")
                    config = lab.ros_peers(CONFIG)
                    (path / "effective-config.json").write_text(json.dumps(config, indent=2) + "\n")
                    # Allow neighbor discovery and establish a separate quiet baseline.
                    time.sleep(2)
                    capture.mark("baseline_start")
                    time.sleep(4)
                    for ident in FLOWS:
                        probe = path / "probes" / f"{ident}.log"
                        if probe.read_text().count("bytes from") < 30:
                            raise RuntimeError(f"Probe {ident} did not establish baseline delivery")
                    # Each host bond's view of the LACP system ID both MLAG peers present, for the baseline check.
                    capture.mark("baseline_bonds", bonds={
                        f"client {node[1]} bond": run(lab.ns(node, "cat", "/proc/net/bonding/bond0"))
                        for node in ("c1", "c2")})
                    if name == "carrier" or peer_case:
                        cut = peer_link if peer_case else carrier
                        try:
                            cut(capture, up=False)
                            time.sleep(PEER_LINK_HOLD_S if peer_case else hold)
                        finally:
                            cut(capture, up=True)
                    elif name == "mobile-move":
                        move_mobile(capture)
                    elif name == "carrier-flap":
                        flap_member(capture)
                    elif mac_age:
                        silence_mobile(capture)
                    else:
                        filter_fault(capture, silent=name == "silent-lacp")
                    if peer_case:
                        time.sleep(PEER_LINK_RECOVERY_S)
                    elif mac_age:
                        time.sleep(MAC_AGE_RETURN_S)
                    else:
                        time.sleep(hold if name in ("carrier", "silent-lacp", "carrier-flap") else 3)
                    capture.mark("recovery_start")
                    time.sleep(3)
                    capture.mark("recovery_end")
                    for peer in PEERS:
                        lab.ros(peer, f':log info "mlag-suite-{path.name}-end"')
                    # Allow outstanding replies and libpcap buffers to drain past the scoring window.
                    time.sleep(2)
                finally:
                    stop.set()
                    if mac_age:
                        restore_mac_age(capture)
        except (RuntimeError, subprocess.SubprocessError, OSError, KeyError, ValueError) as error:
            capture.mark("runner_error", detail=str(error), stderr=getattr(error, "stderr", None))
        finally:
            capture.stop()
            remove_flood_neighbour(capture)
            (path / "syslog.jsonl").write_text(feed.read())
    if all((path / "captures" / f"{point}.pcap").is_file() for point in captures):
        seal_captures(path, captures)
    return keep_proof(path, analyze(path))


def verify_campaign_image(expected, builds, peers):
    pin = re.fullmatch(r"mikrotik/chr:([^@\s]+)@(sha256:[0-9a-f]{64})", expected)
    if pin is None:
        raise ValueError("campaign-image.txt must contain the versioned CHR image and its manifest digest")
    version, digest = pin.groups()
    for peer in peers:
        reference = builds["images"][peer]["reference"]
        match = re.search(r"^\s*version:\s*(\S+)", builds["routeros"][peer], re.MULTILINE)
        reported = match.group(1) if match else None
        if reference.partition("@")[2] != digest or reported != version:
            raise ValueError(f"{peer} reports {reported} on {reference}. Deploy the campaign image {expected}")


def select_topology(cases, bridge_mode="rstp"):
    """Check a case selection before any lab access and name the topology it runs on."""
    if cases and len(set(cases)) != len(cases):
        raise ValueError("choose each case once; use --repeat for repeated execution")
    if any(name in EXTERNAL_CASES for name in cases):
        raise ValueError("The single-homed external cases are archived. Use medium-* for live runs.")
    if bridge_mode not in BRIDGE_MODES:
        raise ValueError(f"Unknown bridge mode {bridge_mode!r}; choose one of {', '.join(BRIDGE_MODES)}")
    if any(name in TWO_PAIR_TARGETS for name in cases):
        if any(name not in TWO_PAIR_TARGETS for name in cases):
            raise ValueError("Select cases from one topology per run")
        kind = "two-pair"
    elif any(name in MEDIUM_TARGETS for name in cases):
        if any(name not in MEDIUM_TARGETS for name in cases):
            raise ValueError("Select cases from one topology per run")
        kind = "medium"
    elif any(name in DIRECT_CASES for name in cases):
        if any(name not in DIRECT_CASES for name in cases):
            raise ValueError("Run direct-client reboot cases in a separate suite")
        kind = "direct"
    elif any(name in ROOT_CASES for name in cases):
        if any(name not in ROOT_CASES for name in cases):
            raise ValueError("Select cases from one topology per run")
        kind = "root"
    else:
        kind = "small"
    if kind in ("medium", "root", "two-pair") and bridge_mode != "rstp":
        raise ValueError("--bridge-mode applies to the small lab only. Medium and root case names set the bridge mode.")
    return kind


def restore_rstp(lab, output):
    try:
        lab.apply_bridge_mode("rstp")
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        message = f"Restoring protocol-mode=rstp failed: {error}. Set it on both MLAG peers by hand."
        with (output / "runner-error.txt").open("a") as file:
            file.write(message + "\n")
        print(message, file=sys.stderr)
    else:
        print("Restored protocol-mode=rstp on both MLAG peers", flush=True)


def run_suite(lab_dir, output, cases, repeat, username, bridge_mode="rstp", settle=0):
    kind = select_topology(cases, bridge_mode)
    # The two-pair topology runs through the same attempt and baseline gate as the Medium lab.
    is_medium, is_direct, is_root = kind in ("medium", "two-pair"), kind == "direct", kind == "root"
    if kind == "two-pair":
        from .external_run import external_attempt
        from .two_pair_run import TwoPairLab
        lab_type, topology_name = TwoPairLab, "medium-two-pair"
    elif is_medium:
        from .external_run import MediumLab, external_attempt
        lab_type, topology_name = MediumLab, "medium"
    elif is_direct:
        from .external_run import DirectLab, external_attempt
        lab_type, topology_name = DirectLab, "small"
    elif is_root:
        from .root_run import RootLab, root_attempt
        lab_type, topology_name = RootLab, "medium-pair-root"
    else:
        lab_type, topology_name = Lab, "small"
    output = output.resolve()
    output.mkdir(parents=True)
    schedule = [{"run": f"{index:02d}-{case_name(name)}", "case": name, "name": case_name(name)}
                for index in range(1, repeat + 1) for name in cases or CASES]
    (output / "schedule.json").write_text(json.dumps(schedule, indent=2) + "\n")
    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    try:
        if sys.platform != "linux" or os.geteuid() != 0:
            raise ValueError("Run on the Linux lab host as root")
        # The lab CHRs keep Containerlab's default login; MLAG_SSH_PASSWORD overrides it, for example in CI.
        password = os.environ.pop("MLAG_SSH_PASSWORD", None) or "admin"
        for tool in HOST_TOOLS:
            if not shutil.which(tool):
                raise ValueError(f"Required command missing: {tool}")
        topology = (lab_dir / LAB_FOLDERS[topology_name] / f"{topology_name}.clab.yml").resolve(strict=True)
        if shutil.which("git"):
            revision = subprocess.run(["git", "-C", str(HERE), "rev-parse", "HEAD"],
                                      capture_output=True, text=True)
        else:
            revision = None
        with Path(f"/run/{lab_type.name}-suite.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with tempfile.TemporaryDirectory(prefix="mlag-") as temporary:
                lab = lab_type(topology, Path(temporary), username, password)
                lab.settle_s = settle
                lab.bridge_mode = bridge_mode
                try:
                    lab.wait_ready()
                    builds = lab.versions()
                    campaign_image = lab_dir / "campaign-image.txt"
                    builds["campaign_image"] = campaign_image.read_text().strip()
                    builds["started"] = datetime.now(timezone.utc).isoformat()
                    builds["git_revision"] = revision.stdout.strip() if revision and revision.returncode == 0 else None
                    shared = lab_dir / "shared"
                    inputs = (topology, campaign_image, topology.parent / f"{topology_name}.rsc",
                              shared / "client.Dockerfile", shared / "client-network.sh",
                              shared / "qemu-data-link.sh", shared / "forward-control.sh", shared / "rsyslog.conf",
                              PROJECT / "uv.lock", PROJECT / "pyproject.toml", *sorted(HERE.glob("*.py")),
                              PROFILES / f"{topology_name}.yml", PROFILES / "sequences" / "mikrotik_routeros" / "common.yml")
                    if is_root or is_medium:
                        inputs += (shared / "root-client.sh",)
                    if any(case_spec(name).reboot_intent for name in cases or ()):
                        inputs += (SMALL_06_PATH,)
                    saved_inputs = output / "inputs"
                    saved_inputs.mkdir()
                    builds["input_sha256"] = {}
                    for source in inputs:
                        copied = saved_inputs / source.name
                        copied.write_bytes(source.read_bytes())
                        builds["input_sha256"][source.name] = hashlib.sha256(copied.read_bytes()).hexdigest()
                    build_file = output / "builds.json"
                    build_file.write_text(json.dumps(builds, indent=2) + "\n")
                    verify_campaign_image(builds["campaign_image"], builds, lab.peers)
                    build_hash = hashlib.sha256(build_file.read_bytes()).hexdigest()
                    for item in schedule:
                        case = output / item["run"]
                        name = item["case"]
                        lab.wait_ready()
                        lab.check_logins()
                        if is_medium or is_direct:
                            with lab.case_mode(name) as changes:
                                result = external_attempt(lab, case, name, build_hash, changes)
                        elif is_root:
                            with lab.compare_fallback(name):
                                result = root_attempt(lab, case, name, build_hash)
                        else:
                            changes = lab.apply_bridge_mode(bridge_mode)
                            lab.wait_ready()
                            result = run_case(lab, case, name, changes)
                        print(f"{case.name}: {result['status']} ({case})", flush=True)
                        if timing := result.get("initial_validation_s"):
                            print(f"  {lab.name} initial validation (reset to verdict): "
                                  f"{timing['reset_to_verdict']:.2f} s", flush=True)
                        if result["status"] == "error" and not INTERRUPTED and not item["run"].endswith("-retry"):
                            # An invalid measurement gets one more attempt in its own folder once the lab
                            # is ready again; the loop reaches the inserted entry next. The errored folder stays.
                            lab.wait_ready()
                            lab.check_logins()
                            retry = {**item, "run": f"{item['run']}-retry"}
                            schedule.insert(schedule.index(item) + 1, retry)
                            (output / "schedule.json").write_text(json.dumps(schedule, indent=2) + "\n")
                            print(f"{case.name}: repeating once as {retry['run']}", flush=True)
                            continue
                        if result["status"] == "error" or (
                            (is_medium or is_direct) and result["status"] == "fail" and (
                                name.endswith("-baseline") or "baseline_rejected" in (case / "events.jsonl").read_text()
                            )
                        ):
                            break
                finally:
                    try:
                        if bridge_mode != "rstp":
                            restore_rstp(lab, output)
                    finally:
                        lab.close()
    except (RuntimeError, OSError, subprocess.SubprocessError, ValueError, KeyError) as error:
        (output / "runner-error.txt").write_text(f"{error}\n")
        print(error, file=sys.stderr)
    return write_suite(output)


# Set by interrupt(), so an operator's Ctrl-C or SIGTERM stops the suite instead of starting a retry.
INTERRUPTED = False


def interrupt(_sig, _frame):
    global INTERRUPTED
    INTERRUPTED = True
    raise RuntimeError("Run interrupted")
