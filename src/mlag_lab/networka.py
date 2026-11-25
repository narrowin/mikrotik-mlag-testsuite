"""Device addresses and base state reads from the lab's Networka profiles."""

from functools import cache
from pathlib import Path

from network_toolkit import NetworkaClient

PROFILES = Path(__file__).resolve().parents[2] / "labs" / "networka"


@cache
def profile(name):
    return NetworkaClient(PROFILES / f"{name}.yml")


def addresses(name, devices):
    """Management address per runner node, from the device names in the given profile."""
    hosts = profile(name).devices
    return {node: hosts[device].host for node, device in devices.items()}


@cache
def reads(sequence):
    """The RouterOS commands of one lab sequence, in file order."""
    sequences = profile("small").sequence_manager.list_vendor_sequences("mikrotik_routeros")
    return tuple(sequences[sequence].commands)
