# code 镜像实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建 `maguowei/code` Docker 镜像，集成 Claude Code、OpenCode、Codex 三大 AI 工具，以及现代化 zsh 终端生态和常用开发工具。

**Architecture:** 单层 Dockerfile，基于 ubuntu:26.04，按逻辑分组 RUN 指令（系统基础 → Node.js → AI 工具 → CLI 工具 → zsh 生态 → Python 3.14 → 配置文件）。配置文件（.zshrc、starship.toml）作为独立文件 COPY 进镜像，便于维护。

**Tech Stack:** ubuntu:26.04, Node.js 22 LTS, Python 3.14, zsh + oh-my-zsh + starship + zoxide, @anthropic-ai/claude-code + opencode-ai + @openai/codex, eza/bat/fd/ripgrep/fzf

---

## Task 1：创建目录结构和配置文件

**Files:**
- Create: `code/.zshrc`
- Create: `code/starship.toml`

### Step 1：创建 code/ 目录

```bash
mkdir -p code
```

### Step 2：创建 `.zshrc`

创建 `code/.zshrc`，内容如下：

```zsh
# oh-my-zsh
export ZSH=/opt/zsh/oh-my-zsh
ZSH_THEME=""
plugins=(git)
source $ZSH/oh-my-zsh.sh

# zsh 补全初始化
autoload -Uz compinit
compinit

# 补全插件
source /opt/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fpath=(/opt/zsh/zsh-completions/src $fpath)

# starship prompt
eval "$(starship init zsh)"

# zoxide（z 命令跳转目录）
eval "$(zoxide init zsh)"

# 工具别名
alias ls='eza --icons'
alias ll='eza -lh --icons --git'
alias la='eza -lah --icons --git'
alias lt='eza --tree --icons'
alias cat='bat --paging=never'
alias find='fd'
alias grep='rg'
```

### Step 3：创建 `starship.toml`

创建 `code/starship.toml`，内容如下：

```toml
# 简洁风格：显示目录、git、Node.js、Python、执行时间
format = """
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$cmd_duration\
$line_break\
$character"""

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = " "

[git_status]
format = '([\[$all_status$ahead_behind\]]($style) )'

[nodejs]
symbol = " "
format = "[$symbol($version)]($style) "

[python]
symbol = " "
format = "[$symbol($version)]($style) "

[cmd_duration]
min_time = 2000
format = "took [$duration]($style) "

[character]
success_symbol = "[❯](green)"
error_symbol = "[❯](red)"
```

### Step 4：提交配置文件

```bash
git add code/.zshrc code/starship.toml
git commit -m "feat: add zsh and starship config for code image"
```

---

## Task 2：编写 Dockerfile

**Files:**
- Create: `code/Dockerfile`

### Step 1：创建 `code/Dockerfile`

```dockerfile
FROM ubuntu:26.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/code"

# Layer 1: 系统基础 - locale、时区、基础工具
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

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    vim \
    jq \
    unzip \
    make \
    build-essential \
    iputils-ping \
    net-tools \
    openssh-client \
    tmux \
    tree \
    htop \
    software-properties-common \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Layer 2: Node.js 22 LTS（NodeSource 官方脚本）
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Layer 3: AI 工具（npm global）
RUN npm install -g \
    @anthropic-ai/claude-code \
    opencode-ai \
    @openai/codex

# Layer 4: 现代 CLI 工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ripgrep \
    fd-find \
    bat \
    fzf \
    zoxide \
    htop \
    && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
    && ln -sf /usr/bin/batcat /usr/local/bin/bat \
    && rm -rf /var/lib/apt/lists/*

# 安装 eza（eza 官方 apt 仓库）
RUN wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
    | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
    | tee /etc/apt/sources.list.d/gierens.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y eza \
    && rm -rf /var/lib/apt/lists/*

# Layer 5: zsh 生态
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    zsh \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/zsh \
    && git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git /opt/zsh/oh-my-zsh \
    && git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions /opt/zsh/zsh-autosuggestions \
    && git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting /opt/zsh/zsh-syntax-highlighting \
    && git clone --depth=1 https://github.com/zsh-users/zsh-completions /opt/zsh/zsh-completions

# 安装 starship（官方脚本）
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes

# Layer 6: Python 3.14
# ubuntu:26.04 若已提供 python3.14 则直接安装，否则通过 deadsnakes PPA 安装
RUN apt-get update && \
    (DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.14 python3.14-dev python3.14-venv 2>/dev/null \
    || (DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common \
        && add-apt-repository ppa:deadsnakes/ppa -y \
        && apt-get update \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
            python3.14 python3.14-dev python3.14-venv)) \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.14 \
    && ln -sf /usr/bin/python3.14 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.14 /usr/local/bin/python3

ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple/

# Layer 7: 配置文件
RUN mkdir -p /root/.config
COPY .zshrc /root/.zshrc
COPY starship.toml /root/.config/starship.toml

ENV SHELL=/bin/zsh
ENV NODE_PATH=/usr/local/lib/node_modules

CMD ["zsh"]
```

