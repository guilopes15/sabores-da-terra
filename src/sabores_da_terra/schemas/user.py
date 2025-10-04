from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .order import OrderPublic


class UserSchema(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=4)
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    orders: list[OrderPublic]
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
    model_config = ConfigDict(from_attributes=True)
