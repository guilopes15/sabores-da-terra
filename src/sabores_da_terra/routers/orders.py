from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.controllers.order_controller import OrderController
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import User
from src.sabores_da_terra.schemas import Message, OrderPublic, OrderSchema
from src.sabores_da_terra.security import get_current_user

router = APIRouter(prefix='/api/orders', tags=['orders'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=OrderPublic)
async def create_order(
    order_data: OrderSchema, current_user: T_CurrentUser, session: T_Session
):
    return await OrderController.create(order_data, current_user, session)


@router.get('/my-orders', response_model=OrderPublic)
async def read_user_order(current_user: T_CurrentUser, session: T_Session):
    return await OrderController.read(current_user, session)


@router.get('/{order_id}', response_model=OrderPublic)
async def read_order_by_id(order_id: int, session: T_Session):
    return await OrderController.read_by_id(order_id, session)


@router.delete('/my-orders', response_model=Message)
async def delete_order(current_user: T_CurrentUser, session: T_Session):
    return await OrderController.delete(current_user, session)


@router.put('/my-orders', response_model=OrderPublic)
async def update_order(
    order_data: OrderSchema, current_user: T_CurrentUser, session: T_Session
):
    return await OrderController.update(order_data, current_user, session)
