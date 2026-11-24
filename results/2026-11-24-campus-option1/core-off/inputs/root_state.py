"""Interpret named RouterOS ports and Linux LACP members."""

import re

from .root_topology import ROOT_ID

PORT_FIELDS = ("status", "role", "edge-port", "learning", "forwarding",
               "designated-bridge-id", "discard-transitions", "forward-transitions")


def uptime(raw):
    match = re.search(r"^uptime-ns=(\d+)", raw, re.M)
    return int(match[1]) if match else None


def router_state(raw):
    raw = raw.replace("witness-bond", "access-uplink")  # Archived interface name.
    bridge, ports = {}, {}
    interfaces = []
    for line in raw.splitlines():
        key, separator, value = line.strip().partition(":")
        if not separator:
            continue
        value = value.strip()
        if key == "interface":
            interfaces = value.split()
            ports = {name: {} for name in interfaces}
        elif interfaces and key in PORT_FIELDS:
            for name, field in zip(interfaces, value.split()):
                ports[name][key] = field
        elif key in ("bridge-id", "root-bridge", "root-bridge-id", "root-port",
                     "topology-changes", "mlag-state", "mlag-active-role",
                     "max-age", "hello-time", "forward-delay"):
            bridge.setdefault(key, value.lower())
    return bridge, ports


def router_members(raw):
    return {
        port: {"actor": actor, "partner": partner, "partner_id": partner_id}
        for port, actor, partner_id, partner in re.findall(
            r'port=(ether\d+) [^\n]*?flags="([^"]+)" partner-sys-id=([^\s]+)[\s\S]*?partner-flags="([^"]+)"',
            raw,
        )
    }


def linux_members(raw):
    aggregate = re.search(r"Active Aggregator Info:\n\s*Aggregator ID: (\d+)", raw)
    members = {}
    for member in raw.split("Slave Interface: ")[1:]:
        name, _, fields = member.partition("\n")
        flags = [int(value) for value in re.findall(r"port state: (\d+)", fields)]
        aggregator = re.search(r"Aggregator ID: (\d+)", fields)
        members[name] = {
            "carrier": "MII Status: up" in fields,
            "eligible": bool(aggregate and aggregator and aggregate[1] == aggregator[1]
                             and len(flags) == 2 and all(value & 0x38 == 0x38 for value in flags)),
        }
    return members


def verify_root(routers, linux):
    for node, expected in {"p1": "primary", "p2": "secondary", "witness": None}.items():
        raw = routers[node]
        bridge, ports = router_state(raw)
        if bridge.get("root-bridge-id") != ROOT_ID:
            raise RuntimeError(f"{node} sees root {bridge.get('root-bridge-id')}, expected {ROOT_ID}")
        if expected:
            if (bridge.get("bridge-id") != ROOT_ID or bridge.get("root-bridge") != "yes"
                    or bridge.get("mlag-state") != "connected" or bridge.get("mlag-active-role") != expected):
                raise RuntimeError(f"{node} did not show connected MLAG as {expected} and root: {bridge}")
            required = ("access-uplink", "client2")
            if ports.get("access-uplink", {}).get("edge-port") != "no":
                raise RuntimeError(f"{node} access-switch bond did not operate as a non-edge port")
            members = {"ether3", "ether4"}
        else:
            uplink = ports.get("uplink", {})
            if (bridge.get("root-port") != "uplink" or bridge.get("root-bridge") != "no"
                    or uplink.get("role") != "root-port" or uplink.get("edge-port") != "no"):
                raise RuntimeError(f"Access switch did not select the non-edge uplink as root port: {bridge}, {uplink}")
            required = ("uplink", "ether4")
            members = {"ether2", "ether3"}
        if any(ports.get(port, {}).get("forwarding") != "yes" for port in required):
            raise RuntimeError(f"{node} required bridge ports did not forward: {ports}")
        links = router_members(raw)
        if set(links) != members or any(
            not all(links[port][side][3:6] == "SCD" for side in ("actor", "partner")) for port in members
        ):
            raise RuntimeError(f"{node} LACP members were not synchronized, collecting and distributing: {links}")
    members = linux_members(linux)
    if set(members) != {"eth1", "eth2"} or not all(
        member["carrier"] and member["eligible"] for member in members.values()
    ):
        raise RuntimeError(f"Client B LACP is not eligible on both legs: {members}")


ACCESS_GUARDS_READBACK = ";".join((
    "/interface bridge port print detail without-paging where interface=uplink",
    "/interface bridge port print detail without-paging where interface=ether4",
    "/interface ethernet print detail without-paging where name=ether4",
))


def access_guards(raw):
    """Edge, BPDU guard and loop protect settings of the access switch uplink and host port."""
    uplink = re.search(r"\binterface=uplink\b.*?\bedge=(\S+)", raw, re.S)
    host = re.search(r"\binterface=ether4\b.*?\bedge=(\S+).*?\bbpdu-guard=(\w+)", raw, re.S)
    loop = re.search(r"\bloop-protect=(\w+)", raw)
    return {"uplink_edge": uplink and uplink[1], "ether4_edge": host and host[1],
            "ether4_bpdu_guard": host and host[2], "ether4_loop_protect": loop and loop[1]}
