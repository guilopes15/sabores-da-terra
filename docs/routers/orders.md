**POST** `/api/orders/` - Cria uma order de venda - ***login required***

Todas as orders são criadas com o status pending por default, mas o status pode ser passado via json.
Cada user so pode ir uma order(pedido) pendente por vez, para criar um novo pedido é necessario pagar ou excluir o pedido atual.

Exemplo de uso com curl:

```bash
curl -X POST "'http://localhost/api/orders/" -H "Content-Type: application/json" -d {"status": "pending", "items": [{"produc_id": 1, "quantity:1"}]}

```

Resquest Body:

```json
{
  "status": "pending" or "paid" or "canceled",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    }
  ]
}
```

Response 200 - OK:

```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": "5.5",
  "status": "pending",
  "created_at": "2025-12-08T21:59:55.992123",
  "updated_at": "2025-12-08T21:59:55.992123",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "quantity": 1,
      "price": "5.5",
      "product_name": "Manga",
      "product_image": "https://i.ibb.co/kVxk8QPN/manga.jpg"
    }
  ]
}
```

Response 404 - NOT FOUND:
```json
{
  "detail": "Product {item.product_id} not found."
}
```
Response 400 - BAD REQUEST:

```json
{
 "detail": "insufficient stock for product {item.product_id}"
}
```

***

**GET** `/api/orders/my-orders` - Busca a order que quem esta logado - ***login required***

Exemplo de uso com curl:

```bash
curl -X GET "http://localhost/api/orders/my-orders"
```
Response 200 - OK:

```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": "30",
  "status": "pending",
  "created_at": "2025-11-30T21:37:55.957840",
  "updated_at": "2025-12-06T15:05:18.982063",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 6,
      "quantity": 1,
      "price": "20",
      "product_name": "manga",
      "product_image": null
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 5,
      "quantity": 1,
      "price": "10",
      "product_name": "Laranja Bahia",
      "product_image": "https://i.ibb.co/kVxk8QPN/laranja-bahia.jpg"
    }
  ]
}

```

Response 404 - NOT FOUND:

```json
{
  "detail": "Order does not exists or not pending."
}

```

***

**GET** `/api/orders/{order_id}` - Busca uma order por ID - ***admin permission required***

Exemplo de uso com curl:

```bash
curl -X GET "http://localhost/api/orders/1"
```
Response 200 - OK:

```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": "30",
  "status": "pending",
  "created_at": "2025-11-30T21:37:55.957840",
  "updated_at": "2025-12-06T15:05:18.982063",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 6,
      "quantity": 1,
      "price": "20",
      "product_name": "manga",
      "product_image": null
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 5,
      "quantity": 1,
      "price": "10",
      "product_name": "Laranja Bahia",
      "product_image": "https://i.ibb.co/kVxk8QPN/laranja-bahia.jpg"
    }
  ]
}

```
Response 404 - NOT FOUND:

```json
{
  "detail": "Order does not exists."
}
```

***

**PUT** `/api/orders/my-orders` - Atualiza os items da order - ***login required***

Exemplo de uso com curl:

```bash
curl -X "http://localhost/api/orders/my-orders" -H -H "Content-Type: application/json" -d {"status": "pending", "items": [{"product_id": 1, "quantity": 3}]}

```
Request body:

```json
{
  "status": "pending" or "paid" or "canceled",
  "items": [
    {
      "product_id": 1,
      "quantity": 3
    }
  ]
}

```

Response 200 - OK:

```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": "70",
  "status": "pending",
  "created_at": "2025-11-30T21:37:55.957840",
  "updated_at": "2025-12-06T15:05:18.982063",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 6,
      "quantity": 3,
      "price": "20",
      "product_name": "manga",
      "product_image": null
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 5,
      "quantity": 1,
      "price": "10",
      "product_name": "Laranja Bahia",
      "product_image": "https://i.ibb.co/kVxk8QPN/laranja-bahia.jpg"
    }
  ]
}
```

Response 404 - NOT FOUND:

```json
{
  "detail": "Order does not exists or not pending."
}
```

OU

```json
{
  "detail": "Product {item.product_id} not found."
}
```

Response 400 - BAD REQUEST:

```json
{
  "detail": "insufficient stock for product_id {item.product_id}"
}
```
***

**DELETE** `/api/orders/my-orders` - Deleta a order que quem esta logado - ***login required***

Exemplo de uso com curl:

```bash
curl -X DELETE "http://localhost/api/orders/my-orders"
```

Response 200 - OK:

```json
{
  "message": "Order deleted."
}

```

Response 404 - NOT FOUND:

```json
{
  "detail": "Order does not exists or not pending."
}
```
