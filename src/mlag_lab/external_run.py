"""Run bridge-mode comparisons on the dual-attached lab topologies."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import os
from queue import SimpleQueue
import subprocess
from threading import Event
import time
import traceback

from network_toolkit.platforms.mikrotik_routeros import intent as ros

from .cases import case_spec, save_case
from .device_state import BRIDGE, SMALL_READS, findings, gate_roles, save_gate
from .direct_topology import DIRECT_CAPTURES, DIRECT_FLOWS, DIRECT_LINKS, DIRECT_NODES, DIRECT_PORTS
from .direct_topology import DIRECT_FLOOD_FLOWS
from .evaluate import analyze
from .proof import keep_proof
from .evidence import packets, seal_captures
from .external_evaluate import bpdu_coverage, broadcast_counts, direct_role_issues
from .legacy import case_name
from .measure import score_flows
from .networka import INSTANCE, lab_name
from .root_run import (
    CONFIG, RootLab, power_loss, rebind_syslog, reboot_guest, sample_loop, verify_live_collectors,
    verify_live_delivery,
)
from .root_run import confirm_carrier
from .root_topology import (
    ACCESS_ROOT_ID, MANAGEMENT_PROBES, MEDIUM_CORE_OFF_CASES, MEDIUM_NODES, MEDIUM_STP_OFF_CASES, MEDIUM_TARGETS,
    ROOT_CAPTURES, ROOT_FLOWS, ROOT_LINKS, ROOT_PORTS, medium_mode, medium_root_id, medium_setup,
)
from .run import ATTEMPT_SCHEMA, Capture, filter_fault, remove_flood_neighbour, run, start_floods

# Access switch port settings per Medium family, applied in every bridge reset so none leaks into the next.
# The baseline gate (intent/state/medium-<setup>.yaml) reads them back.
ACCESS_GUARDS = {
    # Campus option 1: the uplink bond is an RSTP edge port and the host port is guarded against loops.
    True: ("/interface bridge port set [find interface=uplink] edge=yes;"
           "/interface bridge port set [find interface=ether4] edge=yes bpdu-guard=yes;"
           "/interface ethernet set ether4 loop-protect=on"),
    # The medium.rsc startup values for every other family.
    False: ("/interface bridge port set [find interface=uplink] edge=no;"
            "/interface bridge port set [find interface=ether4] edge=yes bpdu-guard=no;"
            "/interface ethernet set ether4 loop-protect=default"),
}
# The two-pair inter-pair bond member between CHR 1 and CHR 3. Container eth2 is the veth behind tap2,
# QEMU NIC 2 and RouterOS ether3, the only local member of each CHR's inter-pair bond.
INTERPAIR_MEMBER = (("p1", "eth2"), ("q1", "eth2"))
INTERPAIR_NIC, INTERPAIR_ETHER = 2, "ether3"
INTERPAIR_HOLD_S, INTERPAIR_RETURN_S = 8, 8
# The Medium families without spanning tree on the MLAG pair; the broadcast check proves they form no loop.
MEDIUM_PAIR_STP_OFF = (*MEDIUM_STP_OFF_CASES, *MEDIUM_CORE_OFF_CASES)


class BridgeComparisonLab(RootLab):
    flows = ROOT_FLOWS
    flood_flows = {}
    management_probes = MANAGEMENT_PROBES
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

    def check_baseline(self, name, report, target):
        return [text for _, text in findings(report)]

    def wait_ready(self):
        """Management access and the probe neighbours; the case's bridge reset and baseline gate do the rest."""
        last_error = "management SSH unavailable"
        deadline = time.monotonic() + self.management_timeout_s
        while time.monotonic() < deadline:
            try:
                self.uptimes()
                self.probe_neighbors()
                return
            except (RuntimeError, subprocess.SubprocessError) as error:
                last_error = str(error)
            time.sleep(1)
        raise RuntimeError(f"Lab management did not settle: {last_error}")

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

    def wait_for_baseline_state(self, name, target):
        limit = 8 if name in MEDIUM_STP_OFF_CASES else self.settle_timeout_s
        deadline = time.monotonic() + limit
        while True:
            before = self.readiness(name)
            if not self.check_baseline(name, before, target) or time.monotonic() >= deadline:
                return
            time.sleep(0.5)


