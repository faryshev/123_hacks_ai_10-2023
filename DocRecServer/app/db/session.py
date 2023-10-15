"""
Модуль подключения к базе данных.
"""
import typing

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import base_config


if not base_config.TESTING:
    engine = create_async_engine(
        f'postgresql+asyncpg://{base_config.POSTGRES_USER}:'
        f'{base_config.POSTGRES_PASSWORD}@{base_config.POSTGRES_SERVER}/{base_config.POSTGRES_DB}',
        echo=base_config.ECHO_DB,
        pool_pre_ping=True,
        future=True,
    )
else:
    engine = create_async_engine(
        'sqlite+aiosqlite://',
        connect_args={'check_same_thread': False}
    )


Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    future=True,
    bind=engine,
    class_=AsyncSession
)


async def get_session() -> typing.AsyncGenerator[AsyncSession, None]:
    """
    Функция создает сеанс базы данных и
    закрывает его после завершения.
    """
    async with Session() as session:
        yield session
