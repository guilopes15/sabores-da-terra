from pydantic import BaseModel, HttpUrl


class CheckoutPublic(BaseModel):
    checkout_url: HttpUrl