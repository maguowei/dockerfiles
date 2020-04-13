FROM golang:1.14-alpine AS builder
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH /opt/app
WORKDIR ${APP_PATH}
RUN go env -w GOPROXY=https://goproxy.cn,direct
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk add -U git
ONBUILD ARG APP_NAME
ONBUILD COPY go.mod go.sum ./
ONBUILD RUN go mod download
ONBUILD COPY . ${APP_PATH}
ONBUILD RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -v -o app ${APP_PATH}/cmd/${APP_NAME}
