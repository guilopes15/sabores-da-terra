from src.sabores_da_terra.models import Product
from sqlalchemy.exc import OperationalError
import pytest
from src.sabores_da_terra.controllers.product_controller import ProductController
from fastapi import HTTPException
from sqlalchemy import select
from src.sabores_da_terra.models import Order


def test_create_product(client, mock_db_time):
    with mock_db_time(model=Product) as time:
        response = client.post(
            '/products',
            json={
                'name': 'manga',
                'description': 'Uma descricao da manga',
                'stock_quantity': 5,
                'price': 30.15,
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
    }


def test_create_product_already_exits(client, product):
    response = client.post(
        '/products',
        json={'name': product.name, 'price': 35.10, 'stock_quantity': 6},
    )
    assert response.json() == {'detail': 'Product already exists.'}


def test_read_users(client):
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
    }


def test_read_products_by_id_wrong_product(client):
    response = client.get('/products/888')
    assert response.json() == {'detail': 'Product does not exists.'}


def test_delete_product(client, product):
    response = client.delete(f'/products/{product.id}')
    assert response.json() == {'message': 'Product deleted'}


def test_delete_product_not_found(client):
    response = client.delete('/products/99999')
    assert response.json() == {'detail': 'Product does not exists.'}


@pytest.mark.asyncio
async def test_delete_product_database_error(product, monkeypatch, session):
    
    async def fake_delete(obj):
        raise OperationalError("force", "me", "test")

    monkeypatch.setattr(session, "delete", fake_delete)
    
    with pytest.raises(HTTPException) as ex:
        await ProductController.delete(product.id, session)

    assert 'Database error.' in ex.value.detail


@pytest.mark.asyncio        
async def test_remove_product_from_pending_orders(client, order, product, session):
    client.delete(f'/products/{product.id}')

    db_order = await session.scalar(select(Order))
    await session.refresh(db_order)
    assert db_order.items == []


def test_patch_product(client, product):
    response = client.patch(
        f'/products/{product.id}', json={'stock_quantity': 25, 'price': 95.15}
    )

    assert response.json() == {
        'id': product.id,
        'price': '95.15',
        'stock_quantity': 25,
        'name': product.name,
        'description': product.description,
        'created_at': product.created_at.isoformat(),
        'updated_at': product.updated_at.isoformat(),
    }


def test_patch_product_not_found(client):
    response = client.patch(
        '/products/777777', json={'stock_quantity': 25, 'price': 95.15}
    )
    assert response.json() == {'detail': 'Product does not exists.'}


def test_patch_product_name_already_exists(client, product, other_product):
    response = client.patch(
        f'/products/{product.id}', json={'name': other_product.name}
    )
    assert response.json() == {'detail': 'Product name already exists.'}
