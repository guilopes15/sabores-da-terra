from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    name: str | None = None
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)
