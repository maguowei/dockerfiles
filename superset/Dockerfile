ARG SUPERSET_VERSION=6.1.0
FROM apache/superset:${SUPERSET_VERSION}
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/superset"
LABEL description="Apache Superset with MySQL driver and Chinese locale"

ARG SUPERSET_VERSION
ENV SUPERSET_VERSION=${SUPERSET_VERSION}

USER root

# MySQL 驱动。必须安装 mysqlclient：Superset 判定 MySQL 是否可用时只检查
# sqlalchemy.dialects.registry.load("mysql") 的默认 dialect（driver=mysqldb），
# 该 dialect 依赖 MySQLdb 模块；仅装 pymysql 不满足检查，UI 数据库列表不会出现 MySQL。
# mysqlclient 在 PyPI 无 Linux wheel，需源码编译，故临时装工具链编译后仅清理编译期依赖，
# 运行时共享库 libmariadb3 必须保留，否则 import MySQLdb 会缺 libmariadb.so.3。
# pymysql 一并保留，供 mysql+pymysql:// 形式使用。
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmariadb3 \
    && apt-mark manual libmariadb3 \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
    && uv pip install --no-cache --python /app/.venv/bin/python mysqlclient pymysql \
    && apt-get purge -y --auto-remove build-essential default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 默认中文界面配置，官方镜像已将 /app/pythonpath 加入 PYTHONPATH
COPY superset_config.py /app/pythonpath/superset_config.py

USER superset
