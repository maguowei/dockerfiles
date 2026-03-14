# maguowei/python:onbuild

基于 `maguowei/python` 的 ONBUILD 应用模板镜像，自动通过 uv 安装依赖。

## 使用方法

在应用的 `Dockerfile` 中：

```dockerfile
FROM maguowei/python:onbuild
LABEL maintainer="example@example.com"

ENV APP_NAME=example
ENV APP_ENV=prod

USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

项目需包含 `pyproject.toml` 和 `uv.lock`，构建时 ONBUILD 指令自动执行 `uv sync --no-dev --frozen`。

## 预置环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `VIRTUAL_ENV` | `/opt/venv` | 虚拟环境路径 |
| `APP_PATH` | `/app` | 应用代码路径（WORKDIR） |
| `APP_LOG_PATH` | `/data/app/log` | 日志路径（Volume） |

## 构建

```bash
make build-python-app
```
