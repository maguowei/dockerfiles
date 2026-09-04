# Superset

基于 `apache/superset` 的定制镜像，预装 MySQL 驱动（mysqlclient + PyMySQL）并默认中文界面。

## 快速开始

### 1. 构建镜像

```bash
make build-superset
```

### 2. 运行服务

单容器方式，metadata 存 SQLite，适合本地试用：

```bash
docker volume create superset_home

# 生成固定 SECRET_KEY，只需生成一次并妥善保存
openssl rand -base64 42

docker run -d \
  --name superset \
  -p 8088:8088 \
  -v superset_home:/app/superset_home \
  -e SUPERSET_SECRET_KEY="替换为上一步生成的值" \
  --restart unless-stopped \
  maguowei/superset
```

生产环境改用 MySQL + Redis，见下方[生产部署](#生产部署mysql--redis)。

### 3. 初始化（仅首次）

```bash
docker exec -it superset superset db upgrade

docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname Admin \
  --email admin@example.com \
  --password admin

docker exec -it superset superset init
```

访问 http://localhost:8088 登录，界面默认为中文。

## 生产部署（MySQL + Redis）

默认的 SQLite 只支持单进程写入，且图表查询完全没有缓存（上游默认 `NullCache`），
仅适合单容器试用。生产环境需换成 MySQL 存 metadata、Redis 做缓存。

### 使用 docker compose

`docker-compose.yaml` 已编排好 MySQL 8.4、Redis 7、Superset 以及 worker、beat、mcp。
先从模板生成 `.env`：

```bash
cd superset
cp .env.example .env
```

模板里标了「必填」的四项必须填，缺任意一项 `docker compose up` 会直接报
`required variable ... is missing a value`（compose 里用 `:?required` 强制）：

| 变量 | 生成方式 |
|------|----------|
| SUPERSET_SECRET_KEY | `openssl rand -base64 42` |
| MYSQL_ROOT_PASSWORD | `openssl rand -base64 24` |
| DATABASE_PASSWORD | `openssl rand -base64 24` |
| MCP_JWT_SECRET | `openssl rand -base64 32` |

其余项（库名、用户名、宿主机端口、`MCP_DEV_USERNAME`、`SUPERSET_PUBLIC_URL`）都有默认值，
按需取消注释覆盖即可。`.env` 含明文密码，已被 `.gitignore` 排除，不要提交到版本库。

启动并初始化：

```bash
docker compose up -d

docker compose exec superset superset db upgrade
docker compose exec superset superset fab create-admin \
  --username admin --firstname Admin --lastname Admin \
  --email admin@example.com --password admin
docker compose exec superset superset init
```

`worker` 和 `beat` 两个服务用于 SQL Lab 异步查询、定时任务和告警报表。不需要这些功能可从
compose 文件中删掉，Superset 本身不依赖它们。

这三个非 web 服务的健康检查都在 compose 里做了调整，原因值得留意：

- `worker` 换成 `celery inspect ping`。镜像内置的 `HEALTHCHECK` 是 curl web 端口，worker
  不跑 web server，沿用会永久 unhealthy。ping 需要加载 superset app，故 `start_period` 留了 120s。
- `beat` 和 `mcp` 直接 `healthcheck: disable: true`。beat 没有 worker 那样的 inspect 接口；
  mcp 监听 5008 且只挂 `/mcp` 一条 streamable-http 路由、没有 `/health`，stateless 下
  `GET /mcp` 恒回 405。两者崩了容器直接退出，`restart` 策略比假 healthy 更可靠。
- `beat` 的 `--schedule` 必须显式指向 `/app/superset_home/`。默认写到 WORKDIR（`/app`，
  root:root 0755），容器以 uid 1000 运行，开 shelve 直接 `Errno 13`，且 celery 会误判成
  文件损坏反复重试。

### 接入已有的 MySQL 与 Redis

配置文件通过环境变量启用，设置 `DATABASE_HOST` 即切到 MySQL，设置 `REDIS_HOST` 即启用 Redis 缓存：

```bash
docker run -d \
  --name superset \
  -p 8088:8088 \
  -v superset_home:/app/superset_home \
  -e SUPERSET_SECRET_KEY="..." \
  -e DATABASE_HOST=mysql.internal \
  -e DATABASE_USER=superset \
  -e DATABASE_PASSWORD=... \
  -e DATABASE_DB=superset \
  -e REDIS_HOST=redis.internal \
  maguowei/superset
```

metadata 库需预先建好，字符集用 `utf8mb4`：

```sql
CREATE DATABASE superset CHARACTER SET utf8mb4;
CREATE USER 'superset'@'%' IDENTIFIED BY '密码';
GRANT ALL PRIVILEGES ON superset.* TO 'superset'@'%';
FLUSH PRIVILEGES;
```

不要显式指定 `COLLATE utf8mb4_unicode_ci`。Superset 的 `uuid` 列是 `binary(16)`，
在该 collation 下与字符串列比较会触发 MySQL 1267 `Illegal mix of collations`，
导致数据库、图表等列表页直接 500（[apache/superset#29483][issue-29483]）。
用 MySQL 8 的默认 `utf8mb4_0900_ai_ci` 即可，compose 文件里也只设了 charset。

[issue-29483]: https://github.com/apache/superset/issues/29483

也可以用 `SUPERSET__SQLALCHEMY_DATABASE_URI` 直接给完整连接串，它在配置文件加载后生效，
优先级最高，适合需要额外连接参数的场景。

### Redis 分库用途

配置文件按用途分库，避免 key 冲突：

| DB | 用途 |
|----|------|
| 0 | Celery broker / result backend |
| 1 | CACHE_CONFIG，元数据缓存 |
| 2 | DATA_CACHE_CONFIG，图表查询结果 |
| 3 | FILTER_STATE_CACHE_CONFIG，dashboard 筛选器状态 |
| 4 | EXPLORE_FORM_DATA_CACHE_CONFIG，图表编辑参数 |
| 5 | 限流计数器 |
| 6 | SQL Lab 异步查询结果 |

### 不配 Redis 时的默认行为

未设置 `REDIS_HOST` 时沿用上游默认值：

| 配置项 | 默认后端 | 实际行为 |
|--------|----------|----------|
| CACHE_CONFIG | NullCache | 完全不缓存 |
| DATA_CACHE_CONFIG | NullCache | 完全不缓存，图表每次都查底层库 |
| FILTER_STATE_CACHE_CONFIG | SupersetMetastoreCache | 存 metadata 库的 `key_value` 表 |
| EXPLORE_FORM_DATA_CACHE_CONFIG | SupersetMetastoreCache | 同上 |
| RESULTS_BACKEND | None | SQL Lab 异步查询不可用 |
| RATELIMIT_STORAGE_URI | None | flask-limiter 用内存并在启动时告警 |

筛选器状态与图表参数默认落在 metadata 库，多 worker 下不会丢；配 Redis 的收益是减少
metadata 库压力和降低延迟。而图表查询默认真的没有缓存，dashboard 每次打开都会重跑全部
SQL —— 这是配 Redis 最主要的动机。SQL Lab 异步查询和定时告警报表则必须有 Redis 才能用。

### 从 SQLite 迁移已有数据

metadata 迁移没有官方内置命令，推荐用导出导入搬运资产：

```bash
# 旧容器导出 dashboard（含依赖的 chart 与 dataset）
docker exec superset superset export-dashboards -f /tmp/dash.zip
docker cp superset:/tmp/dash.zip .

# 新环境完成 db upgrade / create-admin / init 后导入
docker cp dash.zip superset-new:/tmp/
docker exec superset-new superset import-dashboards -p /tmp/dash.zip
```

数据库连接的密码不会随导出带出，导入后需在 UI 里重填。用户账号和权限也不在导出范围内。

## 连接 MySQL 数据源

添加数据库时 MySQL 会直接出现在推荐图标中，SQLAlchemy URI：

```
mysql://user:password@host:3306/dbname            # mysqlclient，默认推荐
mysql+pymysql://user:password@host:3306/dbname    # PyMySQL，纯 Python 实现
```

两个驱动都已预装。`caching_sha2_password` 认证下 mysqlclient 可能失败，此时改用 `mysql+pymysql://`。

镜像必须装 mysqlclient 才能让 MySQL 出现在 UI 列表里：Superset 判定引擎可用性时只检查
`sqlalchemy.dialects.registry.load("mysql")` 返回的默认 dialect（driver 为 `mysqldb`），
该 dialect 依赖 `MySQLdb` 模块。只装 PyMySQL 时它提供的是 `mysql+pymysql` dialect，
不参与该检查，UI 的数据库列表就只会显示 PostgreSQL 和 SQLite。

## AI 功能（MCP）

Superset 5.0+ 内置 MCP（Model Context Protocol）服务，把 dashboard、chart、dataset 和 SQL Lab
暴露成一组工具，供 Claude Code、Claude Desktop 等 AI 客户端用自然语言驱动：列数据集
（`list_datasets`）、跑 SQL（`execute_sql`）、建图表（`generate_chart`）、生成 explore 链接
（`generate_explore_link`）等 20 余个工具。

该服务是独立进程，与 web 进程共用同一份 `superset_config.py` 和 metadata 库。本镜像已预装
`fastmcp`（上游把它放在 `[fastmcp]` extra 里，官方 lean 镜像不含，缺失时 `superset mcp run`
会直接报错退出）。

### 使用 docker compose

`mcp` 服务已在 compose 里编排好，相关变量都在 `.env.example` 模板中：`MCP_JWT_SECRET`
（必填）、`MCP_DEV_USERNAME`、`SUPERSET_PUBLIC_URL`、`MCP_PORT`。

`MCP_JWT_SECRET` 是必填项（compose 里用 `:?required` 强制），不配 MCP 端点就没有任何访问控制。
`MCP_DEV_USERNAME` 指定所有 MCP 请求的执行身份，必须是已存在的 Superset 用户，默认 `admin`。

```bash
docker compose up -d
docker compose logs mcp | tail -5   # 期望 Uvicorn running on http://0.0.0.0:5008
```

### 单容器方式

```bash
docker run -d \
  --name superset-mcp \
  -p 5008:5008 \
  -v superset_home:/app/superset_home \
  -e SUPERSET_SECRET_KEY="与 web 容器相同" \
  -e MCP_DEV_USERNAME=admin \
  -e MCP_JWT_SECRET="..." \
  -e SUPERSET_PUBLIC_URL=http://localhost:8088 \
  maguowei/superset \
  superset mcp run --host 0.0.0.0 --port 5008
```

metadata 用 MySQL 时同样需要传 `DATABASE_*`，用 SQLite 时必须和 web 容器共享
`superset_home` 卷。

### 签发 token

`MCP_JWT_SECRET` 是服务端的签名密钥，token 是用它签出来的凭证 —— 两者不能互换。
把 token 填进 `MCP_JWT_SECRET`（或反过来）会让所有请求返回 `invalid_token`。

密钥从环境变量读，避免占位符没替换就跑。用 compose 部署时直接从 `.env` 取，
保证与运行中的服务用的是同一个值：

```bash
export MCP_JWT_SECRET=$(grep '^MCP_JWT_SECRET=' .env | cut -d= -f2-)

python3 <<'PY'
import base64, hmac, hashlib, json, os, time

SECRET = os.environ["MCP_JWT_SECRET"]

def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")

now = int(time.time())
header = b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
payload = b64(json.dumps({
    "iss": "superset-mcp",      # 需与 MCP_JWT_ISSUER 一致
    "aud": "superset-mcp",      # 需与 MCP_JWT_AUDIENCE 一致
    "sub": "admin",
    "iat": now,
    "exp": now + 86400 * 30,
}, separators=(",", ":")).encode())
sig = b64(hmac.new(SECRET.encode(), header + b"." + payload, hashlib.sha256).digest())
print((header + b"." + payload + b"." + sig).decode())
PY
```

把输出存进 `TOKEN` 供后续验证使用（需与 curl 在同一 shell 会话，否则请求不带
`Authorization` 头，返回体为空）：

```bash
export TOKEN='上一步输出的 token'
```

`sub` 填什么都不影响执行身份（见下方[限制](#限制)），但 `iss` 和 `aud` 必须匹配，否则 401。

### 验证

```bash
# 无 token 应返回 401
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:5008/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'

# 带 token 查实例信息，应返回 current_user
curl -s -X POST http://localhost:5008/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_instance_info","arguments":{}}}'
```

响应是 SSE 格式（`event: message` + `data: {...}`），不是普通 JSON。

### 客户端接入

Claude Code 在项目根目录建 `.mcp.json`：

```json
{
  "mcpServers": {
    "superset": {
      "type": "url",
      "url": "http://localhost:5008/mcp",
      "headers": {
        "Authorization": "Bearer 你的 token"
      }
    }
  }
}
```

Claude Desktop 不接受非 HTTPS 的直连 MCP，需用 `mcp-remote` 转发并附带请求头：

```json
{
  "mcpServers": {
    "superset": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "http://localhost:5008/mcp",
        "--header", "Authorization:Bearer 你的 token"
      ]
    }
  }
}
```

### 常见错误

| 症状 | 原因 |
|------|------|
| `{"error": "invalid_token"}` | `MCP_JWT_SECRET` 与签 token 用的密钥不一致。最常见的是把 token 本身填进了 `MCP_JWT_SECRET`，或签发脚本里的密钥占位符没替换 |
| 响应体完全为空 | 请求没带 `Authorization` 头，通常是 `$TOKEN` 变量在当前 shell 里为空 |
| HTTP 401 但 token 是新签的 | `iss` / `aud` 与 `MCP_JWT_ISSUER` / `MCP_JWT_AUDIENCE` 不匹配 |
| `No authenticated user found` | token 已通过校验，但 `MCP_DEV_USERNAME` 指定的用户在 metadata 库里不存在 |
| explore 链接指向 `localhost:9001` | `SUPERSET_PUBLIC_URL` 未生效，检查是否挂载了自己的配置文件覆盖了镜像内置的那份 |

### 限制

Superset 6.1.0 的 MCP 实现有几处需要提前知道，否则容易误判：

- **不做多用户身份映射。** 所有 MCP 请求都以 `MCP_DEV_USERNAME` 指定的同一个用户身份执行，
  该用户的 RBAC/RLS 权限就是 AI 客户端的权限上限。JWT 的 `sub` 声明不会被解析成 Superset
  用户 —— 上游 `mcp_service/mcp_config.py` 里的 `default_user_resolver` 有定义但无调用点，
  `g.user` 只由 `MCP_DEV_USERNAME` 设置。所以 JWT 在这个版本里纯粹是 401 门禁，不能用来
  区分调用者。若要按人隔离权限，只能一人一个 MCP 实例配不同的 `MCP_DEV_USERNAME`。

- **`MCP_DEV_USERNAME` 必须落在配置文件里。** 设成同名环境变量后 Superset 读不到，工具调用会
  报 `No authenticated user found`。本镜像的 `superset_config.py` 已做转发，所以 compose 和
  `docker run` 里传环境变量是有效的；但如果你挂载了自己的配置文件，需要自行照抄这段逻辑。

- **默认只列出 4 个工具。** `list_tools` 返回 `search_tools`、`call_tool`、`health_check`、
  `get_instance_info`，其余工具靠 `search_tools` 按名字或用途搜索后经 `call_tool` 调用。这是
  上游默认的省 token 策略（初始上下文从约 40k 降到 5-8k）。要一次暴露全部工具，在配置文件里加
  `MCP_TOOL_SEARCH_CONFIG = {"enabled": False}`。

- **图表预览没有图片格式。** `get_chart_preview` 的 `format` 只支持 `url`、`ascii`、`table`、
  `vega_lite`。上游虽有 `mcp_service/screenshot/` 模块，但在 6.1.0 里没有 HTTP 路由也没有工具
  引用它，属未接通状态，因此本镜像不装 headless Chrome。

- **公网暴露必须套 TLS 反代。** MCP 端点是纯 HTTP，token 会明文传输。

## 配置说明

### 构建参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| SUPERSET_VERSION | 6.1.0 | 上游 `apache/superset` 版本 |
| FASTMCP_VERSION | 3.4.7 | MCP 服务依赖，上游约束为 `>=3.1.0,<4.0` |

### 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| SUPERSET_SECRET_KEY | 是 | — | 会话加密密钥，必须固定，变更会导致已存凭据失效 |
| DATABASE_HOST | 否 | — | 设置后 metadata 改用 MySQL，未设置则用 SQLite |
| DATABASE_PORT | 否 | 3306 | MySQL 端口 |
| DATABASE_DB | 否 | superset | metadata 库名 |
| DATABASE_USER | 否 | superset | MySQL 用户 |
| DATABASE_PASSWORD | 否 | 空 | MySQL 密码 |
| REDIS_HOST | 否 | — | 设置后启用 Redis 缓存与 Celery，未设置则不缓存查询结果 |
| REDIS_PORT | 否 | 6379 | Redis 端口 |
| REDIS_PASSWORD | 否 | 空 | Redis 密码 |
| SUPERSET__SQLALCHEMY_DATABASE_URI | 否 | — | 完整 metadata 连接串，优先级高于上述 DATABASE_* |
| MCP_DEV_USERNAME | 否 | — | MCP 请求的执行身份，需为已存在的 Superset 用户；不设则所有工具调用报错 |
| MCP_JWT_SECRET | 否 | — | 设置后 MCP 端点启用 JWT 门禁（HS256），无有效 token 返回 401 |
| MCP_JWT_ISSUER | 否 | superset-mcp | token 的 `iss` 声明，不匹配则 401 |
| MCP_JWT_AUDIENCE | 否 | superset-mcp | token 的 `aud` 声明，不匹配则 401 |
| SUPERSET_PUBLIC_URL | 否 | http://localhost:8088 | 对外访问地址，MCP 工具生成 explore / SQL Lab 链接时使用 |

### 自定义配置

`superset_config.py` 复制到镜像的 `/app/pythonpath/`（官方镜像已将该目录加入 `PYTHONPATH`），当前设置默认语言为中文。需要覆盖时可挂载自己的配置文件：

```bash
-v $(pwd)/superset_config.py:/app/pythonpath/superset_config.py
```

## 注意事项

- 默认用 SQLite 存 metadata 且不缓存查询结果，仅适合单容器场景；生产环境应改用 MySQL/PostgreSQL 与 Redis。
- 上游运行环境为 `/app/.venv`，追加 Python 包需指定该解释器，否则会装进系统 Python 而不被 Superset 加载：

  ```dockerfile
  RUN uv pip install --no-cache --python /app/.venv/bin/python <package>
  ```

- mysqlclient 在 PyPI 没有 Linux wheel，需源码编译。Dockerfile 临时安装 `build-essential`、
  `default-libmysqlclient-dev`、`pkg-config` 编译后清理，但运行时共享库 `libmariadb3` 必须显式
  `apt-mark manual` 保留，否则会被 `--auto-remove` 删掉，导致 `import MySQLdb` 报缺
  `libmariadb.so.3`。

- metadata 用 MySQL 时不要把 collation 设成 `utf8mb4_unicode_ci`，会导致列表页 500，
  原因见上方[接入已有的 MySQL 与 Redis](#接入已有的-mysql-与-redis)。

- `SQLALCHEMY_ENGINE_OPTIONS` 里的连接池参数只在 MySQL 模式下设置。SQLite 用 NullPool，
  传 `pool_size` / `max_overflow` 会让 `create_engine` 抛 TypeError，容器无法启动。

- 首次启动时 `superset db upgrade` 还没执行，日志会出现几条
  `Table 'superset.themes' doesn't exist`，属正常现象，建表完成后不再出现。

- MCP 服务的执行身份由配置文件里的 `MCP_DEV_USERNAME` 决定，JWT 不做身份映射，
  详见[限制](#限制)。

## 参考资料

- [Superset 官方文档](https://superset.apache.org/docs/intro)
- [Docker 镜像使用说明](https://superset.apache.org/docs/quickstart)
- [数据库驱动依赖列表](https://superset.apache.org/docs/configuration/databases)
- [MCP 服务部署与认证](https://superset.apache.org/admin-docs/configuration/mcp-server/)
- [在 Superset 中使用 AI](https://superset.apache.org/user-docs/using-superset/using-ai-with-superset/)
