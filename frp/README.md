# frp

```bash
# frps
$ docker run -it --rm -p 7000:7000 -p 6666:6666 maguowei/frp

# frpc
# example service
python3 -m http.server --bind 127.0.0.1 8888

docker run -it --rm --network host maguowei/frp /frp/frpc tcp --server_addr $(frps_ip):7000 --local_port 8888 --remote_port 6666
```
