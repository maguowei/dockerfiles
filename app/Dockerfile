FROM maguowei/base:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python-app"
LABEL version="1.0.0"

ENV APP_NAME ${APP_NAME}
ENV APP_ENV ${APP_ENV}
ENV APP_SOURCE_CODE_PATH /app
ENV APP_LOG_PATH /data/app/log
ENV PATH .:/home/app/.local/bin:$PATH

RUN groupadd app && useradd -ms /bin/bash -g app app
RUN mkdir -p ${APP_LOG_PATH} && chown -R app:app ${APP_LOG_PATH} \
    && mkdir -p ${APP_SOURCE_CODE_PATH} && chown -R app:app ${APP_SOURCE_CODE_PATH}
WORKDIR ${APP_SOURCE_CODE_PATH}
VOLUME ${APP_LOG_PATH}

USER app
ONBUILD COPY Pipfile* ./
ONBUILD RUN pip3 install --user -i https://mirrors.aliyun.com/pypi/simple/ pipenv \
    && pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple/
ONBUILD COPY --chown=app:app . ${APP_SOURCE_CODE_PATH}
ONBUILD RUN bash -l -c 'echo export PATH="$(pipenv --venv)/bin:${PATH}" >> ~/.bashrc'
EXPOSE 8080
# CMD manage.py runserver 0.0.0.0:8080