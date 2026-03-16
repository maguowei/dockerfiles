FROM ghcr.io/v2fly/v2ray:v5.47.0
LABEL version="0.2.0"
LABEL maintainer="imaguowei@gmail.com"

COPY config.json /etc/v2ray/config.json
RUN sed -i "s/{uuid}/$(v2ray uuid)/g" /etc/v2ray/config.json
EXPOSE 1984
CMD [ "run", "-config", "/etc/v2ray/config.json" ]