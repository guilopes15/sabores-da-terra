# Visão Geral
Sabores da Terra possui rotas organizadas por funcionadlides e que seguem certos padrões. Veja abaixo:

#### URL Base
```
http://localhost/api
```

#### Veja a Documentação Interativa

- Swagger: `http://localhost/docs`
- Redoc: `http://localhost/redoc`
- OpenAPI: `http://localhost/openapi.json`

### Common Responses:

- Os endpoints com ***login required*** ou ***admin permission required*** compartilham responses de error - **401** UNAUTHORIZED.

```json
{
  "detail": "Could not validate credentials"
}
```

- Todos os endpoints que possuem, *Content-Type: application/json* ou *Content-Type: application/x-www-form-urlencoded* ou que precisam passar o token jwt pelo header, compartilham responses de erro de quebra de *contrato* - **422** UNPROCESSABLE ENTITY.

```json
{

  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
