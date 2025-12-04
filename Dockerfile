FROM python:3.12-slim AS builder

ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update
RUN apt-get install -y build-essential gcc libssl-dev libffi-dev python3-dev

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN pip install poetry

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi --without dev --no-root


COPY . .

FROM python:3.12-slim AS runtime

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

EXPOSE 8000
CMD ["sh", "-c", "\
    uvicorn src.sabores_da_terra.app:app --host 0.0.0.0 --workers 2 & \
    python src/sabores_da_terra_bot/main.py \
"]





