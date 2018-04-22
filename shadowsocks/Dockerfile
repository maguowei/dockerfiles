FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip3 install shadowsocks

EXPOSE 1984

ENTRYPOINT ["ssserver"]
