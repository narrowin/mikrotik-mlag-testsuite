"""The root pair, downstream RSTP witness and independent bypass."""

ROOT_CASES = ("root-calibrate", "reboot-secondary", "reboot-primary", "primary-sustained-stop",
              "reboot-primary-no-fallback")
ROOT_ID = "0x1000.02:00:00:21:00:11"
ROOT_NODES = {"p1": "172.30.216.11", "p2": "172.30.216.12", "witness": "172.30.216.13"}
ACCESS_ROOT_ID = "0x0000.02:00:00:21:00:13"
MEDIUM_NODES = {node: address.replace(".216.", ".218.") for node, address in ROOT_NODES.items()}
MEDIUM_TARGETS = {
    f"medium-{mode}-{case}": target
    for mode in ("stp-off", "pair-root", "access-root", "mstp-pair-root", "mstp-access-root")
    for case, target in (("baseline", None), ("calibrate", None),
                         ("reboot-secondary", "p2"), ("reboot-primary", "p1"))
}
# Emulated power loss runs with all bridges STP off only.
MEDIUM_TARGETS.update({"medium-stp-off-power-loss-secondary": "p2", "medium-stp-off-power-loss-primary": "p1"})
MEDIUM_STP_OFF_CASES = tuple(name for name in MEDIUM_TARGETS if name.startswith("medium-stp-off-"))
MANAGEMENT_PROBES = {"p1": 401, "p2": 402}
# How long an emulated power loss keeps the target off before it boots again.
POWER_OFF_HOLD_S = 20
ROOT_LINKS = (
    (("p1", "eth1"), ("p2", "eth1")),
    (("p1", "eth2"), ("witness", "eth1")),
    (("p2", "eth2"), ("witness", "eth2")),
    (("p1", "eth3"), ("c2", "eth1")),
    (("p2", "eth3"), ("c2", "eth2")),
    (("witness", "eth3"), ("c1", "eth1")),
    (("c1", "eth3"), ("c2", "eth3")),
)
ROOT_PORTS = tuple(point for link in ROOT_LINKS for point in link)
ROOT_CAPTURES_V1 = tuple(sorted({
    "c1-eth1", "c2-bond0", "c1-eth3", "c2-eth3", "c2-eth1", "c2-eth2",
    "p1-tap1", "p2-tap1", "p1-tap2", "p2-tap2", "p1-tap3", "p2-tap3",
    "witness-eth1", "witness-eth2", "witness-eth3", "witness-tap1", "witness-tap2",
}))
ROOT_CAPTURES = tuple(sorted((*ROOT_CAPTURES_V1, "p1-tap0", "p2-tap0")))
ROOT_FLOWS = {
    101: ("c1-eth1", "c2-bond0", "10.110.0.12", "client A to client B"),
    201: ("c2-bond0", "c1-eth1", "10.110.0.11", "client B to client A"),
    301: ("c1-eth3", "c2-eth3", "198.51.100.2", "bypass forward"),
    303: ("c2-eth3", "c1-eth3", "198.51.100.1", "bypass reverse"),
}


def target_for(name):
    if name == "root-calibrate":
        return None
    return "p2" if name == "reboot-secondary" else "p1"


def medium_mode(name):
    """Bridge protocol-mode of a Medium selector."""
    if name in MEDIUM_STP_OFF_CASES:
        return "none"
    return "mstp" if name.startswith("medium-mstp-") else "rstp"


def medium_root_id(name):
    if name in MEDIUM_STP_OFF_CASES:
        return None
    return ACCESS_ROOT_ID if name.startswith(("medium-access-root-", "medium-mstp-access-root-")) else ROOT_ID
