# V2Ray

## Usage

```bash
# build
docker build -t maguowei/v2ray .

# generate new uuid
docker run -it --rm maguowei/v2ray v2ctl uuid

# run
docker run --name v2ray -d --restart always -p 1984:1984 -v ${PWD}/config.json:/etc/v2ray/config.json maguowei/v2ray
```

## Ref

- [/v2ray/v2ray-core](https://github.com/v2ray/v2ray-core)
