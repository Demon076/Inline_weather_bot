FROM python:3.12.2-slim-bookworm AS builder

ENV POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=true

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==$POETRY_VERSION \
    && poetry config virtualenvs.in-project $POETRY_VIRTUALENVS_CREATE \
    && poetry install --without dev --no-interaction --no-ansi

FROM python:3.12.2-slim-bookworm

COPY --from=builder /app /app
COPY . ./