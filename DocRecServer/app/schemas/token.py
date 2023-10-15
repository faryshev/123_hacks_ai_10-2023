"""
Модуль схем токена.
"""
from app.schemas.base import APIBase


class AccessToken(APIBase):
    access_token: str
    token_type: str
