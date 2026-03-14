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
