"""Observe the root-pair topology before, during and after its cases."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from decimal import Decimal
import json
import os
from queue import Empty, SimpleQueue
import re
import subprocess
from threading import Event
import time

from .evaluate import analyze
from .proof import keep_proof
from .evidence import seal_captures
from .legacy import NS, case_name
from .networka import INSTANCE, lab_name, reads
from .root_state import uptime, verify_root
from .root_topology import (
    MANAGEMENT_PROBES, POWER_OFF_HOLD_S, ROOT_CAPTURES, ROOT_FLOWS, ROOT_LINKS, ROOT_NODES, ROOT_PORTS, target_for,
)
from .run import CONFIG, UPTIME, UV, Capture, Lab, filter_fault, run, sample_loop


class RootLab(Lab):
    name = lab_name("mlag-medium-pair-root")
    device_names = {**Lab.device_names, "witness": "dc1-access-switch1"}
    nodes = (*ROOT_NODES, "c1", "c2", "syslog")
    peers = ROOT_NODES
    links = ROOT_LINKS
    ports = ROOT_PORTS
    client1_probe_port = "eth1"
    management_timeout_s = 100

    def validate_links(self):
        for left, right in self.links:
            self.verify_veth(left, right)

    def read_router(self, peer):
        sequence = "mlag_medium_access_state" if peer == "witness" else "mlag_medium_core_state"
        return self.ros(peer, ";".join((UPTIME, *reads(sequence))))

    def observe_router(self, peer):
        # Networka drops a dead session, so the next read opens a new one.
        return self.read_router(peer)

    def read_linux(self):
        return run(self.ns("c2", "cat", "/proc/net/bonding/bond0"))

    def readiness(self):
        routers = {peer: self.read_router(peer) for peer in self.peers}
        linux = self.read_linux()
        verify_root(routers, linux)
        return {"routers": routers, "linux": linux, "neighbors": self.probe_neighbors()}

    def probe_neighbors(self):
        neighbors = {
            node: json.loads(run(self.ns(node, "ip", "-j", "neigh", "show", "to", address, "dev", interface)))
            for node, address, interface in (("c1", "10.110.0.12", self.client1_probe_port),
                                             ("c2", "10.110.0.11", "bond0"))
        }
        for node, mac in (("c1", "02:00:00:11:00:12"), ("c2", "02:00:00:11:00:11")):
            entries = neighbors[node]
            if not any(entry.get("lladdr") == mac and "PERMANENT" in entry["state"] for entry in entries):
                raise RuntimeError(f"{node} missing the permanent probe neighbor {mac}")
        return neighbors

    def wait_ready(self):
        last_error = "management SSH unavailable"
        deadline = time.monotonic() + self.management_timeout_s
        while time.monotonic() < deadline:
            try:
                return self.readiness()
            except (RuntimeError, subprocess.SubprocessError) as error:
                last_error = str(error)
            time.sleep(1)
        raise RuntimeError(f"Root baseline did not settle: {last_error}")

    def host_state(self):
        by_node = {}
        for node in (*self.peers, "c1", "c2"):
            interesting = {port for point, port in self.ports if point == node}
            if node in self.peers:
                interesting.update(f"tap{port.removeprefix('eth')}" for port in tuple(interesting))
            links = json.loads(run(self.ns(node, "ip", "-j", "link", "show")))
            by_node[node] = {link["ifname"]: link["flags"] for link in links if link["ifname"] in interesting}
        fdb = {}
        for peer in self.peers:
            entries = json.loads(run(self.ns(peer, "bridge", "-j", "fdb", "show")))
            fdb[peer] = [entry for entry in entries if entry.get("mac") in (
                "02:00:00:11:00:11", "02:00:00:11:00:12",
            )]
        return {"links": by_node, "bond": self.read_linux(), "virtual_cable_fdb": fdb}

    def versions(self):
        versions = super().versions()
        for image in versions["images"].values():
            image["repo_digests"] = json.loads(run(["docker", "image", "inspect",
                                                  "--format", "{{json .RepoDigests}}", image["id"]]))
        for label, args in {
            "uv": (UV, "--version"), "docker": ("docker", "version", "--format", "{{.Server.Version}}"),
            "ip": ("ip", "-Version"), "tcpdump": ("tcpdump", "--version"), "ping": ("ping", "-V"),
        }.items():
            versions[label] = run(args).splitlines()[0]
        versions["kernel"] = os.uname().release
        versions["virtual_cables"] = {
            peer: json.loads(run(self.ns(peer, "bridge", "-j", "-d", "link", "show")))
            for peer in self.peers
        }
        return versions

    @contextmanager
    def compare_fallback(self, name):
        if name != "reboot-primary-no-fallback":
            yield
            return
        original = {}
        try:
            for peer in ("p1", "p2"):
                raw = self.ros(peer, "/interface bridge print detail without-paging where name=bridge")
                flag = re.search(r"\bmlag-lacp-fallback=(yes|no)", raw)
                if flag is None or flag[1] != "yes":
                    raise RuntimeError(f"{peer} does not have a verified default fallback setting")
                original[peer] = flag[1]
                self.ros(peer, "/interface bridge set bridge mlag-lacp-fallback=no")
            self.wait_ready()
            yield
        finally:
            for peer, flag in original.items():
                self.ros(peer, f"/interface bridge set bridge mlag-lacp-fallback={flag}")


def reboot_guest(capture, target, before, samples):
    lab = capture.lab
    prior = uptime(before["routers"][target])
    if prior is None:
        raise RuntimeError(f"{target} missing pre-reboot uptime")
    requested = capture.mark("down_start", target=target, prior_uptime_ns=prior)
    receipt = lab.ros(target, ":execute { :delay 1s; /system reboot }")
    capture.mark("reboot_request_acknowledged", target=target, raw=receipt)
    await_boot(capture, target, prior, requested["epoch_ns"], samples)


def await_boot(capture, target, prior, since_ns, samples):
    """Mark the first target sample whose uptime reset after since_ns."""
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        try:
            sample = samples.get(timeout=0.5)
        except Empty:
            continue
        if sample["started_ns"] < since_ns or "raw" not in sample:
            continue
        returned = uptime(sample["raw"])
        elapsed = sample["done_ns"] - since_ns
        if returned is not None and returned < prior and returned <= elapsed + 2_000_000_000:
            capture.mark("guest_boot_observed", target=target, prior_uptime_ns=prior,
                         uptime_ns=returned, query_start_ns=sample["started_ns"],
                         query_end_ns=sample["done_ns"])
            return
    raise RuntimeError(f"{target} did not prove a new guest boot within 90 s")


def switch_carrier(lab, target, ports, nics, state, guest_action=None):
    """Set the target's data veths and the facing NIC of each neighbouring CHR up or down in one step.

    A CHR sees carrier only through its own QEMU NIC, so a neighbouring CHR needs its facing NIC set as well.
    """
    batch = "".join(f"link set dev {port} {state}\n" for port in ports)

    def links():
        started = time.time_ns()
        run(lab.ns(target, "ip", "-batch", "-"), input=batch)
        return {"started_ns": started, "done_ns": time.time_ns(), "ports": list(ports), "state": state}

    with ThreadPoolExecutor(max_workers=len(nics) + 2) as jobs:
        # Submit every action before waiting, so one failure still applies the others.
        guest = jobs.submit(lab.qmp_action, target, guest_action) if guest_action else None
        linux = jobs.submit(links)
        facing = {f"{node}:nic{nic}": jobs.submit(lab.qmp_action, node, state, f"nic{nic}") for node, nic in nics}
        applied = {"links": linux.result(), "neighbour_qmp": {key: job.result() for key, job in facing.items()}}
        if guest:
            applied["qmp"] = guest.result()
    return applied


def confirm_carrier(capture, phase, start, target, ports, ends, routers, up):
    """Poll carrier at the target veths, every neighbour veth and each neighbouring CHR port until all agree."""
    lab = capture.lab
    points = [*((target, port) for port in ports), *ends]
    expected = len(points) + len(routers)
    hits, flags, status = {}, {}, {}
    qemu = None
    deadline = time.monotonic() + 2
    while True:
        with ThreadPoolExecutor(max_workers=expected + 1) as jobs:
            query = jobs.submit(lab.qmp_action, target, "query-status") if qemu is None else None
            links = {f"{node}:{port}": jobs.submit(lab.link, node, port) for node, port in points}
            guests = {f"{node}:{port}": jobs.submit(lab.ros, node, f"/interface ethernet monitor {port} once")
                      for node, port in routers}
            for key, job in links.items():
                flags[key] = job.result()["flags"]
                # The target's own veth must be administratively down or up; a neighbour must lose or regain carrier.
                own = key.startswith(f"{target}:")
                if ("LOWER_UP" in flags[key]) == up and (not own or ("UP" in flags[key]) == up):
                    hits.setdefault(key, time.monotonic_ns())
            for key, job in guests.items():
                status[key] = job.result().strip()
                if f"status: {'link-ok' if up else 'no-link'}" in status[key]:
                    hits.setdefault(key, time.monotonic_ns())
            if query is not None:
                qemu = query.result()["reply"]["return"]
        if len(hits) == expected or time.monotonic() >= deadline:
            break
        time.sleep(0.03)
    return capture.mark(f"{phase}_observed", target=target, linux_flags=flags, routeros_status=status,
                        qemu_status=qemu, confirmed=sorted(hits),
                        missing=sorted((set(flags) | set(status)) - set(hits)),
                        max_latency_s=(max(hits.values()) - start["mono_ns"]) / 1e9 if len(hits) == expected else None)


def power_loss(capture, target, before, samples):
    """Emulate a power loss of one MLAG peer and its boot.

    Every data link of the target loses carrier and its guest stops in one step. After POWER_OFF_HOLD_S the
    guest is reset and continued so RouterOS boots from scratch, and its links come back as it starts booting.
    The management interface (eth0/tap0) stays untouched, so the management probes measure guest absence.
    """
    lab = capture.lab
    prior = uptime(before["routers"][target])
    if prior is None:
        raise RuntimeError(f"{target} missing pre-power-loss uptime")
    ports, ends = [], []
    for left, right in lab.links:
        for (node, port), far in ((left, right), (right, left)):
            if node == target:
                ports.append(port)
                ends.append(far)
    # ethN in a CHR container is the veth behind tapN, QEMU NIC N and RouterOS ether(N+1).
    nics = [(node, int(port.removeprefix("eth"))) for node, port in ends if node in lab.peers]
    routers = [(node, f"ether{nic + 1}") for node, nic in nics]
    lab.verify_qemu(target)
    for node in dict.fromkeys(node for node, _ in nics):
        lab.verify_qemu(node, [nic for other, nic in nics if other == node])
    try:
        off = capture.mark("power_off_start", target=target, prior_uptime_ns=prior, ports=ports,
                           neighbours=[f"{node}:{port}" for node, port in ends],
                           neighbour_nics=[f"{node}:nic{nic}" for node, nic in nics])
        applied = capture.mark("power_off_applied", target=target,
                               **switch_carrier(lab, target, ports, nics, "down", "stop"))
        confirm_carrier(capture, "power_off", off, target, ports, ends, routers, up=False)
        time.sleep(max(0.0, POWER_OFF_HOLD_S - (time.monotonic_ns() - applied["mono_ns"]) / 1e9))
    finally:
        on = capture.mark("power_on_start", target=target)
        boot = {}
        try:
            for action in ("system_reset", "cont"):
                boot[action] = lab.qmp_action(target, action)
        finally:
            capture.mark("power_on_applied", target=target, qmp=boot,
                         **switch_carrier(lab, target, ports, nics, "up"))
    confirm_carrier(capture, "power_on", on, target, ports, ends, routers, up=True)
    await_boot(capture, target, prior, on["epoch_ns"], samples)


def stop_guest(capture, target):
    lab = capture.lab
    capture.mark("down_start", target=target)
    try:
        stopped = lab.qmp_action(target, "stop")
        status = lab.qmp_action(target, "query-status")["reply"]["return"]
        if status["running"] or status["status"] != "paused":
            raise RuntimeError(f"QEMU did not confirm a paused guest: {status}")
        capture.mark("guest_stopped", target=target, qmp=stopped, status=status)
        time.sleep(35)
    finally:
        capture.mark("guest_resume_requested", target=target)
        continued = lab.qmp_action(target, "cont")
        status = lab.qmp_action(target, "query-status")["reply"]["return"]
        capture.mark("guest_resumed", target=target, qmp=continued, status=status)
        if not status["running"]:
            raise RuntimeError(f"QEMU did not confirm guest resumed: {status}")


def rebind_syslog(capture, target, logs):
    label = f"{capture.lab.name}-{capture.path.name}"
    marker = f"{label}-end"
    address = capture.lab.peers[target]
    if any(log["source_ip"] == address and marker in log["raw"]
           for log in map(json.loads, logs.splitlines())):
        return
    capture.mark("syslog_rebind_requested", target=target)
    action = "/system logging action set [find where name=mlagLabSyslog] src-address="
    capture.lab.ros(target, f"{action}0.0.0.0;{action}{address};"
                    f':log info "{label}-after-rebind"')
    time.sleep(2)


def verify_live_collectors(capture, baseline, logs, *, verify_delivery=True):
    marker = f"{capture.lab.name}-{capture.path.name}-begin"
    sources = {log["source_ip"] for log in map(json.loads, logs.splitlines()) if marker in log["raw"]}
    expected = set(capture.lab.peers.values())
    if sources != expected:
        raise RuntimeError(f"Missing pre-fault management syslog markers from {sorted(expected - sources)}")
    if any(child.poll() is not None for child, _ in capture.processes):
        raise RuntimeError("An observer exited before the fault")
    if verify_delivery:
        verify_live_delivery(capture, baseline)


def verify_live_delivery(capture, baseline, definitions=None):
    if definitions is None:
        definitions = getattr(capture.lab, "flows", ROOT_FLOWS)
    for ident in definitions:
        probe = capture.path / "probes" / f"{ident}.log"
        replies = [(int(Decimal(stamp) * NS), int(seq)) for stamp, seq in re.findall(
            r"^\[(\d+\.\d+)\] \d+ bytes from .*?icmp_seq=(\d+)", probe.read_text(), re.M
        )]
        baseline_replies = [(stamp, seq) for stamp, seq in replies if stamp >= baseline["epoch_ns"]]
        tail = baseline_replies[-10:]
        if (len(baseline_replies) < 30 or tail[-1][1] - tail[0][1] != 9
                or time.time_ns() - tail[-1][0] > 450_000_000):
            raise RuntimeError(f"Probe {ident} did not establish stable baseline delivery")


def root_attempt(lab, path, name, build_hash):
    path.mkdir()
    target = target_for(name)
    manifest = {"schema": 2, "case": name, "name": case_name(name), "topology": lab.name,
                "instance": INSTANCE, "builds_sha256": build_hash, "target": target}
    (path / "attempt.json").write_text(json.dumps(manifest, indent=2) + "\n")
    capture = Capture(lab, path)
    stop = Event()
    target_samples = SimpleQueue()
    feed_path = lab.topology.parent / "pair-root-logs/routeros.jsonl"
    logs = ""
    try:
        with feed_path.open() as feed:
            feed.seek(0, os.SEEK_END)
            try:
                capture.observe(ROOT_CAPTURES, ROOT_PORTS, ROOT_FLOWS, named_ports=True)
                for peer, ident in MANAGEMENT_PROBES.items():
                    capture.launch(["ping", "-n", "-D", "-O", "-i", "0.1", "-e", str(ident), ROOT_NODES[peer]],
                                   path / "probes" / f"{ident}.log")
                with ThreadPoolExecutor(max_workers=4) as workers:
                    jobs = [workers.submit(sample_loop, lambda peer=peer: lab.observe_router(peer),
                                           path / f"state-{peer}.jsonl", stop,
                                           target_samples if peer == target else None) for peer in lab.peers]
                    jobs.append(workers.submit(sample_loop, lab.host_state, path / "state-host.jsonl", stop))
                    try:
                        for peer in lab.peers:
                            lab.ros(peer, f':log info "{lab.name}-{path.name}-begin"')
                        config = lab.ros_peers(CONFIG)
                        (path / "effective-config.json").write_text(json.dumps(config, indent=2) + "\n")
                        time.sleep(2)
                        baseline = capture.mark("baseline_start")
                        time.sleep(4)
                        before = lab.readiness()
                        capture.mark("baseline_confirmed", **before)
                        logs += feed.read()
                        verify_live_collectors(capture, baseline, logs)
                        if name == "root-calibrate":
                            filter_fault(capture, silent=False)
                            time.sleep(3)
                        else:
                            if name == "primary-sustained-stop":
                                stop_guest(capture, target)
                            else:
                                reboot_guest(capture, target, before, target_samples)
                            # Leave time to observe return-side loss even after management comes back.
                            time.sleep(16)
                        capture.mark("recovery_start")
                        time.sleep(3)
                        capture.mark("recovery_end")
                        try:
                            capture.mark("baseline_restored", **lab.readiness())
                        except RuntimeError as error:
                            capture.mark("baseline_restoration_failed", detail=str(error))
                        for peer in lab.peers:
                            lab.ros(peer, f':log info "{lab.name}-{path.name}-end"')
                        time.sleep(2)
                        if target:
                            logs += feed.read()
                            rebind_syslog(capture, target, logs)
                    finally:
                        stop.set()
                        for job in jobs:
                            job.result()
            finally:
                (path / "syslog.jsonl").write_text(logs + feed.read())
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        capture.mark("runner_error", detail=str(error), stderr=getattr(error, "stderr", None))
    finally:
        capture.stop()
        if all((path / "captures" / f"{point}.pcap").is_file() for point in ROOT_CAPTURES):
            seal_captures(path, ROOT_CAPTURES)
    return keep_proof(path, analyze(path))
