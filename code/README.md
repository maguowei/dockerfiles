# maguowei/code

容器内 AI 编程工具集成镜像，基于 [maguowei/base](../base/README.md)。

## 内置工具

### AI 工具

- [Claude Code](https://github.com/anthropics/claude-code) - Anthropic 官方 AI 编程助手 CLI
- [OpenCode](https://opencode.ai) - 开源 AI 编程助手 CLI
- [Codex](https://github.com/openai/codex) - OpenAI Codex CLI

### 继承自 base 镜像

- zsh + starship + 补全插件（autosuggestions / syntax-highlighting / completions）
- Node.js 22 LTS、Python 3.14、Go（最新版）
- eza、bat、fd、ripgrep、fzf、zoxide 等现代 CLI 工具

## 使用方式

### 本地开发（挂载代码目录）

挂载当前目录并注入 API Key：

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  maguowei/code
```

### 作为 Apple Container Machine

镜像内置 systemd（`/sbin/init`）、SSH server 等组件，可在 macOS 上作为 [Apple container](https://github.com/apple/container) 的 machine 常驻运行，把它当作一台带完整 AI 工具链的开发机：

```bash
container image pull maguowei/code
container machine create maguowei/code --cpus 2 --memory 4G --name code --set-default
```

首次启动时镜像内的 `/etc/machine/create-user.sh` 会接管用户创建，将登录 shell 设为 zsh 并带上 base 的 `.zshrc`——登录进去即是配好的 zsh。

常用管理命令：

```bash
container machine run -n code                    # 进入交互 shell（省略 -n 用默认 machine）
container machine run -n code -- nproc           # 在 machine 内执行单条命令
container machine list                           # 列出所有 machine，标记默认
container machine inspect code                   # 查看配置与状态（JSON）
container machine logs -n code                   # 查看日志（--boot 看引导日志，--follow 跟随）
container machine set -n code cpus=4 memory=8G   # 调整配置（重启后生效）
container machine set-default code               # 设为默认 machine
container machine stop code                      # 停止
container machine delete code                    # 删除（会先停止）
```

参考 [container-machine 文档](https://github.com/apple/container/blob/main/docs/container-machine.md)与[命令参考](https://github.com/apple/container/blob/main/docs/command-reference.md#container-machine-management)。

### CI/CD 使用

在 GitHub Actions 中：

```yaml
jobs:
  ai-review:
    runs-on: ubuntu-latest
    container: maguowei/code
    steps:
      - uses: actions/checkout@v4
      - run: claude --help
```
