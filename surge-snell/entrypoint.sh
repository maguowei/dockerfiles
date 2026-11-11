#!/usr/bin/env bash
set -euo pipefail

PSK="${1:-}"

if [ -z "$PSK" ]; then
    echo "Usage: $0 <psk>" >&2
    exit 1
fi

PSK_LEN=$(printf %s "$PSK" | wc -c | tr -d ' ')
if [ "$PSK_LEN" -lt 12 ] || [ "$PSK_LEN" -gt 255 ]; then
    echo "Error: PSK length must be between 12 and 255 bytes (got ${PSK_LEN})." >&2
    exit 1
fi

PSK_ESCAPED=$(printf '%s' "$PSK" | sed -e 's/[\/&]/\\&/g')
sed -i "s/fill_psk/${PSK_ESCAPED}/g" /etc/snell/snell-server.conf
cat /etc/snell/snell-server.conf
exec snell-server -c /etc/snell/snell-server.conf
