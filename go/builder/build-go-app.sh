#!/bin/sh
set -eu

app_name="${1:-${APP_NAME:-}}"
output_dir="${GO_OUTPUT_DIR:-/out}"
binary_name="${GO_BINARY_NAME:-app}"
ldflags="${GO_LDFLAGS:--s -w}"

if [ -z "${app_name}" ]; then
    echo "APP_NAME is required" >&2
    exit 1
fi

mkdir -p "${output_dir}"

go build -v -trimpath -ldflags "${ldflags}" -o "${output_dir}/${binary_name}" "./cmd/${app_name}"

if [ -d "./configs" ]; then
    mkdir -p "${output_dir}/configs"
    cp -R "./configs/." "${output_dir}/configs/"
fi
