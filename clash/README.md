# Clash

## Run

```bash
 docker run --name clash -d --restart always -p 7890:7890 -p 7891:7891 -p 7892:7892 -p 9090:9090 -v ${PWD}/config.yaml:/root/.config/clash/config.yaml maguowei/clash
```

## Ref

- [Dreamacro/clash](https://github.com/Dreamacro/clash)
- [Class Wiki](https://github.com/Dreamacro/clash/wiki/configuration)
- [Unofficial Clash Wiki](https://lancellc.gitbook.io/clash/)
