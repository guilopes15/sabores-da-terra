import pytest
from sqlalchemy import select

from src.sabores_da_terra.models import Order, Product


def test_create_product(client, mock_db_time, admin_token):
    with mock_db_time(model=Product) as time:
        response = client.post(
            '/products',
            headers={'Authorization': f'bearer {admin_token}'},
            json={
                'name': 'manga',
                'description': 'Uma descricao da manga',
                'stock_quantity': 5,
                'price': 30.15,
                'image': 'productimage@href.com'
            },
        )

    assert response.json() == {
        'name': 'manga',
        'description': 'Uma descricao da manga',
        'stock_quantity': 5,
        'price': '30.15',
        'id': 1,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'is_active': True,
        'image': 'productimage@href.com'
    }


def test_create_product_already_exits(client, product, admin_token):
    response = client.post(
        '/products',
        headers={'Authorization': f'bearer {admin_token}'},
        json={'name': product.name, 'price': 35.10, 'stock_quantity': 6},
    )
    assert response.json() == {'detail': 'Product already exists.'}


def test_read_products(client):
    response = client.get('/products')
    assert response.json() == {'products': []}


def test_read_products_with_product(client, product):
    response = client.get('/products')

    assert response.json() == {
        'products': [
            {
                'id': product.id,
                'price': product.price.to_eng_string(),
                'stock_quantity': product.stock_quantity,
                'name': product.name,
                'description': product.description,
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat(),
                'is_active': True,
                'image': 'productimage@href.com'
            }
        ]
    }


def test_read_products_by_id(client, product):
    response = client.get(f'/products/{product.id}')

    assert response.json() == {
        'id': product.id,
        'price': product.price.to_eng_string(),
        'stock_quantity': product.stock_quantity,
        'name': product.name,
        'description': product.description,
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat(),
        'is_active': True,
        'image': product.image
    }


def test_read_products_by_id_wrong_product(client):
    response = client.get('/products/888')
    assert response.json() == {'detail': 'Product does not exists.'}


def test_delete_product(client, product, admin_token):
    response = client.delete(
        f'/products/{product.id}',
        headers={'Authorization': f'bearer {admin_token}'},
    )
    assert response.json() == {'message': 'Product deleted'}


def test_delete_product_not_found(client, admin_token):
    response = client.delete(
        '/products/99999',
        headers={'Authorization': f'bearer {admin_token}'},
    )
    assert response.json() == {'detail': 'Product does not exists.'}


@pytest.mark.asyncio
async def test_remove_product_from_pending_orders(
    client, order, product, session, admin_token
):
    client.delete(
        f'/products/{product.id}',
        headers={'Authorization': f'bearer {admin_token}'},
    )

    db_order = await session.scalar(select(Order))
    await session.refresh(db_order)
    assert db_order.items == []


@pytest.mark.asyncio
async def test_keep_product_from_paid_order(
    client, other_order, product, session, admin_token
):
    client.delete(
        f'/products/{product.id}',
        headers={'Authorization': f'bearer {admin_token}'},
    )
    expected_length = 1
    db_order = await session.scalar(select(Order))
    await session.refresh(db_order)

    assert len(db_order.items) == expected_length


def test_patch_product(client, product, admin_token):
    response = client.patch(
        f'/products/{product.id}',
        headers={'Authorization': f'bearer {admin_token}'},
        json={'stock_quantity': 25, 'price': 95.15},
    )

    assert response.json() == {
        'id': product.id,
        'price': '95.15',
        'stock_quantity': 25,
        'name': product.name,
        'description': product.description,
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat(),
        'is_active': True,
        'image': product.image
    }


def test_patch_product_not_found(client, admin_token):
    response = client.patch(
        '/products/777777',
        headers={'Authorization': f'bearer {admin_token}'},
        json={'stock_quantity': 25, 'price': 95.15},
    )
    assert response.json() == {'detail': 'Product does not exists.'}


def test_patch_product_name_already_exists(
    client, product, other_product, admin_token
):
    response = client.patch(
        f'/products/{product.id}',
        headers={'Authorization': f'bearer {admin_token}'},
        json={'name': other_product.name},
    )
    assert response.json() == {'detail': 'Product name already exists.'}


def test_read_products_offset(client, product, other_product):
    response = client.get('/products/filters?offset=1')

    expected_length = 1

    assert len(response.json()['products']) == expected_length


def test_read_products_limit(client, product, other_product):
    response = client.get('/products/filters?limit=1')

    expected_length = 1

    assert len(response.json()['products']) == expected_length


def test_read_products_by_name(client, product):
    response = client.get('/products/filters?name=uva')

    assert response.json()['products'][0]['name'] == product.name
