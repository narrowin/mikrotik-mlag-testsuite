#!/bin/sh
set -eu

case "${CLAB:-}" in
    /*) ;;
    *) echo "Set CLAB to the absolute path of the qualified Containerlab binary." >&2; exit 1 ;;
esac
if [ ! -f "$CLAB" ] || [ ! -x "$CLAB" ]; then
    echo "Containerlab is not executable at $CLAB" >&2
    exit 1
fi

# Use the default five-minute timer except when the host must age out during the 25 s silence.
case "${1:-}" in
    "") export SMALL_MOBILE_AGE=5m ;;
    age) export SMALL_MOBILE_AGE=10s ;;
    *) echo "Usage: $0 [age]" >&2; exit 1 ;;
esac

cd "$(dirname "$0")"
docker build -t small-mlag-client:local - < ../client.Dockerfile
mkdir -p clab-small-mlag-mobile/syslog
"$CLAB" deploy -t topology.clab.yml
