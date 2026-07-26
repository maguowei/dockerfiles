# maguowei/code

容器内 AI 编程工具集成镜像，基于 [maguowei/base](../base/README.md)。

## 内置工具

### AI 工具

- [Claude Code](https://github.com/anthropics/claude-code) - Anthropic 官方 AI 编程助手 CLI
- [OpenCode](https://opencode.ai) - 开源 AI 编程助手 CLI
- [Codex](https://github.com/openai/codex) - OpenAI Codex CLI

### 继承自 base 镜像

- zsh + oh-my-zsh + starship + 补全插件
- Node.js 22 LTS、Python 3.14、Go（最新版）
- eza、bat、fd、ripgrep、fzf、zoxide 等现代 CLI 工具

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

### 作为 Apple Container Machine

镜像内置 systemd（`/sbin/init`）、SSH server 等组件，可在 macOS 上作为 [Apple container](https://github.com/apple/container) 的 machine 常驻运行，把它当作一台带完整 AI 工具链的开发机：

```bash
container image pull maguowei/code
container machine <name> maguowei/code
```

参考 [container-machine 文档](https://github.com/apple/container/blob/main/docs/container-machine.md)。

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
