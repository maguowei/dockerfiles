FROM alpine
LABEL version="0.1.0"

ENV FRP_VERSION 0.42.0
RUN sed -i "s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g" /etc/apk/repositories
RUN apk --update --no-cache add ca-certificates wget
RUN wget -qO- https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz | tar xzv
RUN mv frp_${FRP_VERSION}_linux_amd64 /frp

FROM scratch
COPY --from=0 /frp /frp
CMD ["/frp/frps"]
