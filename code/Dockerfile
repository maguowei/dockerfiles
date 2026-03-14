FROM maguowei/base:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/code"

# AI 编程工具（npm 全局安装）
RUN npm install -g \
    @anthropic-ai/claude-code \
    opencode-ai \
    @openai/codex \
    @google/gemini-cli

CMD ["zsh"]
