#!/bin/bash
# Run several campaign.sh campaigns at once inside one OrbStack machine, each on its own lab instance.
#
# Usage: labs/parallel.sh [--destroy] <instance> <campaign.sh arguments> [-- <instance> <campaign.sh arguments>]...
#   --destroy   passed to every campaign.sh: each removes the lab it deployed at the end
#   instance    MLAG_INSTANCE of that campaign, 0 to 3
#
# Example, Small instances 1 and 2 and Medium instance 1:
#   labs/parallel.sh --destroy \
#     1 small /var/tmp/c-small-1 "baseline:--bridge-mode none --case baseline" -- \
#     2 small /var/tmp/c-small-2 "baseline:--bridge-mode none --case baseline" -- \
#     1 medium /var/tmp/c-medium-1 "stp-off:--case medium-stp-off-baseline"
#
# Each campaign writes its console output to <campaign dir>/console.log. The script waits for all of them,
# prints one PASS or FAIL line per campaign and exits 1 if any campaign failed.
set -euo pipefail

usage() {
    printf 'Usage: %s [--destroy] <instance> <lab> <campaign dir> <name:run arguments>... [-- <instance> ...]...\n' \
        "$0" >&2
    exit 2
}
options=()
if [ "${1-}" = --destroy ]; then
    options=(--destroy)
    shift
fi
[ "$#" -ge 4 ] || usage

# Split the arguments into campaigns at each --: campaign i is args[starts[i]] and the lengths[i] - 1 that follow.
args=("$@" --)
starts=()
lengths=()
first=0
for index in "${!args[@]}"; do
    if [ "${args[$index]}" = -- ]; then
        starts+=("$first")
        lengths+=("$((index - first))")
        first=$((index + 1))
    fi
done

# One lab instance and one campaign folder per campaign.
seen=" "
for index in "${!starts[@]}"; do
    fields=("${args[@]:${starts[$index]}:${lengths[$index]}}")
    [ "${#fields[@]}" -ge 4 ] || usage
    case "${fields[0]}" in
        0|1|2|3) ;;
        *) printf 'Instance must be 0, 1, 2 or 3, not %q\n' "${fields[0]}" >&2; exit 2 ;;
    esac
    for item in "${fields[1]}-i${fields[0]}" "folder:${fields[2]}"; do
        if [[ "$seen" == *" $item "* ]]; then
            printf 'Two campaigns use %s. Give each campaign its own lab instance and campaign folder.\n' "$item" >&2
            exit 2
        fi
        seen+="$item "
    done
done

here=$(cd "$(dirname "$0")" && pwd -P)
pids=()
for index in "${!starts[@]}"; do
    fields=("${args[@]:${starts[$index]}:${lengths[$index]}}")
    mkdir -p "${fields[2]}"
    log="${fields[2]}/console.log"
    MLAG_INSTANCE=${fields[0]} "$here/campaign.sh" "${options[@]}" "${fields[@]:1}" > "$log" 2>&1 &
    pids+=("$!")
    printf 'Started instance %s %s, PID %s, console %s\n' "${fields[0]}" "${fields[1]}" "$!" "$log"
done

failed=0
for index in "${!starts[@]}"; do
    fields=("${args[@]:${starts[$index]}:${lengths[$index]}}")
    status=0
    wait "${pids[$index]}" || status=$?
    verdict=PASS
    if [ "$status" -ne 0 ]; then verdict=FAIL failed=1; fi
    printf '%s instance %s %s: exit %s, results %s\n' "$verdict" "${fields[0]}" "${fields[1]}" "$status" \
        "$(cd "${fields[2]}" && pwd -P)"
done
exit "$failed"
