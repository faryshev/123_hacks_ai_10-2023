"""
Модуль базы данных.
"""
import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession # noqa
from celery import Celery

from app.db.base import Base
from app.core.config import base_config
from app.db.session import engine, get_session, Session


async def init_db() -> None:
    """
    Инициализация таблиц базы данных.
    """
    import app.models  # noqa

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except sa.exc.DBAPIError as error:
        print(error)
        exit()

