from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.controllers.user_controler import UserControler
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import User
from src.sabores_da_terra.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from src.sabores_da_terra.security import get_current_user

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def create_user(user: UserSchema, session: T_Session):
    return await UserControler.create(user, session)


@router.get('/', response_model=UserList)
async def read_users(session: T_Session):
    return await UserControler.read_all(session)


@router.get('/{user_id}', response_model=UserPublic)
async def read_user_by_id(user_id: int, session: T_Session):
    return await UserControler.read_by_id(user_id, session)


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    return await UserControler.update(user_id, user, session, current_user)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int, session: T_Session, current_user: T_CurrentUser
):
    return await UserControler.delete(user_id, session, current_user)
