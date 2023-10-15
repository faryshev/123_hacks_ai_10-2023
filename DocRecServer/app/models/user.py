"""
Модуль модели пользователя.
"""
import typing

import sqlalchemy as sa
import sqlalchemy.orm

from app import db

if typing.TYPE_CHECKING:
    pass


class User(db.Base):
    """Модель таблицы пользователей.

    :id: Уникальный идентификатор пользователя.

    :telegram_id: Идентификатор telegram.


    :created: Дата и время создания пользователя.
    """
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)

    telegram_id = sa.Column(sa.String, nullable=False, unique=True)
    created = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())

    def __str__(self):
        return f'User #{self.id}'

    def __repr__(self):
        return f'User #{self.id}'

