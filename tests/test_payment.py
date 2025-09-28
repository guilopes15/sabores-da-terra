def test_checkout(client, token, order):
    response = client.post(
        f'/payment/checkout/{order.id}', 
        headers={'Authorization': f'bearer {token}'}
    )

    assert 'checkout_url' in response.json().keys()
    assert 'checkout.stripe.com' in response.json()['checkout_url']


def test_checkout_order_not_found(client, token):
    response = client.post(
        '/payment/checkout/33', 
        headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {'detail': 'Invalid Order.'}


# TODO: Extend query test case on checkout 