from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.sabores_da_terra.routers import (
    auth,
    orders,
    payment,
    products,
    users,
    web_page,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(payment.router)
app.include_router(web_page.router)


BASE_DIR = Path(__file__).resolve().parent

app.mount(
    '/static',
    StaticFiles(directory=BASE_DIR / 'templates/static'),
    name='static',
)
