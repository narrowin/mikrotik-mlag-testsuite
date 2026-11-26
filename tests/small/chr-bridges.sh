#!/bin/sh
set -eu

# Each data port of a CHR node is a veth and a QEMU tap on a small Linux bridge.
for port in eth1 eth2 eth3 eth4 tap1 tap2 tap3 tap4; do
    brport=/sys/class/net/$port/brport
    # QEMU creates the taps within seconds, so 60 s is ample.
    waited=0
    until [ -w "$brport/group_fwd_mask" ]; do
        if [ "$waited" -eq 60 ]; then
            echo "$port is not on a bridge after 60 s" >&2
            exit 1
        fi
        sleep 1
        waited=$((waited + 1))
    done
    # Pass STP (bit 0) and LACP (bit 2), which a Linux bridge drops.
    echo 5 > "$brport/group_fwd_mask"
    # A learning two-port bridge drops replies in this failover.
    echo 0 > "$brport/learning"
done
