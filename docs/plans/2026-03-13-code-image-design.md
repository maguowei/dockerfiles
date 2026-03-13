# code 镜像设计文档

**日期**: 2026-03-13
**状态**: 已批准，待实现

## 概述

创建 `maguowei/code` 镜像，作为容器内 AI 工具使用环境，集成 Claude Code、OpenCode、Codex 三大 AI 编程助手，以及现代化 zsh 终端生态和常用开发工具。

## 镜像信息

| 项目 | 值 |
|------|-----|
| 镜像名 | `maguowei/code` |
| 基础镜像 | `ubuntu:26.04` |
| Python | 3.14（优先官方 apt，否则 deadsnakes PPA 兜底） |
| Node.js | 22 LTS（NodeSource 官方脚本） |
| 平台 | `linux/amd64`, `linux/arm64` |
| 默认 Shell | `zsh` |
| 使用场景 | 本地开发（挂载代码目录）+ CI/CD 流水线 |

## Dockerfile 分层结构

### Layer 1：系统基础

- locale（zh_CN.UTF-8 + en_US.UTF-8）
- 时区（Asia/Shanghai）
- 基础 apt 包：`git`, `curl`, `wget`, `vim`, `jq`, `unzip`, `tar`, `make`, `build-essential`, `ca-certificates`, `iputils-ping`, `net-tools`, `openssh-client`, `tmux`

### Layer 2：Node.js 22 LTS

- 通过 NodeSource 官方脚本安装 Node.js 22.x
- 更新 npm 至最新版

### Layer 3：AI 工具（npm global）

| 工具 | 包名 |
|------|------|
| Claude Code | `@anthropic-ai/claude-code` |
| OpenCode | `opencode-ai` |
| Codex | `@openai/codex` |

### Layer 4：zsh 生态

插件通过 git clone 安装到 `/opt/zsh/`：

```
/opt/zsh/
├── oh-my-zsh/
├── zsh-autosuggestions/
├── zsh-syntax-highlighting/
└── zsh-completions/
```

- **starship**：二进制安装至 `/usr/local/bin/`
- **zoxide**：apt 或官方脚本安装

### Layer 5：现代 CLI 工具

| 工具 | 安装方式 | 替代对象 |
|------|---------|---------|
| `ripgrep` (rg) | apt | grep |
| `fd-find` (fd) | apt | find |
| `bat` | apt | cat |
| `fzf` | apt | — |
| `eza` | apt / cargo | ls |
| `zoxide` | apt / 官方脚本 | cd |
| `htop` | apt | top |
| `tree` | apt | — |

### Layer 6：Python 3.14

- 优先从 ubuntu:26.04 官方 apt 安装 `python3.14`, `python3.14-dev`, `python3.14-venv`
- 若官方 apt 不提供，通过 `ppa:deadsnakes/ppa` 安装
- pip 通过 `get-pip.py` 安装
- 阿里云 PyPI 镜像：`https://mirrors.aliyun.com/pypi/simple/`

### Layer 7：配置文件

- `.zshrc` COPY 进镜像（`/root/.zshrc`）
- `starship.toml` COPY 进镜像（`/root/.config/starship.toml`）

## zsh 配置

### `.zshrc` 核心内容

```zsh
# oh-my-zsh
export ZSH=/opt/zsh/oh-my-zsh
plugins=(git)
source $ZSH/oh-my-zsh.sh

# 补全插件
source /opt/zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fpath+=(/opt/zsh/zsh-completions/src)

# starship prompt
eval "$(starship init zsh)"

# zoxide（z 命令跳转）
eval "$(zoxide init zsh)"

# 工具别名
alias ls='eza --icons'
alias ll='eza -lh --icons'
alias cat='bat'
alias find='fd'
alias grep='rg'
```

### `starship.toml` 配置方向

简洁风格，显示：当前目录、git 分支/状态、Node.js 版本、Python 版本、命令执行时间。

## 环境变量

```dockerfile
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV TZ=Asia/Shanghai
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple/
ENV SHELL=/bin/zsh
ENV NODE_PATH=/usr/local/lib/node_modules
```

## 仓库结构

```
dockerfiles/
└── code/
    ├── Dockerfile
    ├── README.md
    ├── .zshrc
    └── starship.toml
```

## Makefile

```makefile
build-code:
    docker build -t maguowei/code code
```

## GitHub Actions

文件：`.github/workflows/code.yaml`

- 触发：`code/*` 或 `code.yaml` 变更，支持 `workflow_dispatch` 手动触发
- 构建平台：`linux/amd64,linux/arm64`
- 推送目标：`maguowei/code:latest`
- 风格与现有 workflow 保持一致
