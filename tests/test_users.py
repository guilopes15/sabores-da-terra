def test_create_user(client):
    response = client.post(
        '/users',
        json={'email': '0@a.com', 'password': '0000000', 'username': '000'},
    )
    assert response.json() == {'email': '0@a.com', 'username': '000', 'id': 1}


def test_create_user_existent(client, user):
    response = client.post(
        '/users',
        json={'username': 'test', 'email': user.email, 'password': '147258'},
    )
    assert response.json() == {'detail': 'Email already exists.'}


def test_read_users(client):
    response = client.get('/users')
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    response = client.get('/users')
    assert response.json() == {
        'users': [{'username': 'test', 'email': 'test@test.com', 'id': 1}]
    }


def test_read_user_by_id(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.json() == {
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_user_by_id_wrong_user(client, user):
    response = client.get('/users/99')
    assert response.json() == {'detail': 'User does not exists.'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('/users/999')
    assert response.json() == {'detail': 'User does not exists.'}


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2',
            'password': '369258147',
            'email': 'example@test.com',
        },
    )
    assert response.json() == {
        'username': 'test2',
        'email': 'example@test.com',
        'id': 1,
    }


def test_update_user_email_already_exists(client, user, other_user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test3',
            'email': other_user.email,
            'password': '1258963',
        },
    )
    assert response.json() == {'detail': 'Email already exists.'}


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/99',
        json={
            'username': 'test3',
            'email': 'test@test.com',
            'password': '1258963',
        },
    )

    assert response.json() == {'detail': 'User does not exists.'}
