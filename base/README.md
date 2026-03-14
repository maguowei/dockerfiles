# maguowei/base

基于 Ubuntu 26.04 的基础镜像，预装中文环境、常用开发工具和完整 Shell 生态。

## 内置工具

### 系统基础

- Ubuntu 26.04
- 时区：`Asia/Shanghai`
- Locale：`zh_CN.UTF-8` / `en_US.UTF-8`

### 系统工具

- git、vim、curl、wget、jq、make、unzip
- build-essential、openssh-client
- tmux、tree、htop、net-tools

### 运行时

- Node.js 22 LTS（含 npm）
- Python 3.14 + uv 包管理器
- Go（自动获取最新版本）

### 现代 CLI 工具

- eza（ls 增强）
- bat（cat 增强）
- fd（find 增强）
- ripgrep（grep 增强）
- fzf（模糊搜索）
- zoxide（智能目录跳转）

### Shell 环境

- zsh（默认 Shell）
- oh-my-zsh
- starship（prompt）
- zsh-autosuggestions / zsh-syntax-highlighting / zsh-completions

## 使用方式

```bash
docker run -it --rm maguowei/base
```

## 环境变量

| 变量 | 值 |
|------|-----|
| `LANG` | `en_US.UTF-8` |
| `TZ` | `Asia/Shanghai` |
| `SHELL` | `/bin/zsh` |
| `GOPATH` | `/root/go` |
| `GOPROXY` | `https://goproxy.cn,direct` |
| `UV_INDEX_URL` | `https://mirrors.aliyun.com/pypi/simple/` |
