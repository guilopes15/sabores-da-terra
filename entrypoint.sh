#!/bin/sh

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0 --port 8000 src.sabores_da_terra.app:app & 

poetry run python src/sabores_da_terra_bot/main.py
