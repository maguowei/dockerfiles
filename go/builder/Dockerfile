FROM golang:1.26-alpine AS builder
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH=/opt/app
WORKDIR ${APP_PATH}

# 配置镜像源和安装依赖
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories \
    && apk add --no-cache git \
    && go env -w GOPROXY=https://goproxy.cn,direct

ONBUILD ARG APP_NAME
ONBUILD COPY go.mod go.sum ./
ONBUILD RUN go mod download
ONBUILD COPY . ${APP_PATH}
ONBUILD RUN CGO_ENABLED=0 go build -v -ldflags "-s -w" \
    -o ${APP_NAME}.app ${APP_PATH}/cmd/${APP_NAME}
