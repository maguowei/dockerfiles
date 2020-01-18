# V2Ray

## Usage

```bash
# build
docker build -t maguowei/v2ray .

# generate new uuid
v2ctl uuid

# run
docker run -d --restart always -p 1984:1984 maguowei/v2ray
```

## Ref

- [/v2ray/v2ray-core](https://github.com/v2ray/v2ray-core)
