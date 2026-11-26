#!/bin/sh
# Give each virtual data port 10G full duplex, because without it the client bonds never use both cables.
for arg do
    shift
    case "$arg" in
        virtio-net,id=nic*) arg="$arg,speed=10000,duplex=full" ;;
    esac
    set -- "$@" "$arg"
done
exec "/usr/bin/${0##*/}" "$@"