class MediumLab(BridgeComparisonLab):
    name = lab_name("mlag-medium")
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

    def gate(self, name=None):
        return ("medium", "host2", *(() if name is None else (f"medium-{medium_setup(name)}",)))

    def case_target(self, name):
        return MEDIUM_TARGETS[name]

    @contextmanager
    def case_mode(self, name):
        core_off = name in MEDIUM_CORE_OFF_CASES
        if core_off:
            settings = dict.fromkeys(("p1", "p2"), "protocol-mode=none forward-reserved-addresses=no priority=0x1000")
            settings["witness"] = "protocol-mode=rstp priority=0x0000"
        else:
            root = medium_root_id(name)
            mode = medium_mode(name)
            priority = "0x0000" if root == ACCESS_ROOT_ID else "0x8000"
            settings = dict.fromkeys(("p1", "p2"), f"protocol-mode={mode} priority=0x1000")
            settings["witness"] = f"protocol-mode={mode} priority={priority}"
        yield self.reset_bridges(settings, {"witness": ACCESS_GUARDS[core_off]})


class DirectLab(BridgeComparisonLab):
    name = lab_name("mlag-small")
    device_names = RootLab.device_names
    peers = DIRECT_NODES
    nodes = (*peers, "c1", "c2", "mobile", "syslog")
    links = DIRECT_LINKS
    ports = DIRECT_PORTS
    captures = DIRECT_CAPTURES
    flows = DIRECT_FLOWS
    flood_flows = DIRECT_FLOOD_FLOWS
    log_dir = "logs"
    settle_timeout_s = 12
    client1_probe_port = "bond0"

    def reads(self, peer):
        return SMALL_READS

    def gate(self, name=None):
        return ("direct", "hosts", f"direct-{self.bridge_mode}")

    def case_target(self, name):
        if name in ("direct-baseline", "direct-calibrate"):
            return None
        intent = case_spec(name).reboot_intent
        role = intent.fault.reboot_role if intent else name.rsplit("-", 1)[1]
        deadline = time.monotonic() + self.settle_timeout_s
        while time.monotonic() < deadline:
            for node in self.peers:
                replies = ros.collect_bridge(self.client, self.device_name(node), BRIDGE, **self.options())
                try:
                    state = ros.mlag(replies, BRIDGE)
                except ValueError:
                    continue
                if state["connected"] and state.get("role") == role:
                    return node
            time.sleep(0.25)
        return None

    def check_baseline(self, name, report, target):
        roles = gate_roles(report, {node: self.device_name(node) for node in self.peers})
        return [text for _, text in findings(report)] + direct_role_issues(name, roles, target, self.bridge_mode)

    def check_wire(self, path, name, start, end):
        # The client LAGs terminate on hosts, so there is no downstream STP election.
        return []

    @contextmanager
    def case_mode(self, name):
        yield self.apply_bridge_mode(self.bridge_mode)


def interpair_member(capture, up):
    """Set the inter-pair member down or up at both CHRs: both container veths and both QEMU NICs, as peer_link does."""
    lab = capture.lab
    phase = "up" if up else "down"
    start = capture.mark(f"{phase}_start", link=[f"{node}:{port}" for node, port in INTERPAIR_MEMBER])
    with ThreadPoolExecutor(max_workers=2 * len(INTERPAIR_MEMBER)) as jobs:
        # Submit every action before waiting, so a failed restore on one end still restores the other.
        linux = [jobs.submit(run, lab.ns(node, "ip", "link", "set", "dev", port, phase))
                 for node, port in INTERPAIR_MEMBER]
        guest = {node: jobs.submit(lab.qmp_action, node, phase, f"nic{INTERPAIR_NIC}") for node, _ in INTERPAIR_MEMBER}
        for job in linux:
            job.result()
        qmp = {node: job.result() for node, job in guest.items()}
    capture.mark(f"{phase}_applied", qmp=qmp)
    (target, port), far = INTERPAIR_MEMBER
    confirm_carrier(capture, phase, start, target, [port], [far],
                    [(node, INTERPAIR_ETHER) for node, _ in INTERPAIR_MEMBER], up)


