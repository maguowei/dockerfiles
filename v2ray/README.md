# V2Ray

基于 [v2fly/v2ray-core](https://github.com/v2fly/v2ray-core) 的代理工具镜像。

## 使用

```bash
# server：自动生成 UUID，从容器日志获取
docker run --name v2ray -d --restart always -p 1984:1984 maguowei/v2ray
docker logs v2ray | grep "VMess UUID"

# server：通过环境变量指定 UUID（挂载 config.json 时忽略）
docker run --name v2ray -d --restart always -p 1984:1984 \
  -e V2RAY_UUID=8c0e6e5b-1234-5678-90ab-cdef01234567 \
  maguowei/v2ray

# client http 代理（需更新 client_http_config.json 中的 id）
docker run --name v2ray-http-client -d --restart always -p 1080:1080 \
  -v ${PWD}/client_http_config.json:/opt/v2ray/etc/config.json \
  maguowei/v2ray

export http_proxy=http://127.0.0.1:1080;https_proxy=http://127.0.0.1:1080
curl -v https://www.google.com
```
