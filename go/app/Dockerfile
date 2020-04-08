FROM alpine:3.11
LABEL maintainer="imaguowei@gmail.com"

ENV APP_NAME ${APP_NAME}
ENV APP_ENV ${APP_ENV}
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

ONBUILD COPY --from=builder ${APP_PATH}/app ${APP_PATH}/app
EXPOSE 8080
CMD ["app"]
