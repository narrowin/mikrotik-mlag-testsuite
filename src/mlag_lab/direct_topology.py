"""The existing small lab with both client bonds terminating on Linux hosts."""

from .root_topology import ROOT_FLOWS

DIRECT_CASES = ("direct-baseline", "direct-calibrate", "direct-reboot-secondary", "direct-reboot-primary",
                "direct-power-loss-secondary", "direct-power-loss-primary")
DIRECT_NODES = {"p1": "172.30.215.11", "p2": "172.30.215.12"}
DIRECT_LINKS = (
    (("p1", "eth1"), ("p2", "eth1")),
    (("p1", "eth2"), ("c1", "eth1")),
    (("p2", "eth2"), ("c1", "eth2")),
    (("p1", "eth3"), ("c2", "eth1")),
    (("p2", "eth3"), ("c2", "eth2")),
    (("p1", "eth4"), ("mobile", "eth1")),
    (("p2", "eth4"), ("mobile", "eth2")),
    (("c1", "eth3"), ("c2", "eth3")),
)
DIRECT_PORTS = tuple(point for link in DIRECT_LINKS for point in link)
DIRECT_FLOWS = {
    ident: (source.replace("c1-eth1", "c1-bond0"), dest.replace("c1-eth1", "c1-bond0"), address, label)
    for ident, (source, dest, address, label) in ROOT_FLOWS.items()
}
DIRECT_CAPTURES = (
    "c1-bond0", "c1-eth1", "c1-eth2", "c1-eth3", "c2-bond0", "c2-eth1", "c2-eth2", "c2-eth3",
    "mobile-eth1", "mobile-eth2",
    "p1-tap0", "p1-tap1", "p1-tap2", "p1-tap3", "p1-tap4",
    "p2-tap0", "p2-tap1", "p2-tap2", "p2-tap3", "p2-tap4",
)
