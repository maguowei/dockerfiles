FROM alpine:3.16
LABEL version="0.2.0"
LABEL maintainer="imaguowei@gmail.com"

ENV APP_PATH /opt/app
ENV APP_LOG_PATH /data/app/log
ENV PATH .:$PATH
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk add -U tzdata \
    curl \
    iputils \
    net-tools
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime

RUN addgroup -S app && adduser -S app -G app
RUN mkdir -p ${APP_LOG_PATH} && chown -R app:app ${APP_LOG_PATH} \
    && mkdir -p ${APP_PATH} && chown -R app:app ${APP_PATH}
WORKDIR ${APP_PATH}
VOLUME ${APP_LOG_PATH}
USER app
RUN echo "PS1=$" >> ~/.bashrc

ONBUILD ARG APP_NAME
ONBUILD ARG APP_ENV
ONBUILD ENV APP_NAME ${APP_NAME}
ONBUILD ENV APP_ENV ${APP_ENV}
ONBUILD COPY --from=builder ${APP_PATH}/${APP_NAME}.app ${APP_PATH}/${APP_NAME}.app
ONBUILD COPY --from=builder ${APP_PATH}/configs/ ${APP_PATH}/configs
EXPOSE 8080
CMD ["sh", "-c", "${APP_NAME}.app"]
