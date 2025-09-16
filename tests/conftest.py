import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.sabores_da_terra.app import app
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import Product, User, table_registry
from src.sabores_da_terra.security import get_password_hash


@pytest.fixture
def client(session):
    async def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session):
    password = '1234'
    db_user = User(
        username='test',
        email='test@test.com',
        password=get_password_hash(password)
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    db_user.clean_password = password
    return db_user


@pytest_asyncio.fixture
async def other_user(session):
    db_user = User(username='test', email='other@test.com', password='1234')
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@pytest_asyncio.fixture
async def product(session):
    db_product = Product(name='uva', price=25.50, stock_quantity=8)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product


@pytest_asyncio.fixture
async def other_product(session):
    db_product = Product(name='pera', price=30.99, stock_quantity=20)
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product
