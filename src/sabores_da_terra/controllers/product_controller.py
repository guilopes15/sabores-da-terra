from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.sabores_da_terra.models import Product


class ProductController:
    @staticmethod
    async def create(product, session):
        db_product = await session.scalar(
            select(Product).where(Product.name == product.name)
        )
        if db_product:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Product already exists.',
            )

        db_product = Product(**product.model_dump())
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product

    @staticmethod
    async def read_all(session):
        db_products = await session.scalars(select(Product))
        return {'products': db_products.all()}

    @staticmethod
    async def read_by_id(product_id, session):
        db_product = await session.scalar(
            select(Product).where(Product.id == product_id)
        )

        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.',
            )

        return db_product

    @staticmethod
    async def pagination(session, filter_page):
        query = select(Product).where(Product.is_active)

        if filter_page.name:
            query = query.filter(Product.name.ilike(f"%{filter_page.name}%"))

        active_products = await session.scalars(
            query.limit(filter_page.limit).offset(filter_page.offset)
        )

        return {'products': active_products.all()}

    @staticmethod
    async def patch(product_id, product, session):
        db_product = await session.scalar(
            select(Product).where(Product.id == product_id)
        )
        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.',
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

    @staticmethod
    async def delete(product_id, session):
        db_product = await session.scalar(
            select(Product).where(Product.id == product_id)
        )
        if not db_product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product does not exists.',
            )

        db_product.is_active = False
        await session.commit()

        return {'message': 'Product deleted'}
