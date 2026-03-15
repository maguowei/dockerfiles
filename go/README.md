# Golang App multi-stage builds image

基于 ONBUILD 模式的 Go 应用多阶段构建镜像，包含 builder（编译）和 app（运行时）两个镜像。

## 镜像说明

### builder (`maguowei/go-builder:onbuild`)

- 基础镜像：`golang:1.26-alpine`
- 自动执行依赖下载（`go mod download`）和编译
- 使用 `-ldflags "-s -w"` 剥离调试信息，减小二进制体积
- 支持多架构构建（amd64、arm64），由 Docker buildx `--platform` 自动处理
- 版本信息通过 Go 内置 `runtime/debug.ReadBuildInfo()` 自动嵌入

### app (`maguowei/go-app:onbuild`)

- 基础镜像：`alpine:3.21`
- 最小化运行时依赖：`tzdata`、`curl`、`ca-certificates`
- 预配置时区 `Asia/Shanghai`
- 以非 root 用户 `app` 运行
- 自动从 builder 阶段复制编译产物和配置文件

## 使用方法

在你的项目中创建 `Dockerfile`：

```dockerfile
FROM maguowei/go-builder:onbuild AS builder
ARG APP_NAME=myapp

FROM maguowei/go-app:onbuild
ARG APP_NAME=myapp
```

构建并运行：

```bash
docker build --build-arg APP_NAME=myapp -t myapp .
docker run -p 8080:8080 myapp
```

### 项目结构要求

```
.
├── cmd/
│   └── myapp/          # 应用入口，APP_NAME 对应此目录名
│       └── main.go
├── configs/            # 配置文件目录，自动复制到运行时镜像
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

- [Understand how ARG and FROM interact](https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact)
- [Go runtime/debug.ReadBuildInfo](https://pkg.go.dev/runtime/debug#ReadBuildInfo)
