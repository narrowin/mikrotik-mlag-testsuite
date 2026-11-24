#!/bin/sh
set -eu

case "$(uname -sm)" in
    'Linux aarch64'|'Linux x86_64') ;;
    *)
        printf 'Open the repository in GitHub Codespaces or run on ARM64 or x86-64 Linux. See Quick start in README.md.\n' >&2
        exit 2
        ;;
esac

cd "$(dirname "$0")/../.."
topology=labs/small/small.clab.yml
existing=$(sudo docker ps -aq --filter label=containerlab=mlag-small)
if [ -n "$existing" ]; then
    printf 'mlag-small already exists. Use the operator guide to run cases on it, or remove it before starting fresh.\n' >&2
    exit 2
fi

# OrbStack can share the macOS checkout. Use a Linux-only environment there.
case "$(pwd -P)" in
    /Users/*) export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-/var/tmp/mlag-lab-venv-$(id -u)}" ;;
esac
uv sync --locked
sudo docker build -f labs/shared/client.Dockerfile -t mlag-lab-endpoint:local labs/shared
chr_image=$(cat labs/campaign-image.txt)
sudo env "MLAG_CHR_IMAGE=$chr_image" containerlab deploy -t "$topology"

printf 'Waiting for RouterOS and preparing the probe path.\n'
boot_timeout=300
for peer in dc1-core-mlag1 dc1-core-mlag2; do
    container="clab-mlag-small-$peer"
    for attempt in $(seq "$boot_timeout"); do
        health=$(sudo docker inspect --format '{{.State.Health.Status}}' "$container")
        [ "$health" = healthy ] && break
        if [ "$attempt" -eq "$boot_timeout" ]; then
            printf '%s did not become healthy. Check its Docker logs.\n' "$container" >&2
            exit 2
        fi
        sleep 1
    done
    sudo docker exec "$container" /bin/sh /lab/forward-control.sh --wire
done

# Keep the clients sending unicast probes even when ARP cannot cross the lab.
sudo docker exec clab-mlag-small-dc1-traffic-host1 ip neigh replace 10.110.0.12 \
    lladdr 02:00:00:11:00:12 nud permanent dev bond0
sudo docker exec clab-mlag-small-dc1-traffic-host2 ip neigh replace 10.110.0.11 \
    lladdr 02:00:00:11:00:11 nud permanent dev bond0

output="test-results/$(date -u +%Y%m%dT%H%M%SZ)"
status=0
uv run --locked mlag-lab run --case baseline --output "$output" || status=$?
if [ -f "$output/README.md" ]; then
    printf 'Report: %s/README.md\n' "$output"
fi
exit "$status"
