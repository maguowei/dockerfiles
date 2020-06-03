# V2Ray

## Usage

```bash
# build
docker build -t maguowei/v2ray .

# generate new uuid
docker run -it --rm maguowei/v2ray v2ctl uuid

# server un
docker run --name v2ray -d --restart always -p 1984:1984 -v ${PWD}/config.json:/etc/v2ray/config.json maguowei/v2ray

# client http proxy
docker run --name v2ray-http-client -d --restart always -p 1080:1080 -v ${PWD}/client_http_config.json:/etc/v2ray/config.json maguowei/v2ray

export http_proxy=http://127.0.0.1:1080;https_proxy=http://127.0.0.1:1080
curl -v http://api.twitter.com/1.1/statuses/update.json
```

## Ref

- [v2ray/v2ray-core](https://github.com/v2ray/v2ray-core)
