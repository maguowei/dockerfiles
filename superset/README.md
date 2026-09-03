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

`docker-compose.yaml` 已编排好 MySQL 8.4、Redis 7 与 Superset。先准备 `.env`：

```bash
cd superset

cat > .env <<'EOF'
SUPERSET_SECRET_KEY=
MYSQL_ROOT_PASSWORD=
DATABASE_DB=superset
DATABASE_USER=superset
DATABASE_PASSWORD=
SUPERSET_PORT=8088
EOF

# 填入 SECRET_KEY 与两个密码
openssl rand -base64 42
```

`.env` 含明文密码，不要提交到版本库。

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

## 配置说明

### 构建参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| SUPERSET_VERSION | 6.1.0 | 上游 `apache/superset` 版本 |

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

## 参考资料

- [Superset 官方文档](https://superset.apache.org/docs/intro)
- [Docker 镜像使用说明](https://superset.apache.org/docs/quickstart)
- [数据库驱动依赖列表](https://superset.apache.org/docs/configuration/databases)
