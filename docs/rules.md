# Regras de Negócio

Os **controllers**, **models** e **event listeners** definem todas as regras de negócio do projeto.

## Models

Refletem a estrutura do banco de dados a partir de classes.

### Users
- Deve possuir **email único**, para diferenciar cada usuário.
- Possui um campo booleano `is_admin`, para gerenciar permissões.
- Carrega todos os seus pedidos, conectado em forma de relacionamento com o model `Order`.
- Um usuário pode ter vários pedidos.

### Products
- Possui **nome único**, para se diferenciar dos outros produtos.
- Possui o campo booleano `is_active`, que atua como um soft delete.
- É possível definir uma imagem para o produto (opcional); caso não adicione, uma imagem **placeholder** é utilizada.
- Possui **constraints personalizadas**:
    - `stock` deve ser >= 0
    - `preço` deve ser > 0

### Order
- Possui um campo `user_id` como **chave estrangeira**, indicando qual usuário criou o pedido.
- Possui uma **constraint personalizada**: `total_amount` precisa ser >= 0.
- O campo `status` atua como um **enum**, restringindo o status a três categorias.
- O pedido pode ter vários itens.
- Deve possuir todos os dados dos itens do pedido, conectado em relacionamento com `OrderItems`.

### OrderItems
- Possui um campo `order_id` como **chave estrangeira**, indicando a qual order o item pertence.
- Possui um campo `product_id` como **chave estrangeira**, indicando a qual product o item se refere.
- Possui uma **constraint personalizada**: `quantity` deve ser >= 0.
- Possui um campo opcional `product_image`.
- Possui relacionamento com `Products`.

## Controllers

São classes que agrupam métodos e definem o comportamento de cada rota de acordo com o verbo HTTP. Contemplam a **session**, o **schema** e as **permissões**, executam verificações/validações e persistem os dados no banco.

### User Controller

- **create**
    - Possui um parâmetro opcional `admin_secret`.
    - Busca no banco se existe um usuário com o mesmo email.
    - Verifica o `admin_secret` com uma variável de ambiente.
    - Compõe o model `User` com os dados do schema:
        - Se a verificação for verdadeira, é criado um **admin**.
        - Se for falsa, é criado um **user comum**.
    - Persiste no banco e retorna os dados.

- **read_all**
    - Busca no banco e retorna todos os usuários cadastrados.

- **read_by_id**
    - Busca um usuário pelo `id`; se encontrado, retorna, senão retorna erro.

- **update**
    - Se não estiver logado ou o `id` não for o do usuário logado, retorna erro.
    - Altera os dados do usuário e faz commit.
    - Se o email já existir, retorna `IntegrityError`.

- **delete**
    - Se não estiver logado ou o `id` não for o do usuário logado, retorna erro.
    - Deleta o usuário do banco e o cookie.

### Product Controller

- **create**
    - Verifica se o produto já existe; se existir, retorna erro.
    - Preenche o model com os dados e persiste.
    - Retorna os dados do produto.

- **read_all**
    - Retorna todos os produtos cadastrados.

- **read_by_id**
    - Busca um produto pelo `id`; se encontrado, retorna, senão retorna erro.

- **pagination**
    - Filtra produtos pelo nome.
    - Limita a quantidade de produtos retornados.
    - Define o offset de início da busca.

- **patch**
    - Busca o produto pelo `id`; se não encontrar, retorna erro.
    - Altera os dados do produto e persiste.
    - Se o nome do produto já existir, retorna erro.

- **delete**
    - Busca o produto pelo `id`; se não encontrar, retorna erro.
    - Altera o campo `is_active` para `false` e persiste.

### Order Controller

- **create**
    - Requer login; se não, retorna erro.
    - Se o usuário já tiver uma order pendente, retorna a order.
    - Cria a order com os dados iniciais, sem itens.
    - Verifica os produtos da order:
        - Se existem
        - Se estão ativos
        - Se há estoque suficiente
    - Se a verificação falhar, retorna erro.
    - Se a quantidade do produto for > 0, adiciona na order.
    - Persiste os dados e retorna a order.

- **read**
    - Requer login; se não, retorna erro.
    - Busca a order pendente do usuário logado; se existir, retorna, senão retorna erro.

- **read_by_id**
    - Busca uma order pelo `id`; se existir, retorna, senão retorna erro.

- **update**
    - Requer login; se não, retorna erro.
    - Busca a order pendente do usuário logado; se não existir, retorna erro.
    - Valida o produto a ser modificado:
        - Existe?
        - Está ativo?
        - Há estoque suficiente?
    - Verifica se o produto já está na order; se não, adiciona.
        - Se a quantidade do produto for > 0, atualiza quantidade e preço.
        - Se for 0, remove o produto da order.
    - Atualiza o total a pagar da order e persiste.

- **delete**
    - Requer login; se não, retorna erro.
    - Busca uma order pelo `id`; se existir, deleta, senão retorna erro.

### Payment Controller

- **checkout**
    - Requer login; se não, retorna erro.
    - Busca a order pendente do usuário com `total_amount > 0`.
        - Se não existir, retorna erro.
        - Se existir, monta um objeto com todos os itens da order.
        - Cria a página de pagamento a partir do objeto e retorna o link de acesso.

- **webhook**
    - Recebe um POST do sistema de pagamento.
    - Verifica se a assinatura é válida:
        - Se não for, retorna erro.
        - Se for válida, verifica o evento e o status do pagamento.
    - Busca a order pelo `id`:
        - Se não existir, envia um email ao admin informando.
        - Se existir, define o status para `paid`:
            - Subtrai do estoque todos os itens da order paga.
            - Envia um email ao admin com informações da venda.

## Event Listeners

São ações executadas quando certos eventos acontecem nos models, a partir da session.

### Depois que um produto for alterado:

- Quando um produto ficar inativo, ele deve ser removido de pedidos pendentes e o total deve ser atualizado.
- Quando o preço de um produto for alterado, o total de todos os pedidos que o possuem deve ser atualizado.
