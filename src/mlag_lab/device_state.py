"""Device state through Networka's intent layer.

A state sample is one Networka read of several RouterOS JSON commands, saved as
`{started_ns, done_ns, replies: {command: Reply}, port_monitors: {port: command}}`. The accessors below turn a
saved sample into values with Networka's normalizers and raise `ValueError` when the evidence cannot decide.

A gate is a Networka intent file under `intent/state/`. The runner collects it with `run_intent`, adds the Linux
client bonds it reads itself, and saves `intent.yaml`, `evidence.json` and `results.json` in the attempt folder.
The evaluator replays that folder, so every device-state verdict is Networka's pass, fail or error.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess

import yaml
from network_toolkit import intent
from network_toolkit.platforms.linux import intent as linux
from network_toolkit.platforms.mikrotik_routeros import intent as ros

ROUTEROS, LINUX = "mikrotik_routeros", "linux"
BRIDGE = "bridge"
GATES = Path(__file__).with_name("intent") / "state"
# Linux traffic hosts: runner node, device name in the intent files, and their LACP bond.
HOSTS = {"c1": "dc1-traffic-host1", "c2": "dc1-traffic-host2"}
HOST_BOND, HOST_MEMBERS = "bond0", ("eth1", "eth2")
# Device names of the runner nodes in every lab's Networka profile and intent file.
DEVICES = {"p1": "dc1-core-mlag1", "p2": "dc1-core-mlag2", "witness": "dc1-access-switch1",
           "q1": "dc1-access-mlag1", "q2": "dc1-access-mlag2", **HOSTS}
IN_USE = ("synchronization", "collecting", "distributing")


@dataclass(frozen=True)
class Reads:
    """What one state sample of a switch reads: carrier, bond members, bridge ports and host table entries."""

    interfaces: tuple[str, ...]
    bonds: tuple[tuple[str, tuple[str, ...]], ...]
    ports: tuple[str, ...]
    macs: tuple[str, ...] = ()
    # The access switch has no MLAG peer, so its samples do not need MLAG state.
    mlag: bool = True


CLIENT1, CLIENT2, MOBILE = "02:00:00:11:00:11", "02:00:00:11:00:12", "02:00:00:11:00:50"
SMALL_READS = Reads(("ether2", "ether3", "ether4", "ether5"), (("client1", ("ether3",)), ("client2", ("ether4",))),
                    ("ether2", "client1", "client2", "ether5"), (CLIENT1, CLIENT2, MOBILE))
MEDIUM_CORE_READS = Reads(("ether2", "ether3", "ether4"), (("access-uplink", ("ether3",)), ("client2", ("ether4",))),
                          ("ether2", "access-uplink", "client2"), (CLIENT1, CLIENT2))
MEDIUM_ACCESS_READS = Reads(("ether2", "ether3", "ether4"), (("uplink", ("ether2", "ether3")),),
                            ("uplink", "ether4"), (CLIENT1, CLIENT2), mlag=False)
TWO_PAIR_CORE_READS = Reads(("ether2", "ether3", "ether4"), (("interpair", ("ether3",)), ("client2", ("ether4",))),
                            ("ether2", "interpair", "client2"), (CLIENT1, CLIENT2))
TWO_PAIR_ACCESS_READS = Reads(("ether2", "ether3", "ether4"), (("interpair", ("ether3",)), ("client1", ("ether4",))),
                              ("ether2", "interpair", "client1"), (CLIENT1, CLIENT2))
# What each switch of a lab samples. The root-pair runner uses the Medium reads.
SMALL_NODE_READS = dict.fromkeys(("p1", "p2"), SMALL_READS)
MEDIUM_NODE_READS = {"p1": MEDIUM_CORE_READS, "p2": MEDIUM_CORE_READS, "witness": MEDIUM_ACCESS_READS}
TWO_PAIR_NODE_READS = {**dict.fromkeys(("p1", "p2"), TWO_PAIR_CORE_READS), **dict.fromkeys(("q1", "q2"), TWO_PAIR_ACCESS_READS)}


def commands(reads, monitors):
    """The RouterOS JSON commands of one sample, each built by Networka."""
    return (ros.UPTIME, *map(ros.ethernet_monitor, reads.interfaces), ros.bridge_print(BRIDGE),
            ros.bridge_monitor(BRIDGE), ros.PORT_STATS, *monitors.values(),
            *(ros.bond_monitor(bond) for bond, _ in reads.bonds), *map(ros.host_print, reads.macs))


class Sampler:
    """Read one switch's state in one Networka read per call.

    Before sampling starts, Networka's collect_bridge_port selects each bridge port by bridge and interface name
    and names its monitor command, which carries the port's .id. A port it cannot select raises RuntimeError, so
    the attempt stops before any capture. A port keeps its .id across bridge resets and reboots; a stale command
    makes the normalizer report the port as undecided, never as passing.
    """

    def __init__(self, lab, node, reads):
        self.lab, self.device, self.reads, self.monitors = lab, lab.device_name(node), reads, {}
        for port in reads.ports:
            found = ros.collect_bridge_port(lab.client, self.device, BRIDGE, port, **lab.options())
            if "monitor" not in found:
                reply = found.get("stats") or {}
                raise RuntimeError(f"{self.device}: Networka could not select bridge port {port}: "
                                   f"{reply.get('error') or 'not in the bridge-port statistics'}")
            self.monitors[port] = found["monitor"]["command"]

    def __call__(self):
        replies = ros.collect(self.lab.client, self.device, *commands(self.reads, self.monitors), **self.lab.options())
        return {"replies": replies, "port_monitors": dict(self.monitors)}


def view(sample):
    """The replies of a saved sample, keyed as Networka's collectors key them."""
    replies = sample.get("replies") if isinstance(sample, dict) else None
    if not isinstance(replies, dict):
        raise ValueError(str(sample.get("error") or "the sample has no replies") if isinstance(sample, dict)
                         else "no sample")
    return {**replies, "stats": replies.get(ros.PORT_STATS)}


