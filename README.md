# 🌿 Sabores da Terra

**Plataforma online de produtos orgânicos regionais**

Sabores da Terra é uma aplicação web completa para venda de produtos orgânicos, desenvolvida com Server-Side Rendering (SSR). A plataforma integra uma página web moderna, uma API REST e um Bot de Telegram, oferecendo múltiplos canais de acesso para clientes e administradores.

Veja a documentação completa [***aqui***](https://guilopes15.github.io/sabores-da-terra/).

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Fluxo do Sistema](#fluxo-do-sistema)
- [Autenticação e Autorização](#autenticação-e-autorização)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Executando o Projeto](#executando-o-projeto)

---

## Visão Geral

O sistema é composto por três módulos principais:

| Módulo | Descrição |
|---|---|
| **Página Web** | Interface principal para clientes e administradores |
| **API (FastAPI)** | Backend RESTful com autenticação JWT e integração com Stripe |
| **Bot de Telegram** | Canal alternativo para visualização de produtos em tempo real |

---

## Funcionalidades

### 🖥️ Página Web

- Registro e login de clientes
- Home page com vitrine de produtos e barra de pesquisa
- Página individual de cada produto com opção de adicionar ao carrinho
- Carrinho de compras com gerenciamento de itens
- Redirecionamento para sistema de pagamento externo (Stripe)
- Painel administrativo para gestão de produtos, clientes e pedidos

### ⚙️ API

- Gestão de clientes: registro, atualização de dados e exclusão de conta
- Autenticação segura via tokens JWT
- Dois perfis de usuário: **comum** e **admin**
- Gestão de produtos pelo admin: cadastro, controle de estoque, preços e descrições
- Criação e gerenciamento de pedidos com múltiplos produtos
- Endpoints com serialização e validação via contratos Pydantic

### 🤖 Bot de Telegram — `@Sabores_da_terra_bot`

- Visualização de produtos, preços, estoque e imagens em tempo real
- Navegação simples por comandos (ex: `/menu`)
- Links de redirecionamento para a página web e redes sociais da loja

---

## Fluxo do Sistema

```mermaid
graph TD
    A(Cliente)
    A --> B[Pagina Web]
    A --> C[Telegram Bot]

    subgraph app[APP]
        app1[CRUD]
        app2[Sistema de Vendas]
        app3[Painel do admin]
    end
    app4[Sistema de Notificação]

    B --> app
    C --> app
    D[Venda manual] --> app3

    app2 --> app4

    app2 --> |checkout| F(Sistema de Pagamentos Externo)
    F --> |Webhook|app2

    app1 --> E[(database)]
    app2 --> E
    app3 --> E
```

Quando o cliente finaliza a compra, um link de checkout é gerado com todos os itens do pedido e o cliente é redirecionado ao sistema de pagamento externo. Após a confirmação do pagamento, um webhook notifica o sistema, atualiza o status do pedido e dispara um e-mail de aviso ao administrador.

O admin também pode registrar **vendas manuais** diretamente pelo painel, centralizando todas as transações no sistema.

---

## Autenticação e Autorização

### Autenticação — JWT

O token é gerado a partir do preenchimento do OAuth form com e-mail e senha, e pode ser transportado de duas formas:

- **Cookie** — o navegador envia automaticamente nas rotas protegidas
- **Bearer Token** — via header da requisição:
  ```
  Authorization: Bearer seu_token
  ```

### Níveis de Acesso

| Perfil | Permissões |
|---|---|
| **Visitante** | Acessa a home page e as páginas de produtos |
| **Usuário logado** | Cria pedidos, gerencia itens do carrinho e efetua compras |
| **Admin** | Acesso total: gerencia produtos, visualiza pedidos e dados de usuários |

---

## Pré-requisitos

- [Python 3.12](https://www.python.org/)
- [Docker](https://docs.docker.com/engine/install/)

---

## Instalação

```bash
git clone https://github.com/guilopes15/sabores-da-terra.git

cd sabores-da-terra

pip install pipx

pipx ensurepath

pipx install poetry

poetry env use 3.12

poetry install
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (mesmo nível do `pyproject.toml`) com as seguintes variáveis:

```env
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
SMTP_PASSWORD="seu-smtp-password"
EMAIL_SENDER="email-que-vai-mandar-a-notificação"
EMAIL_RECIPIENT="email-que-vai-receber-a-notificação"
```

**Onde obter cada credencial:**

| Variável | Onde obter |
|---|---|
| `STRIPE_API_KEY` e `WEBHOOK_SECRET` | [Dashboard Stripe](https://dashboard.stripe.com/) |
| `TELEGRAM_API_ID` e `TELEGRAM_API_HASH` | [Telegram App Config](https://my.telegram.org/auth?to=apps) |
| `TELEGRAM_BOT_TOKEN` | Converse com `@BotFather` no Telegram |
| `SMTP_PASSWORD` | [Google App Passwords](https://myaccount.google.com/apppasswords) |

---

## Executando o Projeto

### Subir a aplicação localmente

```bash
docker compose up --build
```

A aplicação estará disponível em: **http://localhost/**

### Subir a documentação localmente

```bash
poetry run mkdocs serve
```

### Executar os testes

```bash
poetry run pytest -vv
```

### Executar linter e formatador

```bash
poetry run ruff check . --fix && ruff format .
```
