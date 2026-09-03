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
# 其他常用配置（按需开启）
# ---------------------------------------------------
# 上传 CSV / Excel 的临时目录
# UPLOAD_FOLDER = "/app/superset_home/uploads/"

# 虚拟数据集中使用 Jinja 宏（dataset()、filter_values() 等）
# FEATURE_FLAGS = {"ENABLE_TEMPLATE_PROCESSING": True}
