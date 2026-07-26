#!/bin/sh
# Apple container machine 首次启动时以 root 运行，接管默认用户创建逻辑。
# 注入的环境变量：CONTAINER_USER / CONTAINER_UID / CONTAINER_GID / CONTAINER_HOME / CONTAINER_MACHINE_ID
# 目的：让新建用户默认登录 shell 为 zsh，并带上 base 的 .zshrc（经由 /etc/skel）。
set -eu

# 幂等：用户已存在则直接退出（钩子在首次启动只应生效一次）
if id "$CONTAINER_USER" >/dev/null 2>&1; then
    exit 0
fi

# GID 可能已被占用（如 macOS staff gid 20 撞 Ubuntu dialout）：已存在则复用，否则新建同名组
if ! getent group "$CONTAINER_GID" >/dev/null 2>&1; then
    groupadd -g "$CONTAINER_GID" "$CONTAINER_USER"
fi

# -m 拷贝 /etc/skel（含 .zshrc）到 home；-s 定死登录 shell 为 zsh，绕过默认硬编码的 bash
useradd -u "$CONTAINER_UID" -g "$CONTAINER_GID" -d "$CONTAINER_HOME" -m -s /usr/bin/zsh "$CONTAINER_USER"

# 免密 sudo，对齐 Apple 默认 provisioning 行为
echo "$CONTAINER_USER ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/$CONTAINER_USER"
chmod 0440 "/etc/sudoers.d/$CONTAINER_USER"
