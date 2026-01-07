**POST** `/api/products/` - Criar produto - ***admin permission required***

Exemplo de uso com curl:

```bash
curl -X POST "http://localhost/api/products/" -H "Content-Type: application/json" -d { "name": "manga", "description": "manga organica", "price": "5.5", "stock_quantity": 25, "image": "https://i.ibb.co/kVxk8QPN/manga.jpg" }
```

Request Body:

```json
{
  "name": "manga",
  "description": "manga organica",
  "price": "5.5",
  "stock_quantity": 20,
  "image": "https://i.ibb.co/kVxk8QPN/manga.jpg"
}
```

Response 200 - OK:

```json
{
  "name": "manga",
  "description": "manga organica",
  "price": "5.5",
  "stock_quantity": 20,
  "image": "https://i.ibb.co/kVxk8QPN/manga.jpg",
  "id": 1,
  "is_active": true,
  "created_at": "2025-10-10T15:04:10.328736",
  "updated_at": "2025-10-10T17:05:32.428075"
}
```

Response 409 - CONFLICT:

```json
{
  "detail": "Product already exists."
}
```

***

**GET** `/api/products/` - Busca todos os produtos

Exemplo de uso com curl:

```bash
curl -X GET "http://localhost/api/products/"
```

Response 200 - OK:

```json
{
  "products": [
      {
        "name": "uva",
        "description": "Uva Organica",
        "price": "25.5",
        "stock_quantity": 20,
        "image": null,
        "id": 2,
        "is_active": false,
        "created_at": "2025-10-10T15:04:10.328736",
        "updated_at": "2025-10-10T17:05:32.428075"
      },
      {
        "name": "manga",
        "description": "manga organica",
        "price": "5.5",
        "stock_quantity": 20,
        "image": "https://i.ibb.co/kVxk8QPN/manga.jpg",
        "id": 1,
        "is_active": true,
        "created_at": "2025-10-10T15:04:10.328736",
        "updated_at": "2025-10-10T17:05:32.428075"
      }
  ]
}
```
***
**GET** `/api/products/{product_id}` - Busca produtos por ID

Exemplo de uso com curl:

```bash
curl -X GET http://localhost/api/products/1
```

Response 200 - OK:
```json
"name": "manga",
"description": "manga organica",
"price": "5.5",
"stock_quantity": 20,
"image": "https://i.ibb.co/kVxk8QPN/manga.jpg",
"id": 1,
"is_active": true,
"created_at": "2025-10-10T15:04:10.328736",
"updated_at": "2025-10-10T17:05:32.428075"

```

Response 404 - NOT FOUND:

```json
{
  "detail": "Product does not exists."
}
```
***

**GET** `/api/products/filters` - Busca produtos por queryparams

Queryparams:

- name: str or null =  Busca os produto pelo nome desejado
- offset: int = Por onde começa a busca, default é 0.
- limit: int = quantidade de items máxima retornada, default é 10.

Exemplo de uso com curl:

```bash
curl -X GET "http://localhost/api/products/filters?name=manga&offset=0&limit=10"
```
Response 200 - OK:

```json
"products": [
  {
    "name": "Manga",
    "description": "manga organica",
    "price": "5.5",
    "stock_quantity": 20,
    "image": "https://i.ibb.co/3qxw4J7/manga-palmer-2ys6v2qa3v-1.png",
    "id": 1,
    "is_active": true,
    "created_at": "2025-10-17T14:46:29.369435",
    "updated_at": "2025-12-06T14:06:14.252931"
  }
]
```
***
**PATCH** `/api/products/{product_id}` - Atualiza as informações dos produtos sob demanda - ***admin permission required***

Obs: Todas os campos do request body são opcionais.

Exemplo de uso com curl:
```bash
curl -X PATCH "http://localhost/api/products/1" -H "Content-Type: application/json" -d {"name"="Manga Tommy"}
```
Request Body:

```json
{
  "name": "string",
  "price": 1,
  "stock_quantity": 20,
  "description": "string",
  "image": "string"
}
```

Response 200 - OK:
```json

"name": "Manga Tommy",
"description": "manga organica",
"price": "5.5",
"stock_quantity": 20,
"image": "https://i.ibb.co/3qxw4J7/manga-palmer-2ys6v2qa3v-1.png",
"id": 1,
"is_active": true,
"created_at": "2025-10-17T14:46:29.369435",
"updated_at": "2025-12-06T14:06:14.252931"

```

Response 404 - NOT FOUND:

```json
{
  "detail": "Product does not exists."
}
```

Response 409 - CONFLICT:
```json
{
  "detail": "Product name already exists."
}
```
***

**DELETE** `/api/products/{products_id}` - Deletar produto - ***admin permission required***
O delete faz um soft delete, apenas muda o is_active para false.

Exemplo de uso com curl:
```bash
curl -X "http://localhost/api/products/1"
```
Response 200 - OK:

```json
{
  "message": "Product deleted"
}
```
Response 404 - NOT FOUND:
```json
{
  "detail": "Product does not exists."
}
```
Response 409 - CONFLICT:

```json
{
  "detail": "cannot remove product"
}
```
