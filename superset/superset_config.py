import os

# ---------------------------------------------------
# 语言配置：默认中文界面
# ---------------------------------------------------
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "zh": {"flag": "cn", "name": "Chinese"},
}
BABEL_DEFAULT_LOCALE = "zh"

# ---------------------------------------------------
# Metadata 数据库
# ---------------------------------------------------
# 默认沿用上游的 SQLite（存于 /app/superset_home）。
# 设置 DATABASE_HOST 即切换到 MySQL；也可直接用环境变量
# SUPERSET__SQLALCHEMY_DATABASE_URI 完整覆盖（该变量在配置加载后生效，优先级最高）。
if os.environ.get("DATABASE_HOST"):
    SQLALCHEMY_DATABASE_URI = (
        "mysql://"
        f"{os.environ.get('DATABASE_USER', 'superset')}:"
        f"{os.environ.get('DATABASE_PASSWORD', '')}@"
        f"{os.environ['DATABASE_HOST']}:"
        f"{os.environ.get('DATABASE_PORT', '3306')}/"
        f"{os.environ.get('DATABASE_DB', 'superset')}"
        "?charset=utf8mb4"
    )

    # 连接池仅适用于 MySQL：SQLite 走 NullPool，传 pool_size/max_overflow 会让
    # create_engine 抛 TypeError，容器起不来。
    # pool_recycle 必须小于 MySQL 的 wait_timeout（默认 8 小时）以避免空闲断连。
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
    }

# ---------------------------------------------------
# Redis 缓存
# ---------------------------------------------------
# 设置 REDIS_HOST 即启用。未设置时沿用上游默认：CACHE_CONFIG 与 DATA_CACHE_CONFIG
# 为 NullCache（完全不缓存，图表每次都查库），筛选器状态与图表参数存 metadata 库的
# key_value 表，RESULTS_BACKEND 为 None（SQL Lab 异步查询不可用）。
REDIS_HOST = os.environ.get("REDIS_HOST")

if REDIS_HOST:
    REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
    _auth = f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""

    def _redis_url(db: int) -> str:
        return f"redis://{_auth}{REDIS_HOST}:{REDIS_PORT}/{db}"

    # 分库避免 key 冲突：0 留给 Celery broker，1-4 为各类缓存
    CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 86400,
        "CACHE_KEY_PREFIX": "superset_meta_",
        "CACHE_REDIS_URL": _redis_url(1),
    }
    DATA_CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_KEY_PREFIX": "superset_data_",
        "CACHE_REDIS_URL": _redis_url(2),
    }
    # 以下两项默认存 metadata 库（SupersetMetastoreCache），改用 Redis 可减少
    # metadata 库压力并降低读写延迟
    FILTER_STATE_CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 86400,
        "CACHE_KEY_PREFIX": "superset_filter_",
        "CACHE_REDIS_URL": _redis_url(3),
    }
    EXPLORE_FORM_DATA_CACHE_CONFIG = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 86400,
        "CACHE_KEY_PREFIX": "superset_form_",
        "CACHE_REDIS_URL": _redis_url(4),
    }

    # 限流计数器，不配则 flask-limiter 用内存存储并告警
    RATELIMIT_STORAGE_URI = _redis_url(5)

    # SQL Lab 异步查询与定时任务，需额外运行 celery worker 才生效
    class CeleryConfig:
        broker_url = _redis_url(0)
        result_backend = _redis_url(0)
        imports = (
            "superset.sql_lab",
            "superset.tasks.scheduler",
            "superset.tasks.cache",
        )
        worker_prefetch_multiplier = 1
        task_acks_late = True

    CELERY_CONFIG = CeleryConfig

    from flask_caching.backends.rediscache import RedisCache

    RESULTS_BACKEND = RedisCache(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        password=REDIS_PASSWORD or None,
        db=6,
        key_prefix="superset_results_",
    )

# ---------------------------------------------------
# MCP 服务（AI 客户端接入）
# ---------------------------------------------------
# 由 superset mcp run 启动的独立进程读取本段配置，与 web 进程共用同一份文件。

# 对外访问地址。MCP 工具生成 explore / SQL Lab 链接时读
# WEBDRIVER_BASEURL_USER_FRIENDLY，上游默认回落到 http://localhost:9001（开发端口），
# 与本镜像的 8088 不符，会返回打不开的链接，故显式设置。
SUPERSET_PUBLIC_URL = os.environ.get("SUPERSET_PUBLIC_URL", "http://localhost:8088")
SUPERSET_WEBSERVER_ADDRESS = SUPERSET_PUBLIC_URL
WEBDRIVER_BASEURL = f"{SUPERSET_PUBLIC_URL.rstrip('/')}/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

# 所有 MCP 请求的执行身份。名字里的 DEV 有误导：6.1.0 里它是唯一的身份来源，
# 即使开了 JWT 也一样 —— token 的 sub 不会映射到 Superset 用户（default_user_resolver
# 在上游有定义但无调用点），g.user 只由此项设置。该用户的 RBAC/RLS 权限即为 AI 客户端
# 的权限上限。必须写在配置文件里，设成同名环境变量不生效。
_mcp_user = os.environ.get("MCP_DEV_USERNAME")
if _mcp_user:
    MCP_DEV_USERNAME = _mcp_user

# JWT 门禁。设置 MCP_JWT_SECRET 即启用：无有效 Bearer token 的请求返回 401。
# 注意它只做访问控制，不区分调用者身份（见上），因此不能替代多用户隔离。
# 公网暴露时除本项外还必须套 TLS 反代。
_mcp_jwt_secret = os.environ.get("MCP_JWT_SECRET")
if _mcp_jwt_secret:
    MCP_AUTH_ENABLED = True
    MCP_JWT_ALGORITHM = "HS256"
    MCP_JWT_SECRET = _mcp_jwt_secret
    MCP_JWT_ISSUER = os.environ.get("MCP_JWT_ISSUER", "superset-mcp")
    MCP_JWT_AUDIENCE = os.environ.get("MCP_JWT_AUDIENCE", "superset-mcp")

# ---------------------------------------------------
# 其他常用配置（按需开启）
# ---------------------------------------------------
# 上传 CSV / Excel 的临时目录
# UPLOAD_FOLDER = "/app/superset_home/uploads/"

# 虚拟数据集中使用 Jinja 宏（dataset()、filter_values() 等）
# FEATURE_FLAGS = {"ENABLE_TEMPLATE_PROCESSING": True}
