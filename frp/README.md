# frp

基于 [fatedier/frp](https://github.com/fatedier/frp) 的内网穿透工具镜像。

```bash
# frps
docker run -d --name frps -p 7000:7000 -p 7500:7500 \
  --entrypoint /frp/frps maguowei/frp \
  --token xxxx --dashboard-port 7500 --dashboard-pwd xxxxx

# frpc
docker run -it --rm --network host maguowei/frp /frp/frpc tcp \
  --server_addr <frps_ip>:7000 --local_port 8888 --remote_port 6666
```
