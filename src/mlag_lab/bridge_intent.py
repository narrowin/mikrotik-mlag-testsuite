"""Collect and check the RouterOS bridge-port forwarding intent."""

from dataclasses import asdict, dataclass
import json
import re
from subprocess import SubprocessError


PORT_STATS = ":put [:serialize to=json options=json.no-string-conversion [/interface/bridge/port/print stats as-value]]"
PORT_MONITOR = ":put [:serialize to=json options=json.no-string-conversion [/interface/bridge/port/monitor {} once as-value]]"


@dataclass(frozen=True)
class BridgePortIntent:
    node: str
    bridge: str
    port: str
    forwarding: bool

    @property
    def target(self):
        return f"{self.node}:{self.bridge}/{self.port}"


def port_id(intent, raw):
    rows = json.loads(raw)
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("bridge-port statistics must be a JSON array of objects")
    selected = [row for row in rows if row.get("bridge") == intent.bridge and row.get("interface") == intent.port]
    if len(selected) != 1:
        raise ValueError(f"expected one bridge-port record, found {len(selected)}")
    identity = selected[0].get(".id")
    if not isinstance(identity, str) or not re.fullmatch(r"\*[0-9a-fA-F]+", identity):
        raise ValueError("bridge port has no valid RouterOS .id")
    if sum(row.get(".id") == identity for row in rows) != 1:
        raise ValueError("bridge port .id is ambiguous")
    return identity


def collect_bridge_port_replies(read, intents):
    """Keep the exact command and reply from each read for offline replay."""
    replies = {}
    for intent in intents:
        stats = {"command": PORT_STATS}
        replies[intent.target] = evidence = {"stats": stats}
        try:
            stats["raw"] = read(intent.node, PORT_STATS)
            identity = port_id(intent, stats["raw"])
            monitor = {"command": PORT_MONITOR.format(identity)}
            evidence["monitor"] = monitor
            monitor["raw"] = read(intent.node, monitor["command"])
        except (OSError, RuntimeError, SubprocessError, TypeError, ValueError) as error:
            evidence["error"] = str(error)
    return replies


def bridge_port_verdicts(intents, replies):
    verdicts = []
    for intent in intents:
        result = {**asdict(intent), "observed": None, "verdict": "unavailable"}
        try:
            evidence = replies[intent.target]
            if "error" in evidence:
                raise ValueError(evidence["error"])
            stats, monitor = evidence["stats"], evidence["monitor"]
            if stats["command"] != PORT_STATS:
                raise ValueError("unexpected bridge-port statistics command")
            identity = port_id(intent, stats["raw"])
            if monitor["command"] != PORT_MONITOR.format(identity):
                raise ValueError("monitor command does not select the recorded port .id")
            port = json.loads(monitor["raw"])
            if not isinstance(port, dict) or port.get(".id") != identity:
                raise ValueError("monitor reply does not identify the selected port")
            observed = port.get("forwarding")
            if not isinstance(observed, bool):
                raise ValueError("monitor forwarding is missing or is not a JSON boolean")
            result["observed"] = observed
            result["verdict"] = "match" if observed is intent.forwarding else "mismatch"
        except KeyError:
            result["reason"] = "missing bridge-port capture evidence"
        except (TypeError, ValueError) as error:
            result["reason"] = str(error)
        verdicts.append(result)
    return verdicts


def bridge_port_detail(result):
    target = f"{result['node']}:{result['bridge']}/{result['port']}"
    detail = (f"Bridge-port intent {target} forwarding expected {result['forwarding']!r}, "
              f"observed {result['observed']!r} ({result['verdict']})")
    return f"{detail}: {result['reason']}" if "reason" in result else detail
