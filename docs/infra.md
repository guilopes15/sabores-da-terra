
## Configurações de Build

O projeto usa containers para isolar o app do restante do sistema.

- O arquivo Dockerfile possui as configurações e os comandos necessários para a criação da imagem.
- Foi utilizado o recurso de multistage build para reduzir o tamanho da imagem de 800MB para 300MB.

```Dockerfile
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

```

## Gerencimento de Containers
O projeto possui 4 containers ao todo, o arquivo compose.yaml gerencia e define como os container vão ser criados e como irão se comportar.

- sabores_da_terra_app: O principal container do projeto, responsável por executar tanto a API quanto o Bot. E possui uma réplica adicional para permitir o load balance e maior disponibilidade do serviço.
- sabores_da_terra_database: O Postgres foi defindo como o banco de dados do projeto, juntamente com um driver async.
- nginx: Um load balance e ao mesmo tempo um proxy reverso, usado para alternar a carga de requisições igualmente entre as duas copias do app. Foi adicionado um rate limit de 10 reqs/s para amenizar possiveis ataques Ddos.

```yaml
services:
  sabores_da_terra_database:
    image: postgres:17
    environment:
      POSTGRES_USER: app_user
      POSTGRES_DB: app_db
      POSTGRES_PASSWORD: app_password
    command: postgres -c 'max_connections=500'
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '0.3'
          memory: '1GB'

  sabores_da_terra_app1: &sabores_da_terra
    image: sabores_da_terra
    build: .
    entrypoint: ./entrypoint.sh
    depends_on:
      - sabores_da_terra_database
    environment:
      DATABASE_URL: postgresql+asyncpg://app_user:app_password@sabores_da_terra_database:5432/app_db
    deploy:
      resources:
        limits:
          cpus: '0.3'
          memory: '0.4GB'

  sabores_da_terra_app2:
    <<: *sabores_da_terra

  nginx:
    image: nginx:alpine
    container_name: sabores_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - sabores_da_terra_app1
      - sabores_da_terra_app2
    ulimits:
      nproc: 1000000
      nofile:
        soft: 1000000
        hard: 1000000
    deploy:
      resources:
        limits:
          cpus: '0.1'
          memory: '0.2GB'

volumes:
  pgdata:
```

## Gerenciamneto de recursos
O projeto tem um gerenciamento de recursos de hardware minuncioso, e utiliza ao todo 1cpu e 2gb de memoria.

- Cada container do sabores_da_terra_app possui 2 workers, consumindo em média 340MB.
- O banco de dados tem a maior parte da memoria disponivel para maior disponibilidade.

## Teste de carga e Performace
Foi utilizado o [siege](https://github.com/JoeDog/siege) para executar o teste de carga.

- O Teste foi feito usando apenas 1 rota de GET (leitura).
- Leve em consideração que o teste foi feito em um ambiente wsl, com 1cpu e 2gb de memoria e sem cache.

Mesmo com as limitações acima, o app consegui manter 450 usuarios simultaneos, com 100% de disponilidade e 0 falhas de requests.

Veja o resultado abaixo:

![grafico](assets/siege_analysis.png)
