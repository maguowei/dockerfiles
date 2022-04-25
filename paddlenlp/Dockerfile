FROM python:3.9-slim
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/paddlenlp"
LABEL version="0.1.0"

RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "s/security.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    locales \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_CTYPE zh_CN.UTF-8

ENV PIP_INDEX_URL https://mirror.baidu.com/pypi/simple
ENV PIPENV_PYPI_MIRROR https://mirror.baidu.com/pypi/simple

ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

ENV POETRY_VIRTUALENVS_CREATE false
RUN pip install -U pip && pip install poetry

RUN pip install paddlepaddle==2.2.2 && \
    pip install paddlenlp && \
    pip install pypinyin && \
    pip install ipython

CMD ["ipython"]