def mlag(sample):
    return ros.mlag(view(sample), BRIDGE)


def stp(sample):
    return ros.stp_bridge(view(sample), BRIDGE)


def bridge_port(sample, port):
    replies = view(sample)
    command = (sample.get("port_monitors") or {}).get(port)
    return ros.bridge_port({"stats": replies["stats"], "monitor": replies.get(command)}, BRIDGE, port)


def member(sample, bond, port):
    return ros.lacp_member(view(sample), bond, port)


def in_use(state, side="actor"):
    """Synchronized, collecting and distributing on one side of a normalized LACP member."""
    flags = state.get(side)
    if flags is None:
        raise ValueError("no LACP partner")
    return all(flags[name] for name in IN_USE)


def host(sample, mac):
    return ros.host_entry(view(sample), BRIDGE, mac)


def carrier(sample, interface):
    return ros.interface_up(view(sample), interface)


def uptime(sample):
    return ros.uptime_ns(view(sample))


def known(read, *args):
    """The value, or None when the evidence cannot decide."""
    try:
        return read(*args)
    except ValueError:
        return None


def summary(sample, reads, *, stp_on=False):
    """Every value one sample reads, as Networka normalizes it; an undecided value holds its reason.

    With spanning tree on, a sample without the bridge and root bridge IDs is undecided.
    """
    def value(read, *args):
        try:
            return read(sample, *args)
        except ValueError as error:
            return {"unverified": str(error)}

    def lacp(bond, port):
        state = value(member, bond, port)
        if "unverified" in state:
            return state
        return {side: sorted(name for name, on in flags.items() if on)
                for side, flags in state.items() if side in ("actor", "partner")}

    def spanning_tree(sample):
        state = stp(sample)
        if stp_on and not {"bridge_id", "root_bridge_id"} <= state.keys():
            raise ValueError("the bridge monitor reports no bridge or root bridge ID with spanning tree on")
        return state

    return {**({"mlag": value(mlag)} if reads.mlag else {}), "stp": value(spanning_tree),
            "carrier": {name: value(carrier, name) for name in reads.interfaces},
            "ports": {name: value(bridge_port, name) for name in reads.ports},
            "lacp": {f"{bond}/{port}": lacp(bond, port) for bond, ports in reads.bonds for port in ports},
            "hosts": {mac: value(host, mac) for mac in reads.macs}}


def complete(state):
    """No value of a summary is undecided."""
    if isinstance(state, dict):
        return "unverified" not in state and all(complete(value) for value in state.values())
    return True


def host_bond(text, member, bond=HOST_BOND):
    """Linux bonding driver view of one member, from /proc/net/bonding text the suite read."""
    command = linux.bonding(bond)
    evidence = {command: {"command": command, "output": text, "error": None if isinstance(text, str) else "no reply"}}
    result = linux.check_bond_member(evidence, bond, member, {"carrier": True, "eligible": True})
    if result.verdict == "error":
        raise ValueError(result.reason)
    return result.observed


def partner_id(platform, replies, bond, port):
    """LACP system the partner of one bond member sends, as `priority/mac`; None when the evidence cannot say."""
    try:
        system = platform.lacp_member(replies, bond, port).get("partner_system")
    except ValueError:
        return None
    return f"{system['priority']}/{system['mac']}" if system else None


def lacp_system_ids(report, partner_bonds=None):
    """The LACP system ID each MLAG bond presents on each of its members, read on the partner side in the gate.

    The Linux hosts' bond readings give the partner each host member sees. partner_bonds maps a label to the
    (node, bond, member) of RouterOS switches whose bond faces one MLAG pair.
    """
    if report is None:
        return "not available: the run saved no baseline gate"
    bonds = {}
    for node, device in HOSTS.items():
        members = {member: partner_id(linux, reading(report.evidence, device, "collect_bond", HOST_BOND, member),
                                      HOST_BOND, member) for member in HOST_MEMBERS}
        if any(members.values()):
            bonds[f"client {node[1]} bond"] = {member: value for member, value in members.items() if value}
    for label, ports in (partner_bonds or {}).items():
        members = {f"{node}:{port}": partner_id(ros, reading(report.evidence, DEVICES[node], "collect_bond", bond, port),
                                                bond, port) for node, bond, port in ports}
        if any(members.values()):
            bonds[label] = {member: value for member, value in members.items() if value}
    return {label: {"members": members, "same": len(members) >= 2 and len(set(members.values())) == 1}
            for label, members in bonds.items()} or "not available: the baseline gate holds no partner system ID"


