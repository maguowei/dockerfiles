# ---------------------------------------------------
# 语言配置：默认中文界面
# ---------------------------------------------------
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "zh": {"flag": "cn", "name": "Chinese"},
}
BABEL_DEFAULT_LOCALE = "zh"

# ---------------------------------------------------
# 其他常用配置（按需开启）
# ---------------------------------------------------
# 单容器模式默认使用文件系统缓存，接入 Redis 时再配置 CACHE_CONFIG
# CACHE_CONFIG = {
#     "CACHE_TYPE": "RedisCache",
#     "CACHE_DEFAULT_TIMEOUT": 300,
#     "CACHE_REDIS_URL": "redis://redis:6379/0",
# }

# 上传 CSV / Excel 的临时目录
# UPLOAD_FOLDER = "/app/superset_home/uploads/"
