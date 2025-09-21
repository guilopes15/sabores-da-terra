from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import Order, OrderItem, Product, User
from src.sabores_da_terra.schemas import Message, OrderPublic, OrderSchema
from src.sabores_da_terra.security import get_current_user

router = APIRouter(prefix='/orders', tags=['orders'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=OrderPublic)
async def create_order(
    order_data: OrderSchema, current_user: T_CurrentUser, session: T_Session
):
    db_order = await session.scalar(
        select(Order).where(Order.user_id == current_user.id)
    )

    if db_order and db_order.status == 'pending':
        return db_order

    db_order = Order(user_id=current_user.id, total_amount=0)
    session.add(db_order)
    await session.flush()

    items = []

    for item in order_data.items:
        product = await session.scalar(
            select(Product).where(Product.id == item.product_id)
        )
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Product {item.product_id} not found.',
            )
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'insufficient stock for product {item.product_id}',
            )

        if item.quantity > 0:

            items_to_add = OrderItem(
                    order_id=db_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price,
            )

            items.append(items_to_add)

            db_order.total_amount += product.price * item.quantity

    session.add_all(items)
    await session.commit()
    await session.refresh(db_order)

    return db_order


@router.get('/my-orders', response_model=OrderPublic)
async def read_user_order(
    current_user: T_CurrentUser,
    session: T_Session
):

    db_order = await session.scalar(
        select(Order).where(
            (Order.user_id == current_user.id) & (Order.status == 'pending')
        )
    )

    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order does not exists or not pending.')

    return db_order


@router.get('/{order_id}', response_model=OrderPublic)
async def read_order_by_id(order_id: int, session: T_Session):
    db_order = await session.scalar(select(Order).where(Order.id == order_id))
    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order does not exists.'
        )

    return db_order


@router.delete('/my-orders', response_model=Message)
async def delete_order(current_user: T_CurrentUser, session: T_Session):
    db_order = await session.scalar(
        select(Order).where(
            (Order.user_id == current_user.id) & (Order.status == 'pending')
        )
    )

    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order does not exists or not pending.')

    await session.delete(db_order)
    await session.commit()
    return {'message': 'Order deleted.'}


@router.put('/my-orders', response_model=OrderPublic)
async def update_order(
    order_data: OrderSchema,
    current_user: T_CurrentUser, session: T_Session):
    db_order = await session.scalar(
        select(Order).where(
            (Order.user_id == current_user.id) & (Order.status == 'pending')
        )
    )

    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Order does not exists or not pending.')

    for item in order_data.items:
        product = await session.scalar(
            select(Product).where(Product.id == item.product_id)
        )

        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Product {item.product_id} not found.',
            )

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'insufficient stock for product_id {item.product_id}',
            )

        order_item = next(
            filter(
                lambda x: x.product_id == item.product_id, db_order.items
                ), None)

        if order_item:
            if item.quantity == 0:
                db_order.total_amount -= order_item.quantity * product.price
                db_order.items.remove(order_item)

            else:

                difference = item.quantity - order_item.quantity
                db_order.total_amount += product.price * difference
                order_item.quantity = item.quantity
        elif item.quantity > 0:
            items_to_add = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price
            )

            db_order.items.append(items_to_add)
            db_order.total_amount += product.price * item.quantity

    await session.commit()
    await session.refresh(db_order)

    return db_order
