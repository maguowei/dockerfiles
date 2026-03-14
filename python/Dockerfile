FROM python:3.14-slim
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python"

# 使用阿里云镜像加速 apt
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list.d/debian.sources

# 安装 locale 和时区依赖
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    locales \
    tzdata \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 uv
RUN pip install --no-cache-dir uv

ENV UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV UV_COMPILE_BYTECODE=1

CMD ["python3"]
