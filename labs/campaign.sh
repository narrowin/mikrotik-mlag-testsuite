#!/bin/bash
# Run suites one after another on one lab inside one OrbStack machine.
#
# Usage: labs/campaign.sh [--destroy] <lab> <campaign dir> <suite spec>...
#   --destroy   remove the lab at the end if this script deployed it; by default the lab stays up
#   lab         small | medium | medium-pair-root | medium-two-pair
#   suite spec  "<sub-folder>:<mlag-lab run arguments>", for example
#               "rstp-l2:--bridge-mode rstp --case calibration --case bond-member-loss"
#
# The lab runs from a copy of labs/ on the machine's own disk, because Containerlab writes
# clab-<name>/ and the syslog feed next to the topology file. The runner gets that copy with
# --lab-dir. Each suite writes to <campaign dir>/<sub-folder>.
#
# MLAG_INSTANCE (0 to 3, default 0) picks the lab instance. Instance 0 is the lab as named in its topology.
# Instance N runs as <name>-i<N> on the management subnet whose third octet is 10*N higher, from its own copy
# <MLAG_LABS_COPY>-i<N>, in which the RouterOS startup configs send syslog to that instance's collector.
#
# The copy is synced from the checkout only while no lab is deployed from it. If the lab is already deployed,
# the script neither syncs nor redeploys: the deployment must come from the copy, which is then used as it is.
# A lab deployed from another copy, for example /var/tmp/mlag-clean/labs, runs with
# MLAG_LABS_COPY=/var/tmp/mlag-clean/labs.
#
# Environment: MLAG_INSTANCE, MLAG_LABS_COPY (default /var/tmp/mlag-labs),
# UV_PROJECT_ENVIRONMENT (default /var/tmp/mlag-campaign-venv-<uid>), MLAG_SSH_PASSWORD.
set -euo pipefail

usage() {
    printf 'Usage: %s [--destroy] <small|medium|medium-pair-root|medium-two-pair> <campaign dir> <name:run arguments>...\n' \
        "$0" >&2
    exit 2
}
destroy=no
if [ "${1-}" = --destroy ]; then
    destroy=yes
    shift
fi
[ "$#" -ge 3 ] || usage
lab=$1
campaign_arg=$2
shift 2

# Base lab name and management subnet third octet of instance 0.
case "$lab" in
    small) name=mlag-small octet=215 topology=small/small.clab.yml ;;
    medium) name=mlag-medium octet=218 topology=medium/medium.clab.yml ;;
    medium-pair-root) name=mlag-medium-pair-root octet=216 topology=medium/medium-pair-root.clab.yml ;;
    medium-two-pair) name=mlag-medium-two-pair octet=219 topology=medium/medium-two-pair.clab.yml ;;
    *) usage ;;
esac
instance=${MLAG_INSTANCE:-0}
case "$instance" in
    0) ;;
    1|2|3) name=$name-i$instance ;;
    *) printf 'MLAG_INSTANCE must be 0, 1, 2 or 3, not %q\n' "$instance" >&2; exit 2 ;;
esac
export MLAG_INSTANCE=$instance
net=$((octet + 10 * instance))
if [ "$(uname -s)" != Linux ]; then
    printf 'Run this inside the OrbStack machine, for example: orb -m <machine> %s ...\n' "$0" >&2
    exit 2
