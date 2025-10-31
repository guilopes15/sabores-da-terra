import json
from contextlib import contextmanager
from datetime import datetime
from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.sabores_da_terra.app import app
from src.sabores_da_terra.database import get_session
from src.sabores_da_terra.models import (
    Order,
    OrderItem,
    Product,
    User,
    table_registry,
)
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
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
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
async def user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime(2025, 9, 17)):
        password = '1234'
        db_user = User(
            username='test',
            email='test@test.com',
            password=get_password_hash(password),
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        db_user.clean_password = password
        return db_user


@pytest_asyncio.fixture
async def other_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime(2025, 9, 17)):
        password = '123456'
        db_user = User(
            username='test123',
            email='other@test.com',
            password=get_password_hash(password),
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        db_user.clean_password = password
        return db_user


@pytest_asyncio.fixture
async def admin(session, mock_db_time):
    with mock_db_time(model=User, time=datetime(2025, 9, 17)):
        password = '1234'
        db_user = User(
            username='test456',
            email='test987@test.com',
            password=get_password_hash(password),
            is_admin=True,
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        db_user.clean_password = password
        return db_user


@pytest_asyncio.fixture
async def product(session, mock_db_time):
    with mock_db_time(model=Product, time=datetime(2025, 9, 17)):
        db_product = Product(
            name='uva',
            price=25.50,
            stock_quantity=8,
            image='productimage@href.com'
        )

        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product


@pytest_asyncio.fixture
async def other_product(session, mock_db_time):
    with mock_db_time(model=Product, time=datetime(2025, 9, 17)):
        db_product = Product(name='pera', price=30.99, stock_quantity=20)
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product


@pytest_asyncio.fixture
async def inactive_product(session, mock_db_time):
    with mock_db_time(model=Product, time=datetime(2025, 9, 17)):
        db_product = Product(name='maca', price=25.85, stock_quantity=12)
        db_product.is_active = False
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']


@pytest.fixture
def admin_token(client, admin):
    response = client.post(
        '/auth/token',
        data={
            'username': admin.email,
            'password': admin.clean_password,
        },
    )
    return response.json()['access_token']


@contextmanager
def _mock_db_time(
    model, time=datetime(2025, 9, 17), event_name='before_insert'
):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, event_name, fake_time_hook)
    yield time
    event.remove(model, event_name, fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def order(session, mock_db_time, product, user):
    with mock_db_time(model=Order, event_name='before_update'):
        db_order = Order(user_id=user.id, total_amount=0)
        session.add(db_order)
        await session.flush()
        order_items = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=1,
            price=product.price,
            product_name=product.name,
            product_image=product.image
        )
        session.add(order_items)
        db_order.total_amount = product.price * order_items.quantity
        await session.commit()
        await session.refresh(db_order)
        return db_order


@pytest_asyncio.fixture
async def other_order(session, mock_db_time, product, user):
    with mock_db_time(model=Order, event_name='before_update'):
        db_order = Order(user_id=user.id, total_amount=0)
        session.add(db_order)
        await session.flush()
        order_items = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=1,
            price=product.price,
            product_name=product.name
        )
        session.add(order_items)
        db_order.total_amount = product.price * order_items.quantity
        db_order.status = 'paid'
        await session.commit()
        await session.refresh(db_order)
        return db_order


@contextmanager
def _mock_stripe_signature_verification(
    order_id=1, status='paid', checkout_type='checkout.session.completed'
):
    fake_event = {
        'type': checkout_type,
        'data': {
            'object': {
                'payment_status': status,
                'metadata': {'order_id': order_id},
            }
        },
    }

    with patch('stripe.Webhook.construct_event', return_value=fake_event):
        yield


@pytest.fixture
def mock_stripe_signature_verification(order):
    return _mock_stripe_signature_verification


@pytest.fixture
def webhook_payload():
    with open('tests/assets/hook_payload.txt', 'r', encoding='utf-8') as _file:
        data = json.dumps(_file.read())
    return data
