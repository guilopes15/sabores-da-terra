from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import User
from src.sabores_da_terra.schemas import Token
from src.sabores_da_terra.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from src.sabores_da_terra.settings import Settings

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    session: T_Session,
    form_data: T_OAuth2Form,
    response: Response
):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=Settings().ACCESS_TOKEN_EXPIRE_MINUTES * 60,

    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_token(user: T_CurrentUser, response: Response):

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    new_access_token = create_access_token(data={'sub': user.email})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=Settings().ACCESS_TOKEN_EXPIRE_MINUTES * 60,

    )

    return {'access_token': new_access_token, 'token_type': 'bearer'}
