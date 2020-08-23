FROM maguowei/python:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python-app"
LABEL version="1.1.0"

ENV APP_NAME ${APP_NAME}
ENV APP_ENV ${APP_ENV}
ENV APP_SOURCE_CODE_PATH /app
ENV APP_LOG_PATH /data/app/log
ENV PATH .:$PATH

RUN groupadd app && useradd -ms /bin/bash -g app app
RUN mkdir -p ${APP_LOG_PATH} && chown -R app:app ${APP_LOG_PATH} \
    && mkdir -p ${APP_SOURCE_CODE_PATH} && chown -R app:app ${APP_SOURCE_CODE_PATH}
WORKDIR ${APP_SOURCE_CODE_PATH}
VOLUME ${APP_LOG_PATH}

ONBUILD COPY Pipfile* ./
ONBUILD RUN pipenv install --system
ONBUILD COPY --chown=app:app . ${APP_SOURCE_CODE_PATH}
# USER app
EXPOSE 8080
