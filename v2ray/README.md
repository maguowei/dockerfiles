# V2Ray

## Usage

```bash
# build
docker build -t maguowei/v2ray .

# generate new uuid
docker run -it --rm maguowei/v2ray uuid

# server run
docker run --name v2ray -d --restart always -p 1984:1984 maguowei/v2ray

# get client id
docker exec -it v2ray cat /etc/v2ray/config.json|grep "id"

# client http proxy; client_http_config.json need update id
docker run --name v2ray-http-client -d --restart always -p 1080:1080 -v ${PWD}/client_http_config.json:/etc/v2ray/config.json maguowei/v2ray

export http_proxy=http://127.0.0.1:1080;https_proxy=http://127.0.0.1:1080
curl -v http://api.twitter.com/1.1/statuses/update.json
```

## Ref

- [v2fly/v2ray-core](https://github.com/v2fly/v2ray-core)
