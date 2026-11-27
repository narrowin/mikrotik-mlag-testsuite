#!/bin/sh
set -eu

case "$(hostname)" in
    host1) host=11 ;;
    host2) host=12 ;;
    mac-move-host) host=50 ;;
esac

# Check carrier every 100 ms. The LACP hosts match the switches' fast timers.
if [ "$host" = 50 ]; then
    ip link add bond0 address "02:00:00:11:00:$host" type bond mode active-backup miimon 100 num_grat_arp 1
else
    ip link add bond0 address "02:00:00:11:00:$host" type bond mode 802.3ad miimon 100 lacp_rate fast xmit_hash_policy layer2+3
fi
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
    ip link set "$cable" up
done
ip address add "10.110.0.$host/24" dev bond0
ip link set bond0 up

if [ "$host" = 50 ]; then
    ip link set bond0 type bond active_slave eth1
fi

# Keep the unknown-unicast probe readable without an ARP reply.
if [ "$host" = 11 ] && [ "${SMALL_MAC_MOVE_AGE:-5m}" = 5m ]; then
    ip neigh replace 10.110.0.99 lladdr 02:00:00:11:00:99 nud permanent dev bond0
fi

# The age case must deliver IP packets while the MAC-move host cannot answer ARP.
if [ "${SMALL_MAC_MOVE_AGE:-5m}" = 10s ]; then
    if [ "$host" = 50 ]; then
        for peer in 11 12; do
            ip neigh replace "10.110.0.$peer" lladdr "02:00:00:11:00:$peer" nud permanent dev bond0
        done
    else
        ip neigh replace 10.110.0.50 lladdr 02:00:00:11:00:50 nud permanent dev bond0
    fi
fi

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
