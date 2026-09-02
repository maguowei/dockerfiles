# Superset

基于 `apache/superset` 的定制镜像，预装 MySQL 驱动（mysqlclient + PyMySQL）并默认中文界面。

## 快速开始

### 1. 构建镜像

```bash
make build-superset
```

### 2. 运行服务

```bash
# 持久化 metadata（默认 SQLite 存于 /app/superset_home）
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

| 变量 | 必需 | 说明 |
|------|------|------|
| SUPERSET_SECRET_KEY | 是 | 会话加密密钥，必须固定，变更会导致已存凭据失效 |

### 自定义配置

`superset_config.py` 复制到镜像的 `/app/pythonpath/`（官方镜像已将该目录加入 `PYTHONPATH`），当前设置默认语言为中文。需要覆盖时可挂载自己的配置文件：

```bash
-v $(pwd)/superset_config.py:/app/pythonpath/superset_config.py
```

## 注意事项

- 默认使用 SQLite 存储 metadata 与文件系统缓存，仅适合单容器场景；生产环境应改用外部 PostgreSQL/MySQL 与 Redis。
- 上游运行环境为 `/app/.venv`，追加 Python 包需指定该解释器，否则会装进系统 Python 而不被 Superset 加载：

  ```dockerfile
  RUN uv pip install --no-cache --python /app/.venv/bin/python <package>
  ```

- mysqlclient 在 PyPI 没有 Linux wheel，需源码编译。Dockerfile 临时安装 `build-essential`、
  `default-libmysqlclient-dev`、`pkg-config` 编译后清理，但运行时共享库 `libmariadb3` 必须显式
  `apt-mark manual` 保留，否则会被 `--auto-remove` 删掉，导致 `import MySQLdb` 报缺
  `libmariadb.so.3`。

## 参考资料

- [Superset 官方文档](https://superset.apache.org/docs/intro)
- [Docker 镜像使用说明](https://superset.apache.org/docs/quickstart)
- [数据库驱动依赖列表](https://superset.apache.org/docs/configuration/databases)
