def test_create_product(client):
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
