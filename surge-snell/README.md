# Surge snell

## Usage

```bash
# build
docker build -t maguowei/surge-snell .
# run
docker run --name surge-snell -d --restart always -p 1984:1984 maguowei/surge-snell ${the_psk}

# use Kubernetes
kubectl run surge-snell --generator=run-pod/v1 --image=maguowei/surge-snell --restart=Always -- ${the_psk}
kubectl expose pod surge-snell --port=1984 --type LoadBalancer
```

## Ref

- [Snell Protocol](https://manual.nssurge.com/others/snell.html)
