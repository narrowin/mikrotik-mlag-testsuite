"""QEMU monitor actions for one CHR, run as a child inside the CHR's network namespace.

This module imports only the standard library, so a timed fault action starts fast and needs no Networka.
"""

import json
import re
import socket
import sys
import time

QMP_PORT = 5001


def qmp_client(command, arguments=None):
    with socket.create_connection(("127.0.0.1", QMP_PORT), timeout=3) as conn, conn.makefile("rwb") as stream:
        if "QMP" not in json.loads(stream.readline()):
            raise RuntimeError("Invalid QEMU monitor greeting")
        action = {"execute": command, "id": 2}
        if arguments is not None:
            action["arguments"] = arguments
        for request in ({"execute": "qmp_capabilities", "id": 1}, action):
            started = time.time_ns()
            stream.write((json.dumps(request) + "\n").encode())
            stream.flush()
            while True:
                reply = json.loads(stream.readline())
                if reply.get("id") == request["id"]:
                    break
            if "return" not in reply:
                raise RuntimeError(f"QEMU rejected {request['execute']}: {reply}")
        print(json.dumps({"started_ns": started, "done_ns": time.time_ns(),
                          "request": request, "reply": reply}))


if __name__ == "__main__":
    if len(sys.argv) in (3, 4) and sys.argv[1] == "_qmp":
        action = sys.argv[2]
        nic = sys.argv[3] if len(sys.argv) == 4 else "nic2"
        if action in ("up", "down") and re.fullmatch(r"nic[1-4]", nic):
            qmp_client("set_link", {"name": nic, "up": action == "up"})
        elif action in ("stop", "cont", "query-status", "system_reset") and len(sys.argv) == 3:
            qmp_client(action)
        else:
            sys.exit(f"Unknown lab QMP action: {' '.join(sys.argv[2:])}")
