"""
Модуль дополнительных функций.
"""
import re

import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, status

from app import db, models
from app.api import details


def abort(code: int, detail: str = None) -> None:
    """Функция вызывает HTTPException.

    :param code: Код ошибки.
    :param detail: Сообщение об ошибке.
    """
    if code == 403 and not detail:
        detail = details.NOT_ENOUGH_PERMISSIONS

    raise HTTPException(status_code=code, detail=detail)


def error_detail(e: sa.exc.DBAPIError) -> str:
    """
    Функция получения описания ошибки.

    :param e: Exception

    :return: описание ошибки
    """
    message = e.args[0]

    field = re.search('Key \((.*)\)=\(.+\)', message, re.DOTALL | re.IGNORECASE)
    fields = field.group(1).split(', ') if field else ''

    fields_error = ''

    for i, clm in enumerate(fields):
        fields_error += clm.upper()
        if i != len(fields) - 1:
            fields_error += '_AND_'

    if 'already exists' in message:
        error = f'{fields_error}_ALREADY_EXISTS'
    elif 'is not present in table' in message:
        error = f'{fields_error}_NOT_EXISTS'
    elif 'invalid input value for enum' in message:
        error = f'INVALID_INPUT_VALUE_FOR_ENUM'
    else:
        error = 'UNKNOWN_ERROR'

    return error


async def get_user(
        session: db.AsyncSession,
        telegram_id: str,
        load_target_coin: bool = False,
        load_bundles: bool = False,
        load_exchanges: bool = False
) -> models.User:
    """
    Функция получения пользователя.

    :param session: Сессия БД.
    :param telegram_id: Идентификатор telegram пользователя.
    :param load_target_coin: Загрузить целевую монету пользователя.
    :param load_bundles: Загрузить связки пользователя.
    :param load_exchanges: Загрузить биржи пользователя.

    :return: models.User
    """
    user_query = sa.select(models.User).where(models.User.telegram_id == telegram_id)

    if load_target_coin:
        user_query = user_query.options(joinedload(models.User.target_coin))
    if load_bundles:
        user_query = user_query.options(
            selectinload(models.User.bundles).options(
                joinedload(models.Bundle.coin),
                joinedload(models.Bundle.exchange1),
                joinedload(models.Bundle.exchange2)
            ),
            selectinload(models.User.user_exchanges).options(
                joinedload(models.UserExchange.exchange)
            )
        )
    if load_exchanges:
        user_query = user_query.options(
            selectinload(models.User.user_exchanges).options(
                joinedload(models.UserExchange.exchange)
            )
        )

    user = await session.scalar(user_query)
    if not user:
        abort(code=status.HTTP_404_NOT_FOUND, detail=details.USER_IS_NOT_FOUND)

    return user
