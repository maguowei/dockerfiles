FROM ubuntu:20.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/surge-snell"
LABEL version="0.1.0"

ENV SNELL_VERSION v2.0.5
# RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget \
    unzip \
    && wget -O snell-server.zip https://github.com/surge-networks/snell/releases/download/${SNELL_VERSION}/snell-server-${SNELL_VERSION}-linux-amd64.zip \
    && unzip snell-server.zip \
    && rm snell-server.zip \
    && mv snell-server /usr/local/bin/ \
&& rm -rf /var/lib/apt/lists/*

COPY snell-server.conf /etc/snell/snell-server.conf
COPY entrypoint.sh /entrypoint.sh
EXPOSE 1984

ENTRYPOINT ["/entrypoint.sh"]
