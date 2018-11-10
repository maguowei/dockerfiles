FROM ubuntu:18.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/shadowsocks"
LABEL version="18.04"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN pip3 install git+https://github.com/shadowsocks/shadowsocks.git@master

EXPOSE 1984

ENTRYPOINT ["ssserver"]
