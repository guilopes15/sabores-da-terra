from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductSchema(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
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
