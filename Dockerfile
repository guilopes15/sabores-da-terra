FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN apt-get update

RUN pip install poetry

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
CMD ["sh", "-c", "poetry run uvicorn --host 0.0.0.0 src.sabores_da_terra.app:app"]