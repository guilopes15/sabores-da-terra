from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import User
from src.sabores_da_terra.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from src.sabores_da_terra.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def create_user(user: UserSchema, session: T_Session):
    db_user = await session.scalar(
        select(User).where(User.email == user.email)
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
        )

    db_user = User(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password)
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
async def read_users(session: T_Session):
    db_users = await session.scalars(select(User))
    return {'users': db_users.all()}


@router.get('/{user_id}', response_model=UserPublic)
async def read_user_by_id(user_id: int, session: T_Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User does not exists.'
        )

    return db_user


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permission.'
        )

    await session.delete(current_user)
    await session.commit()
    return {'message': 'User deleted'}


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permission.'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        await session.commit()
        await session.refresh(current_user)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
        )

    return current_user
