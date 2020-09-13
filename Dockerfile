FROM python:3.8.5-alpine3.12 as base

    # python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.0.10 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTIONS=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    \
    # paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

    ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM base as build

RUN apk update \
    && apk upgrade --no-cache \
    && apk add --no-cache alpine-sdk libffi-dev openssl-dev \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && pip install "poetry==$POETRY_VERSION" \
    && poetry --version

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev \
    && apk del --purge alpine-sdk libffi-dev openssl-dev

FROM base as final
COPY --from=build $PYSETUP_PATH $PYSETUP_PATH
COPY watch.py /app/
COPY ./watcher /app/watcher/
WORKDIR /app
USER nobody
CMD ["python","/app/watch.py"]
