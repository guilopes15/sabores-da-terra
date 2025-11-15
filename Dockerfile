FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/
COPY . .

RUN apt-get update
RUN apt-get install -y build-essential gcc libssl-dev libffi-dev python3-dev

RUN pip install poetry

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
CMD ["sh", "-c", "poetry run uvicorn --host 0.0.0.0 src.sabores_da_terra.app:app" "&" "poetry run python src/sabores_da_terra_bot/main.py"]