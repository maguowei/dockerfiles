# base 镜像优化设计文档

**日期**：2026-03-14
**分支**：dev
**关联镜像**：`maguowei/base`、`maguowei/code`

---

## 背景

`base` 镜像作为个人开发者工具集，同时也是 `code` 镜像的唯一上游依赖。当前存在以下问题：

1. `software-properties-common` 安装了 `add-apt-repository`，但 Dockerfile 全程未调用，纯冗余
2. `make` 在 Layer 2 中显式声明，但已包含在 `build-essential` 中，重复
3. `gnupg` 安装后残留在最终镜像层，实际仅用于 eza apt key 导入
4. Go 版本动态拉取 latest，构建不可重现，有破坏性更新风险
5. CI workflows 使用旧版 actions（v1/v2），存在安全隐患和功能缺失

---

## 方案：方案 B（分层优化）

### 1. base/Dockerfile 包清理

**Layer 2 变更**：

- 删除 `software-properties-common`（零使用）
- 删除 `make`（build-essential 的子集，重复）
- 删除 `gnupg`（移至 eza 安装层）

**eza 安装层**：gnupg 在同一 RUN 中安装、使用、删除，不污染最终层：

```dockerfile
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gnupg \
    && mkdir -p /etc/apt/keyrings \
    && wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc \
    | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" \
    | tee /etc/apt/sources.list.d/gierens.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends eza \
    && apt-get remove -y gnupg && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
```

### 2. Go 版本钉选策略

使用 `ARG GO_MAJOR=1.26` 钉住主版本，通过 Go 官方 JSON API 自动获取当前主版本的最新补丁：

```dockerfile
ARG GO_MAJOR=1.26
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
        x86_64)  GOARCH="amd64" ;; \
        aarch64) GOARCH="arm64" ;; \
    esac && \
    GO_VERSION=$(curl -fsSL "https://go.dev/dl/?mode=json" | \
        jq -r --arg major "${GO_MAJOR}" \
        '[.[] | select(.stable == true) | .version | select(startswith("go" + $major + "."))] | first') && \
    curl -fsSL "https://go.dev/dl/${GO_VERSION}.linux-${GOARCH}.tar.gz" \
    | tar -xz -C /usr/local
```

升级主版本时只需修改 `ARG GO_MAJOR` 的值。

### 3. CI Workflow 升级

`base.yaml` 和 `code.yaml` 各升级 4 处 actions：

| 当前版本 | 目标版本 |
|----------|----------|
| `actions/checkout@v3` | `actions/checkout@v4` |
| `docker/setup-buildx-action@v1` | `docker/setup-buildx-action@v3` |
| `docker/login-action@v1` | `docker/login-action@v3` |
| `docker/build-push-action@v2` | `docker/build-push-action@v6` |

---

## 关键文件

| 文件 | 操作 |
|------|------|
| `base/Dockerfile` | 修改 Layer 2、eza 安装层、Go 安装层 |
| `.github/workflows/base.yaml` | 升级 4 个 actions |
| `.github/workflows/code.yaml` | 升级 4 个 actions |

---

## 验证方式

```bash
# 本地构建验证
make build

# 确认 gnupg 不在最终镜像中
docker run --rm maguowei/base dpkg -l gnupg  # 应报 not found

# 确认 Go 版本为 1.26.x
docker run --rm maguowei/base go version  # 应输出 go1.26.x

# 确认 eza 可用
docker run --rm maguowei/base eza --version
```
