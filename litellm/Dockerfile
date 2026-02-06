FROM docker.litellm.ai/berriai/litellm:main-latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/litellm"
LABEL version="latest"
LABEL description="LiteLLM Proxy for Claude API"

# 设置工作目录
WORKDIR /app

# 暴露端口
EXPOSE 4000

# 默认启动命令（可通过 docker run 参数覆盖）
CMD ["--config", "/app/config.yaml", "--port", "4000"]