def run_fault(capture, name, target, samples, observe_after_boot_seconds):
    if name.endswith("-calibrate"):
        filter_fault(capture, silent=False)
        time.sleep(3)
    elif name.endswith("-interpair-member-flap"):
        for node, _ in INTERPAIR_MEMBER:
            capture.lab.verify_qemu(node, (INTERPAIR_NIC,))
        try:
            interpair_member(capture, up=False)
            time.sleep(INTERPAIR_HOLD_S)
        finally:
            interpair_member(capture, up=True)
        time.sleep(INTERPAIR_RETURN_S)
    else:
        fault = power_loss if "-power-loss-" in name else reboot_guest
        fault(capture, target, samples)
        time.sleep(observe_after_boot_seconds)


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
    spec = case_spec(name)
    save_case(spec, path)
    intent = spec.reboot_intent
    fault = intent.fault if intent else None
    flood_flows = intent.flood_flows if intent else lab.flood_flows
    manifest = {"schema": ATTEMPT_SCHEMA, "case": name, "name": case_name(name), "topology": lab.name,
                "instance": INSTANCE, "builds_sha256": build_hash, "target": target, "devices": lab.device_inventory()}
    if "bridge_mode" in changes:
        manifest["bridge_mode"] = changes["bridge_mode"]
    settle = getattr(lab, "settle_s", 0)
    if settle:
        manifest["settle_s"] = settle
    (path / "attempt.json").write_text(json.dumps(manifest, indent=2) + "\n")
    capture = Capture(lab, path)
    applied = capture.mark("configuration_applied", replies=changes)
    stop = Event()
    samples = SimpleQueue()
    feed_path = lab.topology.parent / lab.log_dir / "routeros.jsonl"
    logs = ""
    try:
        with feed_path.open() as feed:
            feed.seek(0, os.SEEK_END)
            try:
                # Networka names each bridge-port monitor before any capture starts; a failure is the attempt's error.
                samplers = {peer: lab.sampler(peer) for peer in lab.peers}
                capture.observe(lab.captures, lab.ports, lab.flows, named_ports=True, immediate=True)
                if flood_flows:
                    start_floods(capture, flood_flows)
                for peer, ident in lab.management_probes.items():
                    capture.launch(["ping", "-n", "-D", "-O", "-i", "0.1", "-e", str(ident), lab.peers[peer]],
                                   path / "probes" / f"{ident}.log")
                with ThreadPoolExecutor(max_workers=len(lab.peers) + 1) as workers:
                    jobs = [workers.submit(sample_loop, samplers[peer], path / f"state-{peer}.jsonl", stop,
                                           samples if peer == target else None) for peer in lab.peers]
                    jobs.append(workers.submit(sample_loop, lab.host_state, path / "state-host.jsonl", stop))
                    try:
                        for peer in lab.peers:
                            lab.ros(peer, f':log info "{lab.name}-{path.name}-begin"')
                        config = lab.ros_peers(CONFIG)
                        (path / "effective-config.json").write_text(json.dumps(config, indent=2) + "\n")
                        lab.wait_for_baseline_state(name, target)
                        if settle:
                            # Hold the baseline back so a state the configuration change left behind must persist.
                            time.sleep(max(0.0, settle - (time.monotonic_ns() - applied["mono_ns"]) / 1e9))
                            capture.mark("settled", seconds=settle)
                        logs += feed.read()
                        repair_missing_syslog(capture, logs)
                        baseline = capture.mark("baseline_start")
                        time.sleep(fault.baseline_seconds if fault else 4)
                        before = save_gate(path / "gate-baseline", lab.readiness(name))
                        finished = capture.mark("baseline_observed", verdict=before.verdict)
                        logs += feed.read()
                        verify_live_collectors(capture, baseline, logs, verify_delivery=False)
                        issues = lab.check_baseline(name, before, target)
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
                        if name in MEDIUM_PAIR_STP_OFF and not issues:
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
                            capture.mark("baseline_confirmed")
                            if not name.endswith("-baseline"):
                                run_fault(capture, name, target, samples,
                                          fault.observe_after_boot_seconds if fault else 16)
                                capture.mark("recovery_start")
                                time.sleep(fault.recovery_seconds if fault else 3)
                                capture.mark("recovery_end")
                                # Leave a state sample beyond the scoring boundary before taking readbacks.
                                time.sleep(0.5)
                                stop.set()
                                for job in jobs:
                                    job.result()
                                after = save_gate(path / "gate-restored", lab.readiness(name))
                                capture.mark("baseline_restored", issues=lab.check_baseline(name, after, target))
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
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        capture.mark("runner_error", detail=f"{type(error).__name__}: {error}", stderr=getattr(error, "stderr", None),
                     traceback=traceback.format_exc())
    finally:
        capture.stop()
        if flood_flows:
            remove_flood_neighbour(capture)
        if all((path / "captures" / f"{point}.pcap").is_file() for point in lab.captures):
            seal_captures(path, lab.captures)
    return keep_proof(path, analyze(path))
