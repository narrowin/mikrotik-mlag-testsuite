#!/bin/sh
set -eu

# Host N is the node hostN and uses 1N as its address and MAC suffix.
n=$(hostname)
n=1${n#host}

# miimon 100 stops sending on a cut cable and lacp_rate fast matches the switches.
# The layer2+3 hash and the fixed MACs and addresses put each stream on the cable to the MLAG primaries in every run.
ip link add bond0 address "02:00:00:11:00:$n" type bond mode 802.3ad miimon 100 lacp_rate fast xmit_hash_policy layer2+3
# A cable joins a bond only while it is down.
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
done
ip address add "10.110.0.$n/24" dev bond0
ip link set bond0 up
# A permanent neighbour for the other host keeps the pinger sending while the switches drop traffic.
peer=$((23 - n))
ip neigh replace "10.110.0.$peer" lladdr "02:00:00:11:00:$peer" nud permanent dev bond0

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
