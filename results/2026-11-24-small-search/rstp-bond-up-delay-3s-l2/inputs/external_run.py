"""Run bridge-mode comparisons on the dual-attached lab topologies."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import os
from queue import SimpleQueue
import subprocess
from threading import Event
import time

from .direct_topology import DIRECT_CAPTURES, DIRECT_FLOWS, DIRECT_LINKS, DIRECT_NODES, DIRECT_PORTS
from .evaluate import analyze
from .evidence import packets, seal_captures
from .external_evaluate import baseline_issues, bpdu_coverage, broadcast_counts, direct_baseline_issues
from .legacy import case_name
from .measure import score_flows
from .root_run import (
    CONFIG, STATE, RootLab, rebind_syslog, reboot_guest, sample_loop, verify_live_collectors,
    verify_live_delivery,
)
from .root_topology import (
    ACCESS_ROOT_ID, MANAGEMENT_PROBES, MEDIUM_NODES, MEDIUM_STP_OFF_CASES, MEDIUM_TARGETS,
    ROOT_CAPTURES, ROOT_FLOWS, ROOT_LINKS, ROOT_PORTS, medium_root_id,
)
from .root_state import router_state
from .run import Capture, filter_fault, run


class BridgeComparisonLab(RootLab):
    flows = ROOT_FLOWS
    log_dir = "logs"
    settle_timeout_s = 32
    management_timeout_s = 30

    def device_inventory(self):
        return {
            node: {
                "name": self.device_name(node),
                "container": self.container_name(node),
                "management_ip": cfg["NetworkSettings"]["Networks"][f"{self.name}-mgmt"]["IPAddress"],
                "role": cfg["Config"]["Labels"].get("role"),
                "runtime": "RouterOS CHR guest" if node in self.peers else "Linux container",
                "host": os.uname().nodename,
            }
            for node, cfg in self.containers.items()
        }

    def readiness(self):
        return {
            "routers": {peer: self.observe_router(peer) for peer in self.peers},
            "linux": self.read_linux(), "neighbors": self.probe_neighbors(),
        }

    def check_baseline(self, name, before, config, target):
        return baseline_issues(name, before, config)

    def check_wire(self, path, name, start, end):
        wire = bpdu_coverage(path, name, start, end)
        if wire["missing"] or wire["unexpected"]:
            return [f"Baseline BPDU coverage missing {wire['missing']}, unexpected {wire['unexpected']}"]
        return []

    def check_links(self):
        observed = {}
        for node in dict.fromkeys(node for node, _ in self.ports):
            links = json.loads(run(self.ns(node, "ip", "-j", "-d", "link", "show")))
            observed[node] = {link["ifname"]: link for link in links}
        carrier = {f"{node}:{port}": observed[node].get(port, {}).get("flags", []) for node, port in self.ports}
        missing = [point for point, flags in carrier.items() if "LOWER_UP" not in flags]
        for (left, left_port), (right, right_port) in self.links:
            first = observed[left].get(left_port, {})
            second = observed[right].get(right_port, {})
            if (not first or not second or first.get("link_index") != second["ifindex"]
                    or second.get("link_index") != first["ifindex"]):
                missing.append(f"{left}:{left_port} and {right}:{right_port} are not opposite veth ends")
        cables = {}
        for peer in self.peers:
            ports = {port for node, port in self.ports if node == peer}
            ports.update(f"tap{port.removeprefix('eth')}" for port in tuple(ports))
            links = json.loads(run(self.ns(peer, "bridge", "-j", "-d", "link", "show")))
            cables[peer] = {link["ifname"]: link for link in links if link["ifname"] in ports}
            for port in ports:
                link = cables[peer].get(port, {})
                if "LOWER_UP" not in link.get("flags", []) or link.get("learning") is not False:
                    missing.append(f"{peer}:{port} lacks carrier or transparent wire settings")
        issues = [f"Physical link baseline: {point}" for point in missing]
        return {"carrier": carrier, "virtual_cables": cables}, issues

    def wait_for_baseline_state(self, name, config, target):
        limit = 8 if name in MEDIUM_STP_OFF_CASES else self.settle_timeout_s
        deadline = time.monotonic() + limit
        while True:
            before = self.readiness()
            if not self.check_baseline(name, before, config, target) or time.monotonic() >= deadline:
                return
            time.sleep(0.5)


class MediumLab(BridgeComparisonLab):
    peers = MEDIUM_NODES
    nodes = (*peers, "c1", "c2", "syslog")
    links = ROOT_LINKS
    ports = ROOT_PORTS
    captures = ROOT_CAPTURES

    def validate_links(self):
        super().validate_links()
        for core in ("p1", "p2"):
            interfaces = json.loads(run(self.ns(core, "ip", "-j", "link", "show")))
            if any(interface["ifname"] == "eth4" for interface in interfaces):
                raise RuntimeError("Redeploy the three-CHR Medium lab before running these cases")

    def read_router(self, peer):
        bonds = ("uplink",) if peer == "witness" else ("access-uplink", "client2")
        return observe_ports(self, peer, (2, 3, 4), bonds)

    def case_target(self, name):
        return MEDIUM_TARGETS[name]

    @contextmanager
    def case_mode(self, name):
        root = medium_root_id(name)
        mode = "rstp" if root else "none"
        priority = "0x0000" if root == ACCESS_ROOT_ID else "0x8000"
        settings = dict.fromkeys(("p1", "p2"), f"protocol-mode={mode} priority=0x1000")
        settings["witness"] = f"protocol-mode={mode} priority={priority}"
        yield self.reset_bridges(settings)


class DirectLab(BridgeComparisonLab):
    name = "mlag-small"
    device_names = RootLab.device_names
    peers = DIRECT_NODES
    nodes = (*peers, "c1", "c2", "mobile", "syslog")
    links = DIRECT_LINKS
    ports = DIRECT_PORTS
    captures = DIRECT_CAPTURES
    flows = DIRECT_FLOWS
    log_dir = "logs"
    settle_timeout_s = 12
    client1_probe_port = "bond0"

    def read_router(self, peer):
        return observe_ports(self, peer, (2, 3, 4, 5), ("client1", "client2"))

    def readiness(self):
        state = super().readiness()
        state["linux_client1"] = run(self.ns("c1", "cat", "/proc/net/bonding/bond0"))
        return state

    def case_target(self, name):
        if name in ("direct-baseline", "direct-calibrate"):
            return None
        role = name.rsplit("-", 1)[1]
        deadline = time.monotonic() + self.settle_timeout_s
        while time.monotonic() < deadline:
            for node in self.peers:
                bridge, _ = router_state(self.read_router(node))
                if (bridge.get("mlag-state"), bridge.get("mlag-active-role")) == ("connected", role):
                    return node
            time.sleep(0.25)
        return None

    def check_baseline(self, name, before, config, target):
        return direct_baseline_issues(name, before, config, target, self.bridge_mode)

    def check_wire(self, path, name, start, end):
        # The client LAGs terminate on hosts, so there is no downstream STP election.
        return []

    @contextmanager
    def case_mode(self, name):
        yield self.apply_bridge_mode(self.bridge_mode)


def observe_ports(lab, peer, ports, bonds):
    command = (STATE[0], *(f"/interface ethernet monitor ether{port} once" for port in ports), *STATE[4:],
               *(f"/interface bonding monitor-slaves bond={bond} once=yes" for bond in bonds))
    return lab.ros(peer, ";".join(command))


def run_fault(capture, name, target, before, samples):
    if name.endswith("-calibrate"):
        filter_fault(capture, silent=False)
        time.sleep(3)
    else:
        reboot_guest(capture, target, before, samples)
        time.sleep(16)


def repair_missing_syslog(capture, logs):
    lab = capture.lab
    marker = f"{lab.name}-{capture.path.name}-begin"
    received = {log["source_ip"] for log in map(json.loads, logs.splitlines()) if marker in log["raw"]}
    missing = {node: address for node, address in lab.peers.items() if address not in received}
    action = "/system logging action set [find where name=mlagLabSyslog] src-address="
    for node, address in missing.items():
        capture.mark("syslog_preflight_rebind", target=node)
        lab.ros(node, f'{action}0.0.0.0;{action}{address};:log info "{marker}"')
    if missing:
        time.sleep(2)


def verify_probe_window(capture, start, end):
    definitions = capture.lab.flows
    seen = {}
    fields = ("frame.time_epoch", "icmp.ident", "icmp.type", "icmp.seq")
    for point in sorted({point for source, dest, _, _ in definitions.values() for point in (source, dest)}):
        observations = {}
        for stamp, row in packets(capture.path / "captures" / f"{point}.pcap", fields, "icmp"):
            if all(row):
                observations.setdefault(tuple(map(int, row)), []).append(stamp)
        seen[point] = observations
    flows = score_flows(seen, start, end, (("baseline", end, end),), [],
                        definitions=definitions, detailed=True)
    evidence = {}
    issues = []
    for ident, flow in flows.items():
        evidence[ident] = {field: flow[field] for field in (
            "sent", "baseline_good", "missed", "duplicates", "capture_mismatches", "max_send_interval_s",
        )}
        if (flow["baseline_good"] < 30 or flow["missed"] or flow["duplicates"]
                or flow["capture_mismatches"] or flow["max_send_interval_s"] > 0.45):
            issues.append(f"Probe {ident} did not pass the loss-free, duplicate-free packet baseline")
    return evidence, issues


def external_attempt(lab, path, name, build_hash, changes):
    path.mkdir()
    target = lab.case_target(name)
    manifest = {"schema": 2, "case": name, "name": case_name(name), "topology": lab.name,
                "builds_sha256": build_hash, "target": target, "devices": lab.device_inventory()}
    if "bridge_mode" in changes:
        manifest["bridge_mode"] = changes["bridge_mode"]
    (path / "attempt.json").write_text(json.dumps(manifest, indent=2) + "\n")
    capture = Capture(lab, path)
    capture.mark("configuration_applied", replies=changes)
    stop = Event()
    samples = SimpleQueue()
    feed_path = lab.topology.parent / lab.log_dir / "routeros.jsonl"
    logs = ""
    try:
        with feed_path.open() as feed:
            feed.seek(0, os.SEEK_END)
            try:
                capture.observe(lab.captures, lab.ports, lab.flows, named_ports=True, immediate=True)
                for peer, ident in MANAGEMENT_PROBES.items():
                    capture.launch(["ping", "-n", "-D", "-O", "-i", "0.1", "-e", str(ident), lab.peers[peer]],
                                   path / "probes" / f"{ident}.log")
                with ThreadPoolExecutor(max_workers=len(lab.peers) + 1) as workers:
                    jobs = [workers.submit(sample_loop, lambda peer=peer: lab.observe_router(peer),
                                           path / f"state-{peer}.jsonl", stop,
                                           samples if peer == target else None) for peer in lab.peers]
                    jobs.append(workers.submit(sample_loop, lab.host_state, path / "state-host.jsonl", stop))
                    try:
                        for peer in lab.peers:
                            lab.ros(peer, f':log info "{lab.name}-{path.name}-begin"')
                        config = {peer: lab.ros(peer, CONFIG) for peer in lab.peers}
                        (path / "effective-config.json").write_text(json.dumps(config, indent=2) + "\n")
                        lab.wait_for_baseline_state(name, config, target)
                        logs += feed.read()
                        repair_missing_syslog(capture, logs)
                        baseline = capture.mark("baseline_start")
                        time.sleep(4)
                        before = lab.readiness()
                        finished = capture.mark("baseline_observed", **before)
                        logs += feed.read()
                        verify_live_collectors(capture, baseline, logs, verify_delivery=False)
                        issues = lab.check_baseline(name, before, config, target)
                        issues += lab.check_wire(path, name, baseline["epoch_ns"], finished["epoch_ns"])
                        links, link_issues = lab.check_links()
                        capture.mark("baseline_links", **links)
                        issues += link_issues
                        probes, probe_issues = verify_probe_window(capture, baseline["epoch_ns"], finished["epoch_ns"])
                        capture.mark("baseline_packets", flows=probes)
                        issues += probe_issues
                        try:
                            verify_live_delivery(capture, baseline)
                        except RuntimeError as error:
                            issues.append(str(error))
                        if name in MEDIUM_STP_OFF_CASES and not issues:
                            started = capture.mark("broadcast_start")
                            with ThreadPoolExecutor(max_workers=2) as workers:
                                probe_jobs = {}
                                for node, port, address in (("c1", "eth1", "10.110.0.12"),
                                                            ("c2", "bond0", "10.110.0.11")):
                                    probe = ["docker", "exec", lab.container_name(node), "arping", "-b",
                                             "-c", "3", "-w", "4", "-I", port, address]
                                    probe_jobs[node] = workers.submit(subprocess.run, probe, capture_output=True,
                                                                      text=True, timeout=6)
                                for node, job in probe_jobs.items():
                                    output = job.result()
                                    (path / "probes" / f"arp-{node}.log").write_text(output.stdout + output.stderr)
                            ended = capture.mark("broadcast_end")
                            counts = broadcast_counts(path, started["epoch_ns"], ended["epoch_ns"])
                            if any(max(pair) < 3 for pair in counts.values()):
                                time.sleep(0.8)
                                counts = broadcast_counts(path, started["epoch_ns"], ended["epoch_ns"])
                            capture.mark("baseline_broadcast_packets", counts=counts)
                            if any(pair != [3, 3] for pair in counts.values()):
                                issues.append(f"Expected three broadcast requests at each end, observed {counts}")
                        if issues:
                            capture.mark("baseline_rejected", issues=issues)
                        else:
                            capture.mark("baseline_confirmed", **before)
                            if not name.endswith("-baseline"):
                                run_fault(capture, name, target, before, samples)
                                capture.mark("recovery_start")
                                time.sleep(3)
                                capture.mark("recovery_end")
                                # Leave a state sample beyond the scoring boundary before taking readbacks.
                                time.sleep(0.5)
                                stop.set()
                                for job in jobs:
                                    job.result()
                                after = lab.readiness()
                                config = {peer: lab.ros(peer, CONFIG) for peer in lab.peers}
                                capture.mark("baseline_restored", **after, issues=lab.check_baseline(name, after, config, target))
                        for peer in lab.peers:
                            lab.ros(peer, f':log info "{lab.name}-{path.name}-end"')
                        time.sleep(2)
                        if target and not issues:
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
        if all((path / "captures" / f"{point}.pcap").is_file() for point in lab.captures):
            seal_captures(path, lab.captures)
    return analyze(path)
