from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.sabores_da_terra.models import OrderStatus


class UserSchema(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=4)
    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    message: str


class ProductSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int
    model_config = ConfigDict(from_attributes=True)


class ProductPublic(ProductSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    products: list[ProductPublic]
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None
    description: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


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


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    orders: list[OrderPublic]
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
    model_config = ConfigDict(from_attributes=True)
