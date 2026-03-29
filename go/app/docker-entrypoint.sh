#!/bin/sh
set -eu

app_bin="${APP_BIN:-/opt/app/app}"

if [ "$#" -eq 0 ]; then
    set -- "${app_bin}"
elif [ "${1#-}" != "$1" ]; then
    set -- "${app_bin}" "$@"
fi

exec "$@"
