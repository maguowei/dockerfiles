# LiteLLM Proxy for Kimi-K2-Thinking

基于 LiteLLM 的 Kimi-K2-Thinking 模型代理服务，通过 Azure OpenAI 端点提供 OpenAI 兼容的 API 接口，方便接入 Claude Code 和其他工具。

## 快速开始

### 1. 构建镜像

```bash
docker build -t maguowei/litellm litellm
```

或使用 Makefile：

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

参数说明：
- `-p 4000:4000`: 映射端口
- `-v $(pwd)/litellm/config.yaml:/app/config.yaml`: 挂载配置文件
- `-e AZURE_API_BASE`: Azure OpenAI 端点地址（不包含 `/openai/v1/`）
- `-e AZURE_API_KEY`: Azure API Key（必需）
- `-e LITELLM_MASTER_KEY`: LiteLLM 主密钥，必须以 `sk-` 开头

### 3. 测试服务

```bash
curl -X POST 'http://localhost:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
  "model": "Kimi-K2-Thinking",
  "messages": [
    {
      "role": "user",
      "content": "你好，请介绍一下你自己"
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

### 模型配置

配置文件中定义了一个模型：
- **model_name**: `Kimi-K2-Thinking` - 客户端调用时使用的模型名称
- **deployment_name**: `Kimi-K2-Thinking` - Azure 上的部署名称

## 接入 Claude Code

在 Claude Code 中配置自定义 API 端点：

```bash
# 设置 API 端点
export OPENAI_API_BASE=http://localhost:4000

# 设置 API Key（使用 LITELLM_MASTER_KEY）
export OPENAI_API_KEY=sk-1234
```

然后在 Claude Code 中使用模型名称 `Kimi-K2-Thinking`。

## 常用命令

```bash
# 查看日志
docker logs -f litellm-proxy

# 重启服务
docker restart litellm-proxy

# 停止服务
docker stop litellm-proxy

# 删除容器
docker rm litellm-proxy
```

## 参考资料

- [LiteLLM 官方文档](https://docs.litellm.ai/)
- [LiteLLM Docker 快速开始](https://docs.litellm.ai/docs/proxy/docker_quick_start)
