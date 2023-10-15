"""
Модуль дополнительных схем.
"""
from app.schemas.base import APIBase


class Status(APIBase):
    status: str
