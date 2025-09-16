from fastapi import FastAPI

from src.sabores_da_terra.routers import auth, products, users

app = FastAPI()
app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)


@app.get('/')
def root():
    return {'message': 'Olá'}
