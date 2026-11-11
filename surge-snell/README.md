# Surge Snell

基于 Surge Snell 协议的代理服务镜像。

## 使用

```bash
# 生成 32 位随机 PSK，客户端需配置相同的 PSK
PSK=$(openssl rand -hex 16)
echo "$PSK"

docker run --name surge-snell -d --restart always -p 1984:1984 \
  maguowei/surge-snell "$PSK"
```

- 镜像基于 Snell v6，默认 `mode = default`。
- `<psk>` 长度需为 12–255 字节，建议使用 32 位以上随机字符串。
- Surge 客户端需支持 Snell v6，且 `mode` 需与服务端保持一致。

## 参考资料

- [Snell Protocol](https://kb.nssurge.com/surge-knowledge-base/zh/release-notes/snell)
