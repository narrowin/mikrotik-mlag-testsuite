# Networka reaches every lab node over SSH at the address containerlab assigned

Networka reads device state and runs commands on every testable node over SSH, switches and Linux hosts alike.
The Linux host image in `tests/shared/client.Dockerfile` runs `sshd` for that reason.
A lab's `devices.yml` holds only the device types and the lab logins.
Networka takes each node's management address from the `topology-data.json` that containerlab writes when it deploys the lab.
Host keys are neither checked nor stored: every `devices.yml` sets `ssh_known_hosts_file: /dev/null`.

## Why

On 2026-11-26 a plan had Networka fall back to `docker exec` for Linux nodes.
The operator rejected it: "it's overcomplicating things if you actually go with the Docker fallback."
In his view a node that is tested must run SSH and accept a login.
Committed addresses had been chosen on 2026-11-25 because replay needed them and two labs shared one deploy folder.
Now each lab has its own folder and management subnet, and replay reads the saved `topology-data.json`, so committed addresses only duplicate what containerlab already knows.
A lab is redeployed many times a day and gets new host keys each time, so a stored key only produces mismatches.
The operator called strict host-key checking in the lab pointless on 2026-11-25.

## Consequences

Every Linux image in a lab needs `sshd` and a root login with the password in `devices.yml`.
Adding a node needs no address in the inventory, only an entry named after the node.
Traffic, cable and capture actions still run on the lab host through `nsenter` as root, not over SSH; whether they must run as root was questioned and is not settled.
