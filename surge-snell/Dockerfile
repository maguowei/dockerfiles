FROM debian:13-slim AS downloader
ARG TARGETARCH
ENV SNELL_VERSION=v5.0.1

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates wget unzip \
    && if [ "${TARGETARCH}" = "amd64" ]; then ARCH=amd64; else ARCH=aarch64; fi \
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
