from fastapi import APIRouter, Depends, HTTPException, Request
import stripe
from typing import Annotated
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.security import get_current_user
from src.sabores_da_terra.models import User, Order
from sqlalchemy.ext.asyncio import AsyncSession
from src.sabores_da_terra.schemas import CheckoutPublic
from sqlalchemy import select
from http import HTTPStatus
from src.sabores_da_terra.settings import Settings

router = APIRouter(prefix='/payment', tags=['payment'])


stripe.api_key = Settings().STRIPE_API_KEY

# card_number = 4242 4242 4242 4242

# date = 12/34
# InvalidRequestError

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/checkout/{order_id}', response_model=CheckoutPublic)
async def checkout(
    order_id: int, 
    current_user: T_CurrentUser, 
    session: T_Session
):
    
    db_order = await session.scalar(
        select(Order).where(
            (Order.id == order_id) & 
            (Order.total_amount > 0) &
            (Order.user_id == current_user.id)
            
        )
    )

    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Invalid Order.'
        )
    
    order_items = db_order.items
    
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
                    
                    
                } for item in order_items
    ] 
    
    
    create_checkout = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url="http://localhost:8000/sucesso",
        cancel_url="http://localhost:8000/erro",
    )

    return {"checkout_url": create_checkout.url}


@router.post('/webhook')
async def webhook(request: Request):
    ...