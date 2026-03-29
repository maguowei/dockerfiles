# Golang App Multi-stage Images

Go 镜像拆成两个显式基础镜像：

- `maguowei/go-builder:latest`：提供编译环境和 `build-go-app` 构建脚本
- `maguowei/go-app:latest`：提供最小运行时、非 root 用户和通用 entrypoint

这套方案不再使用 `ONBUILD`，业务项目需要在自己的 Dockerfile 里显式声明构建步骤。这样更容易调试，也不会把 stage 名称和复制行为藏在基础镜像里。

## 镜像说明

### builder (`maguowei/go-builder:latest`)

- 基础镜像：`golang:1.26-alpine`
- 默认 `CGO_ENABLED=0`
- 内置 `build-go-app`，默认把二进制输出到 `/out/app`
- 如果项目存在 `configs/` 目录，会一并复制到 `/out/configs/`
- 通过 `ARG GOPROXY`、`ARG ALPINE_MIRROR` 覆盖网络环境，而不是写死国内源

### app (`maguowei/go-app:latest`)

- 基础镜像：`alpine:3.21`
- 运行时仅保留 `ca-certificates` 和 `tzdata`
- 固定非 root 用户 `app`（uid/gid `10001`）
- 默认从 `APP_BIN=/opt/app/app` 启动应用
- 不再预设日志目录或 `VOLUME`，建议直接输出到 stdout/stderr

## 使用方法

在你的项目中创建 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1.7

ARG GO_BUILDER_IMAGE=maguowei/go-builder:latest
ARG GO_APP_IMAGE=maguowei/go-app:latest

FROM ${GO_BUILDER_IMAGE} AS builder
ARG APP_NAME=myapp
WORKDIR /src

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download && go mod verify

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    APP_NAME=${APP_NAME} GO_OUTPUT_DIR=/out build-go-app

FROM ${GO_APP_IMAGE}
COPY --from=builder --chown=app:app /out/ /opt/app/

EXPOSE 8080
```

构建并运行：

```bash
docker build --build-arg APP_NAME=myapp -t myapp .
docker run -p 8080:8080 myapp
```

如果你希望二进制名不是 `/opt/app/app`，可以在运行时镜像里设置 `ENV APP_BIN=/opt/app/<your-binary>`。

### 项目结构要求

```
.
├── cmd/
│   └── myapp/          # 应用入口，APP_NAME 对应此目录名
│       └── main.go
├── configs/            # 可选，存在时会被复制到运行时镜像
├── go.mod
├── go.sum
└── Dockerfile
```

### 版本信息读取

应用可通过标准库获取构建时自动嵌入的版本信息：

```go
package main

import (
    "fmt"
    "runtime/debug"
)

func main() {
    info, ok := debug.ReadBuildInfo()
    if ok {
        fmt.Println("Go version:", info.GoVersion)
        for _, s := range info.Settings {
            switch s.Key {
            case "vcs.revision":
                fmt.Println("Git commit:", s.Value)
            case "vcs.time":
                fmt.Println("Commit time:", s.Value)
            case "vcs.modified":
                fmt.Println("Modified:", s.Value)
            }
        }
    }
}
```

### 多架构构建

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
    --build-arg APP_NAME=myapp -t myapp .
```

## Ref

- [Dockerfile cache mounts](https://docs.docker.com/build/cache/optimize/)
- [Go runtime/debug.ReadBuildInfo](https://pkg.go.dev/runtime/debug#ReadBuildInfo)
