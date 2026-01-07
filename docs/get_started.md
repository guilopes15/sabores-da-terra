# Pre-requisitos
- Python 3.12: Para instalar o python acesse o site oficial [clicando aqui](https://www.python.org/).
- Docker: Acesse a documentação oficial do docker para a instação [clicando aqui](https://docs.docker.com/engine/install/).

## Configurando ambiente
Abra o terminal na pasta desejada e siga os passos abaixo:

```bash
git clone https://github.com/guilopes15/sabores-da-terra.git

cd sabores-da-terra

pip install pipx

pipx ensurepath

pipx install poetry

poetry env use 3.12

poetry install
```

## Variaveis de ambiente
Crie um arquivo **.env** na raiz do projeto (no mesmo nivel do pyproject.toml) com as seguintes variaveis.

```plain-text
DATABASE_URL='postgresql+asyncpg://app_user:app_password@localhost:5432/app_db'
SECRET_KEY='sua-chave-secreta'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
STRIPE_API_KEY='chave-de-api-stripe'
WEBHOOK_SECRET='webhook-secret'
ADMIN_SECRET='admin-secret'
TELEGRAM_API_ID=seu-api-id
TELEGRAM_API_HASH="seu-api-hash"
TELEGRAM_BOT_TOKEN="seu-bot-token"
SMTP_PASSWORD="seu-smtp=password"
EMAIL_SENDER="email-que-vai-mandar-a-notificação"
EMAIL_RECIPIENT="email-que-vai-receber-a-notificação"
```
Veja abaixo os tipos das variaveis para não errar nada.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    STRIPE_API_KEY: str
    WEBHOOK_SECRET: str
    ADMIN_SECRET: str
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    TELEGRAM_BOT_TOKEN: str
    EMAIL_SENDER: str
    EMAIL_RECIPIENT: str
    SMTP_PASSWORD: str
```

Acesse o dashboard stripe e crie sua conta para obter a STRIPE_API_KEY e o WEBHOOK_SECRET [clicando aqui](https://dashboard.stripe.com/).

Acesse o telegram app configuration para obter o TELEGRAM_API_ID e o TELEGRAM_API_HASH [clicando aqui](https://my.telegram.org/auth?to=apps).

Converse com o @BotFather no seu proprio app do telegram e crie seu proprio bot para obter o TELEGRAM_BOT_TOKEN.

Acesse o gmail, por exemplo, para obter o SMTP_PASSWORD [clicando aqui](https://myaccount.google.com/apppasswords).

## Subindo o server localmente
Com os passos anteriores feitos com sucesso, digite no terminal o seguinte comando:

```bash
docker compose up --build
```

Com isso o app já esta no ar em: *http://localhost/*
