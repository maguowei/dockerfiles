FROM alpine:3.11
LABEL maintainer="imaguowei@gmail.com"

ENV APP_NAME ${APP_NAME}
ENV APP_ENV ${APP_ENV}
ENV APP_SOURCE_CODE_PATH /opt/app
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
    && mkdir -p ${APP_SOURCE_CODE_PATH} && chown -R app:app ${APP_SOURCE_CODE_PATH}
WORKDIR ${APP_SOURCE_CODE_PATH}
VOLUME ${APP_LOG_PATH}
USER app
RUN echo "PS1=$" >> ~/.bashrc

ONBUILD COPY --from=builder /opt/app/app /opt/app/app
EXPOSE 8080
CMD ["app"]
