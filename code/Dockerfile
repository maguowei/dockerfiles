FROM maguowei/base:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/code"

# Apple Container Machine 支持：告知 systemd 运行于容器环境
ENV container=container

# 补齐 container machine 所需组件（base 已含 curl/wget/vim/net-tools/iputils-ping）
# systemd + systemd-sysv 提供 /sbin/init（container machine 的唯一硬性要求）
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    systemd \
    systemd-sysv \
    dbus \
    openssh-server \
    iproute2 \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# systemd 容器化配置：清空 machine-id（首启生成）、设默认 target、屏蔽容器中无意义的单元、调整 sshd
# networkd-dispatcher 在精简安装下未安装，故用 mask（对不存在单元亦安全幂等）替代 disable
RUN >/etc/machine-id \
    && >/var/lib/dbus/machine-id \
    && systemctl set-default multi-user.target \
    && systemctl mask \
        dev-hugepages.mount \
        sys-fs-fuse-connections.mount \
        systemd-update-utmp.service \
        systemd-tmpfiles-setup.service \
        console-getty.service \
        networkd-dispatcher.service \
    && sed -i -e 's/^AcceptEnv LANG LC_\*$/#AcceptEnv LANG LC_*/' /etc/ssh/sshd_config

# container machine 用户默认使用 zsh：把 base 的 .zshrc 铺进 /etc/skel（新用户 home 模板），
# 并安装自定义 provisioning 钩子，把登录 shell 设为 zsh（默认 provisioner 硬编码 bash）
RUN cp /root/.zshrc /etc/skel/.zshrc
COPY create-user.sh /etc/machine/create-user.sh
RUN chmod +x /etc/machine/create-user.sh

# AI 编程工具（npm 全局安装）
RUN npm install -g \
    @anthropic-ai/claude-code \
    opencode-ai \
    @openai/codex

CMD ["zsh"]
