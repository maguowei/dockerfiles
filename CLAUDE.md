# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Docker 镜像集合仓库,包含多个用于不同场景的定制化 Docker 镜像。所有镜像都托管在 Docker Hub 的 `maguowei` 命名空间下。

## 仓库结构

仓库采用平铺目录结构,每个顶层目录对应一个镜像或一组相关镜像:

- **base**: Ubuntu 24.04 基础镜像,预装中文环境、常用工具和 Python 3.12
- **go**: Go 语言相关镜像,包含 `builder`(构建镜像)和 `app`(运行时镜像)两个子目录
- **python**: Python 基础镜像,基于 base 镜像扩展
- **python-app**: Python 应用镜像,使用 ONBUILD 指令,基于 poetry 管理依赖
- **frp**: 内网穿透工具 frp 的镜像
- **surge-snell**: Surge Snell 代理协议镜像
- **v2ray**: V2Ray 代理工具镜像
- **nginx**: Nginx Web 服务器镜像
- **elasticsearch**: Elasticsearch 搜索引擎镜像
- **tidb**: TiDB 数据库镜像

每个镜像目录包含:
- `Dockerfile`: 镜像构建定义
- `README.md`: 镜像使用说明(部分镜像包含)
- 其他配置文件或脚本(如需要)

## 构建命令

### 本地构建

使用 Makefile 中定义的目标构建镜像:

```bash
# 构建基础镜像
make build

# 构建 Go 相关镜像
make build-go-app       # Go 应用镜像
make build-go-builder   # Go 构建镜像

# 构建 Python 相关镜像
make build-python       # Python 基础镜像
make build-python-app   # Python 应用镜像

# 构建其他服务镜像
make build-frp          # FRP 内网穿透
make build-surge-snell  # Surge Snell 代理
make build-v2ray        # V2Ray 代理
make build-nginx        # Nginx Web 服务器
make build-elasticsearch # Elasticsearch 搜索引擎
make build-tidb         # TiDB 数据库
```

注意:部分镜像(如 frp、surge-snell)使用 `--platform=linux/amd64` 参数构建特定平台镜像。

### CI/CD 构建

GitHub Actions 自动化构建流程位于 `.github/workflows/` 目录:
- 每个镜像对应一个独立的 workflow 文件(如 `base.yaml`、`go.yaml`)
- 当对应镜像目录或 workflow 文件变更时自动触发构建
- 支持多平台构建(linux/amd64、linux/arm64),具体平台根据镜像而定
- 构建完成后自动推送到 Docker Hub

所有 workflow 都可以通过 `workflow_dispatch` 手动触发。

## 镜像架构模式

### ONBUILD 模式镜像

部分镜像(如 `go/builder`、`python-app`)使用 ONBUILD 指令模式,作为应用镜像的基础:

**go/builder**:
- 使用 `FROM maguowei/go-builder:onbuild` 作为基础镜像
- 自动执行依赖下载和编译,编译时注入版本信息(GitCommit、BuildTime、GoVersion)
- 需要设置 `APP_NAME` 构建参数指定应用名称

**python-app**:
- 使用 `FROM maguowei/python-app:onbuild` 作为基础镜像
- 自动执行 poetry 依赖安装
- 预配置应用路径、日志路径和环境变量

### 镜像依赖链

- `base` → `python` → `python-app`
- `golang:1.23-alpine` → `go/builder`
- `ubuntu:24.04` → `base`

## 环境配置

### 镜像源配置

镜像中使用阿里云镜像源加速:
- Ubuntu APT 源: `mirrors.aliyun.com`
- Alpine APK 源: `mirrors.aliyun.com`
- Python PyPI 源: `mirrors.aliyun.com/pypi/simple/`
- Go Proxy: `goproxy.cn`

### 时区和本地化

base 镜像预配置:
- 时区: `Asia/Shanghai`
- 支持中文(zh_CN.UTF-8)和英文(en_US.UTF-8)

## 提交规范

严格遵循 Conventional Commits 规范:

```
<type>: <description>

[optional body]
```

常用 type:
- `feat`: 新增镜像或功能
- `fix`: 修复镜像构建或运行问题
- `chore`: 依赖版本更新、配置调整
- `docs`: 文档更新
- `ci`: CI/CD 配置更新

示例:
- `chore: upgrade frp 0.63.0`
- `feat: add elasticsearch image`
- `ci: update github actions to v3`
