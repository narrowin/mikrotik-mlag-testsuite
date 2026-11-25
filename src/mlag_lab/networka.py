"""Device addresses and base state reads from the lab's Networka profiles."""

from functools import cache
import os
from pathlib import Path

from network_toolkit import NetworkaClient

PROFILES = Path(__file__).resolve().parents[2] / "labs" / "networka"


def read_instance():
    """MLAG_INSTANCE: 0 is the base lab; 1 to 3 run beside it with their own lab name and management subnet."""
    value = os.environ.get("MLAG_INSTANCE", "0") or "0"
    if value not in ("0", "1", "2", "3"):
        raise SystemExit(f"MLAG_INSTANCE must be 0, 1, 2 or 3, not {value!r}")
    return int(value)


INSTANCE = read_instance()


def lab_name(base):
    """The Containerlab name of this instance: the base name for instance 0, otherwise <base>-i<N>."""
    return base if INSTANCE == 0 else f"{base}-i{INSTANCE}"


def shift(address, steps=INSTANCE):
    """Move a management address to another instance: each instance adds 10 to the third octet."""
    first, second, third, host = address.split(".")
    return f"{first}.{second}.{int(third) + 10 * steps}.{host}"


def recorded(nodes, manifest):
    """Node addresses of the instance a saved attempt ran on; attempts without a record ran on instance 0."""
    steps = manifest.get("instance", 0) - INSTANCE
    return {node: shift(address, steps) for node, address in nodes.items()}


@cache
def profile(name):
    return NetworkaClient(PROFILES / f"{name}.yml")


def addresses(name, devices):
    """Management address per runner node of this instance, from the device names in the given profile."""
    hosts = profile(name).devices
    return {node: shift(hosts[device].host) for node, device in devices.items()}


@cache
def reads(sequence):
    """The RouterOS commands of one lab sequence, in file order."""
    sequences = profile("small").sequence_manager.list_vendor_sequences("mikrotik_routeros")
    return tuple(sequences[sequence].commands)
