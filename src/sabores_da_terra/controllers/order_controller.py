from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select

from src.sabores_da_terra.models import Order, OrderItem, Product


class OrderController:
    @staticmethod
    async def create(order_data, current_user, session):
        if not current_user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials')

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
                select(Product).where(
                    (Product.id == item.product_id) &
                    (Product.is_active)
                )
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
                    product_name=product.name,
                    product_image=product.image
                )

                items.append(items_to_add)

                db_order.total_amount += product.price * item.quantity

        session.add_all(items)
        await session.commit()
        await session.refresh(db_order)

        return db_order

    @staticmethod
    async def read(current_user, session):
        if not current_user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials')

        db_order = await session.scalar(
            select(Order).where(
                (Order.user_id == current_user.id)
                & (Order.status == 'pending')
            )
        )

        if not db_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order does not exists or not pending.',
            )

        return db_order

    @staticmethod
    async def read_by_id(order_id, session):
        db_order = await session.scalar(
            select(Order).where(Order.id == order_id)
        )
        if not db_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order does not exists.',
            )

        return db_order

    @staticmethod
    async def update(order_data, current_user, session):
        if not current_user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials')

        db_order = await session.scalar(
            select(Order).where(
                (Order.user_id == current_user.id)
                & (Order.status == 'pending')
            )
        )

        if not db_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order does not exists or not pending.',
            )

        for item in order_data.items:
            product = await session.scalar(
                select(Product).where(
                    (Product.id == item.product_id) &
                    (Product.is_active)
                )
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
                ),
                None,
            )

            if order_item:
                if item.quantity == 0:

                    await session.delete(order_item)
                    await session.refresh(db_order, attribute_names=["items"])

                else:
                    order_item.quantity = item.quantity
                    order_item.price = product.price

            elif item.quantity > 0:
                items_to_add = OrderItem(
                    order_id=db_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price,
                    product_name=product.name,
                    product_image=product.image
                )

                db_order.items.append(items_to_add)
        db_order.total_amount = sum(
            item.quantity * item.price for item in db_order.items
        )

        await session.commit()
        await session.refresh(db_order)

        return db_order

    @staticmethod
    async def delete(current_user, session):
        if not current_user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Could not validate credentials')

        db_order = await session.scalar(
            select(Order).where(
                (Order.user_id == current_user.id)
                & (Order.status == 'pending')
            )
        )

        if not db_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Order does not exists or not pending.',
            )

        await session.delete(db_order)
        await session.commit()
        return {'message': 'Order deleted.'}
