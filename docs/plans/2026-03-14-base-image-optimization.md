# base 镜像优化实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 清理 base/Dockerfile 中的冗余包、隔离 gnupg 生命周期、钉选 Go 主版本、升级 CI workflow actions。

**Architecture:** 三处独立改动：Dockerfile 层优化（移除冗余包、gnupg 生命周期隔离）、Go 版本策略（ARG + jq 过滤 go1.26.x）、CI actions 升级（base.yaml + code.yaml 各 4 处替换）。

**Tech Stack:** Dockerfile、GitHub Actions、jq、Go dl JSON API

---

### Task 1：清理 Layer 2 冗余包

**Files:**
- Modify: `base/Dockerfile`（Layer 2 的 apt-get install 块）

**Step 1: 查看当前 Layer 2**

```bash
grep -n "software-properties-common\|make\|gnupg" base/Dockerfile
```

预期输出：能看到这三个包出现在同一个 RUN 块中。

**Step 2: 修改 Dockerfile**

找到 Layer 2 的 RUN 块（约第 27-45 行），删除以下三行：
```
    make \
    software-properties-common \
    gnupg \
```

删除后 Layer 2 的包列表为：
```dockerfile
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    vim \
    jq \
    unzip \
    build-essential \
    iputils-ping \
    net-tools \
    openssh-client \
    tmux \
    tree \
    htop \
    && rm -rf /var/lib/apt/lists/*
```

**Step 3: 验证语法**

```bash
docker build --no-cache --target=base -f base/Dockerfile base/ 2>&1 | head -30
```

如果没有 `--target` 支持，直接：
```bash
docker build -f base/Dockerfile base/ 2>&1 | tail -20
```

**Step 4: Commit**

```bash
git add base/Dockerfile
git commit -m "chore: remove redundant packages from base Layer 2"
```

---

### Task 2：eza 安装层隔离 gnupg 生命周期

**Files:**
- Modify: `base/Dockerfile`（eza 安装的 RUN 块）

**Step 1: 查看当前 eza 安装块**

```bash
grep -n "eza\|gierens\|gnupg\|gpg" base/Dockerfile
```

**Step 2: 修改 eza 安装层**

将当前 eza 安装的 RUN 块替换为：

```dockerfile
# 安装 eza（通过官方 apt 仓库，gnupg 用完即删）
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

**Step 3: 验证构建**

```bash
docker build -t maguowei/base:test base/
```

预期：构建成功，无报错。

**Step 4: 验证 eza 可用、gnupg 已删除**

```bash
docker run --rm maguowei/base:test eza --version
docker run --rm maguowei/base:test dpkg -l gnupg 2>&1 | grep -E "^ii|no packages"
```

预期：eza 版本正常输出；gnupg 不在已安装列表中（输出 "no packages found" 或空）。

**Step 5: Commit**

```bash
git add base/Dockerfile
git commit -m "chore: isolate gnupg lifecycle within eza install layer"
```

---

### Task 3：Go 版本改为主版本钉选 + 补丁自动

**Files:**
- Modify: `base/Dockerfile`（Go 安装的 RUN 块，约第 108-115 行）

**Step 1: 查看当前 Go 安装块**

```bash
grep -n "GO_VERSION\|go.dev\|GOARCH\|GOPATH" base/Dockerfile
```

**Step 2: 修改 Go 安装层**

在 Go 安装的 RUN 块上方添加 ARG，并将 RUN 块替换为：

```dockerfile
# Layer 7: Go（主版本钉选，补丁自动跟进）
ARG GO_MAJOR=1.26
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
        x86_64)  GOARCH="amd64" ;; \
        aarch64) GOARCH="arm64" ;; \
    esac && \
    GO_VERSION=$(curl -fsSL "https://go.dev/dl/?mode=json" | \
        jq -r --arg major "${GO_MAJOR}" \
        '[.[] | select(.stable == true) | .version | select(startswith("go" + $major + "."))] | first') && \
    echo "Installing Go version: ${GO_VERSION}" && \
    curl -fsSL "https://go.dev/dl/${GO_VERSION}.linux-${GOARCH}.tar.gz" \
    | tar -xz -C /usr/local
```

**Step 3: 验证构建**

```bash
docker build -t maguowei/base:test base/
```

**Step 4: 验证 Go 版本**

```bash
docker run --rm maguowei/base:test go version
```

预期输出示例：`go version go1.26.1 linux/arm64`（主版本为 1.26）

**Step 5: Commit**

```bash
git add base/Dockerfile
git commit -m "chore: pin go major version to 1.26 with auto patch tracking"
```

---

### Task 4：升级 base.yaml CI actions

**Files:**
- Modify: `.github/workflows/base.yaml`

**Step 1: 查看当前版本**

```bash
grep "uses:" .github/workflows/base.yaml
```

**Step 2: 批量替换 4 处 actions**

```bash
sed -i '' \
  's|actions/checkout@v3|actions/checkout@v4|g' \
  .github/workflows/base.yaml

sed -i '' \
  's|docker/setup-buildx-action@v1|docker/setup-buildx-action@v3|g' \
  .github/workflows/base.yaml

sed -i '' \
  's|docker/login-action@v1|docker/login-action@v3|g' \
  .github/workflows/base.yaml

sed -i '' \
  's|docker/build-push-action@v2|docker/build-push-action@v6|g' \
  .github/workflows/base.yaml
```

**Step 3: 验证替换结果**

```bash
grep "uses:" .github/workflows/base.yaml
```

预期：所有 `@v1`、`@v2`、`@v3`（旧）均已替换为新版本。

**Step 4: Commit**

```bash
git add .github/workflows/base.yaml
git commit -m "ci: upgrade github actions to latest versions in base workflow"
```

---

### Task 5：升级 code.yaml CI actions

**Files:**
- Modify: `.github/workflows/code.yaml`

**Step 1: 查看当前版本**

```bash
grep "uses:" .github/workflows/code.yaml
```

**Step 2: 批量替换 4 处 actions**

```bash
sed -i '' \
  's|actions/checkout@v3|actions/checkout@v4|g' \
  .github/workflows/code.yaml

sed -i '' \
  's|docker/setup-buildx-action@v1|docker/setup-buildx-action@v3|g' \
  .github/workflows/code.yaml

sed -i '' \
  's|docker/login-action@v1|docker/login-action@v3|g' \
  .github/workflows/code.yaml

sed -i '' \
  's|docker/build-push-action@v2|docker/build-push-action@v6|g' \
  .github/workflows/code.yaml
```

**Step 3: 验证替换结果**

```bash
grep "uses:" .github/workflows/code.yaml
```

**Step 4: Commit**

```bash
git add .github/workflows/code.yaml
git commit -m "ci: upgrade github actions to latest versions in code workflow"
```

---

### Task 6：端到端验证

**Step 1: 完整重建镜像**

```bash
make build
```

**Step 2: 运行验证命令**

```bash
# 确认工具均可用
docker run --rm maguowei/base go version      # 应为 go1.26.x
docker run --rm maguowei/base eza --version   # 应正常输出
docker run --rm maguowei/base uv --version    # 应正常输出
docker run --rm maguowei/base node --version  # 应为 v22.x

# 确认 gnupg 已删除
docker run --rm maguowei/base dpkg -l | grep gnupg  # 应无输出

# 确认 zsh 启动正常
docker run --rm maguowei/base zsh -c "echo OK"  # 应输出 OK
```

**Step 3: 构建 code 镜像（验证继承链）**

```bash
make build-code
docker run --rm maguowei/code claude --version
```
