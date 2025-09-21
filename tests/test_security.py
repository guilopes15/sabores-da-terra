import pytest
from fastapi import HTTPException
from jwt import decode, encode

from src.sabores_da_terra.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from src.sabores_da_terra.settings import Settings


def test_create_access_token(user):
    data = {'sub': user.email}
    token = create_access_token(data)
    result = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert user.email in result.values()
    assert 'exp' in result.keys()
    assert result['exp']


def test_password_checker():
    password_hash = get_password_hash('test')
    assert verify_password('test', password_hash)


@pytest.mark.asyncio
async def test_get_current_user(session, user):
    data = {'sub': user.email}
    token = encode(data, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    current_user = await get_current_user(session, token)
    assert current_user


@pytest.mark.asyncio
async def test_get_current_user_without_sub(session):
    data = {}
    token = encode(data, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)

    with pytest.raises(HTTPException) as ex:
        await get_current_user(session, token)

    assert ex.value.detail == 'Could not validate credentials'


@pytest.mark.asyncio
async def test_get_current_user_not_found(session):
    data = {'sub': 'invalid@invalid.com'}

    token = encode(data, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)

    with pytest.raises(HTTPException) as ex:
        await get_current_user(session, token)

    assert ex.value.detail == 'Could not validate credentials'
