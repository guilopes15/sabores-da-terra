from http import HTTPStatus

from freezegun import freeze_time


def test_login_for_access_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_login_for_access_token_invalid_password(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': '654321'}
    )

    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_for_access_token_wrong_user(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'invalid@invalid.com',
            'password': user.clean_password,
        },
    )

    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'bearer {token}'}
    )

    assert response.json()['token_type'] == 'bearer'
    assert 'access_token' in response.json()


def test_refresh_token_expire(client, user):
    with freeze_time('2025-09-17 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-09-17 13:01:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'bearer {token}'},
            json={
                'username': 'wrong123',
                'email': 'test@wrong.com',
                'password': '1472369',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token_expire_dont_refresh(client, user):
    with freeze_time('2025-09-17 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-09-17 13:01:00'):
        response = client.post(
            '/auth/refresh_token', headers={'Authorization': f'bearer {token}'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
