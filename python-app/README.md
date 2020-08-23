# Python App Base Image

## Usage

```bash
FROM maguowei/python-app:onbuild
LABEL maintainer="example@example.com"
LABEL name="maguowei/example"

ENV APP_NAME example
ENV APP_ENV dev

USER app

VOLUME /var/lib/${APP_NAME}/data
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
