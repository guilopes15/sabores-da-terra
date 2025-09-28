from fastapi import FastAPI

from src.sabores_da_terra.routers import auth, orders, products, users, payment

app = FastAPI()
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(payment.router)


@app.get('/')
def root():
    return {'message': 'Olá'}
