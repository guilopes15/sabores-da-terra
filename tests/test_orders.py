from datetime import datetime

from src.sabores_da_terra.models import Order


def test_create_order(client, token, product, mock_db_time):
    with mock_db_time(model=Order, event_name='before_update') as time:
        item_quantity = 3

        response = client.post(
            '/orders',
            json={
                'items': [
                    {'product_id': product.id, 'quantity': item_quantity}
                ]
            },
            headers={'Authorization': f'bearer {token}'},
        )

    assert response.json() == {
        'id': 1,
        'user_id': 1,
        'total_amount': (item_quantity * product.price).to_eng_string(),
        'status': 'pending',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'items': [
            {
                'id': 1,
                'order_id': 1,
                'product_id': product.id,
                'quantity': 3,
                'price': product.price.to_eng_string(),
            }
        ],
    }


def test_create_order_without_product(client, token):
    item_quantity = 5

    response = client.post(
        '/orders',
        json={'items': [{'product_id': 99, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Product 99 not found.'}


def test_create_order_inactive_product(client, token, inactive_product):
    item_quantity = 5

    response = client.post(
        '/orders',
        json={
            'items': [
                {'product_id': inactive_product.id, 'quantity': item_quantity}
            ]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'detail': f'Product {inactive_product.id} not found.'
    }


def test_create_order_insufficient_stock(client, token, product):
    response = client.post(
        '/orders',
        json={'items': [{'product_id': product.id, 'quantity': 20}]},
        headers={'Authorization': f'bearer {token}'},
    )
    assert response.json() == {
        'detail': f'insufficient stock for product {product.id}'
    }


def test_create_order_total_amount(client, token, product):
    item_quantity = 6
    expected_amount = product.price * item_quantity

    response = client.post(
        '/orders',
        json={
            'items': [{'product_id': product.id, 'quantity': item_quantity}]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json()['total_amount'] == expected_amount.to_eng_string()


def test_create_order_should_return_2_items(
    client, token, product, other_product
):
    data = [
        {'product_id': product.id, 'quantity': 4},
        {'product_id': other_product.id, 'quantity': 10},
    ]
    expected_items = 2
    response = client.post(
        '/orders',
        json={'items': data},
        headers={'Authorization': f'bearer {token}'},
    )
    assert len(response.json()['items']) == expected_items


def test_create_order_already_exists(client, token, product, order):
    item_quantity = 3
    time = datetime(2025, 9, 17)

    response = client.post(
        '/orders',
        json={
            'items': [{'product_id': product.id, 'quantity': item_quantity}]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'id': 1,
        'user_id': 1,
        'total_amount': order.total_amount.to_eng_string(),
        'status': 'pending',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'items': [
            {
                'id': 1,
                'order_id': 1,
                'product_id': product.id,
                'quantity': order.items[0].quantity,
                'price': product.price.to_eng_string(),
            }
        ],
    }


def test_read_order_by_id(client, order):
    response = client.get(f'/orders/{order.id}')
    time = datetime(2025, 9, 17)
    assert response.json() == {
        'id': 1,
        'user_id': 1,
        'total_amount': order.total_amount.to_eng_string(),
        'status': 'pending',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'items': [
            {
                'id': 1,
                'order_id': order.id,
                'product_id': order.items[0].product_id,
                'quantity': order.items[0].quantity,
                'price': order.items[0].price.to_eng_string(),
            }
        ],
    }


def test_read_order_by_id_not_found(client):
    response = client.get('/orders/99')
    assert response.json() == {'detail': 'Order does not exists.'}


def test_read_user_order(client, token, order):
    response = client.get(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )
    time = datetime(2025, 9, 17)
    assert response.json() == {
        'id': 1,
        'user_id': 1,
        'total_amount': order.total_amount.to_eng_string(),
        'status': 'pending',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'items': [
            {
                'id': 1,
                'order_id': order.id,
                'product_id': order.items[0].product_id,
                'quantity': order.items[0].quantity,
                'price': order.items[0].price.to_eng_string(),
            }
        ],
    }


def test_read_user_order_not_pending(client, token, other_order):
    response = client.get(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_read_user_order_not_found(client, token):
    response = client.get(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )
    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_delete_order(client, token, order):
    response = client.delete(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {'message': 'Order deleted.'}


def test_delete_order_not_found(client, token):
    response = client.delete(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_delete_order_not_pending(client, token, other_order):
    response = client.delete(
        '/orders/my-orders', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_update_orders(client, order, token, product):
    item_quantity = 3

    response = client.put(
        '/orders/my-orders',
        json={
            'items': [{'product_id': product.id, 'quantity': item_quantity}]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    response_data = response.json()

    assert (
        response_data['total_amount']
        == (item_quantity * product.price).to_eng_string()
    )
    assert response_data['items'][0]['quantity'] == item_quantity


def test_update_order_not_found(client, token):
    item_quantity = 5

    response = client.put(
        '/orders/my-orders',
        json={'items': [{'product_id': 1, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_update_order_not_pending(client, token, other_order):
    item_quantity = 4

    response = client.put(
        '/orders/my-orders',
        json={'items': [{'product_id': 1, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'detail': 'Order does not exists or not pending.'
    }


def test_updated_order_product_not_found(client, token, order):
    item_quantity = 4

    response = client.put(
        '/orders/my-orders',
        json={'items': [{'product_id': 85, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Product 85 not found.'}


def test_updated_order_inactive_product(
    client, token, order, inactive_product
):
    item_quantity = 4

    response = client.put(
        '/orders/my-orders',
        json={
            'items': [
                {'product_id': inactive_product.id, 'quantity': item_quantity}
            ]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'detail': f'Product {inactive_product.id} not found.'
    }


def test_update_order_insufficient_stock(client, token, order):
    item_quantity = 50

    response = client.put(
        '/orders/my-orders',
        json={'items': [{'product_id': 1, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'insufficient stock for product_id 1'}


def test_update_order_remove_item_quantity_0(client, token, order):
    item_quantity = 0

    response = client.put(
        '/orders/my-orders',
        json={'items': [{'product_id': 1, 'quantity': item_quantity}]},
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json()['items'] == []


def test_update_order_add_new_item(
    client, token, other_product, order, product
):
    item_quantity = 9
    expected_items = 2
    response = client.put(
        '/orders/my-orders',
        json={
            'items': [
                {'product_id': other_product.id, 'quantity': item_quantity}
            ]
        },
        headers={'Authorization': f'bearer {token}'},
    )

    response_data = response.json()

    assert (
        response_data['total_amount']
        == (
            product.price + (other_product.price * item_quantity)
        ).to_eng_string()
    )
    assert len(response_data['items']) == expected_items


# TODO: Remove product from pending order update total amount
# TODO: Test total amount is zero from empty items