FROM maguowei/python:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/python-app"

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV APP_PATH=/app
ENV APP_LOG_PATH=/data/app/log

RUN groupadd app && useradd -ms /bin/bash -g app app \
    && mkdir -p ${APP_LOG_PATH} ${APP_PATH} ${VIRTUAL_ENV} \
    && chown -R app:app ${APP_LOG_PATH} ${APP_PATH} ${VIRTUAL_ENV}

WORKDIR ${APP_PATH}
VOLUME ${APP_LOG_PATH}

ONBUILD COPY pyproject.toml uv.lock* ./
ONBUILD RUN uv sync --no-dev --frozen
ONBUILD COPY --chown=app:app . ${APP_PATH}

EXPOSE 8080
