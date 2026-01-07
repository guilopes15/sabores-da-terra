**POST** `/api/payment/checkout/{order_id}` - Gera uma url para o sistema de pagamento externo. ***login required***

Exemplo de uso com curl:

```bash
curl -X POST "http://localhost/api/payment/checkout/1"
```

Response 200 - OK:

```json
{
  "checkout_url": "https://example.com/"
}

```

Response 404 - NOT_FOUND:
```json
{
  "detail": "Invalid Order."
}
```
***

**POST** `/api/payment/webhook` - Recebe um request quando um pagamento for realizado

Response 200 - OK:

```json
{
  "message": "Order processed successfully."
}
```

Response 401 - UNAUTHORIZED:

Assinatura invalida (request que não veio do sistema de pagamento).

```json
{
  "message": "Invalid signature"
}
```
Response 200 - OK:

Payment_status diferente de paid:

```json
{
  "message": "No orders processed."
}
```

Obs: quando nehuma order for encontrada um email é enviado ao admin do sistema.
