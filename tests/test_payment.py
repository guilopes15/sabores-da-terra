def test_checkout(client, token, order):
    response = client.post(
        f'/payment/checkout/{order.id}',
        headers={'Authorization': f'bearer {token}'},
    )
    assert 'checkout_url' in response.json().keys()
    assert 'checkout.stripe.com' in response.json()['checkout_url']


def test_checkout_order_not_found(client, token):
    response = client.post(
        '/payment/checkout/33', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {'detail': 'Invalid Order.'}


def test_checkout_order_not_pending(client, token, other_order):
    response = client.post(
        f'/payment/checkout/{other_order.id}',
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Invalid Order.'}


def test_checkout_order_wrong_user(client, token, order, other_user):
    response = client.post(
        '/auth/token',
        data={
            'username': other_user.email,
            'password': other_user.clean_password,
        },
    )

    token = response.json()['access_token']

    response = client.post(
        f'/payment/checkout/{order.id}',
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Invalid Order.'}


def test_checkout_order_zero_amount(client, token):
    response = client.post(
        '/orders',
        json={'items': []},
        headers={'Authorization': f'bearer {token}'},
    )

    order_id = response.json()['id']

    response = client.post(
        f'/payment/checkout/{order_id}',
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Invalid Order.'}


def test_webhook(client, mock_stripe_signature_verification, webhook_payload):
    with mock_stripe_signature_verification(order_id=1):
        response = client.post(
            '/payment/webhook',
            headers={'stripe-signature': 'fake'},
            json=webhook_payload,
        )

        assert response.json() == {'message': 'Order processed successfully.'}


def test_webhook_invalid_signature(client, webhook_payload):
    response = client.post(
        '/payment/webhook',
        headers={'stripe-signature': 'invalid'},
        json=webhook_payload,
    )
    assert response.json() == {'detail': 'Invalid signature'}


def test_webhook_order_not_found(
    client, mock_stripe_signature_verification, webhook_payload
):
    with mock_stripe_signature_verification(order_id=None):
        response = client.post(
            '/payment/webhook',
            headers={'stripe-signature': 'fake'},
            json=webhook_payload,
        )

    assert response.json() == {'message': 'No orders processed.'}


def test_webhook_order_not_paid(
    client, mock_stripe_signature_verification, webhook_payload
):
    with mock_stripe_signature_verification(order_id=1, status='pending'):
        response = client.post(
            '/payment/webhook',
            headers={'stripe-signature': 'fake'},
            json=webhook_payload,
        )

    assert response.json() == {'message': 'No orders processed.'}


def test_webhook_checkout_not_completed(
    client, mock_stripe_signature_verification, webhook_payload
):
    with mock_stripe_signature_verification(checkout_type='uncompleted'):
        response = client.post(
            '/payment/webhook',
            headers={'stripe-signature': 'fake'},
            json=webhook_payload,
        )

    assert response.json() == {'message': 'No orders processed.'}
