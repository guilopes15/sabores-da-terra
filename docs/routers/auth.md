**POST** `/api/auth/token` - Gera o token JWT

Exemplo de uso com curl:

```bash
curl -X POST "http://localhost/api/auth/token" -H 'Content-Type: application/x-www-form-urlencoded' -d "username=test%40test.com&password=123456"
```

Response 200 - OK:
```json
{
  "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNzY1Mjk3NTE3fQ.rKIJYxrcyTI3jBhZPvI5jMclyFLM8f8_RZ5P6nz-tVI",
  "token_type": "bearer"
}

```
Response 400 - BAD_REQUEST:

```json
{
"detail": "Incorrect email or password"
}
```

***

**POST** `/api/auth/refresh_token` - Extende o tempo de uso do usuario autenticado - ***login required***

Exemplo de uso com curl:

```bash
curl -X POST "http://localhost/api/auth/refresh_token" -H "Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNzY1Mjk3NTE3fQ.rKIJYxrcyTI3jBhZPvI5jMclyFLM8f8_RZ5P6nz-tVI "

```
Response 200 - OK:

```json
{
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwIjoxNzY1Mjk4NTQ4fQ.PALsRe1IcjLQjn_gkuPkdDJvTtx0bwzuo6epu8hZhMQ",
 "token_type": "bearer"
}
```
