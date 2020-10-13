# Clash

## Run

```bash
docker run --name clash -d --restart always -p 7890:7890 -v ${PWD}/config.yaml:$HOME/.config/clash/config.yaml dreamacro/clash
```

## Ref

- [Dreamacro/clash](https://github.com/Dreamacro/clash)
- [Class Wiki](https://github.com/Dreamacro/clash/wiki/configuration)
- [Unofficial Clash Wiki](https://lancellc.gitbook.io/clash/)
