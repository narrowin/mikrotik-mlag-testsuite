#!/bin/sh
set -eu

case "${CLAB:-}" in
    /*) ;;
    *)
        echo "Set CLAB to the absolute path of the qualified Containerlab binary." >&2
        exit 1
        ;;
esac
if [ ! -f "$CLAB" ] || [ ! -x "$CLAB" ]; then
    echo "Containerlab is not executable at $CLAB" >&2
    exit 1
fi

cd "$(dirname "$0")"

# The Small lab's host image serves both hosts. It needs no build context, so the Dockerfile comes on standard input.
docker build -t small-mlag-client:local - < ../small/client.Dockerfile
# Containerlab checks the collector bind path before it creates the node directory.
mkdir -p clab-medium-mlag/syslog
"$CLAB" deploy -t topology.clab.yml
