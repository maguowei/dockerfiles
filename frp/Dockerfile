FROM alpine
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk --update --no-cache add ca-certificates wget
RUN wget -qO- https://github.com/fatedier/frp/releases/download/v0.32.0/frp_0.32.0_linux_amd64.tar.gz | tar xzv
RUN mv frp_0.32.0_linux_amd64 /frp

FROM scratch
COPY --from=0 /frp /frp
CMD ["/frp/frps"]
