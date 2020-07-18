# Nginx

```bash
# set envs
$ export SERVER_NAME=.example.com
$ export SSL_CERTIFICATE_NAME=example.com
$ export PROXY_PASS=http://127.0.0.1:8080

# run
$ docker run --name nginx -d -p 443:443 -p 80:80 -v /etc/letsencrypt/live:/etc/letsencrypt/live -e SERVER_NAME -e SSL_CERTIFICATE_NAME -e PROXY_PASS --restart always maguowei/nginx
```
