#!/bin/bash
# Run suites one after another on one lab inside one OrbStack machine.
#
# Usage: labs/campaign.sh <lab> <campaign dir> <suite spec>...
#   lab         small | medium | medium-pair-root | medium-two-pair
#   suite spec  "<sub-folder>:<mlag-lab run arguments>", for example
#               "rstp-l2:--bridge-mode rstp --case calibration --case bond-member-loss"
#
# The lab runs from a copy of labs/ on the machine's own disk, because Containerlab writes
# clab-<name>/ and the syslog feed next to the topology file. The runner gets that copy with
# --lab-dir. Each suite writes to <campaign dir>/<sub-folder>. The script never destroys a lab.
#
# If the lab is already deployed, the script neither syncs nor redeploys: the deployment must come from the copy in
# MLAG_LABS_COPY, which is then used as it is. A lab deployed from another copy, for example
# /var/tmp/mlag-clean/labs, runs with MLAG_LABS_COPY=/var/tmp/mlag-clean/labs.
#
# Environment: MLAG_LABS_COPY (default /var/tmp/mlag-labs),
# UV_PROJECT_ENVIRONMENT (default /var/tmp/mlag-campaign-venv-<uid>), MLAG_SSH_PASSWORD.
set -euo pipefail

usage() {
    printf 'Usage: %s <small|medium|medium-pair-root|medium-two-pair> <campaign dir> <name:run arguments>...\n' \
        "$0" >&2
    exit 2
}
[ "$#" -ge 3 ] || usage
lab=$1
campaign_arg=$2
shift 2

case "$lab" in
    small) name=mlag-small topology=small/small.clab.yml ;;
    medium) name=mlag-medium topology=medium/medium.clab.yml ;;
    medium-pair-root) name=mlag-medium topology=medium/medium-pair-root.clab.yml ;;
    medium-two-pair) name=mlag-medium-two-pair topology=medium/medium-two-pair.clab.yml ;;
    *) usage ;;
esac
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

# The runner accepts only containers whose clab-topo-file label is this topology file.
deployed=$(as_root docker ps -a --filter "label=containerlab=$name" --format '{{.Label "clab-topo-file"}}' | sort -u)
if [ -n "$deployed" ]; then
    # A running lab keeps the copy it was deployed from untouched, for example one deployed from another local
    # copy such as MLAG_LABS_COPY=/var/tmp/mlag-clean/labs. Its topology, configs and syslog feed stay as deployed.
    printf 'Not syncing %s: %s is deployed, so the copy stays as it was deployed\n' "$labs" "$name"
else
    # Keep the copy's clab-* lab directories and syslog feeds; they belong to a running lab.
    printf 'Syncing %s/labs/ to %s/\n' "$repo" "$labs"
    if command -v rsync >/dev/null; then
        rsync -a --delete --exclude 'clab-*/' --exclude '*logs/' "$repo/labs/" "$labs/"
    else
        tar -C "$repo/labs" --exclude='clab-*' --exclude='*logs' -cf - . | tar -C "$labs" -xf -
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
else
    if ! as_root docker image inspect mlag-lab-endpoint:local >/dev/null 2>&1; then
        as_root docker build -f "$labs/shared/client.Dockerfile" -t mlag-lab-endpoint:local "$labs/shared"
    fi
    if ! as_root docker image inspect rsyslog/rsyslog:latest >/dev/null 2>&1; then
        as_root docker pull rsyslog/rsyslog:latest
    fi
    chr_image=$(cat "$labs/campaign-image.txt")
    syslog_image=$(as_root docker image inspect --format '{{index .RepoDigests 0}}' rsyslog/rsyslog:latest)
    printf '%s deploy started %s\n' "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    as_root env "MLAG_CHR_IMAGE=$chr_image" "MLAG_SYSLOG_IMAGE=$syslog_image" containerlab deploy -t "$topology"
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
            as_root docker exec "clab-mlag-small-$peer" /bin/sh /lab/forward-control.sh --wire
        done
        as_root docker exec clab-mlag-small-dc1-traffic-host1 ip neigh replace 10.110.0.12 \
            lladdr 02:00:00:11:00:12 nud permanent dev bond0
        as_root docker exec clab-mlag-small-dc1-traffic-host2 ip neigh replace 10.110.0.11 \
            lladdr 02:00:00:11:00:11 nud permanent dev bond0
    fi
    printf '%s deploy finished %s\n' "$name" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi

cd "$repo"
uv sync --locked
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
printf '=== campaign %s done %s\n' "$campaign" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit "$worst"
