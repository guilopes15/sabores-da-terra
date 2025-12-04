from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.sabores_da_terra.settings import Settings

engine = create_async_engine(
    Settings().DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600

)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
