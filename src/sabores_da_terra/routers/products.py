from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import Product
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
    db_product = await session.scalar(
        select(Product).where(Product.name == product.name)
    )
    if db_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Product already exists.'
        )

    db_product = Product(**product.model_dump())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@router.get('/', response_model=ProductList)
async def read_products(session: T_Session):
    db_products = await session.scalars(select(Product))
    return {'products': db_products.all()}


@router.get('/{product_id}', response_model=ProductPublic)
async def read_product_by_id(product_id: int, session: T_Session):
    db_product = await session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product does not exists.'
        )

    return db_product


@router.delete('/{product_id}', response_model=Message)
async def delete_product(product_id: int, session: T_Session):
    db_product = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product does not exists.'
        )

    await session.delete(db_product)
    await session.commit()

    return {'message': 'Product deleted'}


@router.patch('/{product_id}', response_model=ProductPublic)
async def patch_product(
    product_id: int, product: ProductUpdate, session: T_Session
):
    db_product = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product does not exists.'
        )

    try:
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)

        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product name already exists.',
        )

    return db_product
