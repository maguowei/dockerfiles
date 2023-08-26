FROM v2fly/v2fly-core:v5.4.1
LABEL version="0.2.0"
LABEL maintainer="imaguowei@gmail.com"

COPY config.json /etc/v2ray/config.json
RUN sed -i "s/{uuid}/$(v2ctl uuid)/g" /etc/v2ray/config.json
EXPOSE 1984
