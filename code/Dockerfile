FROM maguowei/base:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/code"

# AI 编程工具（npm 全局安装）
RUN npm install -g \
    @anthropic-ai/claude-code \
    opencode-ai \
    @openai/codex \
    @google/gemini-cli

# 复制 zsh 及 starship 配置文件
RUN mkdir -p /root/.config
COPY .zshrc /root/.zshrc
COPY starship.toml /root/.config/starship.toml

CMD ["zsh"]
