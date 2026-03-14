FROM ubuntu:26.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/base"
LABEL version="26.04"

# Layer 1: 系统基础 - locale、时区配置
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    apt-utils \
    locales \
    && locale-gen zh_CN.UTF-8 && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV TZ=Asia/Shanghai

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    tzdata \
    && echo $TZ > /etc/timezone \
    && rm /etc/localtime \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# Layer 2: 基础系统工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    htop \
    iputils-ping \
    jq \
    net-tools \
    openssh-client \
    tmux \
    tree \
    unzip \
    vim \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Layer 3: Node.js 22 LTS（通过 NodeSource 官方脚本安装）
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

ENV NODE_PATH=/usr/local/lib/node_modules

# Layer 4: 现代 CLI 工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ripgrep \
    fd-find \
    bat \
    fzf \
    zoxide \
    && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
    && ln -sf /usr/bin/batcat /usr/local/bin/bat \
    && rm -rf /var/lib/apt/lists/*

# 安装 eza（通过官方 apt 仓库，gnupg 用完即删）
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gnupg \
    && mkdir -p /etc/apt/keyrings \
    && wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
    | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
    | tee /etc/apt/sources.list.d/gierens.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends eza \
    && apt-get remove -y gnupg && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Layer 5: zsh 生态
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    zsh \
    && rm -rf /var/lib/apt/lists/*

# 安装 oh-my-zsh 及 zsh 补全插件
RUN mkdir -p /opt/zsh \
    && git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git /opt/zsh/oh-my-zsh \
    && git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions /opt/zsh/zsh-autosuggestions \
    && git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting /opt/zsh/zsh-syntax-highlighting \
    && git clone --depth=1 https://github.com/zsh-users/zsh-completions /opt/zsh/zsh-completions

# 安装 starship prompt（amd64/arm64 均有 musl 版本）
RUN ARCH=$(uname -m) && \
    curl -fsSL "https://github.com/starship/starship/releases/latest/download/starship-${ARCH}-unknown-linux-musl.tar.gz" \
    | tar -xz -C /usr/local/bin

# Layer 6: Python 3.14（ubuntu:26.04 原生提供）
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3.14 \
    python3.14-dev \
    python3.14-venv \
    && ln -sf /usr/bin/python3.14 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.14 /usr/local/bin/python3 \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv 包管理器
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

# Layer 7: Go（主版本钉选，补丁自动跟进）
ARG GO_MAJOR=1.26
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
        x86_64)  GOARCH="amd64" ;; \
        aarch64) GOARCH="arm64" ;; \
    esac && \
    GO_VERSION=$(curl -fsSL "https://go.dev/dl/?mode=json" | \
        jq -r --arg major "${GO_MAJOR}" \
        '[.[] | select(.stable == true) | .version | select(startswith("go" + $major + "."))] | first') && \
    echo "Installing Go version: ${GO_VERSION}" && \
    curl -fsSL "https://go.dev/dl/${GO_VERSION}.linux-${GOARCH}.tar.gz" \
    | tar -xz -C /usr/local

ENV GOPATH=/root/go
ENV GOPROXY=https://goproxy.cn,direct

ENV PATH="/root/.local/bin:/usr/local/go/bin:/root/go/bin:$PATH"
ENV SHELL=/bin/zsh

# 复制 zsh 默认配置文件
COPY .zshrc /root/.zshrc

CMD ["zsh"]
