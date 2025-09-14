from fastapi import FastAPI

from src.sabores_da_terra.routers import products, users

app = FastAPI()
app.include_router(users.router)
app.include_router(products.router)


@app.get('/')
def root():
    return {'message': 'Olá'}
