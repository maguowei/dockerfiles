# docker-shadowsocks

## Usage

```bash
# build
docker build -t maguowei/shadowsocks .
# run
docker run -d --restart always -p 1984:1984 maguowei/shadowsocks -p 1984 -k password -m aes-256-cfb --fast-open --workers 4

# use Kubernetes
kubectl run shadowsocks --generator=run-pod/v1 --image=maguowei/shadowsocks --restart='Always' --command -- ssserver -p 1984 -k ${password} -m aes-256-cfb --fast-open --workers 4

kubectl expose pod shadowsocks --port=1984 --type LoadBalancer
```

## Ref

- [README](https://github.com/shadowsocks/shadowsocks/blob/master/README.md)
- [wiki](https://github.com/shadowsocks/shadowsocks/wiki)
