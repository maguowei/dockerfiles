FROM ubuntu:20.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/base"
LABEL version="20.04"

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
    git \
    wget \
    curl \
    iputils-ping \
    net-tools \
    vim \
    build-essential \
&& rm -rf /var/lib/apt/lists/*

CMD ["bash"]
