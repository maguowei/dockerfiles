# V2Ray

## Usage

```bash
# build
docker build -t maguowei/v2ray .

# server: auto-generate UUID at startup; read it from container logs
docker run --name v2ray -d --restart always -p 1984:1984 maguowei/v2ray
docker logs v2ray | grep "VMess UUID"

# server: provide your own UUID via env (V2RAY_UUID is ignored if config.json is mounted)
docker run --name v2ray -d --restart always -p 1984:1984 \
    -e V2RAY_UUID=8c0e6e5b-1234-5678-90ab-cdef01234567 \
    maguowei/v2ray

# client http proxy; client_http_config.json need update id
docker run --name v2ray-http-client -d --restart always -p 1080:1080 \
    -v ${PWD}/client_http_config.json:/opt/v2ray/etc/config.json \
    maguowei/v2ray

export http_proxy=http://127.0.0.1:1080;https_proxy=http://127.0.0.1:1080
curl -v http://api.twitter.com/1.1/statuses/update.json
```

## Ref

- [v2fly/v2ray-core](https://github.com/v2fly/v2ray-core)
