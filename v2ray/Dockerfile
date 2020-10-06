FROM golang:alpine AS builder
RUN apk update && apk add --no-cache git bash wget curl
WORKDIR /go/src/v2ray.com/core
RUN git clone --progress https://github.com/v2fly/v2ray-core.git . && \
    bash ./release/user-package.sh nosource noconf codename=$(git describe --tags) buildname=docker-fly abpathtgz=/tmp/v2ray.tgz

FROM alpine:latest

LABEL maintainer="imaguowei@gmail.com"

COPY --from=builder /tmp/v2ray.tgz /tmp
# RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk update && apk upgrade \
    && apk add --update tzdata \
    && apk --no-cache add ca-certificates \
    && update-ca-certificates \
&& rm -rf /var/cache/apk/*

ENV TZ=Asia/Shanghai
ENV PATH /usr/bin/v2ray:$PATH
COPY config.json /etc/v2ray/config.json

RUN apk update && apk add ca-certificates && \
    mkdir -p /usr/bin/v2ray && \
    tar xvfz /tmp/v2ray.tgz -C /usr/bin/v2ray

RUN sed -i "s/{uuid}/$(v2ctl uuid)/g" /etc/v2ray/config.json
EXPOSE 1984
CMD ["v2ray", "-config=/etc/v2ray/config.json"]
