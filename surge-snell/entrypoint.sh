#!/usr/bin/env bash

PSK=$1
sed -i "s/fill_psk/${PSK}/g" /etc/snell/snell-server.conf
cat /etc/snell/snell-server.conf
snell-server -c /etc/snell/snell-server.conf