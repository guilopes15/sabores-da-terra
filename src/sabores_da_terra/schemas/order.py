from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.sabores_da_terra.models import OrderStatus


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(ge=0)


class OrderSchema(BaseModel):
    items: list[OrderItemSchema]


class OrderItemPublic(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal
    product_name: str
    model_config = ConfigDict(from_attributes=True)


class OrderPublic(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemPublic]
    model_config = ConfigDict(from_attributes=True)
