from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.controllers.product_controller import (
    ProductController,
)
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.schemas import (
    Message,
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)

router = APIRouter(prefix='/products', tags=['products'])
T_Session = Annotated[AsyncSession, Depends(get_session)]


@router.post('/', response_model=ProductPublic)
async def create_product(product: ProductSchema, session: T_Session):
    return await ProductController.create(product, session)


@router.get('/', response_model=ProductList)
async def read_products(session: T_Session):
    return await ProductController.read_all(session)


@router.get('/{product_id}', response_model=ProductPublic)
async def read_product_by_id(product_id: int, session: T_Session):
    return await ProductController.read_by_id(product_id, session)


@router.patch('/{product_id}', response_model=ProductPublic)
async def patch_product(
    product_id: int, product: ProductUpdate, session: T_Session
):
    return await ProductController.patch(product_id, product, session)


@router.delete('/{product_id}', response_model=Message)
async def delete_product(product_id: int, session: T_Session):
    return await ProductController.delete(product_id, session)
