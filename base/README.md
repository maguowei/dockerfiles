# maguowei/base

Ubuntu 26.04 基础镜像（`Asia/Shanghai` 时区，`zh_CN.UTF-8` / `en_US.UTF-8` locale）。

**系统**: git, vim, curl, wget, jq, make, unzip, build-essential, openssh-client, tmux, tree, htop, net-tools
**运行时**: Node.js 22 LTS（含 npm）, Python 3.14 + uv, Go（最新版）
**CLI**: eza, bat, fd, ripgrep, fzf, zoxide
**Shell**: zsh + oh-my-zsh + starship, autosuggestions / syntax-highlighting / zsh-completions

```bash
docker run -it --rm maguowei/base
```

| 变量 | 值 |
|------|-----|
| LANG | en_US.UTF-8 |
| TZ | Asia/Shanghai |
| SHELL | /bin/zsh |
| GOPATH | /root/go |
| GOPROXY | https://goproxy.cn,direct |
| UV_INDEX_URL | https://mirrors.aliyun.com/pypi/simple/ |
