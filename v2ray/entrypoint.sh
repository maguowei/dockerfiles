#!/bin/sh
set -eu

TEMPLATE="/opt/v2ray/etc/config.template.json"
CONFIG="/opt/v2ray/etc/config.json"

if [ ! -f "$CONFIG" ]; then
    # 用户未挂载 config.json,基于模板渲染
    if [ -z "${V2RAY_UUID:-}" ]; then
        V2RAY_UUID="$(cat /proc/sys/kernel/random/uuid)"
        echo "[v2ray] No V2RAY_UUID provided, generated: ${V2RAY_UUID}"
    else
        echo "[v2ray] Using V2RAY_UUID from environment: ${V2RAY_UUID}"
    fi
    sed "s/{uuid}/${V2RAY_UUID}/g" "$TEMPLATE" > "$CONFIG"
    echo "[v2ray] VMess UUID: ${V2RAY_UUID}"
else
    # 用户挂载或上次启动已渲染过
    echo "[v2ray] Using existing config at ${CONFIG}; V2RAY_UUID is ignored."
    if grep -q '{uuid}' "$CONFIG" 2>/dev/null; then
        echo "[v2ray] WARNING: '{uuid}' placeholder still present in ${CONFIG}; v2ray will likely fail to start."
    fi
fi

exec v2ray "$@"
