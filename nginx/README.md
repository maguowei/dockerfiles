# Nginx

## Certbot

- [certbot](https://certbot.eff.org/docs/install.html#operating-system-packages)

```bash
# Get certbot
$ sudo apt-get update
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository universe
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot
$ certbot --help

# obtain wildcard certificates
$ sudo certbot certonly --manual --cert-name exanple.com -d '*.exanple.com' -d exanple.com --agree-tos --manual-public-ip-logging-ok --preferred-challenges dns-01

# Display information about certs you have from Certbot
sudo certbot certificates

# renew
$ sudo certbot renew

# revoke
$ sudo certbot revoke --cert-path /etc/letsencrypt/live/exanple.com/fullchain.pem

# delete
$ sudo certbot delete --cert-name exanple.com
```

## Run Nginx

```bash
# set envs
$ export SERVER_NAME=.example.com
$ export SSL_CERTIFICATE_NAME=example.com
$ export PROXY_PASS=http://127.0.0.1:8080

# run
$ docker run --name nginx -d -p 443:443 -p 80:80 -v /etc/letsencrypt:/etc/letsencrypt -e SERVER_NAME -e SSL_CERTIFICATE_NAME -e PROXY_PASS --restart always maguowei/nginx
```

## Reference

- [Certbot documentation](https://certbot.eff.org/docs/)
- [lets-encrypt ubuntubionic-nginx](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx)
- [How do I enable ACMEv2 and retrieval of wildcard certificates](https://github.com/certbot/certbot/issues/5719)
- [Nginx Configuring HTTPS servers](http://nginx.org/en/docs/http/configuring_https_servers.html)
