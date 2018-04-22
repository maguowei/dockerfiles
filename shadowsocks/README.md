# docker-shadowsocks

## Usage

```bash
docker run -d -p 1984:1984 maguowei/shadowsocks -p 1984 -k password -m aes-256-cfb --fast-open --workers 4
```

## Ref:

* [README](https://github.com/shadowsocks/shadowsocks/blob/master/README.md)
* [wiki](https://github.com/shadowsocks/shadowsocks/wiki)