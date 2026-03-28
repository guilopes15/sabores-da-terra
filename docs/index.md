# Sobre o projeto

Bem vindo á documentação do Sabores da Terra, uma Plataforma online de produtos orgânicos regionais.

A Plataforma utiliza a técnica de desenvolvimento [Server-Side Rendering(SSR)](https://developer.mozilla.org/en-US/docs/Glossary/SSR) e contem: *uma pagina web, se comunica com o banco de dados via API e um Bot de Telegram.*

## Pagina Web
A pagina web é a principal interface para o uso e o gerencianto da loja.

- Posui uma pagina de registro e login de clientes.
- Possui uma home page com os principais produtos e uma barra de pesquisa para encontrar o produto desejado.
- Cada produto possui sua propria pagina com todas as suas informações e um botão para adicionar o produto no carrinho de compras.
- O carrinho de compras mostra todos os items do pedido do cliente. Com a possibilidade de alterar items como desejar.
- O botão de compra redireciona o cliente para um sistema de pagamento externo.
- Um painel administrativo permite ao admin criar, alterar e remover produtos, além de visualizar dados dos clientes e dos pedidos.


### Login e Cadastro
[![login and register](assets/login_register.png)](assets/login_register.png)

### Home Page
[![home](assets/sabores_home_page.PNG)](assets/sabores_home_page.PNG)

### Product Page
[![produto](assets/product_page.PNG)](assets/product_page.PNG)

### Meu perfil
[![perfil](assets/perfil.PNG)](assets/perfil.PNG)

### Carrinho de compras
[![carrinho](assets/cart.PNG)](assets/cart.PNG)

### Painel do Admin
[![admin](assets/admin_panel.PNG)](assets/admin_panel.PNG)

## API
Sabores da Terra possui uma api moderna, desenvolvida com FastAPI.

- Possui gestão de clientes com resgisto, alteração dos dados pessoais e exclusão de conta.
- Sistema seguro de autenticação baseado em tokens JWT.
- Possui 2 tipos de usuarios: comum e admin.
- Gestao de produtos pelo Admin: Cadastro de produtos para a venda, controle de estoque e alteraçao de preços, nome e descrição.
- Criação de Pedidos: Os clientes podem comprar varios produtos de uma vez, remover ou alterar a quantidade dos produtos individualmente a qualquer momento.
- Endpoints recebem e retornan Json, serializado e validado por contratos do Pydantic.


## Bot de Telegram - @Sabores_da_terra_bot
O bot de telegram permite qualquer pessoa sem login, visualizar os produtos em tempo real.

- O bot possui uma interface de utilização simples atravez de comandos. Por exemplo /menu.
- Tambem possui links de redirecionamento para a pagina web e para as redes socias da loja.

[![bot](assets/bot.jpg)](assets/bot.jpg)
[![bot](assets/bot2.jpg)](assets/bot2.jpg)
