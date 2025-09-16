def test_login_for_access_token(client, user):
    response = client.post('/auth/token', data={
        'username': user.email, 'password': user.clean_password
    })

    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_login_for_access_token_invalid_password(client, user):
    response = client.post('/auth/token', data={
        'username': user.email, 'password': '654321'
    })

    assert response.json() == {
        'detail': 'Incorrect email or password'
    }


def test_login_for_access_token_wrong_user(client, user):
    response = client.post('/auth/token', data={
        'username': 'invalid@invalid.com', 'password': user.clean_password
    })

    assert response.json() == {
        'detail': 'Incorrect email or password'
    }
