# Nginx

```bash
# set envs
$ export  SERVER_NAME=.example.com
$ export SSL_CERTIFICATE_NAME=example.com
$ export PROXY_PASS=http://api.example.com

# run
$ docker run --name nginx -d -p 80:80 --restart always -e SERVER_NAME -e SSL_Certificate_Name -e PROXY_PASS maguowei/nginx
```