fi
for spec in "$@"; do
    suite=${spec%%:*}
    if [ "$suite" = "$spec" ] || [ -z "$suite" ] || [[ "$suite" == */* ]]; then
        printf 'Suite spec %q needs the form <sub-folder>:<mlag-lab run arguments>\n' "$spec" >&2
        exit 2
    fi
done

as_root() {
    if [ "$(id -u)" -eq 0 ]; then "$@"; else sudo "$@"; fi
}

repo=$(cd "$(dirname "$0")/.." && pwd -P)
labs=${MLAG_LABS_COPY:-/var/tmp/mlag-labs}
if [ "$instance" -ne 0 ]; then labs=$labs-i$instance; fi
mkdir -p "$campaign_arg" "$labs"
campaign=$(cd "$campaign_arg" && pwd -P)
labs=$(cd "$labs" && pwd -P)
if [ "$labs" = "$repo/labs" ]; then
    printf 'MLAG_LABS_COPY must be a separate folder on this machine, not the checkout labs/ folder\n' >&2
    exit 2
fi
export PATH="$PATH:/usr/sbin:/sbin"
export UV_PROJECT_ENVIRONMENT=${UV_PROJECT_ENVIRONMENT:-/var/tmp/mlag-campaign-venv-$(id -u)}

topology="$labs/$topology"
# The topology files read these variables; every Containerlab call on this lab passes the same values.
lab_env=("MLAG_LAB_NAME=$name" "MLAG_MGMT_NET=$net")

# lock <fd> <file>: hold an exclusive lock on <file> through file descriptor <fd> until unlock <fd>.
lock() {
    [ -e "$2" ] || : > "$2"
    eval "exec $1<\"\$2\""
    flock "$1"
}
unlock() { eval "exec $1<&-"; }

# Campaigns started together share this copy's sync and deploy, the endpoint image and the uv environment.
lock 8 "$labs.lock"
# The runner accepts only containers whose clab-topo-file label is this topology file.
deployed=$(as_root docker ps -a --filter "label=containerlab=$name" --format '{{.Label "clab-topo-file"}}' | sort -u)
in_use=$(as_root docker ps -a --filter label=containerlab \
    --format '{{.Label "containerlab"}} {{.Label "clab-topo-file"}}' | awk -v copy="$labs/" \
    'index($2, copy) == 1 { print $1 }' | sort -u | tr '\n' ' ')
if [ -n "$in_use" ]; then
    # A running lab keeps the copy it was deployed from untouched, for example one deployed from another local
    # copy such as MLAG_LABS_COPY=/var/tmp/mlag-clean/labs. Its topology, configs and syslog feed stay as deployed.
    printf 'Not syncing %s: %sis deployed from it, so the copy stays as it was deployed\n' "$labs" "$in_use"
else
    # Keep the copy's clab-* lab directories and syslog feeds; they belong to a running lab.
    printf 'Syncing %s/labs/ to %s/\n' "$repo" "$labs"
    if command -v rsync >/dev/null; then
        rsync -a --delete --exclude 'clab-*/' --exclude '*logs/' "$repo/labs/" "$labs/"
    else
        tar -C "$repo/labs" --exclude='clab-*' --exclude='*logs' -cf - . | tar -C "$labs" -xf -
    fi
    if [ "$instance" -ne 0 ]; then
        # The startup configs name the collector and each CHR's syslog source address. The Networka profiles name
        # every node's management address. Move both to this instance.
        for config in small/small.rsc:215 medium/medium-pair-root.rsc:216 medium/medium.rsc:218 \
            medium/medium-two-pair.rsc:219 large/large.rsc:220 networka/small.yml:215 networka/medium.yml:218 \
            networka/medium-pair-root.yml:216 networka/medium-two-pair.yml:219 networka/large.yml:220; do
            base=${config#*:}
            sed -i "s/172\.30\.$base\./172.30.$((base + 10 * instance))./g" "$labs/${config%:*}"
        done
    fi
fi
mkdir -p "$labs/small/logs" "$labs/medium/logs" "$labs/medium/pair-root-logs" "$labs/medium/two-pair-logs"
if [ -n "$deployed" ]; then
    if [ "$(printf '%s\n' "$deployed" | wc -l)" -ne 1 ] || [ "$(realpath -m "$deployed")" != "$(realpath "$topology")" ]; then
        printf '%s is already deployed from %s, not from %s.\n' "$name" "${deployed//$'\n'/ and }" "$topology" >&2
        printf 'Pass that copy with MLAG_LABS_COPY=<folder that holds the topology>, or remove the lab yourself.\n' >&2
        exit 2
    fi
    stopped=$(as_root docker ps -a --filter "label=containerlab=$name" --format '{{.Names}} {{.State}}' \
        | grep -v ' running$' || true)
    if [ -n "$stopped" ]; then
        printf '%s is deployed from %s, but these containers are not running:\n%s\n' "$name" "$topology" "$stopped" >&2
        exit 2
    fi
    printf '%s is already running from %s\n' "$name" "$topology"
    if [ "$destroy" = yes ]; then
        printf 'Leaving %s deployed at the end: this script did not deploy it\n' "$name"
    fi
else
    lock 9 /var/tmp/mlag-campaign-setup.lock
    # Build every time: the cache makes it quick, and an image from an older Dockerfile would lack sshd.
    as_root docker build -f "$labs/shared/client.Dockerfile" -t mlag-lab-endpoint:local "$labs/shared"
    if ! as_root docker image inspect rsyslog/rsyslog:latest >/dev/null 2>&1; then
        as_root docker pull rsyslog/rsyslog:latest
    fi
    unlock 9
    chr_image=$(cat "$labs/campaign-image.txt")
    syslog_image=$(as_root docker image inspect --format '{{index .RepoDigests 0}}' rsyslog/rsyslog:latest)
    lab_env+=("MLAG_CHR_IMAGE=$chr_image" "MLAG_SYSLOG_IMAGE=$syslog_image")
    if [ "$destroy" = yes ]; then
        # Never destroy by --name: Containerlab re-reads the file without the variables and hits another lab.
        trap 'printf "%s destroy %s\n" "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
              as_root env "${lab_env[@]}" containerlab destroy -t "$topology" --cleanup' EXIT
    fi
    printf '%s deploy started %s\n' "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    as_root env "${lab_env[@]}" containerlab deploy -t "$topology"
    printf 'Waiting for every container with a health check to become healthy\n'
    for container in $(as_root docker ps --filter "label=containerlab=$name" --format '{{.Names}}'); do
        for attempt in $(seq 300); do
            health=$(as_root docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' \
                "$container")
            case "$health" in healthy|none) break ;; esac
            if [ "$attempt" -eq 300 ]; then
                printf '%s did not become healthy. Check its Docker logs.\n' "$container" >&2
                exit 2
            fi
            sleep 1
        done
    done
    if [ "$lab" = small ]; then
        # The Small lab wires its virtual cables and pins the probe neighbors after boot, as quickstart.sh does.
        for peer in dc1-core-mlag1 dc1-core-mlag2; do
            as_root docker exec "clab-$name-$peer" /bin/sh /lab/forward-control.sh --wire
        done
        as_root docker exec "clab-$name-dc1-traffic-host1" ip neigh replace 10.110.0.12 \
            lladdr 02:00:00:11:00:12 nud permanent dev bond0
        as_root docker exec "clab-$name-dc1-traffic-host2" ip neigh replace 10.110.0.11 \
            lladdr 02:00:00:11:00:11 nud permanent dev bond0
    fi
    printf '%s deploy finished %s\n' "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

unlock 8

cd "$repo"
lock 9 /var/tmp/mlag-campaign-setup.lock
uv sync --locked
unlock 9
worst=0
for spec in "$@"; do
    suite=${spec%%:*}
    read -r -a arguments <<< "${spec#*:}"
    printf '=== %s start %s\n' "$suite" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    status=0
    uv run --locked mlag-lab run --lab-dir "$labs" --output "$campaign/$suite" "${arguments[@]}" || status=$?
    printf '=== %s end %s exit %s\n' "$suite" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$status"
    if [ "$status" -gt "$worst" ]; then worst=$status; fi
done
printf '=== campaign %s (%s) done %s\n' "$campaign" "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$worst"
