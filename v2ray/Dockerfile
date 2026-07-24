FROM ghcr.io/v2fly/v2ray:v5.47.0 AS upstream

FROM alpine:3.21
LABEL version="0.3.0"
LABEL maintainer="imaguowei@gmail.com"

RUN apk add --no-cache ca-certificates

COPY --from=upstream /opt/v2ray/bin/v2ray /usr/local/bin/v2ray
COPY config.json /opt/v2ray/etc/config.template.json
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 1984
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run", "-config", "/opt/v2ray/etc/config.json"]