# Gates: Networka intent files, collected live and replayed offline.

def load_gate(*names):
    """The items of the named intent files under intent/state/, in order."""
    return [item for name in names for item in intent.load_intent(GATES / f"{name}.yaml")]


def now():
    return datetime.now(UTC).isoformat()


def read_host_bonds(lab, items):
    """Networka evidence for the Linux items: each host's bonding driver text, read through nsenter."""
    devices = {}
    for node, device in HOSTS.items():
        bonds = sorted({item.params["bond"] for item in items if item.device == device})
        if not bonds:
            continue
        started, replies = now(), {}
        for bond in bonds:
            command = linux.bonding(bond)
            try:
                output = subprocess.run(lab.ns(node, "cat", f"/proc/net/bonding/{bond}"), capture_output=True,
                                        text=True, timeout=12, check=True).stdout
                replies[bond] = {"command": command, "output": output, "error": None}
            except (OSError, subprocess.SubprocessError) as error:
                replies[bond] = {"command": command, "output": None, "error": str(error)}
        readings = []
        for item in items:
            if item.device != device:
                continue
            # The reading key run_intent uses: the bond, then the member for checks that take one.
            key = [item.params["bond"], *([item.params["member"]] if "member" in item.params else [])]
            if not any(reading["args"] == key for reading in readings):
                reply = replies[key[0]]
                readings.append({"collector": "collect_bond", "args": key, "replies": {reply["command"]: reply}})
        devices[device] = {"device_type": LINUX, "readings": readings, "started": started, "finished": now()}
    return devices


def run_gate(lab, items):
    """Collect the RouterOS items with Networka and the Linux items through nsenter, then evaluate them together."""
    linux_devices = set(HOSTS.values())
    switches = [item for item in items if item.device not in linux_devices]
    report = intent.run_intent(lab.client, switches, interactive_creds=lab.credentials)
    evidence = {**report.evidence, "devices": {**report.evidence["devices"], **read_host_bonds(lab, items)}}
    return intent.replay_intent(items, evidence)


def save_gate(folder, report):
    """Save a gate as Networka does, so `nw intent replay FOLDER` and `replay_gate` give the same results."""
    folder.mkdir()
    items = [item.to_yaml() for item, _ in report.results]
    (folder / intent.INTENT_FILE).write_text(yaml.safe_dump(items, sort_keys=False))
    (folder / intent.EVIDENCE_FILE).write_text(json.dumps(report.evidence, indent=2) + "\n")
    (folder / intent.RESULTS_FILE).write_text(json.dumps(report.to_json(), indent=2) + "\n")
    return report


def replay_gate(folder):
    return intent.replay_directory(folder)


def findings(report):
    """(level, text) for every item that did not pass: fail for a failed item, error for an unverified one."""
    found = []
    for item, result in report.results:
        label = item.name or f"{item.device} {item.check} {json.dumps(item.params)}"
        if result.verdict == "fail":
            found.append(("fail", f"{label}: expected {json.dumps(result.expected)}, "
                                  f"observed {json.dumps(result.observed)}"))
        elif result.verdict == "error":
            found.append(("error", f"{label}: unverified, {result.reason}"))
    return found


def reading(evidence, device, collector, *args):
    """The replies of one saved reading of a gate, empty when the gate has none."""
    saved = ((evidence.get("devices") or {}).get(device) or {}).get("readings") or []
    for entry in saved:
        if entry.get("collector") == collector and entry.get("args") == list(args) and "error" not in entry:
            return entry.get("replies") or {}
    return {}


def gate_roles(report, devices):
    """MLAG role and root bridge ID each switch reported in a gate, read from its bridge reading."""
    found = {}
    for node, device in devices.items():
        replies = reading(report.evidence, device, "collect_bridge", BRIDGE)
        found[node] = {"role": known(lambda: ros.mlag(replies, BRIDGE).get("role")),
                       "root_id": known(lambda: ros.stp_bridge(replies, BRIDGE).get("root_bridge_id"))}
    return found


def relative(text, folder):
    """A message with the attempt folder's path removed, so a replay from a copy reads the same."""
    return text.replace(f"{folder.parent}/", "")


def grade_gate(folder, check, label, phase=None):
    """Replay a saved gate into suite checks, one per item that did not pass.

    A failed Networka item is a suite fail; an unverified item and a missing gate are evidence errors.
    """
    if not (folder / intent.INTENT_FILE).exists():
        check("error", False, f"{label}: {folder.name} was not saved", phase)
        return None
    try:
        report = replay_gate(folder)
    except intent.IntentError as error:
        check("error", False, f"{label}: {relative(error.message, folder)}", phase)
        return None
    found = findings(report)
    for level, text in found:
        check(level, False, f"{label}: {text}", phase)
    if not found:
        check("fail", True, f"{label}: all {len(report.results)} Networka intent items pass", phase)
    return report
