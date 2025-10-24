from datetime import datetime
from http import HTTPStatus

from src.sabores_da_terra.models import User


def test_create_user(client, mock_db_time):
    with mock_db_time(model=User) as time:
        response = client.post(
            '/users',
            json={
                'email': '0@a.com',
                'password': '0000000',
                'username': '000',
            },
        )
    assert response.json() == {
        'email': '0@a.com',
        'username': '000',
        'id': 1,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
        'is_admin': False,
        'orders': [],
    }


def test_create_user_existent(client, user):
    response = client.post(
        '/users',
        json={'username': 'test', 'email': user.email, 'password': '147258'},
    )
    assert response.json() == {'detail': 'Email already exists.'}


def test_read_users(client, admin_token):
    time = datetime(2025, 9, 17)
    response = client.get(
        '/users', headers={'Authorization': f'bearer {admin_token}'}
    )
    assert response.json() == {
        'users': [
            {
                'created_at': time.isoformat(),
                'email': 'test987@test.com',
                'id': 1,
                'is_admin': True,
                'orders': [],
                'updated_at': time.isoformat(),
                'username': 'test456',
            }
        ]
    }


def test_read_users_with_users(client, user, admin_token):
    time = datetime(2025, 9, 17)
    response = client.get(
        '/users', headers={'Authorization': f'bearer {admin_token}'}
    )

    assert response.json() == {
        'users': [
            {
                'username': 'test',
                'email': 'test@test.com',
                'id': 1,
                'created_at': time.isoformat(),
                'updated_at': time.isoformat(),
                'is_admin': False,
                'orders': [],
            },
            {
                'created_at': time.isoformat(),
                'email': 'test987@test.com',
                'id': 2,
                'is_admin': True,
                'orders': [],
                'updated_at': time.isoformat(),
                'username': 'test456',
            },
        ]
    }


def test_read_users_with_order(client, user, product, order, admin_token):
    time = datetime(2025, 9, 17)
    response = client.get(
        '/users', headers={'Authorization': f'bearer {admin_token}'}
    )

    assert response.json() == {
        'users': [
            {
                'username': 'test',
                'email': 'test@test.com',
                'id': 1,
                'created_at': time.isoformat(),
                'updated_at': time.isoformat(),
                'is_admin': False,
                'orders': [
                    {
                        'id': 1,
                        'user_id': user.id,
                        'total_amount': product.price.to_eng_string(),
                        'status': 'pending',
                        'created_at': time.isoformat(),
                        'updated_at': time.isoformat(),
                        'items': [
                            {
                                'id': 1,
                                'order_id': 1,
                                'product_id': product.id,
                                'quantity': 1,
                                'price': product.price.to_eng_string(),
                                'product_name': product.name
                            }
                        ],
                    }
                ],
            },
            {
                'created_at': time.isoformat(),
                'email': 'test987@test.com',
                'id': 2,
                'is_admin': True,
                'orders': [],
                'updated_at': time.isoformat(),
                'username': 'test456',
            },
        ]
    }


def test_read_user_by_id(client, user, admin_token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'bearer {admin_token}'}
    )

    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
        'is_admin': False,
        'orders': [],
    }


def test_read_user_by_id_wrong_user(client, user, admin_token):
    response = client.get(
        '/users/99', headers={'Authorization': f'bearer {admin_token}'}
    )
    assert response.json() == {'detail': 'User does not exists.'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user, token):
    response = client.delete(
        '/users/999', headers={'Authorization': f'bearer {token}'}
    )
    assert response.json() == {'detail': 'Not enough permission.'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2',
            'password': '369258147',
            'email': 'example@test.com',
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {
        'username': 'test2',
        'email': 'example@test.com',
        'id': 1,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
        'is_admin': False,
        'orders': [],
    }


def test_update_user_email_already_exists(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test3',
            'email': other_user.email,
            'password': '1258963',
        },
        headers={'Authorization': f'bearer {token}'},
    )
    assert response.json() == {'detail': 'Email already exists.'}


def test_update_user_not_found(client, user, token):
    response = client.put(
        '/users/99',
        json={
            'username': 'test3',
            'email': 'test@test.com',
            'password': '1258963',
        },
        headers={'Authorization': f'bearer {token}'},
    )

    assert response.json() == {'detail': 'Not enough permission.'}


def test_create_admin(client):
    response = client.post(
        '/users',
        headers={'admin-secret': 'admin'},
        json={
            'email': 'test@a.com',
            'password': '0000123',
            'username': 'admin_user',
        },
    )

    assert response.json()['is_admin']


def test_read_users_not_permission(client, token):
    response = client.get(
        '/users', headers={'Authorization': f'bearer {token}'}
    )
    assert response.json() == {'detail': 'Admin permission required.'}


def test_update_user_without_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2',
            'password': '369258147',
            'email': 'example@test.com',
        },
        headers={},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
