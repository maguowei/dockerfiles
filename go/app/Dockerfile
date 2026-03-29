FROM alpine:3.21

ARG ALPINE_MIRROR=

LABEL org.opencontainers.image.title="go-app" \
      org.opencontainers.image.description="Reusable Go runtime base image" \
      org.opencontainers.image.authors="imaguowei@gmail.com"

ENV APP_PATH=/opt/app \
    APP_BIN=/opt/app/app \
    TZ=Asia/Shanghai \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_CTYPE=zh_CN.UTF-8

RUN if [ -n "${ALPINE_MIRROR}" ]; then \
        sed -i "s|https://dl-cdn.alpinelinux.org|${ALPINE_MIRROR}|g" /etc/apk/repositories; \
    fi \
    && apk add --no-cache ca-certificates tzdata \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && addgroup -g 10001 -S app \
    && adduser -u 10001 -S -D -H -G app app \
    && mkdir -p "${APP_PATH}" \
    && chown -R app:app "${APP_PATH}"

COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

WORKDIR ${APP_PATH}
USER app

STOPSIGNAL SIGTERM
EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD []
