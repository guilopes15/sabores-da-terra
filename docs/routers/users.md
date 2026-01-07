**POST** `/api/users` - Usada para criar novo usuario comum

Exemplo de uso com curl:
```bash
curl -X "POST http://localhost/api/users" -H "Content-Type: application/json" -d '{"username":"example", "email": "example@example.com", "password": 123456}'
```

**POST** `/api/users` - Tambem usada para criar novo usuario admin

Exemplo de uso com curl:

```bash
curl -X POST "http://localhost/api/users" -H "Content-Type: application/json" -H "admin_secret": "admin-secret-key" -d '{"username":"example", "email": "example@example.com", "password": 123456}'
```

Request Body:
```json
{
  "username": "example"
  "email": "example@example.com"
  "password": 123456
}
```
Response 201 - CREATED:

```json
{
  "id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-12-06T14:40:38.334Z",
  "updated_at": "2025-12-06T14:40:38.334Z",
  "is_admin": "false",
  "orders": []
}
```

Response 409 - CONFLICT:

```json
{
  "detail": "Email already exists."
}
```

***

**GET** `/api/users/` - Busca todos os usuarios cadastrados no sistema

Exemplo de uso com curl:

```bash
curl -X GET "http://localhost/api/users"
```

Response 200 - OK:

```json
"users": [
    {
      "id": 1,
      "username": "example",
      "email": "example@example.com",
      "created_at": "2025-12-06T14:40:38.334Z",
      "updated_at": "2025-12-06T14:40:38.334Z",
      "is_admin": true,
      "orders": []


    },

    {
      "id": 2,
      "username": "test",
      "email": "test@example.com",
      "created_at": "2025-12-06T14:40:38.334Z",
      "updated_at": "2025-12-06T14:40:38.334Z",
      "is_admin": false,
      "orders": []
    }

```
***
**GET** `/api/users{user_id}` - Busca usuario por ID

Exemplo de uso com curl:
```bash
curl -X GET "http://localhost/api/users/1"
```

Response 200 - OK - Exemplo 1 :

```json
{
  "id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-12-06T14:40:38.334Z",
  "updated_at": "2025-12-06T14:40:38.334Z",
  "is_admin": true,
  "orders": []
}
```
Response 200 - OK - Exemplo 2 (com orders):

```json
{
  "id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-12-08T15:19:26.991Z",
  "updated_at": "2025-12-08T15:19:26.992Z",
  "is_admin": true,
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "total_amount": "50.50",
      "status": "pending",
      "created_at": "2025-12-08T15:19:26.992Z",
      "updated_at": "2025-12-08T15:19:26.992Z",
      "items": [
        {
          "id": 1,
          "order_id": 1,
          "product_id": 1,
          "quantity": 2,
          "price": "25.25",
          "product_name": "batata",
          "product_image": "https://i.ibb.co/kVxk8QPN/batata.jpg"
        }
      ]
    }
  ]
}
```
Response 404 - NOT FOUND:

```json
{
  "detail": "User does not exists."
}
```
***
**PUT** `/api/users/{user_id}` - Atualiza todas as informações do usuario - ***login required***

Exemplo de uso com curl:

```bash
curl -X PUT "http://localhost/api/users/1" -H "Content-Type: application/json" -d {"username": "string", "email": "string@example.com", "password": "654321"}
```

Request Body:

```json
{
  "username": "example",
  "email": "example@example.com",
  "password": "654321"
}
```

Response 200 - OK:

```json
{
  "id": 1,
  "username": "example",
  "email": "example@example.com",
  "created_at": "2025-12-06T15:12:40.304Z",
  "updated_at": "2025-12-06T15:12:40.304Z",
  "is_admin": true,
  "orders": []
}
```
Resquest 409 - CONFLICT:

```json
{
  "detail": "Email already exists."
}
```

Request 403 - FORBIDDEN:
```json
{
  "detail": "Not enough permission."
}
```
***

**DELETE** `/api/users/{user_id}` - Deletar usuario - ***login required***

Exemplo com curl:

```bash
curl -X DELETE "http://localhost/api/users/1"
```
Response 200 - OK:

```json
{
  "message": "User deleted"
}
```

Response 403 - FORBIDDEN;
```json
{
  "detail": "Not enough permission."
}
```
