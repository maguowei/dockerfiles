FROM golang:1.26-alpine

ARG ALPINE_MIRROR=
ARG GOPROXY=https://proxy.golang.org,direct

LABEL org.opencontainers.image.title="go-builder" \
      org.opencontainers.image.description="Reusable Go builder base image" \
      org.opencontainers.image.authors="imaguowei@gmail.com"

ENV CGO_ENABLED=0 \
    GOPROXY=${GOPROXY} \
    TZ=Asia/Shanghai

WORKDIR /src

RUN if [ -n "${ALPINE_MIRROR}" ]; then \
        sed -i "s|https://dl-cdn.alpinelinux.org|${ALPINE_MIRROR}|g" /etc/apk/repositories; \
    fi \
    && apk add --no-cache ca-certificates git tzdata \
    && update-ca-certificates \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

COPY --chmod=755 build-go-app.sh /usr/local/bin/build-go-app
