FROM python:3.12-slim
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python"
LABEL version="0.2.0"

RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    locales \
    && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8

ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
ENV PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple/

ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install -U pip && pip install poetry

CMD ["python"]
