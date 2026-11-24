"""External-root topology and case inputs."""

from .root_topology import ROOT_CAPTURES, ROOT_LINKS, ROOT_NODES

EXTERNAL_TARGETS = {
    "external-baseline": None,
    "external-calibrate": None,
    "external-reboot-secondary": "p2",
    "external-reboot-primary": "p1",
    "external-root-loss": None,
    "external-combined-loss": "p1",
    "external-no-stp-baseline": None,
    "external-no-stp-calibrate": None,
    "external-no-stp-reboot-secondary": "p2",
    "external-no-stp-reboot-primary": "p1",
    "external-all-stp-off-baseline": None,
    "external-all-stp-off-calibrate": None,
    "external-all-stp-off-reboot-secondary": "p2",
    "external-all-stp-off-reboot-primary": "p1",
}
EXTERNAL_CASES = tuple(EXTERNAL_TARGETS)
ARCHIVED_EXTERNAL_MANAGEMENT = {
    **{node: address.replace(".216.", ".217.") for node, address in ROOT_NODES.items()},
    "r1": "172.30.217.14",
    "r2": "172.30.217.15",
}
EXTERNAL_LAB_NAME = "mlag-medium"
EXTERNAL_NODES = {node: address.replace(".217.", ".218.")
                  for node, address in ARCHIVED_EXTERNAL_MANAGEMENT.items()}
EXTERNAL_DEVICE_NAMES = {
    "p1": "dc1-core-mlag1",
    "p2": "dc1-core-mlag2",
    "witness": "dc1-access-switch1",
    "r1": "dc1-stp-root1",
    "r2": "dc1-stp-root2",
    "c1": "dc1-traffic-host1",
    "c2": "dc1-traffic-host2",
    "syslog": "dc1-syslog-collector",
}
ROOT_ATTACHMENTS = {"r1": "p1", "r2": "p2"}
ROOT_MACS = {"r1": "02:00:00:21:00:14", "r2": "02:00:00:21:00:15"}
EXTERNAL_LINKS = (
    *ROOT_LINKS,
    (("r1", "eth1"), ("p1", "eth4")),
    (("r2", "eth1"), ("p2", "eth4")),
)
EXTERNAL_PORTS = tuple(point for link in EXTERNAL_LINKS for point in link)
EXTERNAL_CAPTURES = tuple(sorted((*ROOT_CAPTURES, "witness-tap3", "p1-tap4", "p2-tap4", "r1-tap1", "r2-tap1")))
NO_STP_CASES = tuple(name for name in EXTERNAL_CASES if name.startswith("external-no-stp-"))
ALL_STP_OFF_CASES = tuple(name for name in EXTERNAL_CASES if name.startswith("external-all-stp-off-"))
PREFERRED_R1 = ("external-reboot-secondary", "external-combined-loss", "external-all-stp-off-reboot-secondary")


def preferred_root(name):
    return "r1" if name in PREFERRED_R1 else "r2"


def election_ids(preferred):
    backup = "r1" if preferred == "r2" else "r2"
    return f"0x0000.{ROOT_MACS[preferred]}", f"0x1000.{ROOT_MACS[backup]}"
