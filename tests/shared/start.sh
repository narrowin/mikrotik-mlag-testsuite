#!/bin/sh
# Deploy one lab: tests/shared/start.sh <lab-folder> [age]
set -eu

usage() { echo "Usage: $0 <lab-folder> [age]" >&2; exit 1; }
[ $# -ge 1 ] && [ $# -le 2 ] || usage
[ -f "$1/lab/topology.clab.yml" ] || { echo "No lab/topology.clab.yml in $1" >&2; exit 1; }

CLAB="$(cd "$(dirname "$0")" && pwd)/containerlab"

# Small-mac-move reads the MAC ageing timer. Use the default five minutes except when
# the host must age out during the 25 s silence of mac-age-relearn.
case "${2:-}" in
    "") SMALL_MAC_MOVE_AGE=5m ;;
    age) SMALL_MAC_MOVE_AGE=10s ;;
    *) usage ;;
esac
export SMALL_MAC_MOVE_AGE

# The host image needs no build context, so the Dockerfile comes on standard input.
docker build -t mlag-host:local - < "$(dirname "$0")/host.Dockerfile"
cd "$1/lab"
name=$(sed -n 's/^name: *//p' topology.clab.yml)
# Containerlab checks the collector bind path before it creates the node directory.
mkdir -p "clab-$name/syslog"
"$CLAB" deploy -t topology.clab.yml

# Return only when every host is ready: its host setup finished and its bond is up.
# A bond is up when each LACP member is in the active aggregator and in sync, collecting
# and distributing, or when an active-backup bond has an active member.
# Containers without host setup, such as the collector and the CHRs, are skipped.
setup_pending() {
    docker exec "$1" test -f /lab/host-setup.sh && ! docker exec "$1" test -f /run/host-setup.done
}
bond_down() {
    docker exec "$1" cat /proc/net/bonding/bond0 2>/dev/null | awk '
        # LACP port state bits 3, 4 and 5: in sync, collecting, distributing.
        function ready(state) { return int(state / 8) % 8 == 7 }
        /^Bonding Mode: fault-tolerance/ { ab = 1 }
        /^Currently Active Slave:/ { active = $4 }
        /^\tNumber of ports:/ { ports = $4 }
        /^Slave Interface:/ { members++; actor = 0 }
        /^details actor lacp pdu:/ { actor = 1 }
        actor && /port state:/ { if (ready($3)) ready_members++; actor = 0 }
        END {
            if (!members) exit 1
            if (ab) exit (active != "" && active != "None")
            exit (ports == members && ready_members == members)
        }'
}
deadline=$(($(date +%s) + 60))
for host in $(docker ps --filter "label=containerlab=$name" --format '{{.Names}}'); do
    while setup_pending "$host" || bond_down "$host"; do
        if [ "$(date +%s)" -ge "$deadline" ]; then
            if setup_pending "$host"; then
                echo "host setup of $host did not finish 60 s after deploy" >&2
            else
                echo "bond0 of $host is not up 60 s after deploy" >&2
            fi
            exit 1
        fi
        sleep 1
    done
done
