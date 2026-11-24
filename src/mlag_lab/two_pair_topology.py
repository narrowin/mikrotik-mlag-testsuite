"""Two MLAG pairs joined by one distributed LACP bond.

Pair A (p1, p2) is the intended STP root. Pair B (q1, q2) carries host 1, pair A carries host 2.
Bridge MACs are ordered so that pair B wins a MAC tie-break against pair A's secondary: with equal
bridge priorities the root moves to pair B whenever pair A presents its secondary's bridge ID.
"""

from .root_topology import ROOT_FLOWS

TWO_PAIR_LAB = "mlag-medium-two-pair"
TWO_PAIR_NODES = {"p1": "172.30.219.11", "p2": "172.30.219.12", "q1": "172.30.219.13", "q2": "172.30.219.14"}
TWO_PAIR_DEVICES = {"q1": "dc1-access-mlag1", "q2": "dc1-access-mlag2"}
PAIRS = {"p1": "A", "p2": "A", "q1": "B", "q2": "B"}
PEER = {"p1": "p2", "p2": "p1", "q1": "q2", "q2": "q1"}
ROLES = {"p1": "primary", "p2": "secondary", "q1": "primary", "q2": "secondary"}
MLAG_PRIORITIES = {"p1": 10, "p2": 20, "q1": 10, "q2": 20}
ADMIN_MACS = {"p1": "02:00:00:21:00:11", "p2": "02:00:00:21:00:14", "q1": "02:00:00:21:00:12", "q2": "02:00:00:21:00:13"}
CLIENT_BONDS = {"p1": "client2", "p2": "client2", "q1": "client1", "q2": "client1"}
TWO_PAIR_PROBES = {"p1": 401, "p2": 402, "q1": 403, "q2": 404}

# Bridge priority per switch. "equal" is the field failure (every pair on the same priority),
# "field" is the deployed field design (same priority inside a pair, a lower value on the root pair).
SETUPS = {
    "equal": {"p1": "0x8000", "p2": "0x8000", "q1": "0x8000", "q2": "0x8000"},
    "field": {"p1": "0x2000", "p2": "0x2000", "q1": "0x4000", "q2": "0x4000"},
    "stp-off": {"p1": "0x8000", "p2": "0x8000", "q1": "0x8000", "q2": "0x8000"},
    "stp-off-strict": {"p1": "0x8000", "p2": "0x8000", "q1": "0x8000", "q2": "0x8000"},
}
# "stp-off" runs both pairs with spanning tree off, the setup that passed every one-pair case.
# "stp-off-strict" adds lacp-strict=yes on the inter-pair bond, so a member without an LACP partner
# stops carrying traffic even while its link keeps carrier.
MODES = {"equal": "rstp", "field": "rstp", "stp-off": "none", "stp-off-strict": "none"}
STRICT_SETUPS = ("stp-off-strict",)
TWO_PAIR_STEPS = (("baseline", None), ("calibrate", None), ("reboot-a-primary", "p1"),
                  ("reboot-a-secondary", "p2"), ("reboot-b-primary", "q1"), ("reboot-b-secondary", "q2"),
                  ("interpair-member-flap", None))
TWO_PAIR_TARGETS = {f"two-pair-{setup}-{step}": target for setup in SETUPS for step, target in TWO_PAIR_STEPS}

TWO_PAIR_LINKS = (
    (("p1", "eth1"), ("p2", "eth1")),
    (("q1", "eth1"), ("q2", "eth1")),
    (("p1", "eth2"), ("q1", "eth2")),
    (("p2", "eth2"), ("q2", "eth2")),
    (("p1", "eth3"), ("c2", "eth1")),
    (("p2", "eth3"), ("c2", "eth2")),
    (("q1", "eth3"), ("c1", "eth1")),
    (("q2", "eth3"), ("c1", "eth2")),
    (("c1", "eth3"), ("c2", "eth3")),
)
TWO_PAIR_PORTS = tuple(point for link in TWO_PAIR_LINKS for point in link)
TWO_PAIR_CAPTURES = tuple(sorted((
    "c1-bond0", "c1-eth1", "c1-eth2", "c1-eth3", "c2-bond0", "c2-eth1", "c2-eth2", "c2-eth3",
    *(f"{node}-tap{nic}" for node in TWO_PAIR_NODES for nic in range(4)),
)))
TWO_PAIR_FLOWS = {
    ident: (source.replace("c1-eth1", "c1-bond0"), dest.replace("c1-eth1", "c1-bond0"), address, label)
    for ident, (source, dest, address, label) in ROOT_FLOWS.items()
}


def two_pair_setup(name):
    return max((setup for setup in SETUPS if name.startswith(f"two-pair-{setup}-")), key=len)


def two_pair_mode(name):
    return MODES[two_pair_setup(name)]


def two_pair_lacp_strict(name):
    return "yes" if two_pair_setup(name) in STRICT_SETUPS else "no"


def bridge_id(priority, mac):
    return f"{int(priority, 0):#06x}.{mac}"


def expected_ids(name):
    """Root ID that every switch must report, and the bridge ID each pair presents."""
    priorities = SETUPS[two_pair_setup(name)]
    pair_ids = {"A": bridge_id(priorities["p1"], ADMIN_MACS["p1"]), "B": bridge_id(priorities["q1"], ADMIN_MACS["q1"])}
    return pair_ids["A"], pair_ids
