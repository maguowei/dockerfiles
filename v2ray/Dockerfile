FROM ubuntu:18.04 as builder

# RUN sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl \
    ca-certificates

RUN curl -L -o install-release.sh https://raw.githubusercontent.com/v2ray/v2ray-core/master/release/install-release.sh
RUN chmod +x install-release.sh && ./install-release.sh

FROM alpine:latest

LABEL maintainer="imaguowei@gmail.com"

COPY --from=builder /usr/bin/v2ray  /usr/bin/v2ray
COPY config.json /etc/v2ray/config.json
# RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk update && apk upgrade \
    && apk add --update tzdata \
    && apk --no-cache add ca-certificates \
    && update-ca-certificates \
&& rm -rf /var/cache/apk/*

ENV TZ=Asia/Shanghai
RUN mkdir /var/log/v2ray/

ENV PATH /usr/bin/v2ray:$PATH
COPY config.json /etc/v2ray/config.json

RUN sed -i "s/{uuid}/$(v2ctl uuid)/g" /etc/v2ray/config.json
EXPOSE 1984
CMD ["v2ray", "-config=/etc/v2ray/config.json"]
