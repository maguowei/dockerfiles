# maguowei/python

Python 应用镜像家族，基于 `python:3.14-slim`，集成 uv 包管理器、中文环境和时区配置。

## maguowei/python（基础层）

预置系统级环境和 uv 配置，作为 ONBUILD 镜像的基座。

### 预置环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| LANG | en_US.UTF-8 | 系统语言 |
| LC_CTYPE | zh_CN.UTF-8 | 字符类型 |
| TZ | Asia/Shanghai | 时区 |
| UV_INDEX_URL | https://mirrors.aliyun.com/pypi/simple/ | uv 镜像源 |
| UV_COMPILE_BYTECODE | 1 | 编译 Python 字节码 |

## maguowei/python:onbuild（ONBUILD 应用模板）

在基础层之上添加 ONBUILD 指令，构建时自动通过 uv 安装依赖。

### 使用方法

在应用的 `Dockerfile` 中：

```dockerfile
FROM maguowei/python:onbuild

ENV APP_NAME=example
ENV APP_ENV=prod

USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

项目需包含 `pyproject.toml` 和 `uv.lock`，构建时 ONBUILD 指令自动执行 `uv sync --no-dev --frozen`。

### 预置环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| VIRTUAL_ENV | /opt/venv | 虚拟环境路径 |
| APP_PATH | /app | 应用代码路径（WORKDIR） |
| APP_LOG_PATH | /data/app/log | 日志路径（Volume） |

## 构建

```bash
make build-python       # maguowei/python
make build-python-app   # maguowei/python:onbuild
```
