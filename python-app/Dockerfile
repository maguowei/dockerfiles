FROM maguowei/python:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python-app"
LABEL version="Python-App 1.0.0"

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
COPY entrypoint.sh /usr/local/bin
ONBUILD COPY Pipfile* ./
ONBUILD RUN pipenv install
ONBUILD COPY --chown=app:app . ${APP_SOURCE_CODE_PATH}
ONBUILD ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8080
