# Go 镜像优化设计

## 背景

当前 Go 镜像存在以下问题：
- Go 版本过旧（1.23），需升级到 1.26
- builder 硬编码 `GOARCH=amd64`，与 CI 多架构构建不一致
- 硬编码 `VERSION_IMPORT_PATH` 耦合特定项目
- app 运行时镜像安装了不必要的调试工具
- `ONBUILD` 隐式触发复制和编译，不利于调试和复用
- CI workflow 使用过旧的 GitHub Actions 版本

## 设计方案

### builder 镜像（`go/builder/Dockerfile`）

```dockerfile
FROM golang:1.26-alpine

ARG ALPINE_MIRROR=
ARG GOPROXY=https://proxy.golang.org,direct

ENV CGO_ENABLED=0 \
    GOPROXY=${GOPROXY}

WORKDIR /src

RUN if [ -n "${ALPINE_MIRROR}" ]; then \
        sed -i "s|https://dl-cdn.alpinelinux.org|${ALPINE_MIRROR}|g" /etc/apk/repositories; \
    fi \
    && apk add --no-cache ca-certificates git \
    && update-ca-certificates

COPY --chmod=755 build-go-app.sh /usr/local/bin/build-go-app
```

改进点：
- Go 升级到 1.26
- 移除硬编码 `GOOS`/`GOARCH`，由 Docker buildx `--platform` 自动处理
- 移除 `VERSION_IMPORT_PATH` 和 `-ldflags -X` 版本注入，改用 Go 内置 `debug/buildinfo`
- 使用 `-trimpath` 和 `-ldflags "-s -w"` 降低产物体积并移除构建路径
- 移除 `ONBUILD`，改为显式在业务 Dockerfile 中触发构建
- 提供 `build-go-app` 脚本，统一输出到 `/out/`
- 允许通过构建参数覆盖 `GOPROXY` 和 Alpine 镜像源

### app 运行时镜像（`go/app/Dockerfile`）

```dockerfile
FROM alpine:3.21

ARG ALPINE_MIRROR=

ENV APP_PATH=/opt/app \
    APP_BIN=/opt/app/app \
    TZ=UTC

RUN if [ -n "${ALPINE_MIRROR}" ]; then \
        sed -i "s|https://dl-cdn.alpinelinux.org|${ALPINE_MIRROR}|g" /etc/apk/repositories; \
    fi \
    && apk add --no-cache ca-certificates tzdata \
    && addgroup -g 10001 -S app \
    && adduser -u 10001 -S -D -H -G app app \
    && mkdir -p "${APP_PATH}" \
    && chown -R app:app "${APP_PATH}"

COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

WORKDIR ${APP_PATH}
USER app

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD []
```

改进点：
- Alpine 升级到 3.21
- 精简依赖：仅保留 `tzdata`、`ca-certificates`
- 合并 RUN 层减少镜像层数
- 固定非 root uid/gid，便于宿主机权限对齐
- 移除默认日志目录和 `VOLUME`，鼓励直接输出 stdout/stderr
- 使用 entrypoint 脚本直接 `exec` 应用，避免 shell 作为 PID 1

### CI Workflow（`.github/workflows/go.yaml`）

升级 GitHub Actions 版本：
- `actions/checkout@v3` → `v4`
- `docker/setup-buildx-action@v1` → `v3`
- `docker/login-action@v1` → `v3`
- `docker/build-push-action@v2` → `v6`

### 文档更新

更新 `CLAUDE.md` 中的镜像依赖链：
- `golang:1.23-alpine` → `golang:1.26-alpine` → `go/builder`
- 补充 `alpine:3.21` → `maguowei/go-app`

## 版本信息注入方式变更

放弃 `-ldflags -X` 手动注入，改用 Go 1.18+ 内置的 `debug/buildinfo`。应用端通过 `runtime/debug.ReadBuildInfo()` 读取：
- `vcs.revision` → git commit hash
- `vcs.time` → 提交时间
- `vcs.modified` → 是否有未提交修改
- `info.GoVersion` → Go 版本

## 验证

1. 本地构建测试：`make build-go-builder` 和 `make build-go-app`
2. 使用示例 Dockerfile 验证显式多阶段构建可正常编译和启动
3. 检查镜像体积是否减小
4. 确认多架构支持：`docker buildx build --platform linux/amd64,linux/arm64`
