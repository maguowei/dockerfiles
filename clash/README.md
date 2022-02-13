# Clash

## Run

```bash
docker run --name clash -d --restart always -p 7890:7890 -p 9090:9090 -v ${PWD}/config.yaml:/root/.config/clash/config.yaml maguowei/clash
```

## Ref

- [Dreamacro/clash](https://github.com/Dreamacro/clash)
- [Class Wiki](https://github.com/Dreamacro/clash/wiki/configuration)
- [Clash Dashboard](https://github.com/Dreamacro/clash-dashboard)
