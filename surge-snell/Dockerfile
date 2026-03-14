FROM debian:13-slim AS downloader
ARG TARGETARCH
ARG TARGETVARIANT
ENV SNELL_VERSION=v5.0.1

RUN apt-get update && apt-get install -y --no-install-recommends wget unzip \
    && case "${TARGETARCH}${TARGETVARIANT}" in \
        amd64)  ARCH=amd64   ;; \
        armv7)  ARCH=armv7l  ;; \
        *) echo "Unsupported arch: ${TARGETARCH}${TARGETVARIANT}" && exit 1 ;; \
    esac \
    && wget -O /tmp/snell.zip "https://dl.nssurge.com/snell/snell-server-${SNELL_VERSION}-linux-${ARCH}.zip" \
    && unzip /tmp/snell.zip -d /tmp \
    && chmod +x /tmp/snell-server

FROM debian:13-slim
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/surge-snell"

COPY --from=downloader /tmp/snell-server /usr/local/bin/snell-server
COPY snell-server.conf /etc/snell/snell-server.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 1984
ENTRYPOINT ["/entrypoint.sh"]
