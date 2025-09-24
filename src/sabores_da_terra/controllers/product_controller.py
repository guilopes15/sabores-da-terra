from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError

from src.sabores_da_terra.models import Product


class ProductController():
    async def create(product, session):
        db_product = await session.scalar(
        select(Product).where(Product.name == product.name)
        )
        if db_product:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Product already exists.'
            )

        db_product = Product(**product.model_dump())
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

    async def read_all(session):
        db_products = await session.scalars(select(Product))
        return {'products': db_products.all()}

    async def read_by_id(product_id, session):
        db_product = await session.scalar(
            select(Product).where(Product.id == product_id)
        )

        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.'
            )

        return db_product

    async def patch(product_id, product, session):
        db_product = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.'
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

    async def delete(product_id, session):
        db_product = await session.scalar(
            select(Product).where(Product.id == product_id)
        )
        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.'
            )
        
        try:
            await session.delete(db_product)
            await session.commit()
        
        except (OperationalError, IntegrityError):
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Database error.'
            )

        return {'message': 'Product deleted'}
