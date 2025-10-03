from http import HTTPStatus

import stripe
from fastapi import HTTPException
from sqlalchemy import select

from src.sabores_da_terra.models import Order, Product
from src.sabores_da_terra.settings import Settings


class PaymentController():

    @staticmethod
    async def checkout(order_id, current_user, session):
        db_order = await session.scalar(
        select(Order).where(
            (Order.id == order_id) &
            (Order.total_amount > 0) &
            (Order.user_id == current_user.id) &
            (Order.status == 'pending')

            )
        )

        if not db_order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Invalid Order.'
            )

        items = [
                    {
                        'price_data': {
                        "currency": "brl",
                        "unit_amount": int(item.price * 100),
                        "product_data": {
                            'name': item.product.name,
                            'description': item.product.description
                            },
                        },
                        "quantity": item.quantity,
                    } for item in db_order.items
        ]

        create_checkout = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url="http://localhost:8000/sucesso",
            cancel_url="http://localhost:8000/erro",
            metadata={
                "order_id": db_order.id}
        )

        return {"checkout_url": create_checkout.url}

    @staticmethod
    async def webhook(request, session):
        sig_header = request.headers.get("stripe-signature")

        try:
            payload = await request.body()

            event = stripe.Webhook.construct_event(
                payload, sig_header, Settings().WEBHOOK_SECRET
            )

        except stripe.error.SignatureVerificationError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid signature"
            )

        if event["type"] == "checkout.session.completed":
            session_data = event["data"]["object"]

            if session_data["payment_status"] == "paid":
                order_id = session_data["metadata"].get("order_id")

                if order_id:

                    db_order = await session.scalar(
                        select(Order).where(Order.id == int(order_id))
                    )

                    db_order.status = 'paid'

                    for item in db_order.items:
                        db_product = await session.scalar(
                            select(Product).where(
                                (Product.id == item.product_id) &
                                Product.is_active)
                        )

                        if db_product:
                            db_product.stock_quantity = max(
                                db_product.stock_quantity - item.quantity, 0)

                    await session.commit()

                    return {'message': 'Order processed successfully.'}

        return {'message': 'No orders processed.'}
