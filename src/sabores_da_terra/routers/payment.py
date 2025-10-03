from http import HTTPStatus
from typing import Annotated

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import Order, Product, User
from src.sabores_da_terra.schemas import CheckoutPublic, Message
from src.sabores_da_terra.security import get_current_user
from src.sabores_da_terra.settings import Settings
from src.sabores_da_terra.controllers.payment_controller import PaymentController
router = APIRouter(prefix='/payment', tags=['payment'])


stripe.api_key = Settings().STRIPE_API_KEY
WEBHOOK_SECRET = Settings().WEBHOOK_SECRET

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
    return await PaymentController.checkout(order_id, current_user, session)


@router.post('/webhook', response_model=Message)
async def webhook(request: Request, session: T_Session):
    return await PaymentController.webhook(request, session)
