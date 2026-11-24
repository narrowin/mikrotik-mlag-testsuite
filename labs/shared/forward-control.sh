#!/bin/sh
set -eu

# The veth and TAP share a private two-port bridge. Pass STP, LACP and LLDP.
wire=no
if [ "${1:-}" = "--wire" ]; then
    wire=yes
    shift
fi
if [ "$#" -eq 0 ]; then
    set -- eth1 eth2 eth3 eth4 tap1 tap2 tap3 tap4
fi
for port do
    mask="/sys/class/net/$port/brport/group_fwd_mask"
    remaining=60
    until [ -w "$mask" ]; do
        if [ "$remaining" -eq 0 ]; then
            printf 'Missing bridge port for %s\n' "$port" >&2
            exit 1
        fi
        sleep 1
        remaining=$((remaining - 1))
    done
    printf '16389\n' > "$mask"
    if [ "$wire" = yes ]; then
        printf '0\n' > "${mask%/*}/learning"
    fi
done
