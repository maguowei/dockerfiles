ARG TIDB_VERSION=6.0.0
FROM ubuntu:22.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/tidb"
LABEL version="0.4.0"

ARG TIDB_VERSION
ENV TIDB_VERSION=${TIDB_VERSION}

RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    apt-utils \
    locales

RUN locale-gen zh_CN.UTF-8 && locale-gen en_US.UTF-8

ENV PATH=${PATH}:/root/.tiup/bin

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
    curl \
&& rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
RUN tiup install tidb:v${TIDB_VERSION} tikv:v${TIDB_VERSION} pd:v${TIDB_VERSION} tiflash:v${TIDB_VERSION} grafana:v${TIDB_VERSION} prometheus:v${TIDB_VERSION} playground

CMD ["sh", "-c", "tiup playground --host 0.0.0.0"]