### Step 2：提交 Dockerfile

```bash
git add code/Dockerfile
git commit -m "feat: add Dockerfile for code image"
```

---

## Task 3：本地构建验证

> 此步骤验证 Dockerfile 能够成功构建，并且工具都可正常使用。

### Step 1：本地构建镜像

```bash
docker build -t maguowei/code:local code/
```

期望：构建成功，无报错退出。

### Step 2：验证 AI 工具

```bash
docker run --rm maguowei/code:local zsh -c "claude --version && echo 'claude ok'"
docker run --rm maguowei/code:local zsh -c "opencode --version && echo 'opencode ok'"
docker run --rm maguowei/code:local zsh -c "codex --version && echo 'codex ok'"
```

期望：每个命令输出版本号并打印 `ok`。

### Step 3：验证 CLI 工具

```bash
docker run --rm maguowei/code:local zsh -c "
  rg --version | head -1 &&
  fd --version &&
  bat --version &&
  fzf --version &&
  eza --version &&
  zoxide --version &&
  starship --version &&
  python --version &&
  node --version &&
  echo 'all tools ok'
"
```

期望：所有工具输出版本号，最后打印 `all tools ok`。

### Step 4：验证 zsh 配置

```bash
docker run --rm maguowei/code:local zsh -i -c "echo shell_ok"
```

期望：输出 `shell_ok`，无报错。

---

## Task 4：添加 Makefile 目标

**Files:**
- Modify: `Makefile`

### Step 1：在 Makefile 末尾添加 build-code 目标

在 `Makefile` 最后一行后追加：

```makefile
build-code:
	docker build -t maguowei/code code
```

注意：缩进必须使用 **Tab**，不能用空格。

### Step 2：验证 make 目标

```bash
make -n build-code
```

期望：输出 `docker build -t maguowei/code code`，无报错。

### Step 3：提交

```bash
git add Makefile
git commit -m "chore: add build-code makefile target"
```

---

## Task 5：创建 GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/code.yaml`

### Step 1：创建 `.github/workflows/code.yaml`

```yaml
name: code
on:
  workflow_dispatch:
  push:
    paths:
      - "code/*"
      - ".github/workflows/code.yaml"
jobs:
  App:
    name: Build Code
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: code
          platforms: linux/amd64,linux/arm64
          push: true
          tags: maguowei/code
```

### Step 2：提交 workflow

```bash
git add .github/workflows/code.yaml
git commit -m "ci: add github actions workflow for code image"
```

---

## Task 6：创建 README.md

**Files:**
- Create: `code/README.md`

### Step 1：创建 `code/README.md`

```markdown
# maguowei/code

容器内 AI 编程工具集成镜像，基于 Ubuntu 26.04。

## 内置工具

### AI 工具
- [Claude Code](https://github.com/anthropics/claude-code) - Anthropic 官方 AI 编程助手 CLI
- [OpenCode](https://opencode.ai) - 开源 AI 编程助手 CLI
- [Codex](https://github.com/openai/codex) - OpenAI Codex CLI

### Shell 环境
- zsh + oh-my-zsh
- starship（prompt）
- zsh-autosuggestions / zsh-syntax-highlighting / zsh-completions
- zoxide（智能目录跳转）

### 现代 CLI 工具
- eza（ls 增强）、bat（cat 增强）、fd（find 增强）、ripgrep（grep 增强）
- fzf（模糊搜索）、htop、tmux、tree

### 运行时
- Node.js 22 LTS
- Python 3.14

## 使用方式

### 本地开发（挂载代码目录）

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  maguowei/code
```

### 挂载 API Key

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  maguowei/code
```

### CI/CD 使用

在 GitHub Actions 中：

```yaml
jobs:
  ai-review:
    runs-on: ubuntu-latest
    container: maguowei/code
    steps:
      - uses: actions/checkout@v3
      - run: claude --help
```
```

### Step 2：提交 README

```bash
git add code/README.md
git commit -m "docs: add README for code image"
```

---

## 注意事项

1. **Python 3.14 兼容性**：ubuntu:26.04 处于 Beta 阶段，若官方 apt 未提供 `python3.14`，Dockerfile 中的 `||` 分支会自动切换到 deadsnakes PPA。
2. **eza 安装**：依赖 `http://deb.gierens.de` 第三方仓库，若网络不通可考虑改用 cargo 安装：`cargo install eza`（需先安装 Rust）。
3. **npm 全局包版本**：`@anthropic-ai/claude-code`、`opencode-ai`、`@openai/codex` 均安装 latest，若有特定版本需求可在包名后加 `@x.y.z`。
4. **构建时间**：git clone 多个 zsh 插件 + npm 全局安装 AI 工具耗时较长，首次构建约 5-15 分钟。
