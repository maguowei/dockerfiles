FROM alpine:3.21
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH=/opt/app
ENV APP_LOG_PATH=/data/app/log

# 配置镜像源，安装最小运行时依赖
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories \
    && apk add --no-cache tzdata curl ca-certificates \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 创建非 root 用户和目录
RUN addgroup -S app && adduser -S app -G app \
    && mkdir -p ${APP_LOG_PATH} ${APP_PATH} \
    && chown -R app:app ${APP_LOG_PATH} ${APP_PATH}

WORKDIR ${APP_PATH}
VOLUME ${APP_LOG_PATH}
USER app

ONBUILD ARG APP_NAME
ONBUILD ENV APP_NAME=${APP_NAME}
ONBUILD COPY --from=builder ${APP_PATH}/${APP_NAME}.app ${APP_PATH}/${APP_NAME}.app
ONBUILD COPY --from=builder ${APP_PATH}/configs/ ${APP_PATH}/configs/

EXPOSE 8080
CMD ["sh", "-c", "${APP_NAME}.app"]
