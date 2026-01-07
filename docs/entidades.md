**User → Order**

- Um usuário pode realizar vários pedidos (1:N).

**Order → OrderItem**

- Um pedido pode conter vários itens (1:N).

**OrderItem → Product**

- Cada item do pedido refere-se a um único produto (N:1).

**Veja abaixo:**

```mermaid
erDiagram
    User ||--o{ Order : places
    Order ||--o{ OrderItem : contains
    OrderItem }o--|| Product : refers_to

    User {
        int id PK
        string email UK
        string username
        string password
        bool is_admin
        datetime created_at
        datetime updated_at
    }

    Product {
        int id PK
        string name UK
        string description
        decimal price
        int stock_quantity
        bool is_active
        string image
        datetime created_at
        datetime updated_at
    }

    Order {
        int id PK
        int user_id FK
        decimal total_amount
        string status
        datetime created_at
        datetime updated_at
    }

    OrderItem {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
        string product_name
        string product_image
    }
```
