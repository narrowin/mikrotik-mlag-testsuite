#!/bin/sh
# Deploy one lab: tests/shared/start.sh <lab-folder> [age]
set -eu

usage() { echo "Usage: $0 <lab-folder> [age]" >&2; exit 1; }
[ $# -ge 1 ] && [ $# -le 2 ] || usage
[ -f "$1/lab/topology.clab.yml" ] || { echo "No lab/topology.clab.yml in $1" >&2; exit 1; }

case "${CLAB:-}" in
    /*) ;;
    *) echo "Set CLAB to the absolute path of the qualified Containerlab binary." >&2; exit 1 ;;
esac
if [ ! -f "$CLAB" ] || [ ! -x "$CLAB" ]; then
    echo "Containerlab is not executable at $CLAB" >&2
    exit 1
fi

# Small-mobile reads the MAC ageing timer. Use the default five minutes except when
# the host must age out during the 25 s silence of mac-age-relearn.
case "${2:-}" in
    "") SMALL_MOBILE_AGE=5m ;;
    age) SMALL_MOBILE_AGE=10s ;;
    *) usage ;;
esac
export SMALL_MOBILE_AGE

# The host image needs no build context, so the Dockerfile comes on standard input.
docker build -t small-mlag-client:local - < "$(dirname "$0")/client.Dockerfile"
cd "$1/lab"
name=$(sed -n 's/^name: *//p' topology.clab.yml)
# Containerlab checks the collector bind path before it creates the node directory.
mkdir -p "clab-$name/syslog"
"$CLAB" deploy -t topology.clab.yml

# Return only when every host bond is up: each LACP member in the active aggregator
# and in sync, collecting and distributing, or an active-backup bond with an active member.
# Containers without bond0, such as the collector and the CHRs, are skipped.
bond_down() {
    docker exec "$1" cat /proc/net/bonding/bond0 2>/dev/null | awk '
        /^Bonding Mode: fault-tolerance/ { ab = 1 }
        /^Currently Active Slave:/ { active = $4 }
        /^\tNumber of ports:/ { ports = $4 }
        /^Slave Interface:/ { slaves++; actor = 0 }
        /^details actor lacp pdu:/ { actor = 1 }
        actor && /port state:/ { if (int($3 / 8) % 8 == 7) synced++; actor = 0 }
        END {
            if (!slaves) exit 1
            if (ab) exit (active != "" && active != "None")
            exit (ports == slaves && synced == slaves)
        }'
}
deadline=$(($(date +%s) + 60))
for host in $(docker ps --filter "label=containerlab=$name" --format '{{.Names}}'); do
    while bond_down "$host"; do
        if [ "$(date +%s)" -ge "$deadline" ]; then
            echo "bond0 of $host is not up 60 s after deploy" >&2
            exit 1
        fi
        sleep 1
    done
done
