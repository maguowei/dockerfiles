FROM ubuntu:24.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/base"
LABEL version="22.04"

RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    apt-utils \
    locales

RUN locale-gen zh_CN.UTF-8 && locale-gen en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_CTYPE zh_CN.UTF-8

ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    wget \
    curl \
    iputils-ping \
    net-tools \
    vim \
    zsh \
    build-essential \
    python3-dev \
    python3-setuptools \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

ENV PIP_INDEX_URL https://mirrors.aliyun.com/pypi/simple/
ENV PIPENV_PYPI_MIRROR https://mirrors.aliyun.com/pypi/simple/

RUN python -m pip install -U pip wheel && python -m pip install poetry
RUN wget -O- https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | zsh || true

CMD ["zsh"]
