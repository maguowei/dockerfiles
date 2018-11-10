FROM ubuntu:18.04
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/shadowsocks"
LABEL version="18.04"

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip3 install git+https://github.com/shadowsocks/shadowsocks.git@master

EXPOSE 1984

ENTRYPOINT ["ssserver"]
