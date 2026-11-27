#!/bin/sh
set -eu

# Host N is the node hostN and uses 1N as its address and MAC suffix.
n=$(hostname)
n=1${n#host}

if [ "$n" = 11 ]; then
    # Host1 has one cable, to the access switch.
    port=eth1
    ip link set eth1 address "02:00:00:21:00:$n"
else
    # miimon 100 stops sending on a cut cable, lacp_rate fast matches the switches, and the fixed MAC keeps the bond's cable choice in every run.
    port=bond0
    ip link add bond0 address "02:00:00:21:00:$n" type bond mode 802.3ad miimon 100 lacp_rate fast xmit_hash_policy layer2+3
    # A cable joins a bond only while it is down.
    for cable in eth1 eth2; do
        ip link set "$cable" down
        ip link set "$cable" master bond0
        ip link set "$cable" up
    done
fi
ip address add "10.110.0.$n/24" dev "$port"
ip link set "$port" up
if [ "$port" = bond0 ]; then
    # The unknown-unicast flood probe needs a fixed MAC for an address no host answers.
    ip neigh replace 10.110.0.99 lladdr 02:00:00:21:00:99 nud permanent dev bond0
fi

# The bypass cable gives each host a /30 outside the switches.
ip address add "198.51.100.${n#1}/30" dev eth3
ip link set eth3 up

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
