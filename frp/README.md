# frp

```bash
# frps
$ docker run -d --name frps -p 7000:7000 -p 7500:7500 --entrypoint /frp/frps maguowei/frp --token xxxx --dashboard-port 7500 --dashboard-pwd xxxxx



# frpc
# example service
python3 -m http.server --bind 127.0.0.1 8888

docker run -it --rm --network host maguowei/frp /frp/frpc tcp --server_addr $(frps_ip):7000 --local_port 8888 --remote_port 6666
```

- [fatedier/frp](https://github.com/fatedier/frp)
