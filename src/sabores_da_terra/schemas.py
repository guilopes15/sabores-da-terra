from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=4)
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]


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


class ProductList(BaseModel):
    products: list[ProductPublic]


class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None
    description: str | None = None
