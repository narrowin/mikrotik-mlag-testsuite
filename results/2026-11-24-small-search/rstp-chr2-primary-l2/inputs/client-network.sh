#!/bin/sh
set -eu

host=$1
case "$host" in
    11|12|50) ;;
    *) printf 'Unknown lab host number: %s\n' "$host" >&2; exit 1 ;;
esac

if ! ip link show dev bond0 >/dev/null 2>&1; then
    if [ "$host" = 50 ]; then
        ip link add bond0 type bond mode active-backup miimon 100 num_grat_arp 1
    else
        ip link add bond0 type bond mode 802.3ad miimon 100 lacp_rate fast xmit_hash_policy layer2+3
    fi
fi

ip link set dev bond0 address "02:00:00:11:00:$host"
for member in eth1 eth2; do
    if [ ! -e "/sys/class/net/bond0/lower_$member" ]; then
        ip link set dev "$member" down
        ip link set dev "$member" master bond0
    fi
    ip link set dev "$member" up
done
ip address replace "10.110.0.$host/24" dev bond0
ip link set dev bond0 up

case "$host" in
    11|12)
        ip address replace "198.51.100.${host#1}/30" dev eth3
        ip link set dev eth3 up
        ;;
esac
