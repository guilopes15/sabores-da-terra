from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.sabores_da_terra.models import Order, User
from src.sabores_da_terra.security import get_password_hash


class UserControler:
    @staticmethod
    async def create(user, session):
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
            password=get_password_hash(user.password),
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user, attribute_names=['orders'])

        return db_user


    @staticmethod
    async def read_all(session):
        users = await session.scalars(
            select(User).options(
                selectinload(User.orders).selectinload(Order.items)
            )
        )

        return {'users': users.all()}


    @staticmethod
    async def read_by_id(user_id, session):
        db_user = await session.scalar(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.orders).selectinload(Order.items))
        )

        if not db_user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User does not exists.',
            )

        return db_user


    @staticmethod
    async def update(user_id, user, session, current_user):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permission.',
            )

        try:
            current_user.username = user.username
            current_user.email = user.email
            current_user.password = get_password_hash(user.password)
            await session.commit()

            refreshed_user = await session.scalar(
                select(User)
                .where(User.id == user_id)
                .options(selectinload(User.orders).selectinload(Order.items))
            )

        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
            )

        return refreshed_user
    
    
    @staticmethod
    async def delete(user_id, session, current_user):
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permission.',
            )

        await session.delete(current_user)
        await session.commit()
        return {'message': 'User deleted'}
