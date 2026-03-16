FROM alpine AS builder
RUN apk add --no-cache util-linux
COPY config.json /tmp/config.json
RUN sed -i "s/{uuid}/$(uuidgen)/g" /tmp/config.json

FROM ghcr.io/v2fly/v2ray:v5.47.0
LABEL version="0.2.0"
LABEL maintainer="imaguowei@gmail.com"

COPY --from=builder /tmp/config.json /opt/v2ray/etc/config.json
EXPOSE 1984
CMD [ "run", "-config", "/opt/v2ray/etc/config.json" ]