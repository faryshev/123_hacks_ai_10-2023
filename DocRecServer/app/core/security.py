"""
Модуль функций для аутентификации пользователей.
"""
import typing
from enum import Enum
from re import compile
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie

from app import models
from app.api import details
from app.core.config import base_config


password_regex = compile(r'(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}')
password_required_chars = ['abcdefghijklnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', '1234567890']


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


login_manager = OAuth2PasswordBearer(
    tokenUrl='api/auth/login',
    auto_error=False
)

refresh_token_manager = APIKeyCookie(
    scheme_name='RefreshToken',
    name="refresh_token",
    auto_error=False
)


class ClientType(Enum):
    """Набор констант типов клиентов"""
    WEB = "web"
    APP = "app"
    BOT = "bot"


def create_token(
    subject: typing.Union[str, typing.Any],
    expires_delta: int = None,
    aud: str = 'git',
    is_refresh: bool = False
) -> str:
    """
    Функция генерирует токен.

    :param subject: Полезная нагрузка.
    :param expires_delta: Время действия токена (в минутах).
    :param aud: Сервис предназначения токена.
    :param is_refresh: Рефреш токен.

    :return: Токен.
    """
    if not expires_delta:
        expires_delta = base_config.REFRESH_TOKEN_EXPIRE_MINUTES if is_refresh else base_config.WEB_TOKEN_EXPIRE_MINUTES

    expire = datetime.now() + timedelta(minutes=expires_delta)

    if isinstance(subject, models.User):
        subject = subject.id
    else:
        subject = subject

    payload = {
        "iss": 'git_server_api',
        "sub": subject,
        "aud": aud,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        base_config.SECRET_KEY,
        algorithm=base_config.ALGORITHM_CRYPTOGRAPHY
    )

    return token


def decode_token(token: str) -> dict:
    """Функция декодирует токен.

    :param token: Токен.

    :return: dict
    """
    try:
        payload = jwt.decode(
            token,
            base_config.SECRET_KEY,
            algorithms=[base_config.ALGORITHM_CRYPTOGRAPHY],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=details.TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=details.TOKEN_INVALID)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Функция сравнивает хэш пароля с текущим паролем.

    :param plain_password: Текущий пароль.
    :param hashed_password: Хэшированный пароль пользователя.

    :return: bool.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Функция генерирует хэш пароля.

    :param password: Новый пароль.

    :return: Хэшированный пароль.
    """
    return pwd_context.hash(password)
