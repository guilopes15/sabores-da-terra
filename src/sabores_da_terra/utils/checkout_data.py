from pydantic import BaseModel



class ItemCheckout(BaseModel):
    currency: str =  "brl
    unit_amount: int
    product_data: 

class CheckoutData(BaseModel):
    price_data: dict[ItemCheckout]


