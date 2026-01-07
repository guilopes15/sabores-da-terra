# Autenticação

O Sabores da Terra possui autentificação via backend, usando a estratégia do token JWT.

A criação do token possui 2 fases:

- A partir do preenchimento do OAuth form com email e password, o token é criado e salvo em um cookie com a key ***access_token***.
- Também é retornado no body da requisição via Bearer token.

É possivel fazer o transporte do token e 2 formas diferentes:

- Bearer:
    - O token deve ser enviado no header da requisição: Authorization: bearer *seu_token*.

- Cookie:
    - O navegador envia o cookie automaticamente nas rotas onde é necessaria a autenticação.

# Autorização

Existe 3 niveis de Autorização no Sabores da terra:

- Usuario sem login:
    - Pode acessar a home page do site e a pagina dos produtos qua estão a venda.

- Usuario com login:
    - Pode criar um pedido, que fica disponivel no carrinho de compras.
    - Pode adicionar, remover e alterar os items do pedido a qualquer momento.
    - Pode efetuar a compra os items desejados.

- Usuario admin:
    - Tem acesso ao painel do admin, onde é possivel controlar a criação, alteração e exclusão de produtos. Também possui acesso as informações de todos os pedidos e os dados dos usuarios.
