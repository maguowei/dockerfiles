# LiteLLM Proxy

基于 LiteLLM 的通用 LLM 代理服务，可以将任何 LLM 模型（Claude、GPT、Gemini、Kimi 等）转换为 Claude API 兼容的接口，方便 Claude Code 接入使用。

## 快速开始

### 1. 构建镜像

```bash
make build-litellm
```

### 2. 运行服务

```bash
docker run -d \
  --name litellm-proxy \
  -p 4000:4000 \
  -v $(pwd)/litellm/config.yaml:/app/config.yaml \
  -e AZURE_API_BASE=https://xxxx.openai.azure.com \
  -e AZURE_API_KEY=your-api-key \
  -e LITELLM_MASTER_KEY=sk-1234 \
  maguowei/litellm
```

### 3. 测试服务

```bash
# openai 协议
curl -X POST 'http://localhost:4000/chat/completions' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-1234' \
  -d '{
    "model": "Kimi-K2.5",
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ]
  }'
```

```bash
# anthropic 协议
curl -X POST "http://localhost:4000/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk-1234" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "Kimi-K2.5",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "你好，请介绍一下你自己"
          }
        ]
      }
    ]
  }'
```

## 配置说明

### 环境变量

**必需：**

- `AZURE_API_BASE`: Azure OpenAI 端点地址（例如：`https://xxxx.openai.azure.com`）
- `AZURE_API_KEY`: Azure API 密钥
- `LITELLM_MASTER_KEY`: LiteLLM Proxy 主密钥（用于 API 认证，必须以 `sk-` 开头）

## 参考资料

- [LiteLLM 官方文档](https://docs.litellm.ai/)
- [LiteLLM Docker 快速开始](https://docs.litellm.ai/docs/proxy/docker_quick_start)
- [LiteLLM Use Claude Code with Non-Anthropic Models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)