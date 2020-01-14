# docker-shadowsocks

## Usage

### Server

```bash
# build
docker build -t maguowei/shadowsocks .
# run
docker run --name=shadowsocks -d --restart always -p 1984:1984 maguowei/shadowsocks -p 1984 -k ${password} -m aes-256-cfb --fast-open --workers 4

# use Kubernetes
kubectl run shadowsocks --generator=run-pod/v1 --image=maguowei/shadowsocks --restart=Always --command -- ssserver -p 1984 -k ${password} -m aes-256-cfb --fast-open --workers 4

kubectl expose pod shadowsocks --port=1984 --type LoadBalancer
```

### Client

```bash
export server_ip=xxxx; password=xxxx
docker run --name=sslocal -d --restart always -p 1080:1080 --entrypoint=sslocal maguowei/shadowsocks -s ${server_ip} -p 1984 -b 127.0.0.1 -l 1080 -k ${password} -m aes-256-cfb --fast-open
```

## Ref

- [README](https://github.com/shadowsocks/shadowsocks/blob/master/README.md)
- [wiki](https://github.com/shadowsocks/shadowsocks/wiki)
