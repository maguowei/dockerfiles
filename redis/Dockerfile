FROM redislabsmodules/rmbuilder:latest as builder

ADD https://github.com/RedisBloom/RedisBloom/archive/v2.2.4.tar.gz /
WORKDIR /
RUN tar xzvf v2.2.4.tar.gz
WORKDIR /RedisBloom-2.2.4
RUN set -ex;\
    make clean; \
    make all -j 4; \
    make test;


FROM redis:6.0.5
ENV LIBDIR /usr/lib/redis/modules
WORKDIR /data
RUN set -ex;\
    mkdir -p "$LIBDIR";
COPY --from=builder /RedisBloom-2.2.4/redisbloom.so "$LIBDIR"

CMD ["redis-server", "--loadmodule", "/usr/lib/redis/modules/redisbloom.so"]
