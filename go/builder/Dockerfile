FROM golang:1.14-alpine AS builder
LABEL maintainer="imaguowei@gmail.com"

WORKDIR /opt/app
RUN go env -w GOPROXY=https://goproxy.cn,direct
ONBUILD ARG APP_NAME
ONBUILD COPY . /opt/app
ONBUILD RUN go mod download
ONBUILD RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -v -o app /opt/app/cmd/app/${APP_NAME}
