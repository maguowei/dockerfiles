# Go 镜像优化设计

## 背景

当前 Go 镜像存在以下问题：
- Go 版本过旧（1.23），需升级到 1.26
- builder 硬编码 `GOARCH=amd64`，与 CI 多架构构建不一致
- 硬编码 `VERSION_IMPORT_PATH` 耦合特定项目
- app 运行时镜像安装了不必要的调试工具
- CI workflow 使用过旧的 GitHub Actions 版本

## 设计方案

### builder 镜像（`go/builder/Dockerfile`）

```dockerfile
FROM golang:1.26-alpine AS builder
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH=/opt/app
WORKDIR ${APP_PATH}

# 配置镜像源和安装依赖
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories \
    && apk add --no-cache git \
    && go env -w GOPROXY=https://goproxy.cn,direct

ONBUILD ARG APP_NAME
ONBUILD COPY go.mod go.sum ./
ONBUILD RUN go mod download
ONBUILD COPY . ${APP_PATH}
ONBUILD RUN CGO_ENABLED=0 go build -v -ldflags "-s -w" \
    -o ${APP_NAME}.app ${APP_PATH}/cmd/${APP_NAME}
```

改进点：
- Go 升级到 1.26
- 移除硬编码 `GOOS`/`GOARCH`，由 Docker buildx `--platform` 自动处理
- 移除 `VERSION_IMPORT_PATH` 和 `-ldflags -X` 版本注入，改用 Go 内置 `debug/buildinfo`
- 添加 `-s -w` 剥离调试信息，减小二进制体积
- 合并 RUN 层，使用 `--no-cache`

### app 运行时镜像（`go/app/Dockerfile`）

```dockerfile
FROM alpine:3.21
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH=/opt/app
ENV APP_LOG_PATH=/data/app/log

# 配置镜像源，安装最小运行时依赖
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories \
    && apk add --no-cache tzdata curl ca-certificates \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 创建非 root 用户和目录
RUN addgroup -S app && adduser -S app -G app \
    && mkdir -p ${APP_LOG_PATH} ${APP_PATH} \
    && chown -R app:app ${APP_LOG_PATH} ${APP_PATH}

WORKDIR ${APP_PATH}
VOLUME ${APP_LOG_PATH}
USER app

ONBUILD ARG APP_NAME
ONBUILD ENV APP_NAME=${APP_NAME}
ONBUILD COPY --from=builder ${APP_PATH}/${APP_NAME}.app ${APP_PATH}/${APP_NAME}.app
ONBUILD COPY --from=builder ${APP_PATH}/configs/ ${APP_PATH}/configs/

EXPOSE 8080
CMD ["sh", "-c", "${APP_NAME}.app"]
```

改进点：
- Alpine 升级到 3.21
- 精简依赖：移除 `iputils`、`net-tools`，保留 `tzdata`、`curl`、`ca-certificates`
- 合并 RUN 层减少镜像层数
- 移除 `APP_ENV` ARG（应在运行时通过 `-e` 传入）
- 移除无用的 `PS1` 配置
- 添加 `ca-certificates` 确保 HTTPS 正常

### CI Workflow（`.github/workflows/go.yaml`）

升级 GitHub Actions 版本：
- `actions/checkout@v3` → `v4`
- `docker/setup-buildx-action@v1` → `v3`
- `docker/login-action@v1` → `v3`
- `docker/build-push-action@v2` → `v6`

### 文档更新

更新 `CLAUDE.md` 中的镜像依赖链：
- `golang:1.23-alpine` → `golang:1.26-alpine` → `go/builder`

## 版本信息注入方式变更

放弃 `-ldflags -X` 手动注入，改用 Go 1.18+ 内置的 `debug/buildinfo`。应用端通过 `runtime/debug.ReadBuildInfo()` 读取：
- `vcs.revision` → git commit hash
- `vcs.time` → 提交时间
- `vcs.modified` → 是否有未提交修改
- `info.GoVersion` → Go 版本

## 验证

1. 本地构建测试：`make build-go-builder` 和 `make build-go-app`
2. 检查镜像体积是否减小
3. 确认多架构支持：`docker buildx build --platform linux/amd64,linux/arm64`
