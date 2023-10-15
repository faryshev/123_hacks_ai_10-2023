"""
Модуль схем пользователя.
"""
from pydantic import Field

from app.schemas.base import APIBase


class UserInDb(APIBase):
    id: int

    telegram_id: str


class UserCreate(APIBase):
    telegram_id: str = Field(...)
