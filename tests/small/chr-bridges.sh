#!/bin/sh
set -eu

# Each data veth on a CHR has a numbered QEMU tap on the same Linux bridge.
for eth in /sys/class/net/eth[1-9]*; do
    for port in "${eth##*/}" "tap${eth##*eth}"; do
        brport=/sys/class/net/$port/brport
        # QEMU creates taps during boot. Poll once a second for up to a minute.
        waited=0
        until [ -w "$brport/group_fwd_mask" ]; do
            if [ "$waited" -eq 60 ]; then
                echo "$port is not on a bridge after 60 s" >&2
                exit 1
            fi
            sleep 1
            waited=$((waited + 1))
        done
        # Pass LACP (bit 2) and make accidental BPDUs (bit 0) visible to the peer.
        echo 5 > "$brport/group_fwd_mask"
        # Forward between the tap and veth like a cable, regardless of where a client MAC was learned.
        echo 0 > "$brport/learning"
    done
done
