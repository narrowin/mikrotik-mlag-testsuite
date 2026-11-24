#!/bin/sh
# Advertise speed and full duplex to RouterOS on the virtual data NICs.
for arg do
    shift
    case "$arg" in
        virtio-net,id=nic*) arg="$arg,speed=10000,duplex=full" ;;
    esac
    set -- "$@" "$arg"
done
exec /usr/bin/qemu-system-aarch64 "$@"
